"""Lote de RD das demais UFs com projeção de residentes no ES e controle de cobertura."""
import argparse
import json
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from assistencia_ftp_camila import obter
from oferta_producao_camila import blocos
from observatorio_sus.estudos.camila import assistencia as ass
from observatorio_sus.estudos.camila.lote import executar, salvar, ler
from observatorio_sus.estudos.camila.territorio import mapa,TABELA


def processar(v,nome):
    uf=nome[2:4]
    if uf=="ES":
        raise ValueError("Para o arquivo estadual usar o leitor de atendimento")
    mes="20"+nome[-4:]
    path=obter(v,nome,reserva=750_000_000,fator=5)
    def medir(stage):
        with path.open("rb") as f:
            n,h,t=struct.unpack_from("<IHH",f.read(32),4)
        if shutil.disk_usage(stage).free<500_000_000+3*(n*t+h+path.stat().st_size):
            raise OSError("Espaço disponível inferior ao de três decodificações concomitantes")
        reg=mapa()
        fluxos,qa,ids=Counter(),Counter(),Counter()
        campos="ANO_CMPT MES_CMPT MUNIC_RES MUNIC_MOV DIAG_PRINC IDENT SEXO COD_IDADE IDADE DT_INTER DT_SAIDA N_AIH".split()
        with tempfile.TemporaryDirectory(dir=stage) as tmp:
            shutil.copyfile(path,Path(tmp)/"rd.dbc")
            subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('rd.dbc','rd.dbf')"],cwd=tmp,check=True)
            for b,n in blocos(Path(tmp)/"rd.dbf",campos):
                a=b["estado"]==b" "
                excl=b["estado"]==b"*"
                if not (a|excl).all():
                    raise ValueError("Marcador RD inválido")
                qa["ativos"]+=int(a.sum())
                qa["excluidos"]+=int(excl.sum())
                b=b[a]
                if not ((b["ANO_CMPT"]==mes[:4].encode())&(b["MES_CMPT"]==mes[4:].encode())).all():
                    raise ValueError("Competência RD divergente")
                resid=np.char.startswith(b["MUNIC_RES"],b"32")
                qa["residentes_todas_causas"]+=int(resid.sum())
                for row in b[resid & (b["IDENT"]==b"1")]:
                    aa={k:row[k].decode("latin1").strip() for k in campos}
                    cid=ass.causa(aa["DIAG_PRINC"])
                    if len(cid) not in (3,4) or not cid.startswith("I") or not cid[1:3].isdigit():
                        continue
                    r,at=aa["MUNIC_RES"],aa["MUNIC_MOV"]
                    dt,alta=ass.iso(aa["DT_INTER"]),ass.iso(aa["DT_SAIDA"])
                    qa["datas_inconsistentes"]+=dt is None or alta is None or alta<dt
                    if aa["N_AIH"]:
                        ids[aa["N_AIH"]]+=1
                    else:
                        qa["aih_ausente"]+=1
                    fluxos[mes,uf,dt.year if dt else 0,r,ass.situacao(r,reg),at,ass.situacao(at,reg),aa["SEXO"],aa["COD_IDADE"],aa["IDADE"],cid]+=1
        qa["cabecalho"]=n
        qa["repeticoes_aih"]=sum(v-1 for v in ids.values())
        if qa["ativos"]+qa["excluidos"]!=n:
            raise ValueError("Cabeçalho RD divergente")
        cols="competencia uf_arquivo ano_admissao municipio_res regiao_res municipio_atend regiao_atend sexo_sih unidade_idade idade diagnostico".split()
        salvar(stage/"fluxos.csv",[*cols,"aih"],((*k,v) for k,v in sorted(fluxos.items())))
        return dict(qa=dict(qa),residentes_circulatorios=fluxos.total())
    rec=executar(v/"sih-residentes"/nome/mes,{"dbc":path,"pdr":TABELA},{"uf":uf,"mes":mes,"universo":"residência ES, IDENT1, I00-I99"},medir,
                 [Path(sys.modules[blocos.__module__].__file__),Path(ass.__file__)])
    controle=v/"sih"/nome/mes/"fluxos.csv"
    if controle.exists():
        anterior=[r for r in ler(controle) if r["municipio_res"].startswith("32")]
        novo=ler(v/"sih-residentes"/nome/mes/"fluxos.csv")
        if {tuple(r.values()) for r in anterior}!={tuple(r.values()) for r in novo}:
            raise ValueError("Leitores RD divergem nos residentes do ES")
    return rec["id"]


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("nomes",nargs="+")
    a=p.parse_args()
    def rodar(n):
        try:
            return dict(nome=n,id=processar(a.v,n))
        except Exception as e:
            return dict(nome=n,erro=str(e),tipo=type(e).__name__)
    with ThreadPoolExecutor(3) as pool:
        for r in pool.map(rodar,a.nomes):
            print(json.dumps(r),flush=True)
