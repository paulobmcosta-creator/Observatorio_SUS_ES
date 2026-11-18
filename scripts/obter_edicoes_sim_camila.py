"""Restaurar as edições SIM por SHA e adquirir somente originais ausentes."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import tempfile
from urllib.error import HTTPError
from zipfile import BadZipFile, ZipFile

from observatorio_sus.estudos.camila.lote import ler
from observatorio_sus.estudos.camila.sim import FONTES
from observatorio_sus.extract.adquirir_objetos import HTTPSOficial
from observatorio_sus.io.custodia import adquirir_conjunto, escrever_json, sha256_arquivo
from observatorio_sus.io.operacao_local import CAMPOS_CAMINHO, preflight


def localizar(raizes, edicoes):
    tamanhos = {int(r["bytes"]): r for r in edicoes}
    encontrados = {}
    for raiz in raizes:
        if not raiz.is_dir():
            raise ValueError(f"Custódia indisponível: {raiz}")
        def erro(exc):
            raise exc
        for base, pastas, nomes in os.walk(raiz, onerror=erro):
            pastas[:] = [n for n in pastas if n not in {".git", ".aws", ".codex", ".agents", "staging"}
                         and not n.startswith(".pendente-")]
            for n in nomes:
                p = Path(base) / n
                if p.is_symlink() or not p.is_file():
                    continue
                r = tamanhos.get(p.stat().st_size)
                if r and r["ano"] not in encontrados and sha256_arquivo(p) == r["sha256"]:
                    encontrados[r["ano"]] = p
    return encontrados


def conferir_membro(objeto, arquivo):
    with ZipFile(arquivo) as z:
        if z.namelist() != [objeto["membro"]] or z.getinfo(objeto["membro"]).file_size == 0:
            raise ValueError("Membro diferente do declarado na edição")
        # O SHA fixa o ZIP inteiro. A leitura analítica verifica também o CRC até EOF.


def obter(raizes, destino, anos, adquirir):
    destino = destino.resolve()
    if destino.is_relative_to(Path(__file__).resolve().parents[1]):
        raise ValueError("A custódia deve ficar fora do repositório")
    destino.mkdir(parents=True, exist_ok=True)
    log = Path(tempfile.mkdtemp(prefix="consulta-", dir=destino))
    edicoes = {int(r["ano"]):r for r in ler(FONTES)}
    encontrados = localizar([*raizes, destino], [edicoes[a] for a in anos])
    contexto = dict(utc=datetime.now(timezone.utc).isoformat(), raizes=[str(p) for p in [*raizes,destino]],
                    hash_edicoes=sha256_arquivo(FONTES), recuperados={k:str(v) for k,v in encontrados.items()})
    escrever_json(log/"busca.json", contexto)
    cliente = HTTPSOficial(["s3.sa-east-1.amazonaws.com"], timeout=60)
    config = {k:destino for k in CAMPOS_CAMINHO}
    config["margem_livre_bytes"] = 1024**3
    config["concorrencia_max"] = 1
    falhas = 0
    for ano in anos:
        r = edicoes[ano]
        tamanho = int(r["bytes"])
        nome = r["url"].rsplit("/",1)[-1]
        obj = dict(id=f"sim{ano}", sistema="SIM", familia="mortalidade_geral", competencia=str(ano),
                   uf="BR", parte="unica", revisao=r["sha256"], layout="CSV_nacional_anual",
                   caminho=nome, uri_oficial=r["url"], evidencia_origem="CP01/PROVENIENCIA_SIM.csv",
                   limite_bytes=tamanho, bytes=tamanho, sha256=r["sha256"], membro=r["membro"])
        resultado = dict(edicao=r, utc=datetime.now(timezone.utc).isoformat())
        try:
            if str(ano) in encontrados:
                arq = encontrados[str(ano)]
                conferir_membro(obj, arq)
                resultado.update(estado="custodia_por_sha256", arquivo=str(arq))
            elif adquirir:
                exame = preflight(config,[obj],limite_derivados_bytes=64*1024**2,limite_temporarios_bytes=0)
                resultado["preflight"] = exame
                if exame["estado"] != "APTO_NOS_LIMITES_DECLARADOS":
                    raise ValueError(f"Preflight: {exame}")
                raiz = destino/"SIM"/str(ano)
                recibo = adquirir_conjunto(raiz,[obj],cliente,validar_objeto=conferir_membro)
                arq = raiz/"versoes"/recibo["conteudo_id"]/"objetos"/nome
                resultado.update(estado="oficial_verificado", arquivo=str(arq), custodia=recibo)
            else:
                resultado.update(estado="ausente_sem_aquisicao")
        except (OSError, ValueError, RuntimeError, BadZipFile) as exc:
            falhas += 1
            resultado.update(estado="impedimento",tipo=type(exc).__name__,detalhe=str(exc))
            if isinstance(exc,HTTPError):
                resultado.update(http=exc.code, url_efetiva=exc.url,
                                 cabecalhos={k:exc.headers.get(k) for k in ("Server","Content-Type","Via","X-Mitmproxy-Blocked-Reason","x-amz-request-id")})
        escrever_json(log/f"{ano}.json", resultado)
        print(ano, resultado["estado"], resultado.get("detalhe", ""),flush=True)
    print("Manifestos:", log, flush=True)
    return int(bool(falhas))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("destino", type=Path)
    p.add_argument("--custodia", type=Path, action="append", required=True)
    p.add_argument("--anos", type=int, nargs="+", choices=range(2014,2025), default=[2022,2023,2024])
    p.add_argument("--adquirir", action="store_true")
    a=p.parse_args()
    raise SystemExit(obter(a.custodia, a.destino, list(dict.fromkeys(a.anos)), a.adquirir))
