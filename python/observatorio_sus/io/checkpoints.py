"""A07: lote recuperável de checkpoints sobre arquivos de projeção existentes.

O journal fora de Git conserva bytes anteriores/novos e hashes. Sob escritor
único, uma interrupção é concluída para a geração já preparada. Alteração de
terceiros fora dos hashes anterior/novo bloqueia a recuperação antes da escrita.
Não se afirma transação atômica global ou resistência a queda de energia.
"""
import hashlib
import json
import os
from pathlib import Path
import uuid

from observatorio_sus.io.custodia import sincronizar_diretorio
from observatorio_sus.io.manifestos import caminho_normalizado


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def hash_existente(path):
    return hash_bytes(path.read_bytes()) if path.is_file() else None


def substituir_bytes(path, data):
    """Substituir no mesmo diretório, com temporário único e sincronização."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with tmp.open("xb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
        sincronizar_diretorio(path.parent)
    finally:
        tmp.unlink(missing_ok=True)


def recuperar_lote(raiz, controle, apos_escrita=None):
    """Concluir geração interrompida; chamador deve possuir lock exclusivo."""
    ativa = controle / "ATIVA.json"
    if not ativa.exists():
        return False
    referencia = json.loads(ativa.read_text())
    token = referencia["transacao"]
    if len(token) != 32 or any(c not in "0123456789abcdef" for c in token):
        raise ValueError("Journal ativo inválido.")
    diretorio = controle / token
    data = (diretorio / "journal.json").read_bytes()
    if hash_bytes(data) != referencia["sha256_journal"]:
        raise ValueError("Journal diverge do hash publicado.")
    journal = json.loads(data)
    for r in journal:
        caminho_normalizado(r["arquivo"])
        if hash_bytes((diretorio / "novos" / r["arquivo"]).read_bytes()) != r["novo"]:
            raise ValueError("Geração preparada corrompida.")
        atual = hash_existente(raiz / r["arquivo"])
        if atual not in (r["anterior"], r["novo"]):
            raise RuntimeError("Alteração externa preservada; resolver conflito: " + r["arquivo"])
    for i, r in enumerate(journal):
        substituir_bytes(raiz / r["arquivo"], (diretorio / "novos" / r["arquivo"]).read_bytes())
        if apos_escrita:
            apos_escrita(i)
    ativa.unlink()
    sincronizar_diretorio(controle)
    return True


def aplicar_lote(raiz, controle, arquivos, apos_escrita=None):
    """Preparar todos os bytes antes de escrever projeções; escritor único externo."""
    if (controle / "ATIVA.json").exists():
        raise RuntimeError("Checkpoint interrompido: executar --recuperar antes de continuar.")
    token = uuid.uuid4().hex
    diretorio = controle / token
    diretorio.mkdir(parents=True)
    journal = []
    for nome, data in sorted(arquivos.items()):
        caminho_normalizado(nome)
        destino = raiz / nome
        anterior = destino.read_bytes() if destino.is_file() else None
        substituir_bytes(diretorio / "novos" / nome, data)
        if anterior is not None:
            substituir_bytes(diretorio / "anteriores" / nome, anterior)
        journal.append({"arquivo": nome, "anterior": hash_bytes(anterior) if anterior is not None else None,
                        "novo": hash_bytes(data)})
    data = json.dumps(journal, ensure_ascii=False, sort_keys=True).encode()
    substituir_bytes(diretorio / "journal.json", data)
    substituir_bytes(controle / "ATIVA.json", json.dumps({"transacao": token, "sha256_journal": hash_bytes(data)}).encode())
    recuperar_lote(raiz, controle, apos_escrita)


def conferir_nucleo(raiz, doc, plano, aceitar_plano_atualizado=False):
    """Conferir 52 IDs, estados e hashes vinculados ao último checkpoint."""
    import csv
    p = list(csv.DictReader(plano.open(encoding="utf-8")))
    q = list(csv.DictReader((doc / "FILA_IMPLEMENTACAO.csv").open(encoding="utf-8")))
    estado = json.loads((doc / "ESTADO_EXECUCAO.json").read_text())
    if len(p) != 52 or len({r["id"] for r in p}) != 52 or {r["id"] for r in p} != {r["id"] for r in q}:
        raise ValueError("Plano/fila devem preservar exatamente 52 IDs únicos.")
    if not aceitar_plano_atualizado and {r["id"]: r["estado_execucao"] for r in p} != {r["id"]: r["estado_execucao"] for r in q}:
        raise ValueError("Plano/fila divergentes; declarar edição canônica ou recuperar geração.")
    if {r["id"]: r["estado_execucao"] for r in q} != {k: r["estado"] for k, r in estado["tarefas"].items()}:
        raise ValueError("Fila/estado divergentes.")
    if estado["checkpoint"] not in (doc / "RETOMADA.md").read_text():
        raise ValueError("Retomada aponta para outra geração.")
    ledger = doc / "CHECKPOINT_INTEGRIDADE.json"
    if ledger.exists():
        registro = json.loads(ledger.read_text())
        if registro["checkpoint"] != estado["checkpoint"]:
            raise ValueError("Ledger e estado não correspondem.")
        for nome, digest in registro["sha256"].items():
            if aceitar_plano_atualizado and raiz / nome == plano:
                continue
            if hash_existente(raiz / nome) != digest:
                raise ValueError("Núcleo alterado desde o checkpoint: " + nome)
    return estado
