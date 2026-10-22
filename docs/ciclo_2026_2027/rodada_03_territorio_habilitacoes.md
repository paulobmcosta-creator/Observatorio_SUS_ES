# Rodada 3 — território e revisão documental das habilitações

22/10/2026. Continuidade de R06/R07, autorizada após a rodada 2. **A preparação técnica e a triagem documental foram executadas; R06/R07 não estão concluídas metodologicamente.** As fontes externas necessárias foram bloqueadas pelo proxy. Não foi criada uma regionalização presumida, nem alterada a classificação clínica/normativa.

## Território: o que está demonstrado

O preparador seleciona `CO_MUNICIPIO_GESTOR` e o preserva como `cod_municipio`. O dicionário local `metadata/cnes/dicionario_cnes_piloto.csv` identifica o campo como município gestor. O snapshot comparado contém **78 códigos distintos, todos com seis dígitos**, e **12.548 estabelecimentos**. A identificação local do campo e a sua linhagem são verificáveis; a definição oficial do layout ainda deve ser confrontada com manual primário.

Isso não demonstra município físico de atendimento, residência do usuário, área de cobertura de unidade móvel ou região de saúde. A presença de outros campos como `CO_REGIAO_SAUDE` no layout bruto tampouco dispensa consultar seu dicionário, sua completude e a vigência territorial. Não foi usado esse campo como atalho.

O [inventário territorial](../../metadata/ciclo_2026_2027/execucoes/rodada_03_20261022/inventario_territorial.csv) conserva os códigos e nomes observados e reconcilia suas contagens com os 12.548 estabelecimentos. Os **78 códigos continuam sem correspondência oficial nesta execução**; isso é uma lacuna da evidência disponível, não a afirmação de que os municípios não pertencem a regiões.

### Contrato pronto para receber a fonte oficial

`src/validation/validar_correspondencia_territorial.R` exige uma tabela explícita com códigos textuais CNES/IBGE, identidade da região, intervalo de vigência, URL, ato e hash. Rejeita sobreposição de intervalos, ambiguidade municipal, nomes regionais conflitantes e proveniência mínima incompleta. Não trunca códigos, não completa dígitos e não preenche regiões ausentes. Retorna `regiao_do_municipio_gestor`, preservando o papel do campo.

O arquivo `metadata/territorio/correspondencia_municipio_regiao_pendente.csv` contém **apenas o cabeçalho**. Ele não é uma base oficial. O teste real com esse arquivo usa 31/01/2026 somente como data explícita de cenário negativo: não houve associação nem decisão de adotar o último dia do mês como regra temporal analítica. A regra temporal definitiva permanece pendente de deliberação e da vigência do ato.

O contrato verifica estrutura e coerência, não a autenticidade da fonte nem sua validade legal. Hash/URL preenchidos não substituem leitura documental. Para preencher a tabela, exigir: ato primário da SESA/CIB e anexos; vigência comprovada para a competência; correspondência oficial dos identificadores; conferência dos 78 códigos; registro de alterações territoriais; revisão metodológica identificada. O fim do intervalo representa o último dia coberto pela evidência consultada, sem fabricar validade futura para ato aberto.

## Habilitações: resultado da triagem

A [fila completa](../../metadata/ciclo_2026_2027/execucoes/rodada_03_20261022/fila_revisao_habilitacoes.csv) tem **555 combinações código/tipo** e reconcilia **1.963 registros** do snapshot. **Todas as 555 linhas da classificação têm `fonte_normativa = Revisar`**, inclusive as 203 selecionadas. Logo, o status interno `validado` não é evidência de validação documental concluída.

| Grupo de trabalho | Combinações código/tipo | Registros observados |
|---|---:|---:|
| Selecionadas e observadas; status interno `revisar` | 59 | 197 |
| Selecionadas e observadas; status interno `validado` | 32 | 304 |
| Fora do escopo e observadas | 81 | 1.462 |
| Selecionadas não observadas no snapshot | 112 | 0 |
| Fora do escopo não observadas no snapshot | 271 | 0 |

