"""Sondagem única limitada a 25s; herda proxy/CA e não tenta FTP direto.

Uso: python scripts/avaliar_aquisicao_pysus.py EVIDENCIA_JSON CACHE_NOVO
Nenhuma política de rede é alterada. O teste do catálogo não prova origem oficial.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx


def avaliar(destino, cache):
    """Registrar resultado de chamada PySUS LT/ES/202401 e probe HTTPS oficial."""
    if destino.exists() or cache.exists():
        raise FileExistsError("Use destinos novos para preservar evidências.")
    cache.mkdir(parents=True)
    env = dict(os.environ, PYSUS_CACHEPATH=str(cache.resolve()))
    programa = "from pysus import cnes; d=cnes('ES',2024,1,group='LT'); print({'linhas':len(d),'campos':len(d.columns)})"
    inicio = datetime.now(timezone.utc).isoformat()
    try:
        r = subprocess.run([sys.executable, "-c", programa], env=env, text=True, capture_output=True, timeout=25)
        tentativa = dict(returncode=r.returncode, stdout=r.stdout[-1000:], stderr=r.stderr[-2500:],
                         status="chamada_concluida_requer_auditoria" if r.returncode == 0 else "falhou_antes_de_validar_download")
    except subprocess.TimeoutExpired:
        tentativa = dict(status="timeout_25s; aquisição não validada")
    url = "https://ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados/LT/LTES2401.dbc"
    try:
        with httpx.Client(timeout=10) as client:
            response = client.head(url)
        probe = dict(url=url, metodo="HEAD", status_http=response.status_code, sucesso_download=False)
    except httpx.HTTPError as e:
        probe = dict(url=url, metodo="HEAD", erro=type(e).__name__, mensagem=str(e), sucesso_download=False)
    resultado = dict(inicio_utc=inicio, fim_utc=datetime.now(timezone.utc).isoformat(),
        pysus_versao="2.0.4", chamada="pysus.cnes('ES',2024,1,group='LT')",
        origem_transporte_catalogo="https://nbg1.your-objectstorage.com/pysus/public/catalog.db",
        tentativa=tentativa, sondagem_oficial=probe,
        conversao="não avaliada por este teste", equivalencia_metodologica="não avaliada por este teste",
        rede="restrita; proxy herdado; TCP/FTP sem concessão; sem mudança de política ou rota",
        fonte="CNES/DATASUS; biblioteca e espelho não substituem proveniência oficial")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"pysus": tentativa["status"], "sondagem_oficial": probe}, ensure_ascii=False))


if __name__ == "__main__":
    avaliar(Path(sys.argv[1]), Path(sys.argv[2]))
