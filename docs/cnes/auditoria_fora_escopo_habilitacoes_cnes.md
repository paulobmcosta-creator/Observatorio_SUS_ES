# Auditoria metodológica — habilitações "Fora do escopo inicial" (CNES 202601)

## Objetivo
Realizar auditoria tabular e metodológica dos registros de habilitações classificados como `linha_cuidado = "Fora do escopo inicial"` na base do Ciclo 3, para qualificar decisões antes do Ciclo 4, sem produzir indicadores.

## Por que foi feita antes do Ciclo 4
A categoria "Fora do escopo inicial" concentrou grande volume de registros e poderia conter misturas entre:
- exclusões metodológicas corretas do recorte inicial;
- temas potencialmente estratégicos para ciclos futuros;
- casos que merecem revisão manual da classificação analítica do Ciclo 1.

## Observação conceitual importante
"Fora do escopo inicial" **não** significa ausência de oferta assistencial ou irrelevância sanitária.
Significa apenas que, no recorte metodológico atual do projeto, essas habilitações não foram priorizadas como eixo analítico principal.

## Base e método
### Fontes usadas
- `data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv`
- `metadata/cnes/classificacao_habilitacoes_cnes.csv`
- `docs/cnes/base_habilitacoes_cnes.md`

### Procedimento
1. Filtrar registros com `linha_cuidado == "Fora do escopo inicial"`.
2. Agregar por chave de habilitação e atributos analíticos:
   - `codigo_habilitacao`, `tipo_habilitacao`, `descricao_habilitacao`, `origem_habilitacao`, `linha_cuidado`, `sublinha_cuidado`, `componente_rede`, `usar_observatorio`, `prioridade`, `status_validacao`.
3. Calcular para cada grupo:
   - `n_registros`, `n_estabelecimentos`, `n_municipios`, `exemplos_cnes` (máx. 5), `exemplos_municipios` (máx. 5).
4. Atribuir colunas de auditoria:
   - `categoria_auditoria_escopo`;
   - `recomendacao_auditoria`.

## Produto gerado
A auditoria foi salva em:
- `metadata/cnes/auditoria_fora_escopo_habilitacoes_cnes_202601.csv`

Decisão de localização: `metadata/cnes/` foi escolhido por se tratar de artefato metodológico de curadoria/classificação (não indicador final e não agregação gerencial).

## Critérios usados em `categoria_auditoria_escopo`
Classificação heurística conservadora baseada em texto de `descricao_habilitacao`:
- `Programático/incentivo`
- `Atenção básica/APS`
- `Reabilitação/deficiência`
- `Transplantes`
- `Saúde auditiva/visual`
- `Componente hospitalar genérico`
- `Potencial falso negativo`
- `Ambíguo/revisar`
- `Outro tema futuro`

## Principais achados da auditoria inicial
- Registros auditados (`Fora do escopo inicial`): **1.562**.
- Habilitações distintas auditadas (grupos): **101**.

Esses números correspondem à primeira auditoria diagnóstica, antes das correções pontuais do Ciclo 3C.
- Predomínio de itens `Programático/incentivo` (ex.: adesões, componentes programáticos, incentivos), indicando que grande parte da massa fora do escopo é coerente com exclusão metodológica inicial.
- Existe subconjunto menor classificado como `Potencial falso negativo` (ex.: laqueadura, vasectomia, CEO e alguns temas de triagem), sugerindo necessidade de revisão pontual da matriz analítica do Ciclo 1 em rodada futura.

## Recomendações
1. **Não reclassificar automaticamente** nesta etapa.
2. Priorizar revisão manual de grupos marcados como `Potencial falso negativo` e `Transplantes`.
3. Manter `Programático/incentivo` e parte de `Componente hospitalar genérico` como fora do escopo inicial, salvo mudança formal do recorte metodológico.
4. Registrar temas de `Outro tema futuro` para possível expansão temática em ciclo posterior.

## Limite de escopo desta entrega
Esta entrega é uma **auditoria metodológica diagnóstica**. Não produz indicadores, dashboards, mapas, rankings ou inferências gerenciais finais.

## Resultado final após correção da regressão do Ciclo 3C e reclassificação 1708-H
Após a identificação e correção de uma regressão no Ciclo 3C, a classificação foi restaurada ao estado pré-regressão e foram reaplicadas apenas as correções pontuais autorizadas. Também foi reclassificada a habilitação `1708-H` como Oncologia.

Estado final validado:
- Registros em `Fora do escopo inicial`: **1.462**.
- Auditoria fora do escopo: soma `n_registros = 1.462`.
- Registros em `Não classificada`: **0**.
- `usar_observatorio = Sim`: **501**.
- `usar_observatorio = Não`: **1.462**.
- A auditoria permanece conciliada com a base final de habilitações.

Distribuição final da auditoria por categoria (`n_registros`):
- Programático/incentivo: **1.162**
- Outro tema futuro: **112**
- Saúde sexual e reprodutiva / tema futuro: **80**
- Componente hospitalar genérico: **59**
- Transplantes: **19**
- Reabilitação/deficiência: **15**
- Saúde bucal especializada / tema futuro: **13**
- Saúde auditiva/visual: **2**

Conciliação da distribuição por categoria: **1.462** registros.

As habilitações `0403-H` e `0405-H` foram mantidas fora do escopo atual como tema futuro relacionado à saúde bucal especializada, não devendo ser tratadas como falso negativo das linhas priorizadas nesta etapa.

As habilitações `1901-H` e `1902-H` permaneceram fora do escopo atual como tema futuro relacionado à saúde sexual e reprodutiva.

A auditoria deve orientar revisão metodológica e priorização de temas futuros, mas não deve ser usada isoladamente como regra automática de exclusão de serviços, habilitações ou linhas de cuidado.

Esta entrega permanece como artefato metodológico de curadoria: não é indicador, não produz dashboards, não produz mapas, não produz ranking e não inicia Ciclo 4.
