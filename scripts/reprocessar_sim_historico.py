"""Adquirir oito edições históricas, verificar cada ZIP e reler por dois leitores."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys

from observatorio_sus.estudos.camila import sim
from observatorio_sus.estudos.camila.lote import ler
from observatorio_sus.io.custodia import escrever_json, sha256_arquivo
from obter_edicoes_sim_camila import localizar

ORDEM = (2014, 2015, 2017, 2016, 2018, 2019, 2020, 2021)
SCRIPTS = Path(__file__).resolve().parent


def rodar(script, argumentos, log):
    with log.open("x", encoding="utf-8") as saida:
        subprocess.run([sys.executable, "-u", str(SCRIPTS / script), *map(str, argumentos)],
                       stdout=saida, stderr=subprocess.STDOUT, check=True)


def historico(acervo, custodia, destino):
    if any(p.resolve().is_relative_to(SCRIPTS.parent) for p in (custodia, destino)):
        raise ValueError("Use custódia e destino externos")
    destino.mkdir(parents=True, exist_ok=True)
    edicoes = {int(r["ano"]): r for r in ler(sim.FONTES)}
    falhas = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        pendentes = {}
        for ano in ORDEM:
            pasta = destino / str(ano)
            pasta.mkdir(exist_ok=True)
            tentativa = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            ed = edicoes[ano]
            try:
                livre = shutil.disk_usage(destino).free
                escrever_json(pasta / f"disco-{tentativa}.json", {"livre": livre, "bytes_zip": int(ed["bytes"])})
                print(ano, "aquisição", livre, "bytes livres", flush=True)
                rodar("obter_edicoes_sim_camila.py", [custodia, "--custodia", custodia, "--anos", ano, "--adquirir"],
                      pasta / f"aquisicao-{tentativa}.log")
                zip_local = localizar([custodia], [ed])[str(ano)]
                if zip_local.stat().st_size != int(ed["bytes"]) or sha256_arquivo(zip_local) != ed["sha256"]:
                    raise ValueError("ZIP divergente")
                escrever_json(pasta / f"integridade-{tentativa}.json", dict(ed, caminho=str(zip_local)))
                tarefa = pool.submit(rodar, "confrontar_sim_camila.py",
                                     [acervo, pasta / "comparacao", "--custodia", custodia, "--anos", ano],
                                     pasta / f"confronto-{tentativa}.log")
                pendentes[tarefa] = ano
            except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
                falhas.append((ano, str(exc)))
        for tarefa in as_completed(pendentes):
            ano = pendentes[tarefa]
            try:
                tarefa.result()
                print(ano, "confronto concluído", flush=True)
            except (OSError, subprocess.CalledProcessError) as exc:
                falhas.append((ano, str(exc)))
    if falhas:
        raise RuntimeError(falhas)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("acervo", "custodia", "destino"):
        p.add_argument(arg, type=Path)
    a = p.parse_args()
    historico(a.acervo, a.custodia, a.destino)

