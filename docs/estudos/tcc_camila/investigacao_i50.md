# Investigação da causa básica I50 e recuperação da série do SIM

O recorte nacional de 2022–2024 segue a data de ocorrência válida no ano da edição, o filtro não fetal e o prefixo brasileiro do município de residência. A soma das 27 UFs forma o Brasil. Registros excluídos têm motivos contados em ordem de aplicação. A população analisada em cada edição, o cabeçalho efetivo e os SHA-256 permanecem nos recibos privados.

## Medidas e denominadores

- A mortalidade cardiovascular total G0 abrange os óbitos com causa básica I00–I99. A participação de I50 em G0 usa o numerador com I50 e suas subcategorias na causa selecionada e o denominador de óbitos circulatórios no mesmo território e período.
- A menção conta uma declaração com pelo menos um código I50 no ATESTADO, considerando todas as causas básicas. O extrator aceita código com ou sem ponto e delimitadores entre códigos. Uma segunda leitura usa as linhas A, B, C, D e II. A análise de sensibilidade compara o atestado, as linhas, a união e as declarações com CID identificável.
- A matriz cruza os campos do mesmo registro. CAUSABAS é a causa selecionada, CAUSABAS_O contém a original e CB_PRE documenta a causa anterior à resseleção quando preenchido. Campos vazios e códigos inválidos têm categorias próprias. O preenchimento por UF e ano determina quais comparações admitem interpretação. Uma contagem de zero em I50_pre com CB_PRE integralmente vazio significa ausência de informação.
- O preenchimento lexical dos campos usa o número de valores não vazios entre todos os elegíveis de cada UF. ATESTADO tem também denominador de conteúdo com CID reconhecível. A data de cadastro descreve a entrada no sistema. A data de investigação descreve o campo administrativo disponível. A atribuição da alteração a uma rotina específica exige rastreabilidade adicional.
- As tabelas preservam as versões observadas, com troca de vírgula decimal por ponto na tabulação de VERSAOSCB. As grafias compactadas de 2023 permanecem em estratos próprios. A conferência de pares no ES mantém o texto original. As análises de sensibilidade distinguem cadastro no ano de ocorrência, cadastro entre 2022 e 2024 e SCB preenchido.
- Os comparadores incluem as cinco macrorregiões brasileiras, o Brasil, as demais 26 UFs em conjunto e o Sudeste sem ES. As participações agregadas usam somas de numeradores e denominadores. A classificação das UFs usa a variação em pontos percentuais entre 2022 e 2024. Esses indicadores são descritivos.
- A série mensal de sentinelas preserva categorias coronarianas, hipertensivas e outras categorias circulatórias, I64, R98, R99 e o capítulo R. O conjunto é exploratório. R98 e R99 integram o capítulo R. As categorias podem ser examinadas em paralelo às matrizes pareadas.

O item 4 do Ofício MS nº 208/2024 destina a atualização do SCB ao tratamento das bases referentes a 2025. Uma versão registrada em óbito de ano anterior é evidência de versão observada. A investigação causal depende de informações sobre a operação de codificação e as revisões da edição. [Ofício federal, pp. 3–4 do PDF](https://www.saude.df.gov.br/documents/37101/0/Nota_informativa_1_SIM.pdf/cc99be3a-fbe3-d783-9963-54ce9f53e3ee?t=1741799715860) · [Dicionário da tabela DO](https://svs.aids.gov.br/download/Dicionario_de_Dados_SIM_tabela_DO.pdf)

## Reprodução a partir da custódia

Usar Python 3.12 com pandas 2.2.3 e NumPy 1.26.4, como no estudo. Para as figuras, esta execução usou matplotlib 3.10.7 e contourpy 1.3.2. No exemplo PowerShell, definir `$custodia` como a pasta externa que contém o acervo e os três originais já validados. `$destino` é uma pasta externa para os incrementos privados. Cada lote verifica entradas e saídas por hash e escreve em staging.

```powershell
$env:PYTHONPATH = (Resolve-Path python).Path
$env:PYTHONUTF8 = '1'
$ErrorActionPreference = 'Stop'
foreach ($entrada in (Import-Csv "$custodia/logs/integridade-originais.csv")) {
    $ano = $entrada.ano
    $pasta = Join-Path $destino $ano
    New-Item -ItemType Directory -Force $pasta | Out-Null
    python scripts/investigar_i50_nacional.py $ano $entrada.arquivo "$pasta/leitura"
    if ($LASTEXITCODE) { throw "Falha na leitura de $ano" }
    python scripts/conferir_i50_nacional.py $ano $entrada.arquivo "$pasta/leitura/mensal.csv" "$pasta/conferencia-pandas-v2"
    if ($LASTEXITCODE) { throw "Divergência na conferência de $ano" }
}
python scripts/consolidar_i50_nacional.py $destino "$custodia/comparacao-2022-24-v1" "$destino/analise-v2"
if ($LASTEXITCODE) { throw "Falha na consolidação nacional" }
python scripts/reprocessar_sim_historico.py "$custodia/acervo" "$custodia/originais" "$destino/historico"
if ($LASTEXITCODE) { throw "Conferir os logs anuais da recuperação histórica" }
python scripts/consolidar_serie_sim_camila.py "$destino/historico" "$custodia/comparacao-2022-24-v1" "$destino/serie"
if ($LASTEXITCODE) { throw "Falha na consolidação da série" }
python -m unittest discover -s tests/python -p 'test_camila*.py' -v
```

O leitor CSV e a conferência pandas verificam cinco medidas por UF e mês. Os dois usam a mesma expressão de menção no atestado. A conferência dos campos de causa básica e de G0 em pandas usa regras lexicais independentes. O comparador anterior do ES permite uma terceira verificação mensal de G0 e I50. A matriz de processamento do ES reúne contagens de pares com pelo menos um dos campos original ou selecionado em I50, incluindo data de investigação e marcadores de alteração.

A extensão histórica começa pelos três anos com padronização pendente. O adquirente da branch confere espaço e edição em cada lote anual e reutiliza arquivos íntegros. A leitura dupla usa o cadastro PDR do estudo, as populações e os pesos anteriores. O produto G0 de 30–69 anos usa padronização direta em oito quinquênios com o padrão Brasil 2010 renormalizado. Os valores anteriores e respectivos desvios acompanham cada resultado. Os recibos, ZIPs, matrizes, gráficos e tabelas empíricas pertencem à custódia privada.

