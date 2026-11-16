"""A02: vincular execução SIH a bytes, cobertura e provas, não a flags avulsas.

Valida evidências locais recebidas legitimamente. Não autentica parecer humano
ou origem oficial por um hash; o vínculo documental continua auditável e sujeito
a revisão. Não há leitura DBC nova ou homologação de fixtures neste módulo.
"""
import csv
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlparse

from observatorio_sus.extract.inventariar_sih_rd import UFS
from observatorio_sus.io.custodia import sha256_arquivo, validar_versao


def csv_bytes(linhas, campos):
    stream = io.StringIO(newline="")
    w = csv.DictWriter(stream, fieldnames=campos, lineterminator="\n")
    w.writeheader(); w.writerows(linhas)
    return stream.getvalue().encode()


def conferir_provas(arquivo):
    """Recalcular vínculos/cobertura/perfil e retornar referências e parâmetros."""
    arquivo = Path(arquivo).resolve()
    plano = json.loads(arquivo.read_text())
    if plano.get("natureza") != "empirico" or plano.get("sistema") != "SIH" or plano.get("familia") != "RD":
        raise ValueError("Fixture ou natureza não empírica não pode receber aceite empírico.")
    competencia, identidade = plano["competencia"], plano["conteudo_id"]
    refs = []
    def referenciar(papel, referencia):
        p = (arquivo.parent / referencia["caminho"]).resolve()
        if not p.is_file() or sha256_arquivo(p) != referencia["sha256"]:
            raise ValueError("Evidência ausente/alterada: " + papel)
        refs.append(dict(papel=papel, caminho=str(p), sha256=referencia["sha256"], competencia=competencia, conteudo_id=identidade))
        return p
    _, manifesto = validar_versao((arquivo.parent / plano["snapshot"]).resolve(), identidade)
    objetos = manifesto["objetos"]
    if {o["uf"] for o in objetos} != set(UFS) or any(
        o["sistema"] != "SIH" or o["familia"] != "RD" or o["competencia"] != competencia or
        any(t in o["layout"].lower() for t in ("fixture", "sintetico", "sintético")) for o in objetos
    ):
        raise ValueError("Cobertura observada deve conter as 27 UFs RD da mesma competência/layout real.")
    ids = {o["id"] for o in objetos}
    manifest_path = (arquivo.parent / plano["snapshot"] / "conteudo.json").resolve()
    referenciar("manifesto", {"caminho": str(manifest_path), "sha256": sha256_arquivo(manifest_path)})
    evidencias = {}
    for papel in ("inventario", "aquisicao", "conversao", "paridade", "perfil_ident", "layout", "coorte", "municipios"):
        evidencias[papel] = json.loads(referenciar(papel, plano[papel]).read_text())
        e = evidencias[papel]
        if e.get("conteudo_id") != identidade or e.get("competencia") != competencia:
            raise ValueError("Evidência não pertence ao dataset/competência: " + papel)
        if e.get("natureza") != "empirico":
            raise ValueError("Evidência sintética não promove dataset empírico: " + papel)
    inventario = evidencias["inventario"]
    if {o["id"] for o in inventario["objetos"]} != ids or len(inventario["objetos"]) != len(objetos):
        raise ValueError("Inventário observado e snapshot não reconciliam partes/revisões.")
    for original in objetos:
        observado = next(o for o in inventario["objetos"] if o["id"] == original["id"])
        if any(observado[k] != original[k] for k in ("uf", "parte", "revisao", "bytes", "sha256")):
            raise ValueError("Revisão/hash da parte diverge do inventário observado.")
    obtidos = evidencias["aquisicao"]["objetos"]
    if {o["id"] for o in obtidos} != ids or len(obtidos) != len(objetos):
        raise ValueError("Aquisição não cobre todas as partes.")
    for o in obtidos:
        origem = urlparse(o["uri_efetiva"])
        if origem.scheme not in ("ftp", "https") or origem.hostname != "ftp.datasus.gov.br" or o["status"] != "validado":
            raise ValueError("Origem oficial/linhagem precisa de evidência específica; snapshot/espelho não equivale a aquisição oficial.")
        if o["sha256"] != next(x["sha256"] for x in objetos if x["id"] == o["id"]):
            raise ValueError("Aquisição refere outros bytes.")
    csv_path = referenciar("dataset_csv", plano["derivado"])
    conversao = evidencias["conversao"]
    paridade = evidencias["paridade"]
    for papel, prova in [("conversão", conversao), ("paridade", paridade)]:
        if set(prova["raw_ids"]) != ids or prova["csv_sha256"] != plano["derivado"]["sha256"]:
            raise ValueError(papel + " não cobre todas as partes/derivado.")
    if (paridade.get("resultado") != "COINCIDE" or len(set(paridade["mecanismos_leitura"])) < 2 or
        len(set(paridade.get("decodificadores", []))) < 2):
        raise ValueError("Paridade deve identificar dois mecanismos de leitura e reconciliar os mesmos bytes.")
    for r in paridade["balancos_por_parte"]:
        if r["cabecalho"] != r["ativos"] + r["excluidos"] or r["perdas_nao_explicadas"] != 0:
            raise ValueError("Balanço de leitura não reconciliado.")
    if {r["id"] for r in paridade["balancos_por_parte"]} != ids:
        raise ValueError("Paridade apenas amostral não habilita o lote nacional.")
    perfil, n = Counter(), 0
    with csv_path.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        campos = leitor.fieldnames
        obrigatorios = {"IDENT", "MUNIC_RES", "MUNIC_MOV", "N_AIH", "ANO_CMPT", "MES_CMPT", "DT_INTER", "DT_SAIDA"}
        if not campos or len(campos) != len(set(campos)) or not obrigatorios.issubset(campos):
            raise ValueError("Campos obrigatórios do derivado ausentes/duplicados.")
        for r in leitor:
            if None in r or None in r.values() or r["ANO_CMPT"] + r["MES_CMPT"].zfill(2) != competencia:
                raise ValueError("Registro malformado ou de outra competência.")
            perfil[r["IDENT"]] += 1; n += 1
    if not n or n != conversao["linhas"] or dict(perfil) != evidencias["perfil_ident"]["contagens"]:
        raise ValueError("Perfil IDENT/contagem não corresponde aos dados efetivos.")
    for papel in ("layout", "coorte"):
        prova = evidencias[papel]
        if not prova.get("revisor_funcional") or not prova.get("fundamentacao"):
            raise ValueError("Revisão documental não identificada: " + papel)
        referenciar("documento_" + papel, prova["documento"])
    coorte = evidencias["coorte"]
    if not set(perfil).issubset(coorte["ident_dominio"]) or not set(coorte["ident_elegivel"]).issubset(coorte["ident_dominio"]):
        raise ValueError("Domínio IDENT efetivo não resolvido documentalmente.")
    municipios = evidencias["municipios"]
    es = municipios["municipios_es"]
    if len(es) != len(set(es)) or len(es) != 78 or not set(es).issubset(municipios["municipios_destino_conhecidos"]):
        raise ValueError("Catálogo municipal ES/nacional não reconciliado.")
    referenciar("catalogo_municipal_fonte", municipios["documento"])
    referenciar("plano_provas", {"caminho": str(arquivo), "sha256": sha256_arquivo(arquivo)})
    parametros = {"competencia": competencia, "conteudo_id": identidade,
                  "ident_elegivel": "|".join(coorte["ident_elegivel"]), "ident_dominio": "|".join(coorte["ident_dominio"]),
                  "municipios_es": "|".join(es), "municipios_destino_conhecidos": "|".join(municipios["municipios_destino_conhecidos"])}
    return refs, csv_bytes([dict(chave=k, valor=v) for k, v in parametros.items()], ["chave", "valor"])


def preparar_ou_verificar(plano, destino=None, aceite=None):
    """Gerar vínculo determinístico ou verificar certificado contra todas as provas."""
    refs, parametros = conferir_provas(plano)
    raiz = Path(destino or Path(aceite).parent).resolve()
    refs.append(dict(papel="parametros", caminho=str(raiz / "parametros.csv"), sha256=hashlib.sha256(parametros).hexdigest(),
                     competencia=refs[0]["competencia"], conteudo_id=refs[0]["conteudo_id"]))
    data = csv_bytes(refs, ["papel", "caminho", "sha256", "competencia", "conteudo_id"])
    if aceite:
        if Path(aceite).read_bytes() != data or (raiz / "parametros.csv").read_bytes() != parametros:
            raise ValueError("Aceite/parametrização divergem das provas verificadas.")
    else:
        raiz.mkdir(parents=True, exist_ok=False)
        (raiz / "parametros.csv").write_bytes(parametros)
        (raiz / "aceite.csv").write_bytes(data)
    return raiz / "aceite.csv"
