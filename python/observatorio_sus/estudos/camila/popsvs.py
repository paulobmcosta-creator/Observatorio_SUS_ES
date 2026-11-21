"""Restaurar a série POPSVS de sete anos e pesos do Censo a partir dos originais."""
from collections import Counter
from pathlib import Path
import argparse
import json
import re
import struct
import subprocess
import zipfile

from observatorio_sus.io.custodia import sha256_arquivo
from . import territorio
from .lote import executar, ler, salvar
from .territorio import TABELA, mapa

FONTES=TABELA.parents[2]/"config/estudos/popsvs_camila.csv"

def read_population(path, municipalities):
    year = 2000 + int(path.stem[-2:])
    population = {}
    with zipfile.ZipFile(path) as archive:
        members = [name for name in archive.namelist() if name.lower().endswith(".dbf")]
        if len(members) != 1:
            raise ValueError(f"{path.name}: esperava um DBF")
        with archive.open(members[0]) as stream:
            count, header_length, record_length = struct.unpack_from("<IHH", stream.read(32), 4)
            fields = {}
            offset = 1
            for _ in range((header_length - 33) // 32):
                field = stream.read(32)
                name = field[:11].split(b"\0", 1)[0].decode("ascii")
                width = field[16]
                fields[name] = slice(offset, offset + width)
                offset += width
            required = {"COD_MUN", "ANO", "SEXO", "IDADE", "POP"}
            if not required <= fields.keys() or offset != record_length or stream.read(1) != b"\r":
                raise ValueError(f"{path.name}: cabeçalho DBF incompatível")
            for _ in range(count):
                record = stream.read(record_length)
                if len(record) != record_length:
                    raise ValueError(f"{path.name}: registro truncado")
                if record[0] not in (32,42):
                    raise ValueError("Marcador DBF inválido")
                if record[0] != 32:
                    continue
                municipality = record[fields["COD_MUN"]].strip().decode("ascii")
                if municipality not in municipalities:
                    continue
                file_year, sex, age, value = (int(record[fields[name]]) for name in ("ANO", "SEXO", "IDADE", "POP"))
                key = (municipality, sex, age)
                if file_year != year or value < 0 or key in population:
                    raise ValueError(f"{path.name}: ano, valor ou duplicidade incompatível")
                population[key] = value
            if stream.read() not in (b"", b"\x1a"):
                raise ValueError("Dados além do fim declarado do DBF")
    expected = {(code, sex, age) for code in municipalities for sex in (1, 2) for age in range(81)}
    if population.keys() != expected:
        raise ValueError(f"{path.name}: domínio municipal, sexo ou idade incompatível")
    return year, population

def census_weights(path):
    page = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-layout", str(path), "-"],
                          check=True, capture_output=True, text=True).stdout
    counts = Counter()
    for line in page.splitlines():
        group = re.match(r"^\s*(\d+) a (\d+) anos\s{2,}([\d ]+?)\s{2,}", line)
        oldest = re.match(r"^\s*100 anos ou mais\s{2,}([\d ]+?)\s{2,}", line)
        if group:
            start, end, value = group.groups()
            if int(end) != int(start) + 4:
                raise ValueError("Faixas censitárias incompatíveis")
            counts[min(85, int(start))] += int(value.replace(" ", ""))
        if oldest:
            counts[85] += int(oldest[1].replace(" ", ""))
    if set(counts) != set(range(0, 90, 5)) or counts.total() != 190_755_799:
        raise ValueError("Pesos censitários não reconciliados")
    return counts

def reconstruir(sources,municipalities,censo,saida):
    detail, controls, totals = [], [], Counter()
    for path in sources:
        meta=json.loads(path.with_suffix(".zip.proveniencia.json").read_text())
        if sha256_arquivo(path)!=meta["sha256"] or path.stat().st_size!=meta["bytes"]:
            raise ValueError(f"{path.name}: origem incompatível")
        year, population = read_population(path, municipalities)
        for (municipality, sex, age), value in sorted(population.items()):
            region = municipalities[municipality]
            band = "80+" if age == 80 else f"{age // 5 * 5:02d}"
            detail.append((year, municipality, region, sex, age, value, "80 anos ou mais" if age == 80 else "origem"))
            for scope in ("ES", region):
                totals[year, scope, "TODAS"] += value
                totals[year, scope, band] += value
                if 30 <= age <= 69:
                    totals[year, scope, "30_69"] += value
        digest=sha256_arquivo(path)
        controls.append((year, len(population), len(municipalities), 0, 80,
                         totals[year, "ES", "TODAS"], totals[year, "ES", "30_69"], digest))
    counts = census_weights(censo)
    premature = sum(counts[age] for age in range(30, 70, 5))
    salvar(saida / "POPULACAO_ES_IDADE_ORIGEM.csv", ["ano","ibge7","regiao_pdr_2024","sexo","idade_codigo","habitantes","observacao"], detail)
    salvar(saida / "CONTROLES_POPULACAO.csv", ["ano","chaves","municipios","idade_min","idade_max","total_es","total_es_30_69","sha256_zip_fonte"], controls)
    salvar(saida / "POP_DENOMINADORES.csv", ["ano","territorio","faixa","habitantes"],
         [(*key, value) for key, value in sorted(totals.items())])
    salvar(saida / "PADRAO_BRASIL_CENSO_2010.csv", ["idade_inicio","populacao","peso_total","peso_30_69"],
         [(age, value, value / counts.total(), value / premature if 30 <= age < 70 else "")
          for age, value in sorted(counts.items())])

    return dict(anos=len(sources),linhas=len(detail),pesos=len(counts))


def processar(acervo,destino):
    refs=ler(FONTES)
    entradas={r["membro"]:acervo/r["membro"] for r in refs}
    entradas.update(cadastro=TABELA,pinos=FONTES)
    def calcular(stage):
        for r in refs:
            if sha256_arquivo(entradas[r["membro"]])!=r["sha256"]:
                raise ValueError("Fonte POPSVS/Censo divergente do consolidado")
        codigos=mapa()
        municipios={r["cod_municipio_ibge"]:codigos[r["cod_municipio_cnes"]] for r in ler(TABELA)}
        zips=sorted(p for p in entradas.values() if p.suffix==".zip")
        censo=next(p for p in entradas.values() if p.suffix==".pdf")
        return reconstruir(zips,municipios,censo,stage)
    return executar(destino,entradas,{"truncamento":"80+"},calcular,[Path(territorio.__file__)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acervo",type=Path)
    p.add_argument("destino",type=Path)
    a=p.parse_args()
    print(processar(a.acervo,a.destino)["controles"])
