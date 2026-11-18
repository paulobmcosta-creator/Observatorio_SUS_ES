"""Regressões SIH/CNES do Work sobre o leitor institucional de DBC recebido."""
import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from observatorio_sus.io.custodia import sha256_arquivo
from . import sim, territorio
from .lote import executar, ler, salvar
from .sim import GRUPOS, causa
from .territorio import TABELA, mapa

REPO=TABELA.parents[2]
LEITOR=REPO/"scripts/perfilar_dbc_recebido.py"
REFERENCIAS=REPO/"config/estudos/pilotos_assistenciais_camila.csv"
UFS=set("11 12 13 14 15 16 17 21 22 23 24 25 26 27 28 29 31 32 33 35 41 42 43 50 51 52 53".split())


def situacao(municipio, regioes):
    if municipio in regioes:
        return regioes[municipio]
    if municipio.startswith("32"):
        return "ES_SEM_MUNICIPIO_VALIDO"
    if re.fullmatch(r"[0-9]{6}",municipio) and municipio[:2] in UFS and municipio[2:] not in ("0000","9999"):
        return "OUTRA_UF_CODIGO_PLAUSIVEL"
    return "INDETERMINADO_OU_EXTERIOR"


def estoque_medio(meses):
    """Aplicar a um ano e uma mesma medida. Um mês válido pode ter estoque zero."""
    if (not meses or len({m[:4] for m in meses})!=1 or
            any(not re.fullmatch(r"20[0-9]{2}(0[1-9]|1[0-2])",m) or v<0 for m,v in meses.items())):
        raise ValueError("Competência ou estoque inválido")
    return dict(media=sum(meses.values())/len(meses), competencias=len(meses),
                minimo=min(meses.values()), maximo=max(meses.values()), ultima_valida=max(meses),
                ultimo_estoque=meses[max(meses)], meses_ativos=sum(v>0 for v in meses.values()))


