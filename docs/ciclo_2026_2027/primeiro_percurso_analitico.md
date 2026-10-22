# Primeiro percurso analítico proposto — SIH/RD, residentes do ES

**Especificação para execução após REV01; não executada nesta rodada.** Integra R24/R08/R06/R09/R20 e a atualização R25 do [plano vigente](plano_operacional.md). A escolha é uma proposta fundamentada, sujeita à segunda revisão; a disponibilidade operacional real ainda precisa ser demonstrada.

## Escolha e alternativas

| Candidato | Valor e maturidade comprovada | Dependências / custo relativo | Encaminhamento |
|---|---|---|---|
| LT/ES/202401 | Testa aquisição/conversão de uma família de oferta; não demonstra por si uma pergunta sobre utilização ou fluxos | Um arquivo esperado, sujeito ao catálogo; baixa abrangência, acesso oficial ainda não demonstrado | Manter como ensaio de R32; retirar da posição de bloqueador geral |
| S01, habilitações CNES202601 | Derivados locais e contagens técnicas conferidos; relevância da distribuição da oferta | Exige localização física, relação normativa e vigência; esses elementos não estão resolvidos pelo CSV disponível | Avançar em paralelo quando elegível; não transformar gestor em localização para acelerar |
| **S03/S04, SIH/RD nacional 202401** | Pergunta direta sobre utilização hospitalar e destinos dos residentes ES; infraestrutura reaproveitável em RUE, Oncologia, ICSAP e cardiovascular | Uma família e um mês, mas cobertura de 27 UF; exige regra AIH, semântica temporal, acesso oficial e território; custo maior que LT isolado, menor abrangência que séries temáticas completas | **Recomendado para primeiro percurso da fonte à interpretação**; contrato antes da aquisição e da contagem |
| D2 completo, SIH/SIM/SIA/CNES2014–2024 | Perguntas e decisões metodológicas detalhadas no dossiê | Várias fontes, normas históricas, denominadores, padronização, séries e qualidade; custo alto | Preservar como módulo temático; não usar toda sua complexidade como porta inicial do Observatório |
| Reproduzir tabela herdada de Oncologia/RUE | Alto valor de continuidade e possível economia de trabalho | Produtos, scripts e intermediários externos não foram reinspecionados; custo não estimável sem eles | R26/R28, em paralelo quando o pacote correspondente chegar; pode alterar a ordem após revisão |

Esta comparação é qualitativa. Não mede tempo de equipe nem garante que SIH será operacionalmente acessível. Se a segunda revisão trouxer uma tabela herdada reproduzível com pergunta equivalente e menos dependências, reavaliar a ordem e registrar a razão. Não repetir um downloader existente para contornar uma biblioteca ainda não testada.

## Pergunta, recorte e interpretação

**Quantas AIH normais aprovadas são registradas para residentes do Espírito Santo na competência de processamento 202401, e que proporção das AIH com origem e destino classificáveis corresponde a atendimento fora da região de residência?**

O recorte inicial é hospitalar, todas as causas, todas as idades e destinos nacionais. Mede registros de utilização financiada pelo SUS, não pessoas distintas, necessidade assistencial, acesso efetivo da população, toda a atenção especializada ou qualidade causal dos serviços. Atender fora da região pode refletir referência pactuada e concentração de serviços; não será denominado automaticamente falha da rede.

- Fonte: SIH/SUS, família RD, arquivos oficiais das 27 UF para202401, incluindo eventuais partes/revisões declaradas no catálogo. O arquivo de prestadores ES sozinho não cobre residentes atendidos fora do estado. Não presumir ausência de arquivo como zero.
- Tempo: competência de processamento, distinguida de admissão e alta. Preservar os campos de data disponíveis e explicar a defasagem. Uma AIH processada em janeiro não representa necessariamente admissão em janeiro.
- Coorte: **propor AIH normal (`IDENT=1`)**, verificando esse significado no manual/layout da versão antes de calcular. Prorrogações/longa permanência ficam separadas e reconciliadas; não incorporadas por conveniência. Se a documentação contradisser a proposta, revisar a ficha antes da execução.
- Chave: preservar identificadores originais como texto. `N_AIH` não identifica uma pessoa e sua repetição não autoriza deduplicação genérica. Distinguir arquivo repetido, revisão da fonte, repetição legítima e duplicata lógica segundo o contrato; suspender a agregação se a causa for indeterminada.
- Território: selecionar residência ES por código oficial; usar município do atendimento identificado no layout SIH, sem importar a semântica de município gestor do CNES. Não exigir `CO_UNIDADE` para uma agregação que não depende desse vínculo.
- Perfil territorial institucional: propor uma referência oficial ES adequada a2024, com composição, código, vigência e hash documentados em R06. Não aplicar automaticamente a classificação retrospectiva do D2 ao Observatório inteiro. As quatro regiões do D2 não substituem a conferência da correspondência oficial. Para destinos externos, basta distinguir UF/município e atendimento fora do ES; não é necessário mapear todas as regiões de saúde brasileiras para S04.

## Fórmulas e saídas previstas

