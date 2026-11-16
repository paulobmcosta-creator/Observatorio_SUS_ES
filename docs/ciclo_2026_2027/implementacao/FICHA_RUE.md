# Ponte RUE — uma dimensão histórica reproduzida

Tarefas R28/REV-A01; O1/O2/O4. Referências E025/E040 do Work CP09.

Autoria histórica: percurso formativo de Lorenzo e consolidação técnica coletiva do Observatório, conforme acervo Work 16. A contraprova atual foi implementada em R pelo agente, sem copiar ou executar o script externo como ordem. Competência cadastral 202601; tabela de referência obtida em bytes pelo conector Drive, SHA-256 `d21b2757f724fa6d6fa2a0b077587af7e3cbe21e1767c90842cfac62df4aa0d5`, id `12piXG4BcmVXqkdCeMW79ZlNbex2Z3wM2`. Script histórico id `1Dq27H--7OpIChXaKVlfsLp8_ejr1Wkuf`, SHA-256 `af8ea228a5a65873f18bde1fd79e26dad334557141f539501f08d2934c786575`. Originais externos permanecem fora de Git: termos de redistribuição não inferidos.

Regra: contar valores distintos do campo histórico `cnes`, por `cod_municipio`, com `atende_sus = Sim` e token literal `URGENCIA` separado por `|`, removendo espaços nas bordas. O universo municipal vem da tabela de referência e precisa coincidir com o intermediário; ausência de registro elegível nesse universo observado resulta em zero cadastral.

Atenção: o campo `cnes` do intermediário histórico contém chaves longas herdadas. A contraprova preserva sua identidade literal; não o converte em código público de sete dígitos nem o associa ao novo contrato `co_unidade` sem correspondência. O código municipal é o papel legado do preparador (município gestor prioritário), não localização física comprovada. Não regionalizar este produto automaticamente.

Resultado atual: **78/78 células iguais, zero divergências**, em uma dimensão, com insumos reais históricos. Ambiente R 4.5.0. Resultado, tempo observado e hashes em `evidencias/rue_resultado_real.csv` e `rue_insumos.csv`. As quatro outras dimensões conservam status histórico, sem nova validação.

Comando executado na raiz (ajustar caminho de referência ao recuperar o arquivo original):

```sh
/workspace/.setup-observatorio/bin/Rscript scripts/reproduzir_ponte_rue.R data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv /workspace/attachments/9cb22744-e1db-41e3-a908-95ce32bfcf56/dados_municipais_rue_cnes_202601.csv .cache/implementacao/ponte_rue_20261116
```

Para repetir, escolher destino novo. A tabela municipal comparada está no cache ignorado; somente a prova de igualdade e hashes entram no Git. Não há autorização de divulgação da tabela ou inferência de cobertura SAMU, funcionamento, espera, suficiência ou vazio assistencial. Não houve aquisição CNES nova.
