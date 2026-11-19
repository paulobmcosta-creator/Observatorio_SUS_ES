"""Contar equipes identificáveis por mês e auditar a data de desativação do EP."""
import argparse
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from oferta_producao_camila import blocos
from observatorio_sus.estudos.camila.lote import executar, salvar
from observatorio_sus.estudos.camila.territorio import mapa,TABELA


def vigencia(v,out):
    entradas={p.stem:p for p in (v/"originais-assistencia/EP/ES").glob("*/*.dbc")}
    def medir(stage):
        tab,qa=Counter(),Counter()
        regiao=mapa()
        for nome,path in sorted(entradas.items()):
            if not nome.startswith("EPES"):
                continue
            mes="20"+nome[-4:]
            vistos={}
            with tempfile.TemporaryDirectory(dir=stage) as tmp:
                shutil.copyfile(path,Path(tmp)/"e.dbc")
                subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('e.dbc','e.dbf')"],cwd=tmp,check=True)
                campos=["COMPETEN","CODUFMUN","IDEQUIPE","TIPO_EQP","DT_ATIVA","DT_DESAT","MOTDESAT","CNES"]
                for b,n in blocos(Path(tmp)/"e.dbf",campos):
                    for row in b:
                        if row["estado"]==b"*":
                            qa[mes,"excluidos"]+=1
                            continue
                        if row["estado"]!=b" ":
                            raise ValueError(f"Marcador EP em {mes}")
                        comp,mun,idd,tipo,ini,fim,mot,cnes=[row[k].decode("ascii").strip() for k in campos]
                        if comp!=mes:
                            raise ValueError("Competência EP incompatível")
                        qa[mes,"ativos_dbf"]+=1
                        if not idd or not idd.strip("0"):
                            qa[mes,"sem_identificador"]+=1
                            continue
                        aberta=fim=="900001" and mot=="00"
                        valido=lambda x:len(x)==6 and x.isdigit() and "190001"<=x<="209912" and "01"<=x[-2:]<="12"
                        if not valido(ini) or not (aberta or valido(fim)) or (not aberta and fim<ini):
                            classe="datas_indeterminadas"
                        elif ini>mes or (not aberta and fim<mes):
                            classe="fora_da_competencia"
                        elif not aberta and fim==mes:
                            classe="desativada_na_competencia"
                        else:
                            classe="ativa_ao_fim"
                        attrs=(regiao.get(mun,"ES_IGN"),tipo,classe,cnes)
                        if idd in vistos:
                            qa[mes,"id_repetido"]+=1
                            if vistos[idd]!=attrs:
                                vistos[idd]=("INDETERMINADA","INDETERMINADO","conflito_de_id","")
                        else:
                            vistos[idd]=attrs
            for reg,tipo,classe,_ in vistos.values():
                tab[mes,reg,tipo,classe]+=1
            if len(vistos)+qa[mes,"id_repetido"]+qa[mes,"sem_identificador"]!=qa[mes,"ativos_dbf"]:
                raise ValueError("Balanço EP incompatível")
        salvar(stage/"equipes_mensais.csv",["competencia","regiao","tipo","vigencia","equipes"],((*k,n) for k,n in sorted(tab.items())))
        salvar(stage/"qa.csv",["competencia","controle","n"],((*k,n) for k,n in sorted(qa.items())))
        return dict(meses=sum(k.startswith("EPES") for k in entradas),sentinela_aberta="900001 com MOTDESAT 00",
                    sensibilidade="somar desativada_na_competencia para vigência em algum dia do mês")
    return executar(out,dict(entradas,pdr=TABELA),{"unidade":"IDEQUIPE único na competência"},medir)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("saida",type=Path)
    a=p.parse_args()
    print(vigencia(a.v,a.saida)["controles"])
