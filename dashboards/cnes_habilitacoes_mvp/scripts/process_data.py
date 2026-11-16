from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from metrics import derive_metrics


ROOT = Path(__file__).resolve().parents[1]
STATUS_MAP = {"validado": "Validado", "revisar": "Revisar"}
MONTHS_PT = [
    "jan", "fev", "mar", "abr", "mai", "jun",
    "jul", "ago", "set", "out", "nov", "dez",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_strings(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    for column in frame.columns:
        frame[column] = frame[column].astype("string").str.strip()
    return frame


def competence_label(competence: str) -> str:
    if len(competence) != 6 or not competence.isdigit() or not 1 <= int(competence[4:]) <= 12:
        raise ValueError(f"Competência inválida; esperado AAAAMM: {competence}")
    return f"{MONTHS_PT[int(competence[4:]) - 1]}/{competence[:4]}"


def iter_coordinates(geometry: dict[str, Any]) -> Iterable[tuple[float, float]]:
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        raise ValueError(f"Geometria não suportada: {geometry['type']}")
    for polygon in polygons:
        for ring in polygon:
            for longitude, latitude in ring:
                yield float(longitude), float(latitude)


def svg_paths(features: list[dict[str, Any]], width: int = 430, height: int = 560) -> dict[str, str]:
    coordinates = [point for feature in features for point in iter_coordinates(feature["geometry"])]
    min_lon, max_lon = min(x for x, _ in coordinates), max(x for x, _ in coordinates)
    min_lat, max_lat = min(y for _, y in coordinates), max(y for _, y in coordinates)
    padding = 8.0
    scale = min((width - 2 * padding) / (max_lon - min_lon), (height - 2 * padding) / (max_lat - min_lat))
    offset_x = (width - (max_lon - min_lon) * scale) / 2
    offset_y = (height - (max_lat - min_lat) * scale) / 2

    def project(longitude: float, latitude: float) -> tuple[float, float]:
        return offset_x + (longitude - min_lon) * scale, offset_y + (max_lat - latitude) * scale

    result: dict[str, str] = {}
    for feature in features:
        geometry = feature["geometry"]
        polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
        fragments: list[str] = []
        for polygon in polygons:
            for ring in polygon:
                projected = [project(float(lon), float(lat)) for lon, lat in ring]
                if not projected:
                    continue
                head, *tail = projected
                commands = [f"M {head[0]:.2f} {head[1]:.2f}"]
                commands.extend(f"L {x:.2f} {y:.2f}" for x, y in tail)
                commands.append("Z")
                fragments.append(" ".join(commands))
        result[str(feature["properties"]["codarea"])] = " ".join(fragments)
    return result


def json_scalar(value: Any) -> Any:
    if value is None or value is pd.NA or (isinstance(value, float) and math.isnan(value)):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def expected_input_paths(input_dir: Path, competence: str) -> dict[str, Path]:
    return {
        "habilitacoes": input_dir / f"cnes_habilitacoes_es_{competence}.csv",
        "estabelecimentos": input_dir / f"cnes_estabelecimentos_es_{competence}.csv",
        "municipios_ibge": input_dir / "es_municipios_ibge_localidades.json",
        "malha_ibge": input_dir / "es_municipios_ibge.geojson",
    }


def validate_sources(
    habilitacoes: pd.DataFrame,
    estabelecimentos: pd.DataFrame,
    localidades: pd.DataFrame,
    malha: dict[str, Any],
    selected: pd.DataFrame,
    competence: str,
) -> list[dict[str, str]]:
    key_columns = ["competencia", "cnes", "codigo_habilitacao", "tipo_habilitacao"]
    checks = {
        "competencia_unica": (set(habilitacoes["competencia"].dropna()) == {competence}, "Todos os registros pertencem à competência solicitada."),
        "chave_registro_unica": (not habilitacoes.duplicated(key_columns).any(), "A chave competência + CNES + código + tipo não se repete."),
        "municipios_ibge_unicos": (not localidades["cod_municipio_ibge_7"].duplicated().any(), "Cada código municipal IBGE aparece uma vez."),
        "malha_sem_duplicidade": (len({str(item["properties"]["codarea"]) for item in malha["features"]}) == len(malha["features"]), "Cada feição da malha possui código único."),
        "join_ibge_completo": (selected["cod_municipio_ibge_7"].notna().all(), "Todo registro selecionado foi vinculado ao município IBGE."),
        "cnes_referencial_completo": (selected["cnes"].isin(estabelecimentos["cnes"]).all(), "Todo CNES selecionado existe na base de estabelecimentos."),
        "status_controlado": (selected["situacao_validacao"].isin(["Validado", "Revisar"]).all(), "Todo registro selecionado possui status Validado ou Revisar."),
        "linha_cuidado_preenchida": (selected["linha_cuidado"].notna().all(), "Toda linha de cuidado selecionada está preenchida; categorias novas não desaparecem."),
        "campos_criticos_completos": (selected[["competencia", "cnes", "cod_municipio_ibge_7", "linha_cuidado", "codigo_habilitacao"]].notna().all().all(), "Competência, CNES, município, linha e código estão preenchidos."),
    }
    failed = [name for name, (passed, _) in checks.items() if not passed]
    rows = [
        {"teste": name, "resultado": "APROVADO" if passed else "REPROVADO", "regra": rule}
        for name, (passed, rule) in checks.items()
    ]
    if failed:
        raise AssertionError(f"Validações estruturais reprovadas: {', '.join(failed)}")
    return rows


def main(
    output_dir: Path,
    input_dir: Path,
    competence: str,
    dashboard_json: Path | None = None,
    generated_at: str | None = None,
) -> None:
    source_paths = expected_input_paths(input_dir, competence)
    missing = [str(path) for path in source_paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Arquivos-fonte ausentes: " + ", ".join(missing))
    output_dir.mkdir(parents=True, exist_ok=True)

    habilitacoes = clean_strings(pd.read_csv(source_paths["habilitacoes"], dtype="string"))
    estabelecimentos = clean_strings(pd.read_csv(source_paths["estabelecimentos"], dtype="string"))
    localidades_raw = json.loads(source_paths["municipios_ibge"].read_text(encoding="utf-8"))
    malha = json.loads(source_paths["malha_ibge"].read_text(encoding="utf-8"))

    localidades = pd.DataFrame(
        {
            "cod_municipio_ibge_7": [str(item["id"]) for item in localidades_raw],
            "municipio_ibge": [item["nome"] for item in localidades_raw],
            "regiao_imediata_ibge": [item["regiao-imediata"]["nome"] for item in localidades_raw],
            "regiao_intermediaria_ibge": [item["regiao-imediata"]["regiao-intermediaria"]["nome"] for item in localidades_raw],
        }
    )
    localidades["cod_municipio_ibge_6"] = localidades["cod_municipio_ibge_7"].str[:6]

    key_columns = ["competencia", "cnes", "codigo_habilitacao", "tipo_habilitacao"]
    habilitacoes["cod_municipio_ibge_6"] = habilitacoes["cod_municipio"].str[:6]
    habilitacoes["chave_registro"] = habilitacoes[key_columns].fillna("").agg("|".join, axis=1)
    habilitacoes["chave_tipo_habilitacao"] = habilitacoes[["codigo_habilitacao", "tipo_habilitacao"]].fillna("").agg("|".join, axis=1)
    habilitacoes = habilitacoes.merge(localidades, on="cod_municipio_ibge_6", how="left", validate="many_to_one")

    selected = habilitacoes[habilitacoes["usar_observatorio"].str.casefold() == "sim"].copy()
    selected["numero_leitos_num"] = pd.to_numeric(selected["numero_leitos"], errors="coerce")
    selected["situacao_validacao"] = selected["status_validacao"].map(STATUS_MAP)
    selected["regiao_saude"] = pd.NA
    selected["fonte_regiao_saude"] = pd.NA

    validation_rows = validate_sources(habilitacoes, estabelecimentos, localidades, malha, selected, competence)

    base_columns = [
        "competencia", "chave_registro", "cnes", "nome_estabelecimento",
        "cod_municipio_ibge_6", "cod_municipio_ibge_7", "municipio_ibge",
        "regiao_imediata_ibge", "regiao_intermediaria_ibge", "regiao_saude", "fonte_regiao_saude",
        "atende_sus", "codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao",
        "linha_cuidado", "sublinha_cuidado", "componente_rede", "nivel_complexidade",
        "prioridade", "situacao_validacao", "criterio_classificacao", "competencia_inicio",
        "competencia_fim", "numero_leitos_num", "portaria", "data_atualizacao", "fonte",
        "arquivo_origem", "data_processamento", "chave_tipo_habilitacao",
    ]
    base = selected[base_columns].sort_values(
        ["regiao_intermediaria_ibge", "municipio_ibge", "linha_cuidado", "cnes", "codigo_habilitacao"]
    )
    metrics = derive_metrics(base)

    indicators = (
        base.groupby(
            ["competencia", "cod_municipio_ibge_7", "municipio_ibge", "regiao_imediata_ibge", "regiao_intermediaria_ibge", "linha_cuidado", "situacao_validacao"],
            dropna=False,
        )
        .agg(
            registros_habilitacao=("chave_registro", "nunique"),
            estabelecimentos_habilitados=("cnes", "nunique"),
            tipos_habilitacao=("chave_tipo_habilitacao", "nunique"),
        )
        .reset_index()
    )

    dictionary_rows = [
        ("competencia", "Texto AAAAMM", "Competência mensal do instantâneo CNES.", "CNES/GitHub"),
        ("chave_registro", "Texto", "Chave técnica: competência|CNES|código|tipo de habilitação.", "Derivado"),
        ("cnes", "Texto", "Código do estabelecimento no CNES; unidade de contagem de estabelecimento distinto.", "CNES/GitHub"),
        ("cod_municipio_ibge_7", "Texto", "Código oficial de sete dígitos do município.", "IBGE"),
        ("municipio_ibge", "Texto", "Nome oficial do município.", "IBGE"),
        ("regiao_intermediaria_ibge", "Texto", "Região geográfica intermediária do IBGE; não é região de saúde.", "IBGE"),
        ("regiao_saude", "Texto anulável", "Campo reservado para futura regionalização estadual; não integrado nesta versão.", "Futuro"),
        ("fonte_regiao_saude", "Texto anulável", "Fonte/versionamento da futura regionalização de saúde.", "Futuro"),
        ("codigo_habilitacao", "Texto", "Código oficial da habilitação.", "CNES/GitHub"),
        ("tipo_habilitacao", "Texto", "Tipo associado ao código da habilitação.", "CNES/GitHub"),
        ("chave_tipo_habilitacao", "Texto", "Par código_habilitacao|tipo_habilitacao; COUNT DISTINCT deste campo gera 91 no recorte 202601.", "Derivado"),
        ("linha_cuidado", "Texto", "Linha/eixo analítico classificado pelo pipeline coletivo.", "Observatório/GitHub"),
        ("situacao_validacao", "Texto", "Validado ou Revisar; registros sob revisão permanecem visíveis.", "Observatório/GitHub"),
        ("registros_habilitacao", "Inteiro", "COUNT DISTINCT de chave_registro no recorte.", "Derivado"),
        ("estabelecimentos_habilitados", "Inteiro", "COUNT DISTINCT de cnes no recorte.", "Derivado"),
        ("tipos_habilitacao", "Inteiro", "COUNT DISTINCT de chave_tipo_habilitacao no recorte.", "Derivado"),
    ]
    dictionary = pd.DataFrame(dictionary_rows, columns=["campo", "tipo", "definicao", "origem"])

    paths = svg_paths(malha["features"])
    municipalities = [
        {
            "codigo": row.cod_municipio_ibge_7,
            "nome": row.municipio_ibge,
            "regiaoImediata": row.regiao_imediata_ibge,
            "regiaoIntermediaria": row.regiao_intermediaria_ibge,
            "regiaoSaude": None,
            "path": paths[row.cod_municipio_ibge_7],
        }
        for row in localidades.sort_values("municipio_ibge").itertuples(index=False)
    ]

    records = [
        {
            "competencia": row.competencia,
            "chave": row.chave_registro,
            "cnes": row.cnes,
            "estabelecimento": row.nome_estabelecimento,
            "municipioCodigo": row.cod_municipio_ibge_7,
            "municipio": row.municipio_ibge,
            "regiaoIntermediaria": row.regiao_intermediaria_ibge,
            "regiaoSaude": None,
            "linha": row.linha_cuidado,
            "codigoHabilitacao": row.codigo_habilitacao,
            "tipoHabilitacao": row.tipo_habilitacao,
            "tipoChave": row.chave_tipo_habilitacao,
            "descricaoHabilitacao": row.descricao_habilitacao,
            "status": row.situacao_validacao,
            "atendeSus": row.atende_sus,
        }
        for row in base.itertuples(index=False)
    ]

    source_manifest = [
        {"arquivo": path.name, "papel": role, "sha256": sha256(path), "tamanho_bytes": path.stat().st_size}
        for role, path in source_paths.items()
    ]
    generated_at = generated_at or date.today().isoformat()
    dashboard_payload = {
        "schemaVersion": "2.0.0",
        "metadata": {
            "titulo": "Habilitações estratégicas CNES — Espírito Santo",
            "competencia": competence,
            "competenciaRotulo": competence_label(competence),
            "geradoEm": generated_at,
            "recorte": "usar_observatorio = Sim",
            "nota": "CNES representa oferta cadastrada. Habilitação formal não equivale a produção, acesso ou suficiência.",
            "geografia": "Regiões geográficas intermediárias do IBGE; não correspondem às regiões de saúde.",
            "viewBox": "0 0 430 560",
        },
        "dominios": {
            "linhas": sorted(base["linha_cuidado"].dropna().unique().tolist()),
            "regioesIntermediarias": sorted(localidades["regiao_intermediaria_ibge"].dropna().unique().tolist()),
            "status": ["Validado", "Revisar"],
        },
        "resumoCanonico": metrics["global"],
        "municipios": municipalities,
        "registros": records,
    }

    base.to_csv(output_dir / f"base_habilitacoes_observatorio_{competence}.csv", index=False, encoding="utf-8-sig")
    indicators.to_csv(output_dir / f"indicadores_municipio_linha_{competence}.csv", index=False, encoding="utf-8-sig")
    dictionary.to_csv(output_dir / "dicionario_dados.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(validation_rows).to_csv(output_dir / "validacoes.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(source_manifest).to_csv(output_dir / "manifesto_fontes.csv", index=False, encoding="utf-8-sig")
    dashboard_text = json.dumps(dashboard_payload, ensure_ascii=False, separators=(",", ":"))
    (output_dir / "mvp-data.json").write_text(dashboard_text, encoding="utf-8")
    if dashboard_json is not None:
        dashboard_json.parent.mkdir(parents=True, exist_ok=True)
        dashboard_json.write_text(dashboard_text, encoding="utf-8")
    (output_dir / "resumo_auditoria.json").write_text(
        json.dumps({"metricas": metrics, "validacoes": validation_rows, "fontes": source_manifest}, ensure_ascii=False, indent=2, default=json_scalar),
        encoding="utf-8",
    )
    print(json.dumps(metrics["global"], ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--competencia", default="202601")
    parser.add_argument("--input-dir", type=Path, default=ROOT / "data" / "source")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data" / "processed")
    parser.add_argument("--dashboard-json", type=Path, default=ROOT / "public" / "data" / "mvp-data.json")
    parser.add_argument("--generated-at", default=None)
    arguments = parser.parse_args()
    main(arguments.output_dir, arguments.input_dir, arguments.competencia, arguments.dashboard_json, arguments.generated_at)
