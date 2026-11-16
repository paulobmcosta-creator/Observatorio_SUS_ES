"""Diagnóstico cloud/local somente leitura; relatório só é gravado se solicitado."""
import argparse
import json
from pathlib import Path
from observatorio_sus.io.operacao_local import diagnosticar, ler_configuracao, preflight

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path)
    p.add_argument("--plano-lote", type=Path)
    p.add_argument("--saida", type=Path)
    a = p.parse_args()
    config = ler_configuracao(a.config, Path(__file__).resolve().parents[1]) if a.config else None
    resultado = diagnosticar(config)
    if a.plano_lote:
        if config is None: p.error("Preflight requer configuração externa ao Git.")
        lote = json.loads(a.plano_lote.read_text())
        resultado["preflight"] = preflight(config, lote["objetos"], limite_derivados_bytes=lote.get("limite_derivados_bytes"),
            limite_temporarios_bytes=lote.get("limite_temporarios_bytes"), backup_novo_bytes=lote.get("backup_novo_bytes", 0))
    data = json.dumps(resultado, ensure_ascii=False, indent=2) + "\n"
    if a.saida:
        with a.saida.open("x", encoding="utf-8") as f: f.write(data)
    else:
        print(data)
