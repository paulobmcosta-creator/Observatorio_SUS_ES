# Fixture DBC sintética

`microdatasus_sintetico.dbc` reproduz os bytes hexadecimais de `dbc_fixture()` em
[microdatasus/tests/testthat/test-read_dbc.R](https://github.com/rfsaldanha/microdatasus/blob/7109ec2c42cf674ba453e0d7a20d2f464890b543/tests/testthat/test-read_dbc.R).
Licença MIT preservada em `LICENSE-microdatasus.txt`; copyright dos autores microdatasus.
Não contém dados de pessoas nem representa arquivo oficial do DATASUS.

Referência declarada pelos testes originais: campos CODE, VALUE, WHEN; duas linhas;
CODE `001`/`010`, VALUE `1.5`/NA, WHEN `2020-01-02`/NA. O leitor R interpreta campos
numéricos e datas antes da conversão para texto. O leitor raw do PySUS preserva
`1.500000000000000`/`*******************` e `20200102`/`00000000`.
Portanto, igualdade de campos/códigos não implica igualdade de tipos e ausentes.

Usada por `scripts/executar_poc_ferramentas.py`. O pacote microdatasus não foi
executado no ambiente; a referência é a asserção original. O oráculo R efetivamente
executado nesta rodada é o preparador CNES do Observatório, em dados reais separados.
