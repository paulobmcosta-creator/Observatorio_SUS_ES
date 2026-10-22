# Evidências da revisão integral de 22/10/2026

Base: `937056af0af34b81d27ec38b608f5356488b46a7`. Os artefatos desta pasta são evidências da revisão, não resultados sanitários. Datas técnicas são UTC; comunicação do projeto usa America/Sao_Paulo.

- `diagnosticos_delimitados.R`, `diagnosticos.csv` e `diagnosticos_log.txt`: três casos sintéticos, com dúvida/material/critério prévio/observação/decisão/limite. Saída zero do script significa comportamento reproduzido, inclusive limitações; não correção dos defeitos. Não modifica código, fixtures ou dados reais.
- `header_raw_cnes.json`: somente cabeçalho da fonte recuperada; SHA esperado vem da identificação anterior. Sem nova exposição de linhas cadastrais.
- `ci_remoto.json`: URL, instante, hash da página e extratos da listagem pública; sucesso no SHA explícito, sem log integral nem extrapolação.
- `acessos.json` e `pins_e_refs.json`: condição de acesso e refs observadas; não atribuem erro da rede às bibliotecas.
- `fontes_revisao.csv`: fontes locais centrais com versão, hash, papel e limite. Fontes externas inacessíveis e originais de bibliotecas são identificados no parecer e nas matrizes anteriores, sem fingir nova leitura de fontes bloqueadas.
- `preservacao_sha256.csv`: todos os arquivos rastreados no início, seus hashes antes/depois e estado. Atualizações documentais autorizadas são explícitas. Não certifica a integridade remota de documento inacessível.
- `registro_execucao.json` e `verificacao_final.json`: trabalho efetivo, verificações estruturais e limites. Não confundem testes anteriores com novos.
- `artefatos_sha256.csv`: hashes dos arquivos modificados/adicionados na revisão, exceto o próprio manifesto. Git identifica o conjunto final imutável.

Reprodução dos diagnósticos a partir da raiz, com R disponível e caminho de saída ainda inexistente:

```bash
Rscript metadata/ciclo_2026_2027/revisao_integral_20261022/diagnosticos_delimitados.R /tmp/diagnosticos_revisao_nova.csv
```

A referência é o comportamento no código do commit desta entrega. Depois de R22/R23, esses diagnósticos históricos podem deixar de reproduzir o defeito; não usar o script para impor a permanência do comportamento antigo. Os controles de regressão da correção deverão ser apropriados à regra aprovada.
