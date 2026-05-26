# Etapa 5N.4 — mapeamento estrutural exploratório dos grupos CNES ST, LT e SR via PySUS

## 1. Objetivo
Mapear estruturalmente os grupos CNES ST, LT e SR para competência piloto (ES, 2024-01), registrando apenas metadados estruturais (colunas, dtypes, campos-chave, relação nominal com contratos e riscos de coerção), sem persistência de dados e sem substituição de scripts R.

## 2. Contexto herdado
- 5N: reconhecimento da API funcional `from pysus import cnes`.
- 5N.1: isolamento de ambiente para evitar lock de DuckDB.
- 5N.2: retry/backoff/jitter para instabilidade transitória.
- 5N.3: inventário de grupos candidatos.
- 5N.3R: reteste de ST com sucesso.

## 3. Histórico da primeira falha (`pysus.api.utils`)
A primeira tentativa da 5N.4 registrou falha controlada para ST/LT/SR com `ModuleNotFoundError: No module named 'pysus.api.utils'`.

## 4. Correção pelo caminho público do PySUS
A implementação foi alinhada ao caminho funcional público já validado:
- `from pysus import cnes`
- `cnes(state=uf, year=ano, month=mes, group=grupo)`

Além disso:
- import operacional do PySUS ocorre após isolamento (`HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`);
- modo planejamento não importa PySUS;
- nenhuma persistência de DataFrame é realizada.

## 5. Ambiente usado
- Branch: `work`
- Python: 3.12.3
- PySUS: 2.0.4
- Parâmetros: UF=ES, ano=2024, mês=1, grupos=ST/LT/SR, tentativas=5, backoff=2, jitter=1.

## 6. Resultado geral por grupo

| Grupo | Descrição | DataFrame? | Linhas | Colunas | Tentativas | Causa/erro | Observação |
|---|---|---:|---:|---:|---:|---|---|
| ST | estabelecimentos | Sim | 8867 | 208 | 1 | GRUPO_ACEITO_COM_RETORNO | execução bem-sucedida |
| LT | leitos | Sim | 1014 | 28 | 1 | GRUPO_ACEITO_COM_RETORNO | execução bem-sucedida |
| SR | serviços/classificação | Sim | 20699 | 32 | 1 | GRUPO_ACEITO_COM_RETORNO | execução bem-sucedida |

## 7. Colunas e dtypes por grupo

### 7.1 ST — estabelecimentos
- Colunas (amostra inicial): `CNES`, `CODUFMUN`, `COD_CEP`, `CPF_CNPJ`, `PF_PJ`, `NIV_DEP`, `CNPJ_MAN`, `COD_IR`, `REGSAUDE`, `MICR_REG`, `DISTRSAN`, `DISTRADM`, ... (208 colunas).
- Dtypes: predominância `object` (estrutura observada integralmente sem coerção aplicada nesta etapa).

### 7.2 LT — leitos
- Colunas: `CNES`, `CODUFMUN`, `REGSAUDE`, `MICR_REG`, `DISTRSAN`, `DISTRADM`, `TPGESTAO`, `PF_PJ`, `CPF_CNPJ`, `NIV_DEP`, `CNPJ_MAN`, `ESFERA_A`, `ATIVIDAD`, `RETENCAO`, `NATUREZA`, `CLIENTEL`, `TP_UNID`, `TURNO_AT`, `NIV_HIER`, `TERCEIRO`, `TP_LEITO`, `CODLEITO`, `QT_EXIST`, `QT_CONTR`, `QT_SUS`, `QT_NSUS`, `COMPETEN`, `NAT_JUR`.
- Dtypes: `object` nas colunas retornadas.

### 7.3 SR — serviços/classificação
- Colunas: `CNES`, `CODUFMUN`, `SERV_ESP`, `CLASS_SR`, `SRVUNICO`, `REGSAUDE`, `MICR_REG`, `DISTRSAN`, `DISTRADM`, `TPGESTAO`, `PF_PJ`, `CPF_CNPJ`, `NIV_DEP`, `ESFERA_A`, `ATIVIDAD`, `RETENCAO`, `NATUREZA`, `CLIENTEL`, `TP_UNID`, `TURNO_AT`, `NIV_HIER`, `TERCEIRO`, `CNPJ_MAN`, `CARACTER`, `AMB_NSUS`, `AMB_SUS`, `HOSP_NSUS`, `HOSP_SUS`, `COMPETEN`, `CONTSRVU`, `CNESTERC`, `NAT_JUR`.
- Dtypes: `object` nas colunas retornadas.

## 8. Campos-chave detectados por grupo

| Grupo | Campos-chave detectados |
|---|---|
| ST | CNES, CODUFMUN, CPF_CNPJ, CNPJ_MAN, COMPETEN, TPGESTAO, NAT_JUR, UF |
| LT | CNES, CODUFMUN, CPF_CNPJ, CNPJ_MAN, COMPETEN, TPGESTAO, NAT_JUR, UF, leito |
| SR | CNES, CODUFMUN, CPF_CNPJ, CNPJ_MAN, COMPETEN, TPGESTAO, NAT_JUR, UF |