Os zeros significam ausência de registro **na base fornecida e neste recorte**, não ausência de serviço ou necessidade sanitária. A fila mantém os itens fora do escopo para permitir revisão de exclusões; não os inclui automaticamente no núcleo.

| Linha atualmente selecionada | Combinações na classificação | Registros observados | Registros com revisão interna pendente |
|---|---:|---:|---:|
| RUE | 69 | 220 | 36 |
| UTI / cuidado crítico | 25 | 68 | 26 |
| Nefrologia | 9 | 49 | 13 |
| Oncologia | 24 | 41 | 37 |
| Cardiovascular | 18 | 33 | 30 |
| Saúde mental | 21 | 41 | 6 |
| Outras habilitações estratégicas | 37 | 49 | 49 |
| Total | 203 | 501 | 197 |

A ordenação da fila é uma **proposta de trabalho**: primeiro os selecionados observados com revisão interna pendente; depois os observados com validação apenas interna; em seguida as exclusões observadas e os não observados. Dentro dos grupos, frequência decrescente e código/tipo. Não é pontuação de importância sanitária, critério de inclusão ou aprovação clínica.

`n_estabelecimentos_observados` conta `co_unidade` distintos por combinação. A soma entre combinações é explicitamente denominada `soma_vinculos_estabelecimento_habilitacao`; **não** é número de estabelecimentos distintos de uma linha ou do estado.

### Fichas preparatórias de decisões

As [12 fichas preparatórias](fichas_preparatorias_r07.csv) registram perguntas e riscos apoiados na descrição e justificativa já existentes, sem apresentar normas não consultadas. Incluem:

- **8271/I e 8272/I:** relação da retaguarda com RUE e distinção entre novos/qualificados.
- **3202/H e 0914/S:** diagnóstico citopatológico versus modalidade hospitalar; adesão ao PRONON versus oferta assistencial instalada.
- **0801/H:** a descrição ampla de assistência cardiovascular não corresponde literalmente à justificativa local “contém cirurgia vascular”; exige revisão do fundamento, sem reclassificação automática.
- **2802/H:** distinguir UCINCO de UTI neonatal.
- **8117/I:** confirmar a categoria de DRC e a interpretação da sigla com fonte primária.
- **2407/H e 2208/H:** justificar pertinência das modalidades no grupo residual sem ampliar o núcleo automaticamente.
- **8250/I:** unidade móvel SAMU e limites de atribuir cobertura ao município gestor.
- **2601/H e 8274/I:** habilitação não equivale a leitos; avaliar sobreposição entre cuidado crítico e RUE na unidade de contagem.

As perguntas não constituem achados clínicos confirmados. Todos os pareceres documentais permanecem `pendente_consulta_primaria`; a classificação está preservada. Não foram atribuídas revisões a participantes não designados.

Também é necessário conferir o significado e o formato das competências de início/fim no manual do relacional. O snapshot contém, por exemplo, `122013` em início e `999999` em fim; não se deve interpretá-los como AAAAMM ou como término real por mera conversão numérica. A rotina atual não aplica nova regra de vigência às habilitações nesta rodada.

## Evidências, reprodução e limites

```bash
Rscript scripts/auditar_territorio_habilitacoes.R \
  rodada_02_20261022 rodada_03_nova_execucao 'Nome do executor'
```

Executar na raiz, após a comparação da rodada 2. As bases em `.cache` devem existir e corresponder aos hashes registrados nos produtos da comparação. O executor recusa destino existente, verifica competência, tipos e reconciliação e registra [insumos](../../metadata/ciclo_2026_2027/execucoes/rodada_03_20261022/insumos_sha256.csv), [produtos](../../metadata/ciclo_2026_2027/execucoes/rodada_03_20261022/produtos_sha256.csv) e [execução](../../metadata/ciclo_2026_2027/execucoes/rodada_03_20261022/execucao.csv). Não usa rede e não escreve nas bases nem na classificação. Saída 0 significa diagnóstico concluído, **não** aprovação de R06/R07.

