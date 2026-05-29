# Glossário mínimo CNES — Observatório SUS-ES

| Termo | Definição pedagógica | Observação no projeto |
| ----- | -------------------- | --------------------- |
| Observatório SUS-ES | Projeto científico e educacional para organizar, analisar e documentar dados de saúde pública no Espírito Santo. | O aluno deve compreender sua governança antes de executar qualquer etapa técnica. |
| SUS | Sistema Único de Saúde brasileiro. | É o contexto institucional das bases e indicadores do projeto. |
| Atenção especializada | Conjunto de serviços de maior complexidade que complementam a atenção básica. | Uma das dimensões analíticas que pode ser estudada com CNES. |
| CNES | Cadastro Nacional de Estabelecimentos de Saúde. | Base central do foco atual do repositório. |
| ST | Grupo operacional CNES avaliado na trilha PySUS. | Permanece instável/intermitente. |
| LT | Grupo operacional CNES avaliado na trilha PySUS. | Mantido como grupo inicial de exploração controlada. |
| SR | Grupo operacional CNES avaliado na trilha PySUS. | Mantido como grupo inicial de exploração controlada. |
| R | Linguagem principal usada no pipeline metodológico atual. | Permanece oráculo metodológico. |
| PySUS | Biblioteca Python para acesso a dados do SUS. | Considerada experimental/prototípica neste repositório. |
| Oráculo metodológico | Implementação de referência usada para comparar e validar novas alternativas. | No projeto, R cumpre esse papel para CNES. |
| Contrato de dados | Especificação de campos, tipos, regras e expectativas de uma base. | Não deve ser alterado sem decisão metodológica. |
| Contrato intermediário | Contrato parcial usado entre uma fonte experimental e o modelo esperado. | O contrato PySUS→CNES existe, mas não autoriza base final. |
| Metadado | Informação que descreve uma base, campo, regra ou origem. | Garante rastreabilidade e padronização. |
| Dicionário de dados | Tabela que descreve campos, significados e formatos. | Deve ser lido antes de interpretar variáveis CNES. |
| Campo | Coluna ou atributo de uma base de dados. | Pode exigir preservação textual ou tipo específico. |
| Chave | Campo ou conjunto de campos usado para ligar registros. | Deve ser tratado com cautela para evitar joins incorretos. |
| Identificador | Valor usado para identificar unidade, registro ou entidade. | Nem todo identificador deve ser convertido para número. |
| CNES | Também pode se referir ao código de estabelecimento, dependendo do contexto. | Verificar sempre o significado no documento ou dicionário. |
| CO_UNIDADE | Campo sensível relacionado à identificação de unidade. | Permanece não resolvido na migração PySUS/CNES. |
| CODUFMUN | Código de unidade federativa e município. | Campo territorial que pode exigir preservação textual. |
| COMPETEN | Competência temporal da base, geralmente ano/mês. | Essencial para rastreabilidade temporal. |
| TPGESTAO | Tipo de gestão. | Campo categórico que deve ser interpretado com dicionário. |
| NAT_JUR | Natureza jurídica. | Campo institucional; pode ter códigos padronizados. |
| CPF_CNPJ | Identificador fiscal de pessoa física ou jurídica. | Deve ser tratado como texto quando presente. |
| CNPJ_MAN | CNPJ da mantenedora. | Não deve sofrer coerção numérica indevida. |
| CNESTERC | Campo relacionado a estabelecimento terceiro, conforme contexto CNES. | Deve ser interpretado com documentação específica. |
| data_raw | Pasta para dados brutos. | Não é área livre de escrita do aluno. |
| data_interim | Pasta para dados intermediários. | Não deve receber saídas experimentais sem autorização. |
| data_processed | Pasta para dados processados ou finais. | Não criar base final sem validação e autorização. |
| Pipeline | Sequência organizada de extração, transformação, validação e saída. | O pipeline produtivo atual não deve ser substituído pelo aluno. |
| Rastreabilidade | Capacidade de explicar origem, transformação e decisão associada a um dado. | Princípio central do repositório. |
| Coerção de tipo | Conversão de um campo de um tipo para outro, como texto para número. | Pode destruir zeros à esquerda ou identificadores. |
| Preservação textual | Manutenção de campos como texto para evitar perda de informação. | Importante em identificadores e códigos. |
| Join | Operação de ligação entre tabelas por chaves. | Requer chaves corretas e validação de multiplicidade. |
| Paridade | Comparação entre implementações para verificar equivalência. | Necessária antes de substituir R por Python. |
| Script experimental | Código criado para diagnóstico, prova de conceito ou investigação. | Não deve ser usado como rotina produtiva. |
| Base final | Produto de dados validado para análise ou entrega. | Sua geração não está autorizada nesta revisão. |
