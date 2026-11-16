"""Custódia local de conjuntos imutáveis com escritor único e ponteiro atômico.

Implementação própria (MIT), orientada por CP09 M01/M02/M05/M11 e E051–E054.
Não autentica uma origem só pelo hash. Não promete durabilidade ante falta de
energia: fsync é solicitado; a plataforma e o armazenamento precisam de ensaio.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import uuid

from observatorio_sus.io.manifestos import criar_identidade_conjunto, json_canonico


def sha256_arquivo(caminho):
    """Hash em streaming de arquivo local, sem carregar o conjunto em memória."""
    with Path(caminho).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def sincronizar_diretorio(caminho):
    """Solicitar fsync de diretório POSIX; erro impede afirmar sucesso durável."""
    fd = os.open(caminho, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def escrever_json(caminho, valor):
    """Escrever arquivo novo, sem sobrescrever outro objeto."""
    with Path(caminho).open("xb") as stream:
        stream.write(json_canonico(valor) + b"\n")
        stream.flush(); os.fsync(stream.fileno())


@contextmanager
def escritor_unico(raiz):
    """Reservar lock exclusivo; crash exige inspeção e recuperação manual explícita.

    Não expira lock automaticamente por PID/tempo: outro host pode estar ativo.
    A raiz é armazenamento local autorizado, sem escritores externos ao contrato.
    """
    raiz = Path(raiz)
    raiz.mkdir(parents=True, exist_ok=True)
    lock = raiz / "escritor.lock"
    try:
        lock.mkdir()
    except FileExistsError:
        raise RuntimeError("Escritor ocupado ou lock de crash; inspecionar owner.json antes de recuperar.") from None
    try:
        escrever_json(lock / "owner.json", {"pid": os.getpid(), "host": socket.gethostname(),
                     "utc": datetime.now(timezone.utc).isoformat()})
        yield raiz
    finally:
        shutil.rmtree(lock)


def validar_versao(diretorio, identidade=None):
    """Verificar manifesto, hash/tamanho por objeto e arquivos exatos, recusando links."""
    diretorio = Path(diretorio)
    if diretorio.is_symlink():
        raise ValueError("Versão não pode ser link.")
    for p in diretorio.rglob("*"):
        if p.is_symlink():
            raise ValueError("Link não permitido em snapshot.")
    manifesto = json.loads((diretorio / "conteudo.json").read_text(encoding="utf-8"))
    calculada, canonico = criar_identidade_conjunto(manifesto["objetos"])
    if manifesto != canonico or (identidade is not None and identidade != calculada):
        raise ValueError("Identidade do manifesto diverge.")
    esperados = {"conteudo.json"}
    for objeto in canonico["objetos"]:
        arquivo = diretorio / "objetos" / objeto["caminho"]
        esperados.add("objetos/" + objeto["caminho"])
        if arquivo.stat().st_size != objeto["bytes"] or sha256_arquivo(arquivo) != objeto["sha256"]:
            raise ValueError("Objeto corrompido: " + objeto["id"])
    encontrados = {p.relative_to(diretorio).as_posix() for p in diretorio.rglob("*") if p.is_file()}
    if encontrados != esperados:
        raise ValueError("Arquivos ausentes ou não manifestados no snapshot.")
    return calculada, canonico


class ErroPromocao(OSError):
    """Falha com estado observado após a operação; não implica rollback automático."""

    def __init__(self, resultado, causa):
        super().__init__(f"Promoção {resultado['promocao']}: {type(causa).__name__}")
        self.resultado = resultado


def inspecionar_ponteiro(raiz):
    """Observar ponteiro e integridade sem modificar estado ou inferir durabilidade."""
    try:
        ponteiro = json.loads((Path(raiz) / "CURRENT.json").read_text())
        identidade = ponteiro["conteudo_id"]
        if len(identidade) != 64 or any(c not in "0123456789abcdef" for c in identidade):
            raise ValueError("ID inválido.")
        validar_versao(Path(raiz) / "versoes" / identidade, identidade)
        return {"estado": "versao_integra", "conteudo_id": identidade}
    except FileNotFoundError:
        return {"estado": "ausente_ou_incompleto", "conteudo_id": None}
    except (ValueError, KeyError, TypeError, OSError) as erro:
        return {"estado": "indeterminado", "conteudo_id": None, "erro": type(erro).__name__}


def promover(raiz, identidade):
    """Trocar ponteiro somente para versão integral validada, sob lock do chamador."""
    validar_versao(raiz / "versoes" / identidade, identidade)
    temporario = raiz / ("CURRENT." + uuid.uuid4().hex + ".tmp")
    antes = inspecionar_ponteiro(raiz)
    fase = "antes_replace"
    try:
        escrever_json(temporario, {"schema": 1, "conteudo_id": identidade})
        fase = "replace_iniciado"
        os.replace(temporario, raiz / "CURRENT.json")
        fase = "replace_retornou"
        sincronizar_diretorio(raiz)
        return {"promocao": "realizada", "durabilidade": "fsync_solicitado_com_sucesso",
                "ponteiro_ativo": inspecionar_ponteiro(raiz), "rollback_automatico": False}
    except BaseException as erro:
        depois = inspecionar_ponteiro(raiz)
        novo_ativo = depois["estado"] == "versao_integra" and depois["conteudo_id"] == identidade
        resultado = {"promocao": "versao_integra_ativa" if novo_ativo else
                     ("nao_realizada" if depois == antes else "indeterminada"),
                     "durabilidade": "indeterminada" if fase != "antes_replace" else "nao_avaliada",
                     "fase": fase, "ponteiro_anterior": antes, "ponteiro_ativo": depois,
                     "rollback_automatico": False}
        raise ErroPromocao(resultado, erro) from erro
    finally:
        temporario.unlink(missing_ok=True)


def adquirir_conjunto(raiz, esperados, adaptador, *, validar_objeto=None, antes_promocao=None):
    """Adquirir cada objeto por adaptador.abrir(objeto), validar e promover integralmente.

    esperados: objetos do contrato com bytes/sha256 opcionais (None), URIs e
    limite_bytes obrigatório. Adaptador retorna contexto (stream, metadados).
    validar_objeto recebe objeto/caminho e deve lançar erro se reprovar. Ausências
    não resolvidas nunca são zero. Antes de promover, todos os hashes são relidos.
    antes_promocao é ponto de falha injetável usado nos testes, não regra sanitária.
    """
    # Valida aliases antes de abrir rede; placeholders só para checagem estrutural.
    criar_identidade_conjunto([{**o, "bytes": o.get("bytes") or 0, "sha256": o.get("sha256") or "0" * 64} for o in esperados])
    if any(type(o.get("limite_bytes")) is not int or o["limite_bytes"] <= 0 for o in esperados):
        raise ValueError("Limite de aquisição por objeto obrigatório.")
    with escritor_unico(raiz) as raiz:
        staging = raiz / "staging" / uuid.uuid4().hex
        staging.mkdir(parents=True)
        objetos, recibos = [], []
        try:
            for objeto in sorted(esperados, key=lambda o: o["id"]):
                arquivo = staging / "objetos" / objeto["caminho"]
                arquivo.parent.mkdir(parents=True, exist_ok=True)
                digest, tamanho = hashlib.sha256(), 0
                with adaptador.abrir(objeto) as (origem, metadados), arquivo.open("xb") as destino:
                    for bloco in iter(lambda: origem.read(1024 * 1024), b""):
                        tamanho += len(bloco)
                        if tamanho > objeto["limite_bytes"]:
                            raise ValueError("Objeto excede limite autorizado.")
                        destino.write(bloco); digest.update(bloco)
                    destino.flush(); os.fsync(destino.fileno())
                declarado = metadados.get("headers", {}).get("Content-Length")
                if declarado is not None and (not str(declarado).isdigit() or int(declarado) != tamanho):
                    raise ValueError("Content-Length diverge dos bytes recebidos.")
                if ((objeto.get("bytes") is not None and tamanho != objeto["bytes"]) or
                    (objeto.get("sha256") is not None and digest.hexdigest() != objeto["sha256"])):
                    raise ValueError("Fonte diverge do tamanho/hash esperado: " + objeto["id"])
                if validar_objeto is not None:
                    validar_objeto(objeto, arquivo)
                objetos.append({**objeto, "bytes": tamanho, "sha256": digest.hexdigest()})
                recibos.append({**objeto, **metadados, "bytes": tamanho, "sha256": digest.hexdigest(),
                                "status": "validado", "criterio_validacao": "integridade" if validar_objeto is None else "integridade_e_callback"})
            identidade, manifesto = criar_identidade_conjunto(objetos)
            escrever_json(staging / "conteudo.json", manifesto)
            validar_versao(staging, identidade)
            for diretorio in sorted((p for p in staging.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                sincronizar_diretorio(diretorio)
            sincronizar_diretorio(staging)
            versoes = raiz / "versoes"; versoes.mkdir(exist_ok=True)
            versao = versoes / identidade
            if versao.exists():
                validar_versao(versao, identidade)  # Reexecução não sobrescreve versão imutável.
            else:
                staging.rename(versao); sincronizar_diretorio(versoes)
            recibo = {"schema": 1, "conteudo_id": identidade, "utc": datetime.now(timezone.utc).isoformat(),
                      "esperados": len(esperados), "obtidos": len(objetos), "validados": len(objetos), "objetos": recibos}
            eventos = raiz / "recibos"; eventos.mkdir(exist_ok=True)
            arquivo_recibo = eventos / (uuid.uuid4().hex + ".json")
            escrever_json(arquivo_recibo, recibo)
            sincronizar_diretorio(eventos)
            if antes_promocao is not None:
                antes_promocao(versao)
            promocao = promover(raiz, identidade)
            return {"conteudo_id": identidade, "manifesto": manifesto, "recibo_sha256": sha256_arquivo(arquivo_recibo), "promocao": promocao}
        except BaseException as erro:
            # Não apaga a trilha de falha ao remover staging. Nenhum conteúdo de linha é logado.
            eventos = raiz / "recibos"; eventos.mkdir(exist_ok=True)
            validados = {r["id"]: r for r in recibos}
            falho = objeto["id"] if "objeto" in locals() else None
            escrever_json(eventos / (uuid.uuid4().hex + ".falha.json"), {
                "schema": 1, "utc": datetime.now(timezone.utc).isoformat(),
                "status": "falha_estado_observado", "erro": type(erro).__name__,
                "promocao": erro.resultado if isinstance(erro, ErroPromocao) else {
                    "promocao": "nao_iniciada", "ponteiro_ativo": inspecionar_ponteiro(raiz), "rollback_automatico": False},
                "motivo": str(erro)[:500], "objetos": [validados.get(o["id"], {
                    "id": o["id"], "status": "falha" if o["id"] == falho else "esperado",
                    "evidencia": "excecao_local; nao_prova_inexistencia_oficial"}) for o in esperados]})
            raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)


def restaurar_snapshot(fonte, destino, identidade):
    """Reconstruir custódia a partir de versão integral para diretório realmente vazio."""
    destino = Path(destino)
    if destino.exists() and any(destino.iterdir()):
        raise ValueError("Restauração exige diretório vazio.")
    validar_versao(fonte, identidade)
    with escritor_unico(destino) as raiz:
        versoes = raiz / "versoes"; versoes.mkdir()
        shutil.copytree(fonte, versoes / identidade)
        validar_versao(versoes / identidade, identidade)
        promover(raiz, identidade)
    return destino / "versoes" / identidade


def retornar_versao(raiz, identidade):
    """Restaurar ponteiro de versão existente íntegra; nenhuma fonte é alterada."""
    with escritor_unico(raiz) as raiz:
        if not isinstance(identidade, str) or len(identidade) != 64 or any(c not in "0123456789abcdef" for c in identidade):
            raise ValueError("ID de conteúdo inválido.")
        promover(raiz, identidade)
