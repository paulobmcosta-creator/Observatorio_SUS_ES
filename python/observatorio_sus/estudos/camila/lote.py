"""Execução local em staging, com recibo vinculado aos arquivos de entrada e saída."""
import csv
import hashlib
import inspect
import json
import os
import tempfile
from pathlib import Path

from observatorio_sus.io.custodia import escrever_json, escritor_unico, sha256_arquivo, sincronizar_diretorio
from observatorio_sus.io.manifestos import json_canonico


def ler(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def salvar(path, campos, linhas):
    with path.open("x", encoding="utf-8", newline="") as stream:
        w = csv.writer(stream)
        w.writerow(campos)
        w.writerows(linhas)


def indices(linhas, campo):
    resultado = {r[campo]: r for r in linhas}
    if len(resultado) != len(linhas):
        raise ValueError(f"Duplicidade em {campo}")
    return resultado


def hashes(arquivos):
    return {k: sha256_arquivo(p) for k, p in sorted(arquivos.items())}


def produtos(raiz):
    paths = list(raiz.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise ValueError("Link inesperado no lote")
    return hashes({p.relative_to(raiz).as_posix(): p for p in paths
                   if p.is_file() and p != raiz / "recibo.json"})


def executar(destino, entradas, parametros, calcular, dependencias=()):
    """Uma versão por diretório. Um lote incompleto nunca atende uma leitura de cache."""
    destino = Path(destino).resolve()
    if destino.is_relative_to(Path(__file__).resolve().parents[4]):
        raise ValueError("Use destino externo ao checkout")
    arquivos_metodo = [Path(__file__), Path(inspect.getfile(calcular)), *dependencias]
    metodo = hashes({p.name: p for p in arquivos_metodo})
    contrato = {"entradas": hashes(entradas), "parametros": parametros, "metodo": metodo}
    identidade = hashlib.sha256(json_canonico(contrato)).hexdigest()
    with escritor_unico(destino.parent):
        if destino.exists():
            recibo = json.loads((destino / "recibo.json").read_text())
            if (recibo["id"] != identidade or recibo["contrato"] != contrato or
                    recibo["saidas"] != produtos(destino) or
                    recibo["controles"] != json.loads((destino/"controles.json").read_text())):
                raise ValueError("Destino já contém outra versão ou cache incompleto")
            return recibo
        staging = Path(tempfile.mkdtemp(prefix=".pendente-", dir=destino.parent))
        try:
            controles = calcular(staging)
            if hashes(entradas) != contrato["entradas"]:
                raise ValueError("Insumo mudou durante a execução")
            escrever_json(staging/"controles.json", controles)
            recibo = dict(id=identidade, contrato=contrato, saidas=produtos(staging), controles=controles)
            escrever_json(staging / "recibo.json", recibo)
            sincronizar_diretorio(staging)
            os.rename(staging, destino)
            sincronizar_diretorio(destino.parent)
            return recibo
        except Exception as exc:
            if staging.is_dir():
                escrever_json(staging / "FALHA.json", {"tipo": type(exc).__name__, "motivo": str(exc)})
            raise
