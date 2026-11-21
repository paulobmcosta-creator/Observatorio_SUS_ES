# Identificação das entradas do catálogo

A coluna id preserva a identidade analítica usada nas tabelas e nas figuras. Use chave_historica para identificar uma entrada do dicionário. Para PA e as cinco classes SR, a chave reúne ID, competência e SHA-256 da edição SIGTAP. A consulta retorna o título da competência, a edição e, quando aplicável, a versão dos atributos. Meses sem vigência do procedimento são preservados no histórico completo procedimentos.csv.gz.

Para as definições de recursos originais do CNES, a chave identifica a regra v3.2 e sha256_edicao remete ao dicionário de recursos que a fixou. Essas definições não afirmam vigência ininterrupta de códigos. Consulte a evidência mensal em B06 e o número de meses em T05. As colunas id e chave_historica permitem relacionar as séries existentes e as novas definições sem somar versões históricas.
