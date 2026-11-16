"""Conformidade técnica e sobreposição exata antes de reutilizar o conversor CSV.

Sem recodificação ou deduplicação; SQLite temporário limita memória de chaves.
Sobreposição de linhas entre partes requer decisão, não remoção automática.
Referências CP09 M04/M12; E052/E056/E057. Não implementa leitor DBC.
"""
import csv
import hashlib
from pathlib import Path
import sqlite3
import tempfile

from observatorio_sus.io.manifestos import json_canonico
from observatorio_sus.transform.converter_csv_parquet import abrir_csv, sha256


def avaliar_regra(id, versao, universo, violacoes, *, criterio, limite=0, aplicavel=True,
                  motivo="", erro=None, obrigatoria=True):
    """Avaliar contagem de violações contra limite explícito, sem sucesso vazio.

    None indica insumo indisponível; zero obrigatório falha; execução com erro
    produz ERRO; NÃO_APLICÁVEL exige justificativa. Limite não é nota sanitária.
    """
    if not criterio or not id or not versao:
        raise ValueError("Regra precisa de ID, versão e critério justificado.")
    if erro is not None:
        estado, motivo = "ERRO", str(erro)
    elif not aplicavel:
        if not motivo:
            raise ValueError("Não aplicabilidade exige justificativa.")
        estado = "NÃO_APLICÁVEL"
    elif universo is None or violacoes is None:
        estado, motivo = "PENDENTE", motivo or "Universo/violações indisponíveis."
    elif (type(universo) is not int or type(violacoes) is not int or type(limite) is not int or
          min(universo, violacoes, limite) < 0 or violacoes > universo):
        raise ValueError("Contagens/limite inválidos.")
    elif universo == 0 and obrigatoria:
        estado, motivo = "FALHOU", "Universo obrigatório vazio."
    else:
        estado = "APROVADO" if violacoes <= limite else "FALHOU"
    return dict(id=id, versao=versao, aplicabilidade=aplicavel, universo=universo,
                violacoes=violacoes, criterio=criterio, limite=limite, estado=estado, motivo=motivo)


def validar_partes_csv(partes, campos_obrigatorios, campos_aprovados, *, encoding="utf-8", delimitador=","):
    """Perfilar CSVs por parte; comparar esquema e linhas inteiras entre partes.

    partes: dict ID→Path. Retorna contagens, campos novos e estado de sobreposição.
    Linhas repetidas dentro da mesma parte são preservadas; N_AIH não é chave.
    Mudança de ordem das colunas não oculta sobreposição; cabeçalhos devem ser
    aprovados explicitamente. Conteúdo das linhas não aparece no resultado/log.
    """
    if not partes or not campos_obrigatorios or not set(campos_obrigatorios).issubset(campos_aprovados):
        raise ValueError("Partes ou contrato de campos obrigatório ausente.")
    resumo, total, sobrepostas = [], 0, 0
    with tempfile.TemporaryDirectory(prefix="observatorio_sobreposicao_") as temporario:
        with sqlite3.connect(Path(temporario) / "linhas.sqlite") as banco:
            banco.execute("CREATE TABLE linhas (hash TEXT PRIMARY KEY, parte TEXT NOT NULL)")
            for parte, arquivo in sorted(partes.items()):
                antes = sha256(arquivo)
                with abrir_csv(arquivo, encoding) as stream:
                    leitor = csv.reader(stream, delimiter=delimitador, strict=True)
                    campos = next(leitor, [])
                    if not campos or any(not c for c in campos) or len(set(campos)) != len(campos):
                        raise ValueError("Cabeçalho ausente, vazio ou duplicado: " + parte)
                    faltantes = sorted(set(campos_obrigatorios) - set(campos))
                    novos = sorted(set(campos) - set(campos_aprovados))
                    if faltantes or novos:
                        raise ValueError(f"Esquema exige decisão: parte={parte}; faltantes={faltantes}; novos={novos}")
                    n, sobreposicao = 0, 0
                    ordem = sorted(range(len(campos)), key=lambda i: campos[i])
                    for linha in leitor:
                        if len(linha) != len(campos):
                            raise ValueError("Linha malformada: " + parte)
                        # Campos e células ordenados por nome; digest não inclui a parte.
                        digest = hashlib.sha256(json_canonico([[campos[i], linha[i]] for i in ordem])).hexdigest()
                        existe = banco.execute("SELECT parte FROM linhas WHERE hash=?", (digest,)).fetchone()
                        if existe and existe[0] != parte:
                            sobreposicao += 1
                        banco.execute("INSERT OR IGNORE INTO linhas VALUES (?, ?)", (digest, parte))
                        n += 1
                if sha256(arquivo) != antes:
                    raise ValueError("Fonte alterada durante perfilamento.")
                banco.commit()
                resumo.append(dict(id=parte, linhas=n, campos=campos, sha256=antes,
                                   linhas_sobrepostas_com_parte_anterior=sobreposicao))
                total += n; sobrepostas += sobreposicao
    return dict(partes=resumo, linhas=total, sobreposicoes=sobrepostas,
                estado="PENDENTE" if sobrepostas else "APROVADO",
                motivo="Sobreposição requer classificação documental; nenhuma linha removida." if sobrepostas else "Sem sobreposição exata entre partes.")
