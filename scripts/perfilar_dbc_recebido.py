"""Preparar leitura técnica de DBC recebido legitimamente, sem aquisição remota.

Usa pyreaddbc como dependência independente (AGPL declarada, sem copiar código)
e dbfread. Não demonstra segundo decodificador independente nem contrato SIH
homologado. DBC original e marcadores DBF são preservados; resultados fora de Git.
"""
import argparse
from collections import Counter
import csv
from importlib.metadata import version
import json
from pathlib import Path
import sys
from observatorio_sus.io.custodia import sha256_arquivo


def perfilar(fonte, destino, hash_esperado, encoding, natureza):
    """Converter DBC→DBF por biblioteca madura; perfilar ativos/excluídos sem descartar."""
    if sha256_arquivo(fonte) != hash_esperado:
        raise ValueError("DBC recebido diverge do hash informado.")
    if destino.resolve().is_relative_to(Path(__file__).resolve().parents[1]):
        raise ValueError("Saída de leitura DBC deve ficar fora do checkout Git.")
    from pyreaddbc import dbc2dbf
    from dbfread import DBF
    destino.mkdir(parents=True, exist_ok=False)
    dbf = destino / "recebido.dbf"
    dbc2dbf(str(fonte), str(dbf))
    tabela = DBF(str(dbf), raw=True, load=False)
    campos = [f.name for f in tabela.fields]
    perfil, contagens = Counter(), {"ativo": 0, "excluido": 0}
    csv_path = destino / "registros_lexicos.csv"
    with csv_path.open("x", encoding="utf-8", newline="") as stream:
        w = csv.writer(stream);w.writerow(["_estado_registro_dbf", *campos])
        for estado, registros in [("ativo", tabela.records), ("excluido", tabela.deleted)]:
            for r in registros:
                valores = [r[c].decode(encoding, errors="strict") for c in campos]
                w.writerow([estado, *valores]);contagens[estado] += 1
                if "IDENT" in r:perfil[r["IDENT"].decode(encoding, errors="strict").strip()] += 1
    if sum(contagens.values()) != tabela.header.numrecords:
        raise ValueError("Cabeçalho DBF não reconcilia ativos/excluídos; não promover.")
    if sha256_arquivo(fonte) != hash_esperado:raise ValueError("DBC alterado durante a leitura.")
    resultado = dict(natureza=natureza, sha256_dbc=hash_esperado, sha256_dbf=sha256_arquivo(dbf),
                    sha256_csv=sha256_arquivo(csv_path), registros_cabecalho=tabela.header.numrecords,
                    contagens=contagens, perfil_ident=dict(perfil),
                    campos=[dict(nome=f.name,tipo=f.type,tamanho=f.length,decimais=f.decimal_count) for f in tabela.fields],
                    pyreaddbc=version("pyreaddbc"),dbfread=version("dbfread"),encoding_declarado=encoding,
                    preservacao="células DBF lexicais com padding/marcadores; ativos seguidos de excluídos; estado explícito; sem deduplicação",
                    independencia="NAO_DEMONSTRADA; pyreaddbc e wrappers PySUS podem compartilhar descendência blast",
                    estado="PERFIL_TECNICO; NAO_APROVA_LAYOUT_COORTE_OU_COBERTURA_NACIONAL")
    (destino / "perfil.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n")
    return resultado


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dbc",required=True,type=Path);p.add_argument("--sha256",required=True)
    p.add_argument("--saida",required=True,type=Path);p.add_argument("--encoding",required=True)
    p.add_argument("--natureza",required=True,choices=["empirico_recebido_nao_homologado","fixture_sintetica"])
    a=p.parse_args();r=perfilar(a.dbc,a.saida,a.sha256,a.encoding,a.natureza)
    print(json.dumps({k:r[k] for k in ['natureza','registros_cabecalho','contagens','independencia','estado']},ensure_ascii=False))