## 9. Relação nominal com contratos CNES

| Grupo | Relação com contratos | Cobertura potencial | Campos literais (exemplos) | Campos aproximados | Ausências críticas |
|---|---|---|---|---|---|
| ST | correspondência aproximada | COBERTURA_POTENCIAL_PARCIAL | CO_CNES, TP_GESTAO (quando equivalentes nominais) | cnes/unidade/municipio | persistem ausências frente ao contrato completo |
| LT | correspondência aproximada | COBERTURA_POTENCIAL_PARCIAL | CO_CNES (nominal) | leito/cnes/municipio | cobertura não confirmada para tabelas completas |
| SR | correspondência aproximada | COBERTURA_POTENCIAL_PARCIAL | CO_CNES (nominal) | serviço/classificação/cnes | cobertura contratual plena não confirmada |

## 10. Carregamento dos contratos CNES
- **contratos carregados?** Sim.
- **quantidade de campos críticos carregados:** 33.
- **origem:** `python/observatorio_sus/cnes/contratos.py`.
- **erro de importação:** nenhum (`null`).

## 11. Riscos de coerção de códigos por grupo

| Grupo | Campos com risco (texto obrigatório) | Observação |
|---|---|---|
| ST | CNES, CODUFMUN, CPF_CNPJ, CNPJ_MAN, COMPETEN, TPGESTAO, NAT_JUR, campos com prefixo COD/CO_/CPF/CNPJ | Registrar risco, sem coerção nesta etapa |
| LT | CNES, CODUFMUN, CPF_CNPJ, CNPJ_MAN, COMPETEN, TPGESTAO, NAT_JUR, CODLEITO, prefixos COD/CO_/CPF/CNPJ | Registrar risco, sem coerção nesta etapa |
| SR | CNES, CODUFMUN, CPF_CNPJ, CNPJ_MAN, COMPETEN, TPGESTAO, NAT_JUR, CNESTERC, prefixos COD/CO_/CPF/CNPJ | Registrar risco, sem coerção nesta etapa |

## 12. Lacunas estruturais frente aos contratos
- Relação com contratos permanece nominal/preliminar.
- Nem todos os campos críticos aparecem literalmente em todos os grupos.
- Necessário dicionário explícito PySUS → contratos CNES para consolidar equivalências semânticas.
- Não há validação de paridade com o pipeline R nesta etapa.

## 13. Testes Python executados
- `python -m pytest tests/python` → 33 passed.
- Sem testes de rede no pytest.
- Sem escrita em `data_raw`, `data_interim`, `data_processed` no modo planejamento.

## 14. Perguntas obrigatórias

| Pergunta | Resposta |
|---|---|
| ST foi mapeado? | Sim. |
| LT foi mapeado? | Sim. |
| SR foi mapeado? | Sim. |
| CNES apareceu? | Sim, nos três grupos. |
| CODUFMUN apareceu? | Sim, nos três grupos. |
| COMPETEN apareceu? | Sim, nos três grupos. |
| CO_UNIDADE apareceu? | Não literal nos grupos observados. |
| Contratos foram carregados? | Sim. |
| Houve risco de coerção? | Sim, registrado por grupo. |
| Algum dado foi salvo? | Não. |
| Algum script R pode ser substituído agora? | **Não. Nenhum script R pode ser substituído nesta etapa.** |

## 15. Classificação final
**MAPEAMENTO_ESTRUTURAL_CONCLUIDO_COM_RESSALVAS**.

## 16. Implicações para próxima etapa
A etapa habilita preparação técnica da 5N.5 (multi-competência piloto sem persistência), mantendo pré-condições: sem geração de base histórica, sem substituição de R e com formalização futura do dicionário PySUS→contratos.

## 17. Riscos remanescentes
- Instabilidade de rede eventual (timeout/retry).
- Variação de colunas entre competências.
- Coerção indevida de códigos caso tipagem textual não seja preservada.
- Diferenças semânticas entre nomes PySUS e contratos CNES.

## 18. Critérios de aceite
- [x] Documento 5N.4 robustecido com colunas/dtypes/campos-chave/riscos.
- [x] Matriz nominal de contratos registrada.
- [x] Seção explícita de carregamento dos contratos (status, quantidade, origem, erro).
- [x] Script mantém API pública `from pysus import cnes`.
- [x] Testes offline atualizados e aprovados.
- [x] Sem persistência de dados em `data_*`.
- [x] Sem alteração de scripts R, metadados, docs/cnes e workflows.

## 19. Conclusão
A revisão corretiva pós-5N.4 tornou a etapa documentalmente autossuficiente e tecnicamente mais confiável para análise de contratos: ST/LT/SR foram mapeados com DataFrame, contratos CNES foram carregados com 33 campos críticos, riscos de coerção e lacunas foram registrados e a classificação permanece **MAPEAMENTO_ESTRUTURAL_CONCLUIDO_COM_RESSALVAS**.
