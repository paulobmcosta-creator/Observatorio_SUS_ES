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


def registrar(checkpoint, unidade, proxima, estados=(), bloqueios=()):
    """Atualizar plano/estado e manter cópia anterior; retornar estado validado."""
    caminho = DOC / "ESTADO_EXECUCAO.json"
    estado = json.loads(caminho.read_text())
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
    atomico(PLANO, serializar_csv(plano, list(plano[0])))
    campos = ["id", "prioridade", "objetivos", "planos", "tarefa", "dependencias_ids",
              "criterios_aceite", "evidencia_work", "estado_execucao", "bloqueio_execucao"]
    atomico(DOC / "FILA_IMPLEMENTACAO.csv", serializar_csv(
        [{k: r[k] for k in campos} for r in plano], campos))
    atomico(DOC / "ESTADO_EXECUCAO.anterior.json", caminho.read_text())
    estado.update(checkpoint=checkpoint, timestamp=datetime.now(timezone.utc).isoformat(),
                  ultima_unidade_confirmada=unidade, proximas=[proxima],
                  head_observado=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=RAIZ, text=True).strip(),
                  branch=subprocess.check_output(["git", "branch", "--show-current"], cwd=RAIZ, text=True).strip(),
                  tarefas={r["id"]: {"estado": r["estado_execucao"], "bloqueio": r["bloqueio_execucao"]} for r in plano})
    atomico(caminho, json.dumps(estado, ensure_ascii=False, indent=2) + "\n")
    assert json.loads(caminho.read_text())["checkpoint"] == checkpoint
    log = DOC / "LOG_EXECUCAO.md"
    with log.open("a", encoding="utf-8") as stream:
        stream.write(f"\n- {estado['timestamp']} — **{checkpoint}**: {unidade}. Próxima: {proxima}.\n")
    atomico(DOC / "RETOMADA.md", f"""# Retomada — {checkpoint}

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
    alvos = [PLANO, RAIZ / "scripts/registrar_checkpoint_implementacao.py"]
    alvos += sorted(p for p in DOC.rglob("*") if p.is_file() and p.name != "MANIFESTO_ENTREGAS.csv")
    atomico(DOC / "MANIFESTO_ENTREGAS.csv", serializar_csv([
        {"arquivo": str(p.relative_to(RAIZ)), "bytes": p.stat().st_size,
         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in alvos],
        ["arquivo", "bytes", "sha256"]))
    return estado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for nome in ["checkpoint", "unidade", "proxima"]:
        parser.add_argument("--" + nome, required=True)
    parser.add_argument("--estado", action="append", default=[])
    parser.add_argument("--bloqueio", action="append", default=[])
    args = parser.parse_args()
    registrar(args.checkpoint, args.unidade, args.proxima, args.estado, args.bloqueio)
    print(args.checkpoint)
