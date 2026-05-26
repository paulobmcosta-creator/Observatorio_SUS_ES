# Etapa 5N.4 — mapeamento estrutural exploratório dos grupos CNES ST, LT e SR via PySUS

## 1. Objetivo
Mapear estruturalmente ST, LT e SR para competência piloto via PySUS. Esta etapa não é migração plena, não gera base, não salva dados, não substitui R, não valida paridade, não aplica transformação e não aplica classificação de habilitações.

## 2. Contexto herdado
5N reconheceu API funcional; 5N.1 tratou lock DuckDB; 5N.2 formalizou retry/backoff/jitter; 5N.3 inventariou grupos; 5N.3R retestou ST com sucesso; microcorreção de 5N.3 autorizou 5N.4 com ST/LT/SR.

## 3. Primeira tentativa da 5N.4 (histórico preservado)
A primeira tentativa da 5N.4 falhou nos três grupos com `ModuleNotFoundError: No module named 'pysus.api.utils'`.

## 4. Confronto com caminho funcional 5N.3/5N.3R
Foi comparado `mapear_estrutura_grupos_cnes_pysus.py` com `inventariar_grupos_cnes_pysus.py` e alinhado explicitamente o caminho funcional público:
- `from pysus import cnes`
- `cnes(state=uf, year=ano, month=mes, group=grupo)`

Import operacional permanece após isolamento (`HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`). Planejamento não importa PySUS.

## 5. Ambiente usado
- Branch: `work`
- HEAD de início: `c5941e19defe000cc864e63092ccfdca9c14b13e`
- Python: 3.12.3
- PySUS: 2.0.4

## 6. Resultado do inventário de controle (mesmo ambiente)
Comando de controle (`inventariar... --modo testar_grupos --grupos-candidatos ST LT SR`) retornou DataFrame para ST/LT/SR no mesmo ambiente desta correção.

## 7. Resultado da 5N.4 corrigida

| Grupo | DataFrame? | Linhas | Colunas | Tentativas | Causa/erro |
|---|---:|---:|---:|---:|---|
| ST | Sim | 8867 | 208 | 2 | GRUPO_ACEITO_COM_RETORNO |
| LT | Sim | 1014 | 28 | 1 | GRUPO_ACEITO_COM_RETORNO |
| SR | Sim | 20699 | 32 | 1 | GRUPO_ACEITO_COM_RETORNO |

Observação: ST teve `ReadTimeout` na primeira tentativa e sucesso na segunda dentro do retry configurado.

## 8. Classificação final da 5N.4
**MAPEAMENTO_ESTRUTURAL_CONCLUIDO_COM_RESSALVAS** (estrutura capturada para ST/LT/SR, com ressalvas de relação contratual ainda preliminar e sem paridade com R).

## 9. Próxima etapa recomendada
Avançar para 5N.5 (multi-competência piloto sem persistência), mantendo recomendação de dicionário PySUS→contratos e sem substituição de R.

## 10. Conformidade de escopo
Sem alterações em scripts R, testes R, `data_raw`, `data_interim`, `data_processed`, `metadata`, `docs/cnes` e workflows.
