"""Restaurar backup existente sem os arquivos de trabalho originais ou acesso remoto."""
import argparse
import json
from pathlib import Path
from ensaiar_restauracao_operacional import restaurar_e_executar
from observatorio_sus.io.custodia import restaurar_snapshot

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fonte", required=True, type=Path)
    p.add_argument("--conteudo-id", required=True)
    p.add_argument("--destino-vazio", required=True, type=Path)
    p.add_argument("--sentinela-rue", action="store_true")
    a = p.parse_args()
    if a.sentinela_rue:
        resultado = restaurar_e_executar(a.fonte, a.destino_vazio, a.conteudo_id)
        print(json.dumps({k: resultado[k] for k in ["tipo", "snapshot_id", "segundos", "exit_code", "resultado"]}, ensure_ascii=False))
    else:
        print(restaurar_snapshot(a.fonte, a.destino_vazio, a.conteudo_id))
