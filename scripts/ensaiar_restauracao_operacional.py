"""Reconstruir ambiente stdlib e executar sentinela real em diretório vazio.

Não instala pacotes externos; requer CPython 3.12 com venv já disponível no host.
Separa criação do snapshot (assistida pelo agente) do comando de restauração e
execução (subprocesso sem assistência de IA durante o comando). Ausência de
chamadas de rede no código não prova isolamento. Não é aceite por segundo operador.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import venv

from observatorio_sus.extract.adquirir_objetos import ArquivosLocais
from observatorio_sus.io.custodia import adquirir_conjunto, restaurar_snapshot, sha256_arquivo


def preparar(destino, estabelecimentos, referencia):
    """Selar snapshot local autorizado com código e entradas históricas, sem Git."""
    fontes = {"estabelecimentos": Path(estabelecimentos), "referencia": Path(referencia),
              "sentinela": Path("scripts/executar_sentinela_rue_sem_dependencias.py")}
    nomes = {"estabelecimentos": "estabelecimentos.csv", "referencia": "referencia.csv", "sentinela": "sentinela.py"}
    esperados = [dict(id=id, caminho=nomes[id], sistema="RUE_legado", familia="sentinela",
                     competencia="202601", uf="ES", parte=id, revisao="20261116", layout="rue-historica-v1",
                     bytes=f.stat().st_size, sha256=sha256_arquivo(f), limite_bytes=max(f.stat().st_size, 1),
                     uri_oficial="nao_documentada; recuperacao_acervo_institucional",
                     evidencia_origem="Work E025/E040; hashes e referências na ficha RUE") for id, f in fontes.items()]
    return adquirir_conjunto(destino, esperados, ArquivosLocais(fontes))["conteudo_id"]


def restaurar_e_executar(snapshot, vazio, identidade, exigir_isolamento_rede=False):
    """Restaurar, criar venv sem pip e executar código sentinela em subprocesso isolado."""
    inicio = time.monotonic()
    vazio = Path(vazio)
    if vazio.exists() and any(vazio.iterdir()):
        raise ValueError("Ensaio exige diretório realmente vazio.")
    versao = restaurar_snapshot(snapshot, vazio, identidade)
    ambiente = vazio / "ambiente"
    venv.EnvBuilder(with_pip=False, system_site_packages=False).create(ambiente)
    python = ambiente / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    objetos = versao / "objetos"
    resultado = vazio / "sentinela.json"
    comando = [str(python.resolve()), "-I", str((objetos / "sentinela.py").resolve()),
               str((objetos / "estabelecimentos.csv").resolve()), str((objetos / "referencia.csv").resolve()), str(resultado.resolve())]
    # Invocar o link do venv preserva seu sys.prefix; resolve() seria o runtime host.
    comando[0] = str(python.absolute())
    prefixo = []
    if exigir_isolamento_rede:
        unshare = shutil.which("unshare")
        if not unshare:
            raise RuntimeError("Isolamento de rede exigido, mas unshare não está disponível.")
        prefixo = [unshare, "--net", "--"]
    comando = prefixo + comando
    proc = subprocess.run(comando, capture_output=True, text=True, timeout=30, cwd=vazio,
                          env={"PATH": str(ambiente / "bin"), "LANG": "C.UTF-8"})
    if proc.returncode:
        raise RuntimeError("Sentinela falhou: " + proc.stderr)
    dados = json.loads(resultado.read_text())
    if dados["celulas"] != 78 or dados["divergencias"] != 0:
        raise ValueError("Sentinela diferente da contraprova R real.")
    registro = dict(tipo="ensaio_pelo_agente; nao_segundo_operador", snapshot_id=identidade,
                    diretorio_inicial="vazio_verificado", ambiente_restaurado="venv stdlib sem pip/system-site-packages",
                    dependencia_host=sys.version, comando=comando, exit_code=proc.returncode,
                    stdout=proc.stdout, segundos=time.monotonic() - inicio, resultado=dados,
                    sha256_resultado=sha256_arquivo(resultado), rede_durante_comando="NAO_MEDIDA",
                    isolamento_rede_imposto=bool(prefixo),
                    dependencia_rede="nao_identificada_por_inspecao_do_codigo; nao_equivale_a_isolamento",
                    ia_durante_comando=False, preparo_assistido_por_ia=True,
                    limites="Host CPython preexistente; sem reconstrução OS/R/Arrow; não demonstra atualização nem operador humano.")
    (vazio / "ensaio.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n")
    return registro


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cache", required=True, type=Path)
    p.add_argument("--vazio", required=True, type=Path)
    p.add_argument("--estabelecimentos", required=True)
    p.add_argument("--referencia", required=True)
    p.add_argument("--exigir-isolamento-rede", action="store_true")
    args = p.parse_args()
    id = preparar(args.cache, args.estabelecimentos, args.referencia)
    r = restaurar_e_executar(args.cache / "versoes" / id, args.vazio, id, args.exigir_isolamento_rede)
    print(json.dumps({k: r[k] for k in ["tipo", "snapshot_id", "segundos", "exit_code", "resultado"]}, ensure_ascii=False))
