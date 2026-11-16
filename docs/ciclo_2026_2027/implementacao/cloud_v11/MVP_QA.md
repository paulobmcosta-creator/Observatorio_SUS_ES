# MVP V2 — resultado de validação cloud

Candidata de continuidade, não homologada. Fonte original preservada: 501 chaves, 238 estabelecimentos distintos, 78 códigos municipais e 91 pares código/tipo; 304 status internos Validado e 197 Revisar. Região de saúde continua indisponível. V1 não foi reconstruída; ausência é lacuna arquivística.

23 testes Node passaram (17 originais com JSON recebido + seis novos sintéticos). Build passou. Baseline canônica aprovada; alternativa agregada reprovada deliberadamente, com pelo menos 20 divergências, sem ajustar fonte. Logs exatos em `evidencias/mvp_comandos/execucao.json`. O CI Node executa somente os seis sintéticos e build, sem JSON local.

Playwright 1.62.0/Chromium cloud; desktop 1440×1000 e mobile 390×844. Browser plugin sem ferramenta callable; fallback cloud autorizado pelo mandato v1.1. Não foi usado navegador pessoal. As 14 verificações abaixo passaram:

| Verificação | Resultado |
|---|---|
| mapa_ocupa_viewbox | APROVADO |
| identidade | APROVADO |
| nao_vazia | APROVADO |
| sem_overlay | APROVADO |
| extensao_completa_sem_mudar_dados | APROVADO |
| export_tela_tabela | APROVADO |
| zero_percentual_distinto_de_ausencia | APROVADO |
| vazio_zero_e_percentual_indefinido | APROVADO |
| navegacao_metodologia | APROVADO |
| mobile_sem_transbordamento | APROVADO |
| console_sem_erros_relevantes | APROVADO |
| dados_ausentes_estado_explicito | APROVADO |
| interacao | APROVADO |
| capturas | APROVADO |

Fluxos: todos→RUE 501→220, exportação CSV 220 linhas e distinct reconciliado com cartão; RUE+Validado 184; seleção de Vitória pelo teclado; extensão completa mantém 78 polígonos e totais; combinação vazia exibe zero e percentual indefinido. Mobile sem transbordamento. Console normal sem erros, nenhum pageerror. Dois 404 são exclusivamente a injeção deliberada de ausência de dados (React StrictMode), não falha do fluxo normal.

O enquadramento continental é escolha visual sobre os subpolígonos M/L/Z, com extensão completa disponível; não transforma geometrias nem produz inferência geográfica. Usabilidade humana e homologação continuam pendentes.

Relatório JSON: `evidencias/qa_mvp_resultado.json`. Capturas fora de Git, preservadas no novo ZIP de recuperação em `evidencias_visuais/`, com estes hashes:

| Captura | SHA-256 |
|---|---|
| desktop_inicial.png | `bafb028d35ed8e285f46a01d6c53cd799203cebbd0c4ee28abdae3cab59fc5ed` |
| desktop_rue_validado.png | `12aaac31e9d15aca5f3985e284c86541b2016a7df7890604f833f66cb4bf0bd5` |
| desktop_vazio.png | `9b3ae2b343c219e5f1648803096846edadf22a6cd356e4d4342041f1c8eab5c1` |
| mobile_oncologia.png | `82d76c0225698bbd2ecd4773c7beedc5ddb0a13b4e6a29fb921c9de6ecf116aa` |
