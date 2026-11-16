# Aceite preparado para MVP existente — R10/R33–R36

Sem recriar frontend. Conservar v1 e v2 original e modificar somente cópia versionada quando os ZIPs forem efetivamente disponibilizados. Os números relatados pelo Work são históricos; não foram observados em browser nesta execução.

| Cenário preparado | Resultado a conferir na candidata | Gate atual |
|---|---|---|
| Todas as linhas / filtro por município / combinação vazia | Cartões, tabela, mapa e export calculados do mesmo conjunto filtrado; distintos recalculados nessa escala | ZIP e build ausentes |
| Estabelecimento com vários códigos/tipos | Uma chave não vira vários estabelecimentos; contagens por registro/CNES/par explicitadas | Funções da v2 não disponíveis localmente |
| `regiao_saude` vazia | Categoria explícita; não preencher por região IBGE, município gestor ou geografia sem vigência | Fonte territorial histórica pendente |
| Baseline agregada divergente | Isolar indisponibilidade ou remover só da candidata com registro; preservar original; decisão institucional aberta | Linhagem não resolvida |
| Município sem categoria / seleção extrema | Ausência distinguida de zero observado; sem erro de mapa/export | Fixture e browser dependem do código |
| CSV exportado e tela | Mesmos filtros, registros e distintos; código municipal textual e metadata visíveis | Export tabular independe do painel |
| Retorno de versão | Configuração/dados anteriores recuperáveis; candidata incompleta não substitui atual | REV-A03 parcial |
| Leitura em tela pequena e teclado | Rótulos, contraste, foco e estados vazios legíveis; não depender só de cor | Teste visual real pendente |
| Usuário real executa tarefa | Registrar pessoa funcional, data, tarefa, resultado e dificuldades | Pessoas P1–P3 e sessão humana não designadas |

Produto deve informar título, competência, papel territorial, unidade, fonte/versão, numerador/denominador e limite da interpretação. Os seis controles técnicos CNES não são seis indicadores sanitários. S03/S04 sintéticos não entram no painel empírico. Baseline e região não podem ser corrigidas apenas para completar visualmente a tela. Não há homologação, implantação ou publicação autorizada por estes requisitos.
