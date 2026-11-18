"""Aquisição serial pela interface existente, só após preflight e catálogo explícito.

Default faz somente preflight. --adquirir é operação técnica autorizada pelo
mandato; não é nova solicitação de permissão. Não executar contra fonte já negada
sem nova condição legítima. Configuração e dados devem ficar fora do checkout.
"""
import argparse
import json
from pathlib import Path
from observatorio_sus.io.operacao_local import ler_configuracao, preflight
from observatorio_sus.io.custodia import adquirir_conjunto, validar_versao, retornar_versao
from observatorio_sus.io.manifestos import criar_identidade_conjunto
from observatorio_sus.extract.envelope_datasus import EnvelopeMensal
from observatorio_sus.extract.adquirir_objetos import FTPOficial, ArquivosLocais


def executar_lote(config, plano, adquirir=False, adaptador=None):
    """Reusar identidade/revisão/hash completos; bloquear volume desconhecido antes de abrir fonte."""
    objetos = plano["objetos"]
    exame = preflight(config, objetos, limite_derivados_bytes=plano.get("limite_derivados_bytes"),
                      limite_temporarios_bytes=plano.get("limite_temporarios_bytes"), backup_novo_bytes=plano.get("backup_novo_bytes", 0))
    if not adquirir:
        return {"preflight": exame, "aquisicao": "NAO_INICIADA"}
    identidades = {(o["sistema"], o["familia"], o["competencia"]) for o in objetos}
    if len(identidades) != 1:
        raise ValueError("Lote deve conter uma família/competência; não ampliar ingestão implicitamente.")
    sistema, familia, competencia = next(iter(identidades))
    for valor in (sistema, familia, competencia):
        if not valor or not all(c.isalnum() or c in "_-" for c in valor):
            raise ValueError("Identidade de lote inválida.")
    raiz = config["data_root"] / sistema / familia / competencia
    if all(o.get("sha256") and o.get("bytes") is not None for o in objetos):
        id, _ = criar_identidade_conjunto(objetos)
        if (raiz / "versoes" / id).exists():
            validar_versao(raiz / "versoes" / id, id)
            if plano.get("transporte") == "envelope_datasus":
                # Uma versão pode sobreviver a uma interrupção anterior à escrita do recibo.
                completos = []
                for arquivo in (raiz/"recibos").glob("*.json"):
                    r = json.loads(arquivo.read_text())
                    if r.get("conteudo_id")==id and r.get("validados")==len(objetos):
                        completos.append(r)
                if not any({(v.get("id"),v.get("sha256"),v.get("uri_oficial")) for v in r["objetos"]
                            if v.get("transporte")=="envelope_https_datasus" and v.get("sha256_envelope")}
                           == {(v["id"],v["sha256"],v["uri_oficial"]) for v in objetos} for r in completos):
                    raise ValueError("Versão presente sem recibo do envelope; reconciliar a custódia antes de promover")
            return {"preflight": exame, "aquisicao": "CACHE_VALIDADO_SEM_NOVA_CONSULTA", "conteudo_id": id}
    if exame["estado"] != "APTO_NOS_LIMITES_DECLARADOS":
        return {"preflight": exame, "aquisicao": "NAO_INICIADA"}
    if plano.get("transporte") not in ("ftp", "snapshot", "envelope_datasus"):
        raise ValueError("Transporte explícito obrigatório: ftp, snapshot ou envelope_datasus.")
    # Uma partição é o limite conservador; não há conexão paralela oculta.
    def antes_objeto(objeto):
        restantes = [o for o in objetos if o["id"] >= objeto["id"]]
        if preflight(config, restantes, limite_derivados_bytes=plano["limite_derivados_bytes"],
                     limite_temporarios_bytes=plano["limite_temporarios_bytes"], backup_novo_bytes=plano.get("backup_novo_bytes", 0))["estado"] != "APTO_NOS_LIMITES_DECLARADOS":
            raise RuntimeError("Espaço mudou antes de iniciar lote; nenhuma aquisição iniciada.")
    if plano["transporte"] == "envelope_datasus":
        limite=plano["limite_envelope_bytes"]
        if limite > plano["limite_temporarios_bytes"]:
            raise ValueError("Envelope excede temporários reservados no preflight")
        cliente=adaptador or EnvelopeMensal(config["temporarios"],limite)
    elif plano["transporte"] == "snapshot":
        cliente=adaptador or ArquivosLocais(plano["arquivos_snapshot"])
    else:
        cliente=adaptador or FTPOficial()
    return {"preflight": exame, "aquisicao": "CONCLUIDA_INTEGRIDADE_NAO_HOMOLOGA_CIENCIA", **adquirir_conjunto(raiz, objetos, cliente, antes_objeto=antes_objeto)}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--plano-lote", required=True, type=Path)
    p.add_argument("--adquirir", action="store_true")
    p.add_argument("--resultado", required=True, type=Path)
    a = p.parse_args()
    config = ler_configuracao(a.config, Path(__file__).resolve().parents[1])
    resultado = executar_lote(config, json.loads(a.plano_lote.read_text()), a.adquirir)
    with a.resultado.open("x", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2); f.write("\n")
