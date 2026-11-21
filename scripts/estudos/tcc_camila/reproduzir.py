"""Validar o catálogo integral e reproduzir os agregados selecionados."""
import argparse
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

from projecao import projetar, sha
from produtos import gerar

ROOT = Path(__file__).resolve().parents[3]
PUBLIC = ROOT / "resultados_publicos/tcc_camila"
MANIFEST = ROOT / "docs/estudos/tcc_camila/MANIFESTO_PUBLICO.csv"

def ler_manifesto(nome):
    with (MANIFEST.parent / nome).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def conferir_arquivo(caminho, digest, tamanho=None):
    path = (ROOT / caminho).resolve()
    if not path.is_relative_to((ROOT / "resultados_publicos").resolve()) or not path.is_file():
        raise ValueError("Destino público inválido: " + caminho)
    if (tamanho is not None and path.stat().st_size != int(tamanho)) or sha(path) != digest:
        raise ValueError("Arquivo divergente: " + caminho)


def conferir():
    linhas = ler_manifesto("CATALOGO_RESULTADOS_318.csv")
    destinos = {r["arquivos_publicos_correspondentes"]: r for r in linhas}
    presentes = {
        f.relative_to(ROOT).as_posix()
        for familia in ("tcc_camila", "observatorio_sus_es")
        for f in (ROOT / "resultados_publicos" / familia / "arquivos_homologados").rglob("*")
        if f.is_file()
    }
    if len(linhas) != 318 or len(destinos) != 318 or set(destinos) != presentes:
        raise ValueError("Cobertura divergente do catálogo integral")
    for caminho, row in destinos.items():
        conferir_arquivo(caminho, row["sha256_original"], row["bytes_originais"])

    detalhes = ler_manifesto("MATRIZ_ABERTURA_INTEGRAL_13.csv")
    if len(detalhes) != 13 or len({r["destino_publico"] for r in detalhes}) != 13:
        raise ValueError("Cobertura divergente dos 13 originais detalhados")
    suplementos = {r["arquivo_publico"]: r["sha256_publico"] for r in ler_manifesto("MATRIZ_TRANSFORMACOES.csv")}
    referencias = set()
    for row in detalhes:
        original = destinos[row["destino_publico"]]
        if (row["sha256"], row["bytes"]) != (original["sha256_original"], original["bytes_originais"]):
            raise ValueError("Matriz de abertura divergente: " + row["destino_publico"])
        referencias.update(row["representacao_adicional_ja_existente"].split(";"))
    if referencias != set(suplementos):
        raise ValueError("Cobertura divergente das representações adicionais")
    for caminho, digest in suplementos.items():
        conferir_arquivo(caminho, digest)

    historico = ler_manifesto("MANIFESTO_PUBLICO.csv")
    selecao = {r["caminho"] for r in historico}
    membros = {f.relative_to(ROOT).as_posix() for pasta in ("dados", "figuras")
               for f in (PUBLIC / pasta).rglob("*") if f.is_file()}
    if len(historico) != 17 or len(selecao) != 17 or selecao != membros:
        raise ValueError("Cobertura divergente da seleção histórica")
    for row in historico:
        conferir_arquivo(row["caminho"], row["sha256"], row["bytes"])
    print(f"318 originais, 13 detalhados, {len(suplementos)} representações adicionais e 17 arquivos da seleção histórica conferidos.")

def novo(path):
    if path.exists() and any(path.iterdir()):
        raise ValueError("A saída precisa ser um diretório novo ou vazio")
    path.mkdir(parents=True, exist_ok=True)
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modos = parser.add_subparsers(dest="modo", required=True)
    modos.add_parser("validar-pacote")
    modos.add_parser("teste-sintetico")
    modo = modos.add_parser("gerar-resultados-publicos")
    modo.add_argument("--academico", type=Path, required=True, help="Raiz privada consolidada, com hashes da edição congelada")
    modo.add_argument("--saida", type=Path, required=True)
    modo = modos.add_parser("reproduzir-com-agregados")
    modo.add_argument("--saida", type=Path, required=True)
    modos.add_parser("reproduzir-fontes-oficiais", help="Informar os requisitos da reconstrução integral")
    args = parser.parse_args()
    if args.modo=="validar-pacote":conferir()
    elif args.modo=="teste-sintetico":
        with tempfile.TemporaryDirectory(prefix="tc") as temp:
            subprocess.run([
                sys.executable, "-m", "pytest", "-q", "-rs", "--basetemp", str(Path(temp) / "p"),
                "tests/python", "scripts/integracao_estabelecimentos",
                "scripts/estudos/tcc_camila/test_reproducao.py",
            ], cwd=ROOT, check=True)
    elif args.modo=="gerar-resultados-publicos":
        out=args.saida.resolve()
        if out.is_relative_to(args.academico.resolve()):parser.error("Informe saída externa à edição acadêmica")
        projetar(args.academico, novo(out)/"dados")
        gerar(out/"dados",out)
    elif args.modo=="reproduzir-com-agregados":
        conferir()
        gerar(PUBLIC/"dados",novo(args.saida))
    else:
        parser.exit(2,"Reconstrução integral desde os originais não demonstrada. Requer inventários certificados de DBC/DBF, população, regras SIGTAP e execução histórica completa. Consulte COMO_REPRODUZIR.md.\n")

if __name__=="__main__":
    main()
