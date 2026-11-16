"""Persistir estado e gerar fila a partir do plano canônico, sem carteira paralela.

Executar na raiz do repositório. Usa somente a biblioteca padrão Python 3.12.
O HEAD registrado é o observado antes do checkpoint (não um hash autorreferente).
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from observatorio_sus.io.checkpoints import aplicar_lote, recuperar_lote, conferir_nucleo, hash_bytes
from observatorio_sus.io.custodia import escritor_unico
from datetime import datetime, timezone

RAIZ = Path(__file__).resolve().parents[1]
DOC = RAIZ / "docs/ciclo_2026_2027/implementacao"
PLANO = RAIZ / "docs/ciclo_2026_2027/tarefas_operacionais.csv"
ESTADOS = {"CONCLUIDA", "PARCIAL", "BLOQUEADA", "PENDENTE", "NAO_APLICAVEL"}


def atomico(caminho, texto):
    """Substituir arquivo por temporário sincronizado no mesmo filesystem."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_suffix(caminho.suffix + ".tmp")
    with temporario.open("w", encoding="utf-8", newline="") as stream:
        stream.write(texto)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporario, caminho)


def serializar_csv(linhas, campos):
    """Serializar linhas de dicionários sem alterar texto/IDs."""
    stream = io.StringIO(newline="")
    escritor = csv.DictWriter(stream, fieldnames=campos, lineterminator="\n")
    escritor.writeheader()
    escritor.writerows(linhas)
    return stream.getvalue()


