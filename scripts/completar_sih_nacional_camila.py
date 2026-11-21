"""Adquira somente partições RD descobertas no catálogo e valide cada competência."""
import argparse
import json
import re
import shutil
import struct
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from sih_residencia_camila import processar
from observatorio_sus.estudos.camila.assistencia import situacao
from observatorio_sus.estudos.camila.lote import ler, produtos
from observatorio_sus.estudos.camila.territorio import mapa, TABELA
from observatorio_sus.extract.envelope_datasus import UFS
from observatorio_sus.io.custodia import escrever_json, sha256_arquivo


def catalogo(arquivo):
    """Leia nome e tamanho de cada partição de 2014–2024 na listagem oficial RD."""
    particoes = {}
    for linha in arquivo.read_text().splitlines():
        m = re.search(r"\s(\d+)\s+(RD([A-Z]{2})(\d{4})([^.\s]*)\.dbc)$", linha, re.I)
        if m and "1401" <= m[4] <= "2412":
            nome = m[2][:-4].upper()
            if m[5] or m[3].upper() not in UFS or nome in particoes:
                raise ValueError(f"Revisar partição adicional ou duplicada no catálogo: {nome}")
            particoes[nome] = int(m[1])
    if set(particoes) != {f"RD{uf}{ano:02}{mes:02}" for uf in UFS for ano in range(14,25) for mes in range(1,13)}:
        raise ValueError("Catálogo RD incompleto")
    return particoes


def conferir_particao(v, nome, esperado, regioes):
    """Concilie bytes, domínio geográfico e margens da projeção cardiovascular."""
    uf, mes = nome[2:4], "20"+nome[-4:]
    fonte = v/"originais-assistencia/RD"/uf/mes
    dbc = fonte/(nome+".dbc")
    meta = json.loads((fonte/"aquisicao.json").read_text())
    url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/{nome}.dbc"
    if (meta["uri_oficial"] != url or meta["uri_efetiva"] != url or meta["bytes"] != esperado
            or meta["revisao_antes"] != meta["revisao_depois"] or meta["revisao_antes"]["size"] != esperado
            or dbc.stat().st_size != esperado or sha256_arquivo(dbc) != meta["sha256"]):
        raise ValueError(f"Proveniência ou bytes divergentes: {nome}")
    pasta = v/"sih-residentes"/nome/mes
    recibo = json.loads((pasta/"recibo.json").read_text())
    if (produtos(pasta) != recibo["saidas"] or recibo["contrato"]["entradas"]["dbc"] != meta["sha256"]
            or recibo["contrato"]["entradas"]["pdr"] != sha256_arquivo(TABELA)):
        raise ValueError(f"Recibo analítico divergente: {nome}")
    dims = defaultdict(Counter)
    total = 0
    for r in ler(pasta/"fluxos.csv"):
        n = int(r["aih"])
        mun, at = r["municipio_res"], r["municipio_atend"]
        if (n <= 0 or r["competencia"] != mes or r["uf_arquivo"] != uf or not mun.startswith("32")
                or r["regiao_res"] != situacao(mun, regioes) or r["regiao_atend"] != situacao(at, regioes)
                or not re.fullmatch(r"I[0-9]{2}[A-Z0-9]?", r["diagnostico"])):
            raise ValueError(f"Partição, região ou inclusão clínica divergente: {nome}")
        total += n
        for chave in ("competencia","uf_arquivo","municipio_res","regiao_res","ano_admissao","sexo_sih"):
            dims[chave][r[chave]] += n
        dims["unidade_e_idade"][r["unidade_idade"]+"/"+r["idade"]] += n
    ctrl = recibo["controles"]
    qa = ctrl["qa"]
    if (total != ctrl["residentes_circulatorios"] or qa["ativos"]+qa["excluidos"] != qa["cabecalho"]
            or total > qa["residentes_todas_causas"] or any(sum(vals.values())!=total for vals in dims.values())):
        raise ValueError(f"Margens RD divergentes: {nome}")
    return dict(arquivo=nome,competencia=mes,uf=uf,bytes=esperado,sha256=meta["sha256"],url=url,
                recibo=recibo["id"],sha256_recibo=sha256_arquivo(pasta/"recibo.json"),aih=total,
                ativos=qa["ativos"],excluidos=qa["excluidos"],margens=dims)


