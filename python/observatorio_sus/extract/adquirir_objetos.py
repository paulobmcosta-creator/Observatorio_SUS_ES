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
import ftplib
from contextlib import closing
from urllib.parse import unquote, quote
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


class FTPOficial:
    """FTP stdlib pela rota explícita do inventário, sem conversão presumida a HTTPS.

    Começa sequencial e sem retries. A injeção de fábrica permite ensaio sem rede.
    FTP anônimo não oferece autenticação criptográfica do servidor/conteúdo.
    """

    def __init__(self, hosts_oficiais=("ftp.datasus.gov.br",), timeout=30, fabrica=ftplib.FTP):
        self.hosts = frozenset(hosts_oficiais)
        self.timeout, self.fabrica = timeout, fabrica

    def _uri(self, uri):
        p = urlparse(uri)
        caminho = unquote(p.path)
        if (p.scheme != "ftp" or p.hostname not in self.hosts or p.username or p.password or p.query or p.fragment or
            not caminho.startswith("/") or ".." in caminho.split("/") or any(c in caminho for c in "\r\n\x00")):
            raise ValueError("URI FTP fora da origem/caminho documentados.")
        return p, caminho

    @contextmanager
    def _conectar(self, partes):
        cliente = self.fabrica()
        try:
            cliente.connect(partes.hostname, partes.port or 21, timeout=self.timeout)
            cliente.login("anonymous", "anonymous@")
            cliente.voidcmd("TYPE I")
            yield cliente
        finally:
            cliente.close()

    def _revisao(self, cliente, caminho):
        def observar(funcao):
            try:
                return funcao()
            except ftplib.error_perm as erro:
                if str(erro).startswith(("500", "502")):
                    return None  # Servidor não oferece esse metadado; não afirmar estabilidade.
                raise
        return {"size": observar(lambda: cliente.size(caminho)),
                "mdtm": observar(lambda: cliente.sendcmd("MDTM " + caminho))}

    @contextmanager
    def abrir(self, objeto):
        uri = objeto["uri_oficial"]
        partes, caminho = self._uri(uri)
        with self._conectar(partes) as cliente:
            antes = self._revisao(cliente, caminho)
            metadata = dict(uri_oficial=uri, uri_efetiva=uri, transporte="ftp_nativo", cliente="ftplib",
                            versao_cliente=platform.python_version(), data_utc=datetime.now(timezone.utc).isoformat(),
                            revisao_antes=antes, origem_autenticada=False,
                            evidencia_origem=objeto.get("evidencia_origem", "pendente"),
                            headers={"Content-Length": str(antes["size"])} if antes["size"] is not None else {})
            with closing(cliente.transfercmd("RETR " + caminho)) as socket_dados:
                with socket_dados.makefile("rb") as stream:
                    yield stream, metadata
            cliente.voidresp()
            depois = self._revisao(cliente, caminho)
            if antes != depois:
                raise ValueError("Arquivo FTP mudou durante aquisição.")
            metadata["revisao_depois"] = depois
            metadata["estabilidade"] = "metadados_iguais; nao_autentica_bytes" if any(v is not None for v in antes.values()) else "nao_observavel"

    def descobrir_rd(self, uri_diretorio, competencia):
        """Usar MLSD observado; preservar partes e metadados sem inventar ausência."""
        import re
        partes, caminho = self._uri(uri_diretorio)
        if not re.fullmatch(r"20\d{2}(0[1-9]|1[0-2])", competencia):
            raise ValueError("Competência inválida.")
        encontrados = []
        with self._conectar(partes) as cliente:
            for nome, fatos in cliente.mlsd(caminho, facts=["type", "size", "modify"]):
                if fatos.get("type") != "file" or not re.fullmatch(r"RD[A-Z]{2}" + competencia[2:] + r"[A-Za-z0-9_-]*\.dbc", nome, re.I):
                    continue
                if not fatos.get("size", "").isdigit():
                    raise ValueError("Catálogo sem tamanho observado; requer tratamento documentado.")
                encontrados.append(dict(nome=nome, uri_oficial=uri_diretorio.rstrip("/") + "/" + quote(nome),
                                        bytes=int(fatos["size"]), revisao=fatos.get("modify") or "nao_informada_no_catalogo"))
        return encontrados