def ativos(path,esperado,temp):
    dest=temp/path.stem
    subprocess.run([sys.executable,str(LEITOR),"--dbc",str(path),"--saida",str(dest),
                    "--sha256",esperado,"--encoding","latin1","--natureza","empirico_recebido_nao_homologado"],check=True)
    with (dest/"registros_lexicos.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            if r["_estado_registro_dbf"]=="ativo":
                yield {k:v.strip() for k,v in r.items()}


def cnes(tables,out,mapa,competencia):
    st={}
    qa=Counter(dict(ST_duplicadas=0,HB_sem_ST=0,HB_municipio_divergente=0,HB_sem_regiao=0,
                    HB_vigencia_inclassificavel=0,HB_duplicatas_exatas_analiticas=0,HB_vinculo_SUS_diferente_ST=0))
    for a in tables['ST']:
        k=a['CNES']
        if not re.fullmatch(r'[0-9]{7}',k) or a['COMPETEN']!=competencia or k in st:
            raise ValueError(f'ST: chave duplicada, código ou competência incompatível: {k}')
        st[k]=a
        qa['ST_linhas']+=1
        qa['ST_VINC_SUS_'+(a['VINC_SUS'] or 'vazio')]+=1
    linked=[]
    claves=Counter()
    coding=re.compile(r'(19|20)[0-9]{2}(0[1-9]|1[0-2])')
    for a in tables['HB']:
        n=a['CNES']
        if a['COMPETEN']!=competencia:
            raise ValueError('HB: competência incompatível')
        b=st.get(n)
        qa['HB_linhas']+=1
        qa['HB_sem_ST']+=b is None
        qa['HB_municipio_divergente']+=bool(b and a['CODUFMUN']!=b['CODUFMUN'])
        qa['HB_vinculo_SUS_diferente_ST']+=bool(b and a['VINC_SUS']!=b['VINC_SUS'])
        qa['HB_CNES_encontrado']+=b is not None
        qa['HB_VINC_SUS_'+(a['VINC_SUS'] or 'vazio')]+=1
        m=a['CODUFMUN']
        reg=mapa.get(m,'SEM_REGIAO')
        qa['HB_sem_regiao']+=reg=='SEM_REGIAO'
        start,end=a['CMPT_INI'],a['CMPT_FIM']
        status='VIGENTE_NA_COMPETENCIA'
        if not coding.fullmatch(start) or (end not in ('','000000','999999') and not coding.fullmatch(end)):
            status='VIGENCIA_INCLASSIFICAVEL'
            qa['HB_vigencia_inclassificavel']+=1
        elif start>competencia or (coding.fullmatch(end) and end<competencia):
            status='FORA_DA_VIGENCIA'
        linked.append((n,a['SGRUPHAB'],start,end,competencia,m,reg,a['VINC_SUS'],
                       b['VINC_SUS'] if b else '',b['CODUFMUN'] if b else '',int(b is not None),status))
        claves[n,a['SGRUPHAB']]+=1
    qa['HB_estabelecimentos_distintos']=len({r[0] for r in linked})
    qa['HB_pares_cnes_habilitacao_distintos']=len(claves)
    qa['HB_pares_cnes_habilitacao_repetidos']=sum(v>1 for v in claves.values())
    qa['HB_duplicatas_exatas_analiticas']=len(linked)-len(set(linked))
    if len(linked)!=qa['HB_linhas'] or qa['HB_CNES_encontrado']+qa['HB_sem_ST']!=len(linked):
        raise ValueError('Balanço do relacionamento HB–ST inconsistente')
    salvar(out/f'CNES_HB_ST_{competencia}.csv',['cnes','grupo_habilitacao','inicio','fim','competencia','municipio_hb','regiao_pdr',
          'vinc_sus_hb','vinc_sus_st','municipio_st','cn_es_vinculado','resultado_vigencia'],sorted(linked))
    salvar(out/f'CNES_HB_ST_{competencia}_QA.csv',['controle','valor'],sorted(qa.items()))
    return dict(qa)


def iso(value):
    if not re.fullmatch(r'[0-9]{8}',value):
        return None
    try:
        return date(int(value[:4]),int(value[4:6]),int(value[6:]))
    except ValueError:
        return None

def sih(tabelas,out,mapa,ident,cid_min,cid_max):
    flows,counts,qa,detalhado=Counter(),Counter(),Counter(),Counter()
    for name in sorted(tabelas):
        edition='20'+name[-4:]
        seen=Counter()
        for a in tabelas[name]:
            c=a['ANO_CMPT']+a['MES_CMPT']
            if c!=edition:
                raise ValueError(f'{origin.name}: competência divergente: {c}')
            qa[c,'linhas_ativas']+=1
            diag=causa(a['DIAG_PRINC'])
            if not re.fullmatch(r'I[0-9]{2}[A-Z0-9]?',diag) or not cid_min <= diag[:3] <= cid_max:
                continue
            qa[c,'circulatorias_total']+=1
            qa[c,'circulatorias_IDENT_'+(a['IDENT'] or 'vazio')]+=1
            if a['IDENT']!=ident:
                continue
            qa[c,f'IDENT{ident}_MORTE_'+(a['MORTE'] or 'vazio')]+=1
            qa[c,f'IDENT{ident}_AIH_ausente']+=not a['N_AIH']
            if a['N_AIH']:
                seen[a['N_AIH']]+=1
            i,s=iso(a['DT_INTER']),iso(a['DT_SAIDA'])
            qa[c,f'IDENT{ident}_datas_invalidas_ou_incoerentes']+=i is None or s is None or s<i
            qa[c,f'IDENT{ident}_internacao_outro_ano']+=bool(i and str(i.year)!=c[:4])
            r=a['MUNIC_RES']
            origem=mapa.get(r,'RES_ES_SEM_MUNICIPIO' if r.startswith('32') else 'RES_OUTRA_UF_OU_INDETERMINADA')
            dest=mapa.get(a['MUNIC_MOV'],'ATENDIMENTO_SEM_REGIAO')
            detalhado[c, str(i.year) if i else 'IGNORADO', situacao(r,mapa),situacao(a['MUNIC_MOV'],mapa)] += 1
            flows[c,origem,dest]+=1
            groups=['G0',*(g for g,(lo,hi) in GRUPOS.items() if lo<=int(diag[1:3])<=hi)]
            for g in groups:
                counts[c,'ES',g]+=1
                counts[c,dest,g]+=1
        qa[edition,f'IDENT{ident}_AIH_linhas_repetidas_e_competencia']=sum(v-1 for v in seen.values())
        if sum(n for (c,_,_),n in flows.items() if c==edition)!=counts[edition,'ES','G0']:
            raise ValueError('Fluxos não conciliam com total G0')
    salvar(out/'SIH_PILOTO_FLUXOS.csv',['competencia_processamento','origem_residencia','destino_atendimento',f'aih_g0_ident{ident}'],
          [(*k,v) for k,v in sorted(flows.items())])
    salvar(out/'SIH_PILOTO_PRODUCAO.csv',['competencia_processamento','atendimento','grupo',f'aih_ident{ident}'],
          [(*k,v) for k,v in sorted(counts.items())])
    salvar(out/'SIH_PILOTO_QA.csv',['competencia_processamento','controle','valor'],[(*k,v) for k,v in sorted(qa.items())])

    salvar(out/"SIH_ADMISSAO_ORIGEM_DESTINO.csv",
           ["competencia","ano_admissao","residencia","atendimento","aih"],
           [(*k,v) for k,v in sorted(detalhado.items())])
    if sum(detalhado.values()) != sum(flows.values()):
        raise ValueError("Balanço entre tipos de fluxo")


def conferir_quinto_mes_e_lt(acervo):
    pasta=acervo/"CP04/Resultados"
    fluxos=ler(pasta/"SIH_PILOTO_FLUXOS.csv")
    producao=ler(pasta/"SIH_PILOTO_PRODUCAO.csv")
    total=sum(int(r["aih_g0_ident1"]) for r in fluxos)
    if ({r["competencia_processamento"] for r in fluxos+producao}!={"202411"} or
            [int(r["aih_ident1"]) for r in producao if r["atendimento"]=="ES" and r["grupo"]=="G0"] != [total]):
        raise ValueError("Balanço do quinto mês CP04")
    qa={r["controle"]:int(r["valor"]) for r in ler(pasta/"CNES_LT_202412_QA.csv")}
    if qa["linhas_LT"]!=1031 or any(v for k,v in qa.items() if k!="linhas_LT"):
        raise ValueError("Balanço LT piloto")
    balanco=Counter()
    for r in ler(pasta/"CNES_LT_202412_ESTOQUE_POR_CODIGO.csv"):
        k=r["tp_leito"],r["cod_leito"],r["campo"]
        balanco[k]+=(1 if r["regiao"]=="ES" else -1)*int(r["quantidade"])
    if any(balanco.values()):
        raise ValueError("Partição regional LT diverge do ES")
    return dict(sih_202411_aih=total,lt_202412_registros=qa["linhas_LT"],nivel="derivados_CP04")


def processar(acervo,saida,ident="1",cid_min="I00",cid_max="I99"):
    if ident not in ("1","5") or not all(re.fullmatch(r"I[0-9]{2}",c) for c in (cid_min,cid_max)) or cid_min>cid_max:
        raise ValueError("Filtro SIH inválido")
    refs=ler(REFERENCIAS)
    entradas={r['membro']:acervo/r['membro'] for r in refs}
    entradas.update(cadastro=TABELA, referencias=REFERENCIAS)
    def calcular(stage):
        for r in refs:
            if sha256_arquivo(entradas[r['membro']])!=r['sha256']:
                raise ValueError(f"Edição divergente: {r['membro']}")
        with TemporaryDirectory(dir=stage) as temp:
            dbcs={p.stem:ativos(p,r['sha256'],Path(temp)) for r in refs
                  if (p:=entradas[r['membro']]).suffix==".dbc"}
            hb=cnes({fam:dbcs[fam+"ES2412"] for fam in ("HB","ST")},stage,mapa(),"202412")
            sih({k:v for k,v in dbcs.items() if k.startswith("RD")},stage,mapa(),ident,cid_min,cid_max)
            for d in Path(temp).iterdir():
                (stage/(d.name+"_perfil.json")).write_bytes((d/"perfil.json").read_bytes())
        for p in stage.glob("*.csv"):
            bas=acervo/"CP02/Resultados"/p.name
            if bas.is_file() and (p.name.startswith("CNES") or (ident,cid_min,cid_max)==("1","I00","I99")):
                if sha256_arquivo(bas)!=sha256_arquivo(p):
                    raise ValueError(f"Regressão contra CP02: {p.name}")
        return dict(cnes=hb, estoque_hb_estabelecimentos=estoque_medio({"202412":hb["HB_estabelecimentos_distintos"]}),
                    fontes_dbc=len(dbcs),controle_derivados=conferir_quinto_mes_e_lt(acervo))
    return executar(saida,entradas,dict(ident=ident,cid_min=cid_min,cid_max=cid_max,uf_atendimento="ES"),
                    calcular,[LEITOR,Path(sim.__file__),Path(territorio.__file__)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acervo",type=Path)
    p.add_argument("saida",type=Path)
    p.add_argument("--ident",default="1")
    p.add_argument("--cid-min",default="I00")
    p.add_argument("--cid-max",default="I99")
    a=p.parse_args()
    print(processar(a.acervo,a.saida,a.ident,a.cid_min,a.cid_max)["controles"])
