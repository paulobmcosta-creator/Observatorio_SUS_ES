"""Serialização conservadora de CSV: campos textuais, sem filtros nem recodificação.

Reutiliza PyArrow; não substitui os preparadores R. Referência: D1 §4.2–4.3.
O digest lógico usa a leitura independente csv da biblioteca padrão e inclui
cabeçalho, ordem e todas as células. NA, vazio e espaços continuam distintos.
"""

import csv
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.parquet as pq


def sha256(arquivo):
    """Retornar SHA-256 de arquivo (Path), sem carregar todo o conteúdo."""
    with Path(arquivo).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def abrir_csv(arquivo, encoding):
    """Abrir CSV ou gzip como texto estrito, sem normalizar quebras de linha."""
    abrir = gzip.open if str(arquivo).endswith(".gz") else open
    return abrir(arquivo, "rt", encoding=encoding, newline="")


def atualizar_digest(digest, linha):
    """Acumular uma lista de células como JSON UTF-8 delimitado por newline."""
    digest.update((json.dumps(linha, ensure_ascii=False, separators=(",", ":")) + "\n").encode())


def resumir_csv(arquivo, encoding, delimitador):
    """Retornar cabeçalho, número de linhas e digest lógico de CSV válido."""
    digest = hashlib.sha256()
    with abrir_csv(arquivo, encoding) as stream:
        leitor = csv.reader(stream, delimiter=delimitador, strict=True)
        cabecalho = next(leitor)
        if not cabecalho or any(not c for c in cabecalho) or len(set(cabecalho)) != len(cabecalho):
            raise ValueError("Cabeçalho vazio ou duplicado; nenhuma coluna será descartada.")
        atualizar_digest(digest, cabecalho)
        n = 0
        for linha in leitor:
            if len(linha) != len(cabecalho):
                raise ValueError(f"Linha lógica {n + 2} com quantidade divergente de campos.")
            atualizar_digest(digest, linha)
            n += 1
    return cabecalho, n, digest.hexdigest()


def resumir_parquet(arquivo):
    """Conferir todas as células Parquet e retornar contagem e digest lógico."""
    parquet = pq.ParquetFile(arquivo)
    if any(f.type != pa.string() for f in parquet.schema_arrow):
        raise ValueError("Coluna não textual no Parquet.")
    digest = hashlib.sha256()
    atualizar_digest(digest, parquet.schema_arrow.names)
    n = 0
    for lote in parquet.iter_batches(batch_size=10000):
        for linha in zip(*(c.to_pylist() for c in lote.columns)):
            if any(c is None for c in linha):
                raise ValueError("Nulo introduzido na serialização textual.")
            atualizar_digest(digest, linha)
            n += 1
    return n, digest.hexdigest()


def converter_csv_parquet(fonte, destino, hash_esperado, *, encoding="utf-8", delimitador=",", proveniencia):
    """Converter fonte para diretório novo e verificar integridade célula a célula.

    fonte/destino: caminhos; hash_esperado: SHA-256 do arquivo recebido (gzip se
    comprimido); proveniencia: dict com sistema, família, competência e origem.
    Retorna manifesto. Uma origem primária desconhecida deve ser declarada,
    nunca substituída pela URL da biblioteca. Não publica nem deduplica dados.
    """
    fonte, destino = Path(fonte), Path(destino)
    obrigatorios = {"sistema", "familia", "competencia", "origem_primaria", "origem_recuperacao"}
    if not obrigatorios.issubset(proveniencia) or any(not proveniencia[k] for k in obrigatorios):
        raise ValueError("Proveniência incompleta.")
    if sha256(fonte) != hash_esperado:
        raise ValueError("SHA-256 da fonte diverge; conversão recusada.")
    inicio = datetime.now(timezone.utc).isoformat()
    colunas, n, digest = resumir_csv(fonte, encoding, delimitador)
    destino.mkdir(parents=True, exist_ok=False)
    parcial = destino / "dados.parquet.part"
    try:
        schema = pa.schema([(c, pa.string()) for c in colunas])
        with pacsv.open_csv(
            fonte,
            read_options=pacsv.ReadOptions(encoding=encoding, block_size=8 * 1024 * 1024),
            parse_options=pacsv.ParseOptions(delimiter=delimitador, newlines_in_values=True, ignore_empty_lines=False),
            convert_options=pacsv.ConvertOptions(column_types=schema, strings_can_be_null=False),
        ) as leitor, pq.ParquetWriter(parcial, schema, compression="zstd") as escritor:
            for lote in leitor:
                escritor.write_batch(lote)
        if resumir_parquet(parcial) != (n, digest):
            raise ValueError("Parquet diverge do CSV: linhas, ordem ou células.")
        if sha256(fonte) != hash_esperado:
            raise ValueError("Fonte alterada durante a execução.")
        arquivo = destino / "dados.parquet"
        parcial.rename(arquivo)
        manifesto = {
            **proveniencia, "fonte_local": str(fonte), "sha256_fonte": hash_esperado,
            "bytes_fonte": fonte.stat().st_size, "arquivo_derivado": str(arquivo),
            "sha256_derivado": sha256(arquivo), "bytes_derivado": arquivo.stat().st_size,
            "encoding_csv": encoding, "delimitador_csv": delimitador,
            "campos": colunas, "linhas": n, "sha256_logico": digest,
            "tipo_campos": "string; NA e vazios literais; sem normalização",
            "pyarrow": pa.__version__, "codigo_sha256": sha256(__file__),
            "inicio_utc": inicio, "fim_utc": datetime.now(timezone.utc).isoformat(),
            "resultado": "integridade_tabular_verificada; equivalencia_metodologica_nao_inferida",
        }
        (destino / "manifesto.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n")
        return manifesto
    except BaseException:
        parcial.unlink(missing_ok=True)
        # O diretório reservado permanece como evidência de execução incompleta.
        raise
