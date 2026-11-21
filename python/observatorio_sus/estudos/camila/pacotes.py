"""Receber os volumes e os checkpoints por hash, sem executar membros recebidos."""
import argparse
import shutil
import stat
from collections import Counter
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from observatorio_sus.io.custodia import sha256_arquivo
from .lote import executar, indices, ler, salvar

CONFIG = Path(__file__).resolve().parents[4] / "config/estudos/insumos_camila.csv"


def extrair(path, destino, vistos):
    with ZipFile(path) as z:
        for info in z.infolist():
            n = PurePosixPath(info.filename)
            if (n.is_absolute() or n.as_posix() != info.filename or ".." in n.parts or
                    "\\" in info.filename or ":" in info.filename or info.filename in vistos or
                    stat.S_ISLNK(info.external_attr >> 16)):
                raise ValueError(f"Membro inválido ou repetido: {info.filename}")
            vistos.add(info.filename)
            target = destino / n
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, target.open("xb") as dst:
                shutil.copyfileobj(src, dst)


def conferir(base, esperados, nomes):
    if set(esperados) != nomes:
        raise ValueError("Domínio do inventário diverge")
    for nome, r in esperados.items():
        f = base / nome
        if f.stat().st_size != int(r["bytes"]) or sha256_arquivo(f) != r["sha256"]:
            raise ValueError(f"Integridade divergente: {nome}")


def importar(pasta, destino):
    referencias = ler(CONFIG)
    fontes = {}
    for r in referencias:
        candidatos = list(pasta.rglob(r["arquivo"]))
        if len(candidatos) != 1 or sha256_arquivo(candidatos[0]) != r["sha256"]:
            raise ValueError(f"Esperado exemplar único por hash: {r['arquivo']}")
        fontes[r["id"]] = candidatos[0]

    def processar(stage):
        div = indices(ler(fontes["divisao"]), "caminho_original")
        todos = []
        for chave in ("CP01", "CP02", "CP03", "CP04", "consolidado"):
            base = stage / chave
            vistos = set()
            volumes = ("parte1", "parte2") if chave == "consolidado" else (chave,)
            for v in volumes:
                antes = vistos.copy()
                extrair(fontes[v], base, vistos)
                if chave == "consolidado":
                    esp = {k:r for k,r in div.items() if r["parte"] == fontes[v].name}
                    conferir(base, esp, vistos - antes)
            conferir(base, indices(ler(base/"MANIFESTO_SHA256.csv"), "arquivo"),
                     vistos - {"MANIFESTO_SHA256.csv"})
            if chave == "consolidado":
                inv = ler(stage/"CP02/INVENTARIO_ATIVOS.csv")
                conferir(base, indices([r for r in inv if r["pacote"]=="Consolidado anterior"], "arquivo"), vistos)
            for nome in sorted(vistos):
                f = base / nome
                todos.append((chave, nome, f.stat().st_size, sha256_arquivo(f)))
        frequencia = Counter(r[3] for r in todos)
        salvar(stage/"ativos.csv", ["pacote","membro","bytes","sha256","ocorrencias_conteudo"],
               [(*r, frequencia[r[3]]) for r in todos])
        return {"membros":len(todos),"conteudos_distintos":len(frequencia),"consolidado":len(div)}
    return executar(destino, fontes, {"tipo":"recepcao_arquivos_work"}, processar)


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("pasta",type=Path)
    p.add_argument("destino",type=Path)
    args=p.parse_args()
    print(importar(args.pasta,args.destino)["controles"])
