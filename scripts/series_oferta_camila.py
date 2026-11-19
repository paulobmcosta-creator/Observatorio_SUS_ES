"""Reunir estoques mensais do CNES e procedimentos PA por vigência SIGTAP."""
import argparse
import json
from collections import Counter
from pathlib import Path
import pandas as pd

from observatorio_sus.estudos.camila import sigtap
from observatorio_sus.estudos.camila.lote import executar, produtos, salvar, ler
from observatorio_sus.io.custodia import sha256_arquivo


def consolidar(v,saida):
    lotes=sorted((v/"oferta-serie").glob("*/*/recibo.json"))
    inputs={"piloto_LT":v.parent/"acervo/CP04/Resultados/CNES_LT_202412_ESTOQUE_POR_CODIGO.csv",
            "candidatos":sigtap.CANDIDATOS}
    for path in lotes:
        r=json.loads(path.read_text())
        if produtos(path.parent)!=r["saidas"]:
            raise ValueError(f"Saídas divergentes {path.parent}")
        inputs[path.parent.parent.name]=path
    for arq in (v/"fontes/sigtap").rglob("*.vigencia.csv"):
        inputs["SIGTAP_"+arq.name.split("_")[1][:6]]=arq
    for r in ler(sigtap.FONTES):
        inputs["historico"+r["competencia"]]=v.parent/"acervo"/r["membro"]
    def medir(stage):
        cobertura={(f"{a}{m:02d}",f):"sem_recibo" for a in range(2014,2025) for m in range(1,13)
                   for f in ("EP","EQ","HB","LT","PF","ST","PA","SIGTAP")}
        estoques,producao=Counter(),Counter()
        for path in lotes:
            nome=path.parent.parent.name
            fam,mes=nome[:2],path.parent.name
            cobertura[mes,fam]="original_validado"
            medidas=pd.read_csv(path.parent/"medidas.csv.gz",dtype=str,keep_default_na=False)
            if fam=="PA":
                medidas["valor"]=pd.to_numeric(medidas.valor,errors="raise").astype("int64")
                keys=["competencia_producao","regiao_at","procedimento","cbo","vigencia","medida"]
                for k,n in medidas.groupby(keys).valor.sum().items():
                    producao[(mes,*k)]+=int(n)
                continue
            df=pd.read_csv(path.parent/"estoque.csv",dtype=str,keep_default_na=False)
            df["registros"]=df.registros.astype("int64")
            categorias={"ST":["TP_UNID","VINC_SUS"],"EP":["TIPO_EQP"],"PF":["CBO","PROF_SUS"],"EQ":["TIPEQUIP","CODEQUIP","IND_SUS"],
                        "LT":["TP_LEITO","CODLEITO"],"HB":["SGRUPHAB"]}
            ch=categorias[fam]
            if fam=="HB":
                ini=df.CMPT_INI.str.fullmatch(r"(19|20)\d{2}(0[1-9]|1[0-2])")
                aberta=df.CMPT_FIM.isin(["","000000","999999"])
                fim=df.CMPT_FIM.str.fullmatch(r"(19|20)\d{2}(0[1-9]|1[0-2])")
                df["vigencia"]="inclassificavel"
                df.loc[ini & (aberta|fim),"vigencia"]="fora"
                df.loc[ini & (df.CMPT_INI<=mes) & (aberta|(fim & (df.CMPT_FIM>=mes))),"vigencia"]="vigente"
                ch=ch+["vigencia"]
            for k,n in df.groupby(["regiao",*ch]).registros.sum().items():
                estoques[mes,fam,k[0],"/".join(k[1:]),"registros"]+=int(n)
            if not medidas.empty:
                medidas["valor"]=medidas.valor.astype("int64")
                for k,n in medidas.groupby(["regiao",*categorias[fam],"medida"]).valor.sum().items():
                    estoques[mes,fam,k[0],"/".join(k[1:-1]),k[-1]]+=int(n)
        # Lote LT de dezembro de 2024 já validado na custódia do Work.
        for r in ler(inputs["piloto_LT"]):
            if r["campo"] in ["QT_EXIST","QT_SUS","QT_NSUS"]:
                estoques["202412","LT",r["regiao"],r["tp_leito"]+"/"+r["cod_leito"],r["campo"]]+=int(r["quantidade"])
        cobertura["202412","LT"]="agregado_CP04_validado"
        vig=[]
        for k,path in inputs.items():
            if k.startswith("SIGTAP_"):
                mes=k[7:]
                cobertura[mes,"SIGTAP"]="tabela_oficial"
                vig.extend(ler(path))
        pd.DataFrame(vig).to_csv(stage/"sigtap_historico.csv.gz",index=False)
        sens=[]
        for r in ler(sigtap.FONTES):
            mes=r["competencia"]
            if mes not in {v["competencia"] for v in vig}:
                continue
            path=inputs["historico"+mes]
            if sha256_arquivo(path)!=r["sha256"]:
                raise ValueError("Espelho histórico alterado")
            procs,rel=sigtap.ler_edicao(path,mes)
            for it in (v for v in vig if v["competencia"]==mes):
                cod=it["codigo"]; antigo=" ".join(c for c in ("225120","225210","225203") if (cod,c) in rel) if cod==sigtap.CONSULTA else ""
                sens.append((mes,cod,int(cod in procs),it["presente"],antigo,it["cbos_consulta"],procs.get(cod,""),it["descricao"]))
        salvar(stage/"confronto_espelho_primario.csv",["mes","codigo","presente_espelho","presente_primario","cbo_espelho","cbo_primario","descricao_espelho","descricao_primario"],sens)
        salvar(stage/"cnes_mensal.csv",["competencia","familia","regiao","tipo","medida","quantidade"],
               ((*k,n) for k,n in sorted(estoques.items())))
        salvar(stage/"sia_mensal.csv",["movimento","producao","regiao_atendimento","procedimento","cbo","vigencia","medida","quantidade"],
               ((*k,n) for k,n in sorted(producao.items())))
        salvar(stage/"cobertura.csv",["competencia","familia","estado"],((*k,s) for k,s in sorted(cobertura.items())))
        return dict(competencias={f:sum(s!="sem_recibo" for (m,fam),s in cobertura.items() if fam==f)
                                 for f in ["ST","HB","LT","PF","EP","EQ","PA","SIGTAP"]},
                    competencia_movimento="PA_MVM",competencia_producao="PA_CMP",unidade="quantidades aprovadas/apresentadas e registros")
    return executar(saida,inputs,{"cadastro":"estoque na competência","producao":"vigência por PA_CMP"},medir,[Path(sigtap.__file__)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("destino",type=Path)
    a=p.parse_args()
    print(consolidar(a.v,a.destino)["controles"])
