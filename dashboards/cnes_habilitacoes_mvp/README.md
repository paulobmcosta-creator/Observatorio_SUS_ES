# MVP CNES V2 — candidata de continuidade

Cópia seletiva do ZIP original V2 recebido na Ponte Operacional cloud v1.1, SHA-256 `8fa73c6a9b00efeda20cfaaffe56e96dc038326af16f3b9a8fa7eb97efc749b1`. Original intacto fora de Git em `/workspace/.cache/observatorio-cloud-v11/ponte/`. A V1 é referência histórica/lacuna arquivística; sua ausência não bloqueia desenvolvimento da V2. Não foi reconstruída.

A incorporação de código e os testes foram expressamente autorizados pelo mandato do coordenador. O ZIP não contém LICENSE autônoma nem campo `license` no package.json; esse fato é registrado em `docs/ciclo_2026_2027/implementacao/cloud_v11/MVP_PROVENIENCIA.json`. Não se infere autorização genérica de terceiros. Dependências React/Vite permanecem instaladas separadamente com suas licenças. Autoria formativa e consolidação coletiva seguem o acervo do Observatório; não se atribui autoria humana fictícia às alterações do agente.

## Preparar e executar localmente

Node 24; lock original preservado. Não atualizar dependências em massa.

```sh
npm ci --ignore-scripts --no-audit --no-fund --cache /caminho/cache/npm
python scripts/materializar_dados_locais.py /caminho/MVP_Observatorio_SUS_ES_CNES_202601_v2_HARDENED_NAO_HOMOLOGADO.zip
npm test
npm run test:baseline:canonical
npm run build
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

O materializador confere o hash do ZIP e restaura **somente** o JSON congelado autorizado em `public/data/`, ignorado pelo Git. Recusa arquivo local divergente. Não copia RAW/planilha, não altera dados para satisfazer baseline e não reprocessa CNES por ritual. `data/`, `public/data/`, `artifacts/`, `dist/` e `node_modules/` ficam fora do versionamento deste módulo. Os scripts originais de processamento permanecem como referência; `npm run verify` requer fontes locais adicionais não copiadas automaticamente. O build não equivale a publicação.

## Contratos e limites

- Mantidas 501 chaves, 238 CNES distintos, 78 códigos municipais e 91 pares código/tipo na fonte recebida. Status 304/197 é classificação interna, sem homologação normativa.
- Baseline canônica da fonte linha a linha e baseline agregada solicitada permanecem separadas em `config/`. A primeira reconcilia; a segunda continua divergente. `npm run test:baseline:requested` deve retornar reprovação enquanto não houver linhagem resolvida. A interface sinaliza a pendência.
- `resumoCanonico` completo é obrigatório antes da exibição. Regiões dos registros/municípios devem pertencer ao domínio IBGE e coincidir entre si. No contrato 2.0.0, região de saúde permanece indisponível; candidato territorial não é aplicado.
- Cartões/mapa/tabela/export usam o mesmo subconjunto; distinct é recalculado por filtro. CSV mantém campos textuais e escapa células; importar identificadores como texto no leitor de planilha.
- Zero percentual com registros não é ausência de registro. Percentual sem denominador é indefinido. O enquadramento continental é apenas visual, por intervalos dos subpolígonos M/L/Z do pipeline original; a extensão completa mantém ilhas afastadas, sem mudar geometria, filtros ou contagens.
- Não mede localização física comprovada, funcionamento, acesso, cobertura ou desempenho. Não homologado nem autorizado para divulgação institucional.

## Testes e QA

`npm test` executa os 17 casos existentes sobre os dados recebidos e seis novos casos, total 23. `npm run test:contract` executa somente seis casos sintéticos, sem dados locais; é o escopo do CI Node, acompanhado de build. Os demais 17 e o QA renderizado são evidência local específica, não cobertura presumida do CI.

QA cloud: desktop 1440×1000 e mobile 390×844; Chrome headless via Playwright 1.62.0. Foram verificados filtros, interseções, mapa por teclado, enquadramento, export/tela/tabela, vazio, navegação, ausência de dados, console e transbordamento. Relatório e hashes das capturas estão em `docs/ciclo_2026_2027/implementacao/cloud_v11/evidencias/qa_mvp_resultado.json`; imagens ficam no cache autorizado e no pacote local de recuperação. Usabilidade por usuários reais continua pendente.
