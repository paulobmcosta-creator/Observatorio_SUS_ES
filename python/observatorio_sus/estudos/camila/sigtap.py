"""Conferência de domínios por edição mensal, anterior à mensuração de produção."""
import argparse
import csv
import io
import re
from pathlib import Path
from zipfile import ZipFile

from observatorio_sus.io.custodia import sha256_arquivo
from .lote import executar, ler, salvar
from .territorio import TABELA

REPO=TABELA.parents[2]
CANDIDATOS=REPO/"metadata/estudos/tcc_cardiovascular/candidatos_codigos.csv"
FONTES=REPO/"config/estudos/sigtap_camila.csv"
CONSULTA="0301010072"


def registros(z,tabela,campos,mes):
    layout=list(csv.DictReader(io.StringIO(z.read(tabela+"_layout.txt").decode("latin1"))))
    pos={r["Coluna"]:slice(int(r["Inicio"])-1,int(r["Fim"])) for r in layout}
    tamanho=max(v.stop for v in pos.values())
    with z.open(tabela+".txt") as f:
        for raw in f:
            linha=raw.rstrip(b"\r\n")
            if len(linha)!=tamanho or linha[pos["DT_COMPETENCIA"]].decode()!=mes:
                raise ValueError("Competência ou comprimento divergente do layout mensal")
            yield tuple(linha[pos[c]].decode("latin1").strip() for c in campos)


def ler_edicao(path,mes):
    with ZipFile(path) as z:
        proc=list(registros(z,"tb_procedimento",["CO_PROCEDIMENTO","NO_PROCEDIMENTO"],mes))
        cbo=list(registros(z,"rl_procedimento_ocupacao",["CO_PROCEDIMENTO","CO_OCUPACAO"],mes))
    if len(dict(proc))!=len(proc) or len(set(cbo))!=len(cbo):
        raise ValueError("Chaves duplicadas no SIGTAP")
    return dict(proc),set(cbo)


def avaliar_pa(r,mes,procedimentos,relacao,candidatos,cbos_consulta):
    """Elegibilidade por linha PA para um recorte previamente definido. Preserva as duas quantidades."""
    if r["PA_CMP"]!=mes:
        raise ValueError("Competência da produção e edição SIGTAP divergentes")
    proc,cbo=r["PA_PROC_ID"],r["PA_CBOCOD"]
    for campo in ("PA_QTDAPR","PA_QTDPRO"):
        if not re.fullmatch(r"[0-9]+",r[campo]):
            raise ValueError("Quantidade ausente ou fora do domínio do piloto")
    if proc not in procedimentos:
        status="procedimento_ausente_na_edicao"
    elif proc not in candidatos:
        status="fora_do_recorte"
    elif proc==CONSULTA and (cbo not in cbos_consulta or (proc,cbo) not in relacao):
        status="consulta_cbo_incompativel"
    else:
        status="elegivel"
    return status,int(r["PA_QTDAPR"]),int(r["PA_QTDPRO"])


def processar(acervo,saida):
    refs=ler(FONTES)
    entradas={r["membro"]:acervo/r["membro"] for r in refs}
    entradas.update(candidatos=CANDIDATOS,edicoes=FONTES)
    def calcular(stage):
        candidatos=[r for r in ler(CANDIDATOS) if r["dominio"]=="SIGTAP"]
        saidas=[]
        for r in refs:
            p=entradas[r["membro"]]
            if sha256_arquivo(p)!=r["sha256"]:
                raise ValueError("Edição do espelho difere do manifesto")
            mes=r["competencia"]
            procs,rel=ler_edicao(p,mes)
            ac1={c for c in procs if c.startswith("040603")}
            ac2={v["codigo_normalizado"] for v in candidatos if v["conceito"]=="AC2"} & procs.keys()
            if not ac2 or not ac2<=ac1:
                raise ValueError("Relação AC2/AC1 divergente")
            controle=ler(p.parent/f"AC1_040603_{mes}.csv")
            if {x["codigo"]:x["descricao"] for x in controle}!={c:procs[c] for c in ac1}:
                raise ValueError("A forma 040603 diverge do consolidado")
            for v in candidatos:
                c=v["codigo_normalizado"]
                if not re.fullmatch(r"[0-9]{10}",c):
                    continue
                cbos=" ".join(k for k in ("225120","225210","225203") if (c,k) in rel) if c==CONSULTA else ""
                saidas.append((mes,c,v["conceito"],int(c in procs),int(c in ac1),int(c in ac2),cbos))
        salvar(stage/"validade_mensal.csv",["competencia","procedimento","conceito","presente","AC1","AC2",
              "cbo_candidatos_relacionados"],saidas)
        return dict(edicoes=len(refs),linhas=len(saidas),origem="espelho; autenticidade primária pendente",
                    cobertura_PA="nenhuma competência adquirida")
    # Controles de regressão também integram a identidade do lote.
    for r in refs:
        f=entradas[r["membro"]].parent/f"AC1_040603_{r['competencia']}.csv"
        entradas[f.name]=f
    return executar(saida,entradas,{"quantidade":"aprovada","classificacao":"candidata"},calcular)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acervo",type=Path)
    p.add_argument("saida",type=Path)
    a=p.parse_args()
    print(processar(a.acervo,a.saida)["controles"])
