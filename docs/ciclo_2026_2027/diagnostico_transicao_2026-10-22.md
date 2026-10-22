# Diagnóstico delimitado de transição — 22/10/2026

## Escopo e fontes examinadas

A tarefa desta rodada é sistematizar o ponto de partida, propor critérios e executar uma conferência pequena. A proposta, pp. 8 e 12–16, orienta seis objetivos: O1 inventário; O2 matriz e validação; O3 atualização/padronização; O4 rastreabilidade; O5 painel; O6 disseminação. O projeto não fixa quantidade obrigatória de indicadores.

Foram examinados o PDF completo, seus cronogramas visualmente, o prompt, `AGENTS.md`, a governança, os guias do aluno, o inventário de manutenção, os documentos centrais CNES, schemas/dicionários, código R, fixtures, testes/CI e o encerramento 5N. O [inventário CSV](inventario_transicao.csv) agrupa produtos, insumos e documentação; não transforma cada arquivo auxiliar em uma entrega científica.

Versão do checkout: `6478f93a50d03270a78959730221f2ea5a643658`; árvore inicialmente limpa. `git ls-remote origin refs/heads/main` retornou a mesma revisão. A branch de trabalho preserva essa base. As evidências da nova conferência estão em [execuções](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/execucao.csv).

### Acesso externo e limites de comprovação

Não há conector Drive/Docs disponível nesta sessão. As consultas HTTPS somente de leitura aos dois endereços fornecidos foram recusadas pelo proxy (`CONNECT 403`, curl 56; nenhum HTTP de origem recebido). Isso não demonstra inexistência ou falta de permissão do usuário nos documentos.

- Acervo: <https://drive.google.com/drive/folders/1mi6rvQeHxuCfcMJfOJtGmWRKL358WjZD>.
- Relatório encerrado: <https://docs.google.com/document/d/1gmVyMUhK3o2CtsTEaeqVgk4lj08es5TlWbklIQGekWQ/edit>.
- Arquivo `CONTEXTO_OBSERVATORIO_SUS_ES_RELATORIO_2025_2026_21-10-2026(1).md`: não localizado entre checkout e anexos. Não foi necessário para o incremento local.

O MVP principal, a variante `v2_HARDENED_NAO_HOMOLOGADO.zip`, o script municipal RUE e os cinco relatórios individuais são **informados pelo prompt e não reinspecionados**. Não foram encontrados ZIPs, PBIXs ou rotina RUE no checkout. `dashboards/` e `maps/` só contêm placeholders. Esses limites não autorizam declarar os produtos inexistentes no Drive. A variante permanece separada e sem homologação comprovada. Não se produziu manifesto RUE nem prova retrospectiva de sua execução.

## Conferência única dos números de referência

Leitura integral dos CSVs locais como texto, sem filtros e sem reprocessar dados brutos. [Contagens reprodutíveis](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/contagens_observadas.csv):

| Objeto/unidade | Resultado observado | Interpretação permitida |
|---|---:|---|
| Linhas do snapshot de estabelecimentos | 12.548 | Linhas do produto legado; não identidade pública CNES validada |
| Códigos municipais distintos nesse snapshot | 78 | Códigos observados de seis dígitos; não validação oficial de cobertura/regionalização |
| Linhas do snapshot de habilitações | 1.963 | Registros; não pessoas ou estabelecimentos |
| Valores distintos no campo legado `cnes` das habilitações | 1.283 | Contagem do campo com esse nome; não confirmação de códigos CNES públicos |
| Combinações código/tipo na classificação | 555 | Referência de classificação, não número de registros reais |
| Combinações selecionadas na classificação | 203 | Subconjunto da referência |
| Registros de habilitação selecionados | 501 | 304 com status interno `validado` e 197 `revisar` |
| Registros fora do escopo | 1.462 | Fora do recorte, sem inferir irrelevância sanitária |
| Auditoria fora do escopo | 81 linhas; soma 1.462 | Conciliação de totais observada |

O status `validado` é uma categoria do metadado histórico. Não comprova validação por especialistas, adequação normativa atual, aprovação de gestores ou homologação dos candidatos 2026–2027. A classificação permanece intacta.

