# Reprodução no checkout

Use Python 3.12 em ambiente virtual novo. A partir da raiz instale `python -m pip install -r config/estudos/requirements-reproducao-camila.txt`. A suíte institucional usa a biblioteca compartilhada em `python`. No PowerShell defina `$env:PYTHONPATH=(Resolve-Path python).Path` e `$env:PYTHONUTF8='1'`. Em POSIX use `export PYTHONPATH="$PWD/python" PYTHONUTF8=1`. Os testes que exigem Rscript identificam essa dependência no resultado. SQL é executado com a versão DuckDB fixada.

```text
python scripts/estudos/tcc_camila/reproduzir.py validar-pacote
python scripts/estudos/tcc_camila/reproduzir.py teste-sintetico
python scripts/estudos/tcc_camila/reproduzir.py reproduzir-com-agregados --saida saida-nova
```

O primeiro comando confere cobertura e bytes. O segundo executa os testes institucionais e do estudo. O terceiro produz nove SVGs e duas tabelas. Os seis CSVs de entrada já estão incluídos. O resultado longo T29 conserva ausências. Taxa bruta SIM e proporção de evasão são recalculadas por numerador/denominador e confrontadas a tolerância absoluta de 1e-10 e relativa de 1e-12. Os demais campos da projeção provêm dos agregados homologados.

A derivação a partir da entrega privada usa `gerar-resultados-publicos --academico PASTA-CONSOLIDADA --saida NOVA-PASTA`. A lista fechada de oito fontes é verificada por hash. O modo `reproduzir-fontes-oficiais` informa a indisponibilidade do percurso integral e retorna código 2. Os adaptadores v34 recebem JSON de papéis por caminho relativo ao manifesto. Use `edicao_operacional` para as projeções PA/RD e recibos, `saida` para novos derivados, `academico_anterior`, `estratos_i50`, `estabilidade_municipal`, `agregados_oferta`, `referencia_sih` e `municipios_cnes_zip` para os insumos históricos indicados. Reserve destino privado novo. Para o módulo v341 use `--trabalho` com A (matrizes e recibo), B (interseções) e C (figuras) e forneça `--integracao` para a contraprova. Configure o caminho de importação com os diretórios do checkout `scripts/integracao_estabelecimentos`, `scripts` e `python` se executar esses adaptadores isolados. O escopo experimental a partir dos agregados não certifica sua execução integral desde DBC.


A preparação das matrizes por `v341/qualificar.py manifesto.json` aceita os papéis trabalho, edicao_v34, academico_v34, integracao, historico_sigtap, estoques_regionais, quadro_denominadores, nota_referencia e mandato_referencia. Os ZIPs e recibo originais devem estar na edição v3.4. Para a projeção seletiva use `v34/projetar.py manifesto.json PA|RD|2025` com os papéis edicao_operacional, catalogo_clinico, inventario_rd, inventario_pa, raiz_rd e raiz_pa conforme a família. O código verifica o hash declarado da partição. A custódia conserva as entradas intermediárias e os recibos. O catálogo integral identifica as matrizes incluídas nesta edição.


## Pilotos v3.4.3

As instruções, manifestos e critérios de comparação estão em [Reprodução selecionada](REPRODUCAO_SELECIONADA.md). A referência à ausência de reconstrução integral permanece válida. A contraprova R/SQL foi executada nesta edição com Rscript isolado.

Na v3.5.1, a validação percorre os 318 caminhos do [catálogo integral](CATALOGO_RESULTADOS_318.csv), os 13 detalhados e suas representações adicionais. Em seguida confere o manifesto histórico dos 17 arquivos em dados e figuras. A regeneração selecionada cobre nove SVG e duas tabelas. Os [pilotos oficiais](REPRODUCAO_SELECIONADA.md) foram executados na v3.4.3. A reconstrução integral dos onze anos pertence à etapa futura do Observatório.
