"""Diagnóstico e preflight de armazenamento sem varrer arquivos pessoais.

Configuração/RAW/cache/temporários/saída/backup fora do checkout Git. Todos os
volumes são contabilizados por filesystem, somando os destinos compartilhados.
Limites são limites autorizados, não estimativas medidas da expansão DBC.
"""
import csv
import ctypes
from importlib.metadata import PackageNotFoundError, version
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

CAMPOS_CAMINHO = ("data_root", "cache", "temporarios", "saida", "backup")


def ler_configuracao(arquivo, repositorio):
    """Ler JSON explícito, sem criar diretórios ou alterar ambiente global."""
    arquivo, repositorio = Path(arquivo).resolve(), Path(repositorio).resolve()
    if arquivo.is_relative_to(repositorio):
        raise ValueError("Configuração local deve ficar fora do checkout Git.")
    config = json.loads(arquivo.read_text(encoding="utf-8"))
    for campo in CAMPOS_CAMINHO:
        valor = Path(config[campo]).expanduser()
        if not valor.is_absolute():
            raise ValueError("Caminho absoluto obrigatório: " + campo)
        valor = valor.resolve()
        if valor.is_relative_to(repositorio):
            raise ValueError("Dados/cache/saída devem ficar fora do checkout: " + campo)
        config[campo] = valor
    concorrencia = config.setdefault("concorrencia_max", 1)
    margem = config.setdefault("margem_livre_bytes", 1024**3)
    if type(concorrencia) is not int or not 1 <= concorrencia <= 4 or type(margem) is not int or margem < 0:
        raise ValueError("Concorrência deve ser 1–4 e margem não negativa.")
    return config


def ancestral_existente(path):
    """Encontrar somente o ancestral do caminho configurado, sem busca recursiva."""
    path = Path(path)
    while not path.exists():
        if path.parent == path:
            raise ValueError("Volume/caminho indisponível.")
        path = path.parent
    return path


def diagnosticar(config=None):
    """Ler SO/recursos/runtimes e nomes de processos do projeto, sem argumentos."""
    ram = None
    if platform.system() == "Linux":
        for linha in Path("/proc/meminfo").read_text().splitlines():
            if linha.startswith("MemTotal:"):
                ram = int(linha.split()[1]) * 1024; break
    elif platform.system() == "Windows":
        class Memoria(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in
                ("total", "livre", "page_total", "page_livre", "virtual_total", "virtual_livre", "extra")]
        m = Memoria(); m.length = ctypes.sizeof(m)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            ram = m.total
    runtimes = {}
    for nome in ("python", "Rscript", "git", "node", "npm"):
        caminho = shutil.which(nome)
        item = {"caminho": caminho, "versao": None}
        if caminho:
            try:
                r = subprocess.run([caminho, "--version"], capture_output=True, text=True, timeout=5)
                item.update(exit_code=r.returncode, versao=(r.stdout or r.stderr).strip()[:250])
            except (OSError, subprocess.TimeoutExpired) as e:
                item["erro"] = type(e).__name__
        runtimes[nome] = item
    dependencias = {}
    for nome in ("pyarrow", "duckdb", "pandas", "pysus", "dbfread", "pytest"):
        try: dependencias[nome] = version(nome)
        except PackageNotFoundError: dependencias[nome] = "AUSENTE_NESTE_INTERPRETADOR"
    processos = []
    try:
        cmd = ["tasklist", "/FO", "CSV", "/NH"] if platform.system() == "Windows" else ["ps", "-eo", "pid=,comm="]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        pares = [(l[1], l[0]) for l in csv.reader(io.StringIO(r.stdout)) if len(l) > 1] if platform.system() == "Windows" else [l.split(None, 1) for l in r.stdout.splitlines() if len(l.split(None, 1)) == 2]
        for pid, nome in pares:
            if Path(nome).name.lower().removesuffix(".exe") in ("r", "rscript", "python", "python3", "python3.12", "node", "npm", "git", "vite"):
                processos.append({"pid": pid, "nome": Path(nome).name})
    except (OSError, subprocess.TimeoutExpired):
        pass
    volumes = []
    caminhos = [config[k] for k in CAMPOS_CAMINHO] if config else [Path.cwd()]
    for caminho in caminhos:
        p = ancestral_existente(caminho); uso = shutil.disk_usage(p)
        volumes.append({"caminho_configurado": str(caminho), "ancestral_medido": str(p), "filesystem_id": str(p.stat().st_dev),
                        "total_bytes": uso.total, "livre_bytes": uso.free})
    return dict(sistema=platform.system(), versao_so=platform.release(), arquitetura=platform.machine(),
                cpu_logicos=os.cpu_count(), ram_total_bytes=ram, runtimes=runtimes, dependencias=dependencias,
                volumes=volumes, processos_do_projeto=processos, escopo="somente caminhos configurados e nomes de runtimes; sem argumentos/processos pessoais ou busca de arquivos")


def preflight(config, objetos, *, limite_derivados_bytes=None, limite_temporarios_bytes=None, backup_novo_bytes=0, medir=None):
    """Bloquear lote desconhecido/excessivo antes de rede/escrita. Não excluir versões."""
    medir = medir or shutil.disk_usage
    if not objetos:
        return {"estado": "BLOQUEADO", "motivo": "Inventário obrigatório vazio."}
    limites, observados = [], []
    for objeto in objetos:
        n = objeto.get("bytes_observados", objeto.get("bytes"))
        limite = objeto.get("limite_bytes", n)
        if type(limite) is not int or limite < 0 or n is not None and (type(n) is not int or n < 0 or n > limite):
            return {"estado": "BLOQUEADO", "motivo": "Volume/limite por objeto desconhecido ou inválido; não estimar por nome."}
        limites.append(limite)
        if n is not None: observados.append(n)
    for valor in (limite_derivados_bytes, limite_temporarios_bytes, backup_novo_bytes):
        if type(valor) is not int or valor < 0:
            return {"estado": "BLOQUEADO", "motivo": "Declarar limites de derivados/temporários/backup; expansão não medida."}
    requisitos = {"data_root": sum(limites), "cache": 0, "temporarios": limite_temporarios_bytes,
                  "saida": limite_derivados_bytes, "backup": backup_novo_bytes}
    volumes = {}
    for campo, bytes in requisitos.items():
        p = ancestral_existente(config[campo]); chave = str(p.stat().st_dev)
        grupo = volumes.setdefault(chave, {"caminhos": [], "necessario_bytes": 0, "livre_bytes_observado": medir(p).free})
        grupo["caminhos"].append(str(config[campo])); grupo["necessario_bytes"] += bytes
    for v in volumes.values():
        v["margem_bytes"] = config["margem_livre_bytes"]
        v["cabe"] = v["necessario_bytes"] + v["margem_bytes"] <= v["livre_bytes_observado"]
    return {"estado": "APTO_NOS_LIMITES_DECLARADOS" if all(v["cabe"] for v in volumes.values()) else "BLOQUEADO_ESPACO",
            "volumes": volumes, "bytes_observados": sum(observados), "objetos_com_tamanho_observado": len(observados),
            "objetos_esperados": len(objetos), "limite_raw_bytes": sum(limites),
            "concorrencia_configurada": config["concorrencia_max"], "concorrencia_executor_atual": 1,
            "retencao": "nenhuma exclusao automatica; versoes anteriores ja consomem o espaco livre medido",
            "limite": "Valores declarados nao sao benchmark nem estimativa medida de expansao DBC; revalidar espaco antes de cada arquivo."}