## Divergências que condicionam o novo ciclo

1. **Contrato versus snapshots:** ambos os CSVs intermediários omitem `co_unidade`, embora código e metadados atuais a definam como chave operacional. O campo `cnes` dos estabelecimentos tem comprimentos 13 (12.532 valores), 30 (1) e 31 (15); nas habilitações, os 1.283 valores distintos têm comprimentos 13 (1.280) ou 31 (3). Não é lícito renomeá-lo como chave operacional nem truncá-lo para produzir um código público. O teste não estabelece a origem desses identificadores.
2. **Completude:** três linhas de estabelecimentos têm `nome_estabelecimento` vazio. São lacunas observadas, sem correção silenciosa por fallback.
3. **Schema malformado:** a linha física 30 de `metadata/cnes/schema_habilitacoes_cnes.csv` contém oito campos para um cabeçalho de sete. A vírgula não protegida em `TO_CHAR(DT_ATUALIZACAO,'DD/MM/YYYY')` causa a divergência. A comparação completa com esse schema fica **não executada**; não se inventa um campo chamado `rlEstabSipac` a partir da sobra da linha. A estrutura original foi preservada para revisão em tarefa específica.
4. **Território:** os snapshots usam seis dígitos, enquanto exemplos de schema/fixtures usam sete. O código `preparar_estabelecimentos_cnes.R` prefere `CO_MUNICIPIO_GESTOR` quando presente. Portanto, nem formato IBGE de sete dígitos, nem localização física, nem região de saúde estão validados. Não houve conversão por preenchimento/truncamento, nem escolha de regionalização por memória.
5. **Reprodução dos brutos:** `data_raw/cnes/202601/tbEstabelecimento202601.csv` é um ponteiro Git LFS de 134 bytes, não o CSV de 284.224.999 bytes indicado nele. O objeto esperado tem SHA-256 `a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6`. Sem materializá-lo não se pode verificar o layout bruto nem reconstruir chaves. O teste inicial com a fixture antiga do ciclo 2 revelou que ela contém `CO_UNIDADE`, mas não `CO_CNES`, agora exigido pelo preparador; a fixture foi preservada.
6. **Atualização e proveniência:** os snapshots declaram processamento em 21/05/2026 e competência 202601. Isso não informa data/hora de extração, responsável original, URL específica ou situação final/preliminar. Os registros novos declaram essas lacunas, sem preencher retrospectivamente.

Última alteração do snapshot de estabelecimentos: `2bf259570eaf86d431f0b0d0ec64898b19f283d2`; do preparador atual: `eed7071d6cab93b848d88bbb30a8a217f9208936`. Essa distinção de versões ajuda a explicar o risco de assumir que saídas históricas já foram regeneradas com o código atual; não é uma atribuição causal definitiva.

## Maturidade e decisões propostas

O piloto R e seus seis indicadores básicos existem. Seus testes demonstram comportamento técnico em fixtures, não uma matriz regional validada. Os contratos usam layouts diferentes: o piloto lê `co_cnes`, `co_municipio_gestor`, `competencia_aaaamm`; os produtos dos ciclos 2/3 têm outro schema. Não se deve passar um pelo outro mediante simples renomeação.

Python/PySUS permanece experimental conforme `docs/migracao_python/README.md` e o encerramento 5N. A afirmação ampla do README geral sobre preferência por Python e pipeline completo não é prova de paridade ou maturidade. O R permanece referência; a rotina municipal RUE citada no prompt é outro produto e não é evidência da migração PySUS.

Os ciclos 1–3/3C têm código, metadados e produtos históricos. Os ciclos 4–12 do roadmap não viraram automaticamente o cronograma desta proposta. Não há evidência local de séries finais ICSAP/força de trabalho, artigos/notas gerenciais concluídos ou adoção institucional. Parceiros previstos não equivalem a revisores efetivos dos produtos.

Decisão desta rodada: **preservar os ativos, explicitar as incompatibilidades e entregar um bloqueio técnico verificável**. Resolver chaves/schema e a correspondência territorial precede o cálculo regional. A recuperação do Drive é necessária para avaliar o painel e a autoria dos produtos externos; não bloqueia as entregas locais agora concluídas.
