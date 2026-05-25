# Etapa 5N — reinício da trilha CNES/Python pela API funcional do PySUS

## 1. Objetivo
Esta etapa reinicia a trilha CNES/Python com base no caminho funcional já validado em ambiente local do pesquisador:

```python
from pysus import cnes

cnes(state=UF, year=ano, month=mes, group=grupo)
```

Escopo desta etapa:
- não executa migração plena;
- não substitui R;
- não gera base versionada;
- não altera dados;
- não altera metadados;
- não altera `docs/cnes`.

## 2. Justificativa da reinicialização
- As tentativas anteriores da Etapa 5 focaram em FTP, arquivos remotos, HEAD, tamanho e URL.
- Esse caminho tornou-se distante do uso funcional do PySUS já observado em ambiente local.
- O pesquisador responsável indicou script funcional com `from pysus import cnes`.
- Por isso, a trilha CNES/Python deve recomeçar por reconhecimento da API do PySUS, não por descoberta manual de FTP.

## 3. Código local funcional informado pelo pesquisador
Trecho informado:

```python
from pysus import cnes

df = cnes(
    state=UF,
    year=ano,
    month=mes,
    group=grupo,
)
```

Referências operacionais:
- UF = ES;
- grupos ST, LT e SR;
- período local usado: 2008–2024;
- script local: `baixar_cnes_es_2008_2024.py`;
- esta etapa não reproduz 2008–2024, apenas um piloto de reconhecimento.

## 4. Artefatos descartados/supersedidos
Documentos removidos/supersedidos:
- `docs/migracao_python/05R_reinicio_etapa5_recorte_cnes_pos_download.md`
- `docs/migracao_python/05D_descoberta_operacional_arquivos_cnes.md`
- `docs/migracao_python/05D_revisao_pos_descoberta_operacional_cnes.md`
- `docs/migracao_python/05M_deliberacao_download_piloto_sem_limite_cnes.md`
- `docs/migracao_python/05S_investigacao_recorte_fallback_cnes.md`
- `docs/migracao_python/05_extracao_minima_temporaria_cnes_2025.md`
- `docs/migracao_python/05_revisao_pos_etapa5.md`

Scripts Python removidos/supersedidos:
- `python/observatorio_sus/extract/descobrir_arquivos_cnes.py`
- `python/observatorio_sus/extract/investigar_fallback_cnes.py`
- `python/observatorio_sus/extract/extrair_cnes_temporario_2025.py`

Testes Python removidos/supersedidos:
- `tests/python/test_descobrir_arquivos_cnes_cli.py`
- `tests/python/test_investigar_fallback_cnes_cli.py`
- `tests/python/test_extrair_cnes_temporario_2025_cli.py`

O histórico Git permanece preservado; a árvore atual passa a refletir o novo caminho de reinício da Etapa 5N.

## 5. O que permanece válido
- Etapas 0–4 permanecem válidas.
- Contratos CNES permanecem como contratos-alvo/metodológicos.
- R permanece como oráculo.
- `co_unidade` continua chave operacional.
- `cnes`/`CO_CNES` continua código público.
- Preservação textual de códigos continua obrigatória.
- `data_interim` continua produto gerável, não fonte primária.

## 6. Reconhecimento da API PySUS
- Versão Python observada no ambiente de execução: 3.12.3.
- Versão PySUS observada no ambiente virtual: 2.0.4.
- `from pysus import cnes`: validado por modo `inspecao_api` do script.
- Assinatura da função: capturada via `inspect.signature` quando disponível.
- Parâmetros esperados/observados: `state`, `year`, `month`, `group`.
- Grupos planejados/testados nesta etapa: ST, LT, SR (teste de chamada piloto em ST).

## 7. Chamada piloto
Chamada de referência:

```python
cnes(
    state="ES",
    year=2024,
    month=1,
    group="ST",
)
```

Resultado desta etapa:
- execução sem persistência em `data_*`;
- retorno registrado em JSON (tipo, linhas, colunas, lista de colunas quando disponível);
- presença/ausência de campos semelhantes a `CO_UNIDADE` e `CO_CNES` detectada por regra de nomes;
- campos de município/UF detectados por regra de nomes;
- persistência: não.

Nesta execução, a chamada piloto retornou erro operacional controlado por bloqueio de lock do DuckDB em `/root/pysus/config.db` (sem persistência local) e código de saída 0.

## 8. Implicações para próxima etapa
- Se a chamada piloto funcionar: recomendar Etapa 5N.1 para mapear grupos ST/LT/SR e colunas retornadas.
- Se a chamada piloto falhar por rede: repetir em ambiente com conectividade.
- Se falhar por API: investigar versão PySUS/API.
- Não recomendar retorno à descoberta manual por FTP neste momento.

## 9. Critérios de aceite
- [x] Artefatos experimentais da Etapa 5 anterior removidos/supersedidos.
- [x] Documento 05N criado.
- [x] Script de reconhecimento criado.
- [x] Testes offline criados.
- [x] `from pysus import cnes` testado.
- [x] Chamada piloto ST/ES/2024-01 executada ou erro controlado registrado.
- [x] Nenhum dado salvo em `data_*`.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum `docs/cnes` alterado.
- [x] Nenhum workflow alterado.

## 10. Conclusão
O caminho funcional do PySUS foi restabelecido como base da trilha CNES/Python via `from pysus import cnes`, com reconhecimento API estruturado e chamada piloto controlada para ST/ES/2024-01. A próxima etapa deve priorizar mapeamento de colunas para ST/LT/SR, sem retorno à trilha manual de FTP neste momento. Esta etapa não realiza migração plena nem substituição de R.
