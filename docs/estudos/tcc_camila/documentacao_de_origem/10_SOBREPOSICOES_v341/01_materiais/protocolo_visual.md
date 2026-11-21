# Protocolo para representar interseções de estabelecimentos

## Construção da população e dos conjuntos

Defina a população de referência, a linha de cuidado, a unidade de observação e a pergunta que exige estabelecimento distinto. Em cada fonte, valide a chave, o período, o domínio clínico e as quantidades. Agregue previamente as várias linhas de serviço, vínculo, equipamento ou procedimento em uma variável de presença por CNES e competência. Produtos cartesianos entre fatos assistenciais podem multiplicar contagens. Preserve município, região, competência original, situação territorial e motivo de exclusão. O denominador de cada proporção deve aparecer na tabela.

A aplicação do ES usa a janela congelada de movimento do PA que gerou a matriz integrada v3.4. Os 12 movimentos adicionais da sensibilidade anterior permanecem na edição v3.4. A série complementar mantém a comparabilidade com a nota independente. A população base contém todas as chaves validadas das fontes. Na presente matriz todas têm ST na respectiva competência. O registro mensal é booleano. Ausência de presença positiva e domínio histórico indisponível são distinguidos pela matriz de vigência. As tabelas contam padrões observados mesmo quando um critério ainda não existia; interprete interseções envolvendo o critério apenas na janela em que havia domínio.

## Três perguntas temporais

- **Pertencimento anual.** Reduzir cada coluna a “algum mês do ano” e formar o padrão binário anual. As regiões exclusivas anuais somam o universo, inclusive o padrão vazio. Calcular o estado por deduplicação de CNES, separadamente de cada região.
- **Mesma competência.** Formar o padrão no mês. Para saber se uma combinação inclusiva ocorreu em algum mês do ano, contar uma única vez cada CNES que satisfez simultaneamente os critérios naquele mês. Fundamental para PA por produção e SIH por processamento. Isso não estabelece simultaneidade de eventos clínicos.
- **Persistência e mudanças.** Comparar chaves adjacentes incluindo saídas do universo e entradas no universo. Na matriz de transição anual, FORA identifica ausência da chave no território naquele ano. O padrão 000 representa um prestador presente, externo à união temática. As tabelas de duração contam meses de presença positiva, consecutivos ou intercalados. As transições mensais exigem domínio comparável nos dois meses. Reentrada identifica retorno após pelo menos um mês sem presença, dentro da janela observada.

## Escolher a figura

| Pergunta | Representação | Verificação indispensável |
|---|---|---|
| Como duas ou três características se cruzam? | Venn com números nas regiões exclusivas e tabela das inclusivas. | Formar as quatro ou oito regiões, inclusive as de contagem zero. As áreas são esquemáticas. |
| Um conjunto está contido em outro? | Euler quando a ausência de membros externos foi comprovada. | Testar a diferença entre conjuntos sobre as chaves. Cardinalidades compatíveis sozinhas não provam inclusão. |
| Quais perfis exatos surgem de quatro ou cinco características? | UpSet temático com totais dos conjuntos, pontos ativos, barras por combinação e contagem exterior. | Conferir cada coluna no padrão exato. Mostrar todas as combinações positivas da união. Todas as combinações nulas constam da tabela. |
| Como mudou uma proporção territorial? | Mapa de calor com números/denominadores ou série com eixo explícito. | Manter territórios, janelas e critérios comparáveis. Anotar pequenos denominadores. |
| Quais unidades mudaram de perfil? | Matriz de transição com linhas de origem e colunas de destino. | Fechar margens e identificar entrada e saída do universo. |

O UpSet U01 cruza SR116, vínculo profissional pertinente, vínculo SUS e as duas produções. U02 examina o equipamento e as duas modalidades de cadastro de ECG diante do procedimento aprovado. U03 cruza habilitação, leito clínico, leito cirúrgico e AIH. U04 distingue os instrumentos em que o mesmo prestador informou procedimentos específicos. BPA-C, BPA-I, APAC principal e APAC secundária descrevem instrumento de registro; pertencimento a mais de um instrumento não identifica duplicação de procedimentos. T03 detalha mudanças entre os perfis anuais de 2023 e 2024. Outros recortes têm tabelas auditáveis por critério e ano, evitando multiplicar figuras redundantes.

## Controle e reutilização

Para k conjuntos, o universo possui até 2ᵏ padrões. As combinações exclusivas repartem as chaves sem repetição. A inclusão de um subconjunto S é a soma das regiões exclusivas cujos bits contêm todos os de S. A união é o universo menos os CNES sem qualquer bit. A interseção inclusiva vazia tem como valor o universo. Verificar as margens de cada conjunto diretamente na matriz booleana, comparar o total da união com a contagem direta de chaves e testar casos vazios, padrões raros, ausência de domínio, chaves repetidas e encontro em meses distintos. Preservar os zeros iniciais do CNES e dos padrões binários na leitura de CSV.

Os módulos `conjuntos.py` e `figuras_conjuntos.py` aceitam matrizes booleanas e rótulos fornecidos pela aplicação. O adaptador `qualificar.py` e o catálogo `temas.py` contêm as regras desta linha cardiovascular. Em outra linha de cuidado, homologar um novo catálogo e sua vigência, repetir os testes e registrar proveniência antes de gerar figuras. Para uma tabela de uma linha por unidade, a interface geral é `python conjuntos.py entrada.csv saida.csv --chave unidade --conjuntos grupo_A grupo_B grupo_C`.

Usar rótulos e números além da cor, tipografia legível, SVG vetorial e PNG de alta resolução. Conferir toda contagem exibida contra a tabela anexada e inspecionar o arquivo renderizado. Para distribuições desiguais, a área de um círculo não pode sugerir proporcionalidade sem verificação geométrica. Neste protocolo Venn e Euler são esquemáticos e explicitamente rotulados. Em UpSet, as barras são quantitativas e a associação é indicada pelos pontos. Proteger chaves detalhadas, estratos pequenos e arquivos de auditoria conforme as regras locais de acesso.