A futura aplicação de uma correspondência preenchida exige revisão documental e outro executor com escopo explícito. Este executor recusa mapa preenchido para evitar que um diagnóstico de lacuna seja confundido com regionalização aprovada.

Os novos testes cobrem códigos com zeros, ausência de mapa, ausência de código, códigos com largura incorreta, vigências, sobreposição nos extremos, cardinalidade, identidade de região, chave composta de habilitação, contagens e proteção contra promoção automática do status interno. A fixture territorial é inteiramente sintética, com domínio `example.invalid`; nunca é usada como fonte real. O schema de cada produto está em [dicionário da rodada 3](../../metadata/ciclo_2026_2027/schema_dicionario_rodada03.csv).

## Acesso necessário e ponto de retomada

As quatro consultas abaixo falharam com `curl exit 56`, HTTP do destino `000` e `CONNECT tunnel failed, response 403`. O 403 é do túnel do proxy; não foi uma resposta dos portais. [Registro com URLs e instantes](../../metadata/ciclo_2026_2027/acessos_fontes_rodada03.csv).

| Host necessário | Finalidade |
|---|---|
| `saude.es.gov.br` | Localizar regionalização, atos CIB e anexos territoriais da SESA-ES |
| `cnes.datasus.gov.br` | Dicionários/layouts e documentação das habilitações |
| `bvsms.saude.gov.br` | Normas ministeriais e alterações pertinentes às modalidades |
| `servicodados.ibge.gov.br` | Conferir identidade oficial dos municípios; não substitui a regionalização da saúde |

A política atual permite os destinos do preset de gerenciadores de pacotes e não inclui esses hosts. Não há ferramenta web de busca/navegação disponível nesta sessão. Não foi usada rota alternativa para contornar a política.

**Para desbloquear:** nas configurações de rede do ambiente, adicionar esses quatro hosts, preservando as entradas já existentes, e salvar/publicar a atualização conforme a interface. A skill de setup orienta: “If an existing network allowlist is unavailable, report the required domain additions for environment settings rather than replacing an unknown list.” O estado de execução foi consultado, mas o rascunho editável atual não pode ser lido pela ferramenta; por isso não substituí sua lista. Nenhuma mudança de rede foi salva ou aplicada nesta rodada. [Instrução da skill](skill://plugin_connector_1p_ed5feb9070a08191b08c81c47947bc16/setup/SKILL.md).

Após a atualização, retestar os acessos antes de afirmar disponibilidade. Localizar e preservar os documentos primários com hash e data, preencher a correspondência sob revisão, conferir a vigência e responder às fichas. Hosts de redirecionamento ou anexos poderão ser necessários se forem efetivamente encontrados; nenhum endereço de ato específico foi inventado.

**Ponto de retomada:** continuar a consulta documental de R06/R07 a partir desta fila e deste inventário; não refazer as rodadas anteriores. S01/S02 continuam em revisão metodológica. R08/R09 e agregação regional não foram antecipados sem esses pré-requisitos. Relatório 2025–2026, PDF, snapshots e classificação histórica permanecem preservados.

## Verificação final local

Os **13 scripts do workflow R** passaram localmente em R 4.5.0, incluindo os dois novos testes. [Log completo](../../metadata/ciclo_2026_2027/testes_rodada03_2026-10-22.txt). O CI remoto em R 4.3 não foi executado. A execução real da triagem terminou com código 0 e reconciliação integral; a ausência de correspondência e de normas está explicitada como pendência, não omitida como teste aprovado.

O [manifesto de preservação](../../metadata/ciclo_2026_2027/preservacao_rodada03_sha256.csv) compara todos os arquivos existentes no início desta rodada. As únicas alterações a arquivos anteriores foram o índice de continuidade e o workflow, para registrar o novo trabalho e incluir os testes. Os demais produtos desta rodada são arquivos novos. Não houve mudança no schema clínico, nos scripts preparadores, nas bases, no PDF ou nas evidências das rodadas anteriores. Não houve merge, publicação ou mensagens a terceiros.