def executar(v, destino, lista_atual, trabalhadores):
    """Retome por competência com recibos por objeto mesmo após interrupção do lote."""
    destino.mkdir(exist_ok=True, parents=True)
    base = v/"auditoria-final"
    verificado = json.loads((base/"verificacao.json").read_text())
    for arq, chave in [("originais.csv","sha256_origem"),("recibos.csv","sha256_recibos")]:
        if sha256_arquivo(base/arq) != verificado[chave]:
            raise ValueError("Inventário basal alterado")
    catalogados = catalogo(v/"fontes/rd-lista-ftp.txt")
    if catalogo(lista_atual) != catalogados:
        raise ValueError("Revisão do catálogo oficial difere da edição basal")
    cobertura = ler(v/"sih-final/cobertura.csv")
    if len(cobertura)!=len(catalogados):
        raise ValueError("Cobertura basal incompatível com catálogo")
    lotes = defaultdict(list)
    for r in cobertura:
        if r["completo_fluxo_regional"]=="False":
            lotes[r["competencia"]].append("RD"+r["uf"]+r["competencia"][2:])
    previos={Path(r["arquivo_local"]).stem.upper() for r in ler(base/"originais.csv") if r["familia"]=="RD"}
    alvos={n for ns in lotes.values() for n in ns}
    if alvos & previos or previos|alvos|{"RDES2411"} != set(catalogados):
        raise ValueError("Alvos sobrepostos à custódia anterior ou lacuna no catálogo")
    restantes=sum(catalogados[n] for n in alvos if not (v/"originais-assistencia/RD"/n[2:4]/("20"+n[-4:])/"aquisicao.json").exists())
    temporario=0
    for path in (v/"originais-assistencia/RD").glob("*/*/*.dbc"):
        with path.open("rb") as stream:
            n,h,t=struct.unpack_from("<IHH",stream.read(32),4)
        temporario=max(temporario,n*t+h+path.stat().st_size+1)
    livre=shutil.disk_usage(v).free
    if livre < restantes+trabalhadores*temporario+500_000_000:
        raise OSError("Espaço insuficiente para originais e decodificações simultâneas")
    pre=dict(utc=datetime.now(timezone.utc).isoformat(),livre=livre,bytes_pendentes=restantes,temporario_unitario_observado=temporario,
             trabalhadores=trabalhadores,alvos=len(alvos),competencias=len(lotes),inventario_basal=verificado,
             catalogo_local=sha256_arquivo(v/"fontes/rd-lista-ftp.txt"),catalogo_atual=sha256_arquivo(lista_atual))
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    escrever_json(destino/f"preflight-{stamp}.json",pre)
    print(json.dumps({k:pre[k] for k in ("livre","alvos","competencias","bytes_pendentes")}),flush=True)
    regioes=mapa()
    def objeto(nome):
        processar(v,nome)
        return conferir_particao(v,nome,catalogados[nome],regioes)
    with ThreadPoolExecutor(trabalhadores) as pool:
        for mes,nomes in sorted(lotes.items()):
            final=destino/"lotes"/(mes+".json")
            final.parent.mkdir(exist_ok=True)
            if final.exists():
                anterior=json.loads(final.read_text())
                if sorted(r["arquivo"] for r in anterior["objetos"])!=sorted(nomes):
                    raise ValueError(f"Lote incompatível: {mes}")
                for objeto_gravado in anterior["objetos"]:
                    nome = objeto_gravado["arquivo"]
                    atual = conferir_particao(v,nome,catalogados[nome],regioes)
                    if atual != objeto_gravado:
                        raise ValueError(f"Custódia ou margens alteradas desde o fechamento de {nome}")
                continue
            if shutil.disk_usage(v).free < sum(catalogados[n] for n in nomes)+trabalhadores*temporario+500_000_000:
                raise OSError(f"Espaço insuficiente antes do lote {mes}")
            objetos,erros=[],{}
            futuros={pool.submit(objeto,n):n for n in nomes}
            for f in as_completed(futuros):
                try:
                    objetos.append(f.result())
                except Exception as e:
                    erros[futuros[f]]=f"{type(e).__name__}: {e}"
            if erros:
                escrever_json(destino/f"falhas-{mes}-{stamp}.json",erros)
                print(mes,erros,flush=True)
            else:
                escrever_json(final,dict(competencia=mes,objetos=sorted(objetos,key=lambda r:r["uf"]),
                              livre_depois=shutil.disk_usage(v).free,aih=sum(r["aih"] for r in objetos)))
                print(mes,len(objetos),sum(r["bytes"] for r in objetos),flush=True)
    if any(not (destino/"lotes"/(mes+".json")).exists() for mes in lotes):
        raise ValueError("Persistem competências com falha; conferir logs e retomar os objetos pendentes")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for k in ("v","destino","lista_atual"):
        p.add_argument(k,type=Path)
    p.add_argument("--trabalhadores",type=int,choices=range(1,9),default=6)
    a=p.parse_args()
    executar(a.v,a.destino,a.lista_atual,a.trabalhadores)