def _preparar_registro(checkpoint, unidade, proxima, estados=(), bloqueios=(), metadados=None):
    """Atualizar plano/estado e manter cópia anterior; retornar estado validado."""
    escritas = {}
    def guardar(caminho, texto):
        escritas[str(caminho.relative_to(RAIZ))] = texto.encode("utf-8")
    caminho = DOC / "ESTADO_EXECUCAO.json"
    estado = json.loads(caminho.read_text())
    if metadados:
        permitidos = {"status_global", "motivo_interrupcao", "publicacao_git", "pacote_previsto", "tentativas", "continuidade_cloud", "mandato_versao"}
        if set(metadados) - permitidos:
            raise ValueError("Metadados não podem substituir tarefas/identidade de checkpoint.")
        estado.update(metadados)
    plano = list(csv.DictReader(PLANO.open(encoding="utf-8")))
    por_id = {r["id"]: r for r in plano}
    assert len(por_id) == len(plano) == 52
    for valor in estados:
        chave, situacao = valor.split("=", 1)
        if situacao not in ESTADOS:
            raise ValueError(situacao)
        por_id[chave]["estado_execucao"] = situacao
    for valor in bloqueios:
        chave, motivo = valor.split("=", 1)
        por_id[chave]["bloqueio_execucao"] = motivo
    guardar(PLANO, serializar_csv(plano, list(plano[0])))
    campos = ["id", "prioridade", "objetivos", "planos", "tarefa", "dependencias_ids",
              "criterios_aceite", "evidencia_work", "estado_execucao", "bloqueio_execucao",
              "realizacao_implementacao", "parte_restante", "evidencia_implementacao"]
    guardar(DOC / "FILA_IMPLEMENTACAO.csv", serializar_csv(
        [{k: r[k] for k in campos} for r in plano], campos))
    guardar(DOC / "ESTADO_EXECUCAO.anterior.json", caminho.read_text())
    estado.update(checkpoint=checkpoint, timestamp=datetime.now(timezone.utc).isoformat(),
                  ultima_unidade_confirmada=unidade, proximas=[proxima],
                  head_observado=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=RAIZ, text=True).strip(),
                  branch=subprocess.check_output(["git", "branch", "--show-current"], cwd=RAIZ, text=True).strip(),
                  tarefas={r["id"]: {"estado": r["estado_execucao"], "bloqueio": r["bloqueio_execucao"],
                           "evidencia": r["evidencia_implementacao"], "parte_restante": r["parte_restante"]} for r in plano})
    estado["commits_confirmados"] = subprocess.check_output(
        ["git", "log", "--format=%H %s", estado["base"] + "..HEAD"], cwd=RAIZ, text=True).splitlines()
    comandos = []
    for prova in sorted(DOC.rglob("execucao.json")):
        for registro in json.loads(prova.read_text()).get("testes", []):
            comandos.append({"comando": registro["comando"], "exit_code": registro["exit_code"],
                             "evidencia": str(prova.relative_to(RAIZ))})
    estado["comandos_verificados"] = comandos
    alterados = subprocess.check_output(["git", "diff", "--name-only", estado["base"]], cwd=RAIZ, text=True).splitlines()
    novos = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=RAIZ, text=True).splitlines()
    estado["arquivos_implementacao"] = sorted(set(alterados + novos))
    guardar(caminho, json.dumps(estado, ensure_ascii=False, indent=2) + "\n")
    assert json.loads(escritas[str(caminho.relative_to(RAIZ))])["checkpoint"] == checkpoint
    log = DOC / "LOG_EXECUCAO.md"
    guardar(log, log.read_text() + f"\n- {estado['timestamp']} — **{checkpoint}**: {unidade}. Próxima: {proxima}.\n")
    guardar(DOC / "RETOMADA.md", f"""# Retomada — {checkpoint}

Leia `ESTADO_EXECUCAO.json`, `LOG_EXECUCAO.md` e a fila derivada do plano canônico.
Confira `git status`, `git log -5 --oneline` e o HEAD observado `{estado['head_observado']}`.
Branch: `{estado['branch']}`. Não recriar branch nem repetir frentes concluídas.

Última unidade confirmada: {unidade}.

Próxima unidade exata: **{proxima}**.

Insumos originais e cache autorizado: `/workspace/.cache/observatorio-mandato-cp09/`.
O ZIP anexado permanece intacto fora da árvore Git. O estado registra seu SHA-256.
Não promover staging incompleto. Aprovação funcional está em `DECISOES_R15.md`.
Gate científico/humano não é substituído por teste sintético.

Checkpoint: `python scripts/registrar_checkpoint_implementacao.py --checkpoint CP-IMP-NNN --unidade 'resultado comprovado' --proxima 'ação concreta'`.
Atualize estados com `--estado ID=PARCIAL` e bloqueio com `--bloqueio 'ID=motivo'`.
""")
    ledger = {"schema": 1, "checkpoint": checkpoint, "sha256": {n: hash_bytes(data) for n, data in escritas.items()}}
    guardar(DOC / "CHECKPOINT_INTEGRIDADE.json", json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    nomes = set(estado["arquivos_implementacao"]) | set(escritas)
    nomes.discard(str((DOC / "MANIFESTO_ENTREGAS.csv").relative_to(RAIZ)))
    linhas = []
    for nome in sorted(nomes):
        if nome in escritas:
            data = escritas[nome]
        elif (RAIZ / nome).is_file():
            data = (RAIZ / nome).read_bytes()
        else:
            continue
        linhas.append({"arquivo": nome, "bytes": len(data), "sha256": hash_bytes(data)})
    guardar(DOC / "MANIFESTO_ENTREGAS.csv", serializar_csv(linhas, ["arquivo", "bytes", "sha256"]))
    aplicar_lote(RAIZ, RAIZ / ".cache/checkpoints", escritas)

    return estado


def registrar(checkpoint, unidade, proxima, estados=(), bloqueios=(), aceitar_plano_atualizado=False, metadados=None):
    """Proteger preflight e lote recuperável com lock único de escritor."""
    with escritor_unico(RAIZ / ".cache/checkpoints"):
        if (RAIZ / ".cache/checkpoints/ATIVA.json").exists():
            raise RuntimeError("Checkpoint interrompido: executar --recuperar.")
        conferir_nucleo(RAIZ, DOC, PLANO, aceitar_plano_atualizado)
        resultado = _preparar_registro(checkpoint, unidade, proxima, estados, bloqueios, metadados)
        conferir_nucleo(RAIZ, DOC, PLANO)
        return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for nome in ["checkpoint", "unidade", "proxima"]:
        parser.add_argument("--" + nome, required=False)
    parser.add_argument("--estado", action="append", default=[])
    parser.add_argument("--bloqueio", action="append", default=[])
    parser.add_argument("--recuperar", action="store_true")
    parser.add_argument("--verificar", action="store_true")
    parser.add_argument("--aceitar-plano-atualizado", action="store_true")
    parser.add_argument("--metadados", type=Path, help="JSON de campos operacionais permitidos, aplicado na mesma geração")
    args = parser.parse_args()
    if args.recuperar or args.verificar:
        with escritor_unico(RAIZ / ".cache/checkpoints"):
            if args.recuperar:
                recuperar_lote(RAIZ, RAIZ / ".cache/checkpoints")
            conferir_nucleo(RAIZ, DOC, PLANO)
        print("Checkpoint coerente e hashes conferidos.")
        raise SystemExit(0)
    if not all([args.checkpoint, args.unidade, args.proxima]):
        parser.error("Informe checkpoint, unidade e próxima ação.")
    registrar(args.checkpoint, args.unidade, args.proxima, args.estado, args.bloqueio, args.aceitar_plano_atualizado,
              json.loads(args.metadados.read_text()) if args.metadados else None)
    print(args.checkpoint)
