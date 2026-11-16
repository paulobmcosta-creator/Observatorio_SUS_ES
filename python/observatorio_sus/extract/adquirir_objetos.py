"""Transportes substituíveis do contrato de custódia, sem regras científicas.

Leitura local de snapshot autorizado é contingência sem serviço; não demonstra
atualização. HTTPS direto exige URI oficial comprovada pelo inventário. Não
infere que ftp.datasus.gov.br ofereça o mesmo arquivo por HTTPS. Sem retries de
403, alteração de TLS/proxy ou fallback automático para espelho.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import platform
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


class ArquivosLocais:
    """Restaurar arquivos conhecidos por ID; observar identidade antes/depois da leitura."""

    def __init__(self, arquivos):
        self.arquivos = {k: Path(v) for k, v in arquivos.items()}

    @contextmanager
    def abrir(self, objeto):
        """Entregar stream binário e recibo de restauração, sem alegar coleta oficial."""
        arquivo = self.arquivos[objeto["id"]]
        antes = arquivo.stat()
        with arquivo.open("rb") as stream:
            yield stream, {"uri_oficial": objeto["uri_oficial"], "uri_efetiva": arquivo.resolve().as_uri(),
                           "transporte": "snapshot_local", "cliente": "pathlib", "versao_cliente": platform.python_version(),
                           "data_utc": datetime.now(timezone.utc).isoformat(),
                           "origem_autenticada": False, "evidencia_origem": objeto.get("evidencia_origem", "pendente")}
        depois = arquivo.stat()
        if (antes.st_dev, antes.st_ino, antes.st_size, antes.st_mtime_ns) != (
            depois.st_dev, depois.st_ino, depois.st_size, depois.st_mtime_ns
        ):
            raise ValueError("Arquivo alterado durante aquisição local.")


class HTTPSOficial:
    """Cliente padrão com TLS/proxy herdados; somente hosts oficiais documentados.

    Não há retry automático. Limite de bytes pertence ao adquirente. Redirect
    só é aceito se o host também consta da origem documentada pelo operador.
    """

    def __init__(self, hosts_oficiais, timeout=30):
        self.hosts = frozenset(hosts_oficiais)
        self.timeout = timeout
        pai = self

        class RedirectOficial(HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                pai._validar_uri(newurl)
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        self.opener = build_opener(RedirectOficial())

    def _validar_uri(self, uri):
        partes = urlparse(uri)
        if partes.scheme != "https" or partes.hostname not in self.hosts or partes.username or partes.password:
            raise ValueError("URI fora das origens HTTPS oficiais documentadas.")

    @contextmanager
    def abrir(self, objeto):
        """Abrir URI exata do inventário; conferir revisão por HEAD quando fornecida."""
        uri = objeto["uri_oficial"]
        self._validar_uri(uri)
        with self.opener.open(Request(uri), timeout=self.timeout) as resposta:
            self._validar_uri(resposta.url)
            antes = {k: resposta.headers.get(k) for k in ("ETag", "Last-Modified", "Content-Length")}
            metadata = {"uri_oficial": uri, "uri_efetiva": resposta.url, "transporte": "https_direto",
                        "cliente": "urllib", "versao_cliente": platform.python_version(),
                        "data_utc": datetime.now(timezone.utc).isoformat(), "headers": antes,
                        "origem_autenticada": "TLS_host_documentado; hash_local_nao_autentica_fonte",
                        "checksum_oficial": objeto.get("checksum_oficial"),
                        "evidencia_origem": objeto["evidencia_origem"]}
            yield resposta, metadata
            # Verificação é conservadora: se HEAD falhar, não se promove silenciosamente.
            with self.opener.open(Request(uri, method="HEAD"), timeout=self.timeout) as depois:
                for chave, valor in antes.items():
                    if valor is not None and valor != depois.headers.get(chave):
                        raise ValueError("Objeto oficial mudou durante aquisição: " + chave)
            metadata["verificacao_revisao"] = "HEAD_depois; sem_headers_nao_prova_estabilidade"