| Produto | Definição proposta | Controles e limites |
|---|---|---|
| S03 | Contagem de registros elegíveis de AIH normal aprovada de residentes ES, por território de residência e competência | Divulgar total ES e parcelas regionais, incluindo residência ES sem região resolvida em categoria explícita; não chamar de pacientes |
| S04 | `100 × AIH elegíveis com origem ES regionalizada e destino conhecido fora da região / AIH elegíveis com origem ES regionalizada e destino conhecido` | Informar também total elegível, excluídos por origem não regionalizada e destino ignorado, com denominadores; denominador zero gera indefinido, não zero |
| Matriz origem–destino | Contagens da mesma coorte por região ES de origem e destino: própria região, outras regiões ES, outrasUF e ignorado | Categorias mutuamente exclusivas, soma reconciliada; manter quantidade e proporção com denominador explícito |
| Ficha e interpretação | Fonte, versão, fórmula, unidade, período, cobertura, perdas, limitações e dois exemplos de leitura baseados nas tabelas reais | Exemplos só serão escritos após obter resultados; revisão de pequenos números e comunicação antes de divulgação |

S04 usa contagem direta fora da região. Não empregar `100 − proporção intrarregional` quando ignorados ou origens não classificadas entrarem de modo diferente nos denominadores. Publicar a fração de destinos ignorados junto da proporção conhecida e avaliar se ela impede interpretação. O limite de qualidade/publicação deverá ser justificado antes da análise; nenhum percentual arbitrário foi aprovado nesta revisão.

População, padrão Brasil 2010 e SIGTAP não são necessários a essas contagens/proporções. Taxas futuras exigirão população residente total, estratos equivalentes e período coerente; não anualizar um mês nem subtrair beneficiários ANS. CID/procedimentos e normas entram nos módulos que selecionarem causas, não como filtro global deste ensaio.

## Implementação aproveitada e sequência verificável

1. **R24/R06 — fechar contrato e referências.** Conferir manual SIH/RD, campos, unidade, regra de AIH/prorrogação, revisão de arquivos e correspondência municipal. Registrar regra para ausentes, perdas, duplicidades e difusão. Congelar ficha e critérios antes de ver o resultado.
2. **R08 — adquirir o recorte oficial delimitado.** Reutilizar cliente PySUS somente se cobrir RD/202401, todos os arquivos esperados e campos necessários. Registrar biblioteca/commit, origem oficial, URL/caminho, data de consulta, tamanho, hash e revisão. Alternativas: microdatasus/R ou aquisição direta oficial documentada, conforme a [matriz existente](matriz_decisao_ferramentas.csv). Espelho/DataHub só com linhagem e equivalência demonstradas; download bem-sucedido isolado não habilita uso analítico.
3. **Conversão/cache.** Preservar RAW imutável e separar a chave do cache por fonte, família, competência, UF, revisão e hash. Aproveitar a serialização Arrow verificada; ela não garante a integridade de um DBC real. Comparar conversão com leitor independente: linhas, colunas, ordem quando pertinente, códigos com zeros, identificadores, tipos, faltantes, datas e totais. Documentar divergências e interrupções, sem `ignore_errors` silencioso.
4. **Contrato e integração.** Aplicar coorte e território com cardinalidade explícita; manter contagens antes/depois por motivo de exclusão. Reconciliar recebidos, elegíveis, não elegíveis e indeterminados, sem somar perdas sobrepostas como se fossem independentes. Confirmar cobertura nacional antes de afirmar fluxos interestaduais.
5. **R09/R20 — cálculo e referência.** Produzir S03/S04 e matriz com implementação simples, compará-los a agregação independente em R/SQL sobre a mesma coorte. Contagens inteiras e classificações devem coincidir; diferenças de arredondamento de proporções devem ser explicadas. Se houver tabela oficial de referência com a mesma competência, definição, atualização e universo, comparar também; se não houver, registrar a indisponibilidade e não declarar validação externa.
6. **Interpretação e produto.** Conferir somas/denominadores, analisar perdas e exemplos reais de origem/destino, discutir limites. Tabelas versionadas e ficha são o primeiro produto; mapa depende de geometria compatível e não bloqueia a análise. Painel consome o resultado aprovado, não recalcula regras ocultas.
7. **R25 — atualização 202402.** Repetir o mesmo contrato e demonstrar comparação, reexecução e retorno à versão anterior. Mudança de fonte/layout exige versão nova. Dois meses demonstram atualização, não tendência, sazonalidade ou representatividade anual.

## Aceite e reprodução posterior

O pacote deverá conter: parâmetros declarados (`sistema=SIH`, `familia=RD`, `competencia=202401`, `UFs=27`, `residencia=ES`), ambiente/pins, manifesto RAW, contrato/layout, tabela territorial, dicionário original→tratado, balanço de perdas, comparação independente, tabelas, ficha e nota de interpretação. O comando executável será registrado quando o cliente for selecionado e validado; **não há hoje uma CLI integrada que execute esta especificação inteira**. Não inventar um comando de reprodução nem marcar R09 concluída.

São portas distintas: **aquisição** (cobertura e proveniência), **integridade da conversão** (preservação dos registros/campos) e **equivalência metodológica** (mesma coorte, território, fórmula e interpretação). Uma porta aprovada não substitui a seguinte. Critérios mínimos: nenhum arquivo obrigatório sem resolução, nenhuma perda silenciosa, nenhuma chave fabricada, balanços fechados, referência independente conciliada e limites de interpretação registrados. Pendências que afetem validade suspendem o respectivo resultado.

Este percurso reutiliza infraestrutura em todas as frentes hospitalares, mas não valida automaticamente filtros de Oncologia, RUE, ICSAP ou grupos G0–G5. O próximo ato é **REV01**, não o download ou cálculo desta especificação.
