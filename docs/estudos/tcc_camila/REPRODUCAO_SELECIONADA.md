# Reprodução selecionada desde originais

| Nível | Insumo e resultado demonstrado |
|---|---|
| I | Fixtures e testes locais em clone. A contraprova R/SQL compara a coorte sintética independentemente em R e DuckDB. |
| II | A partir dos seis CSVs de entrada, a coleção v3.4.2 gera nove figuras e duas tabelas. |
| III-Piloto SIM | ZIP nacional de 2024, óbitos não fetais de residentes do ES, causa básica final circulatória. Seis confrontos de contagem e participação incluem estado e residência municipal inclassificável. |
| III-Piloto SIH | RD do ES, processamento de dezembro de 2024. Fluxo por região de residência, atendimento e ano da admissão e indicador de atração interestadual. |
| III-Piloto CNES × SIA | ST, EQ, SR, PA e SIGTAP de dezembro de 2024, ECG 0211020036, movimento e produção do próprio mês. Tabela dos oito padrões estaduais, figura de teste e confronto com a matriz mensal homologada. |
| III-Integral | Projeto futuro do Observatório. A reconstrução de todos os anos e sistemas não foi executada. |

Os hashes e URIs do [manifesto de exemplo](../../../scripts/estudos/tcc_camila/exemplo_pilotos_2024.json) identificam as edições congeladas. Disponibilize os originais legitimamente sob as posições relativas indicadas ou use uma cópia privada do manifesto com caminhos próprios. Prepare ambiente conforme o [manual de reprodução](COMO_REPRODUZIR.md). Execute cada comando a partir do checkout em diretório de saída novo. Os leitores descomprimem em temporários e conservam os bytes da fonte.

```text
python scripts/estudos/tcc_camila/pilotos_oficiais.py SIM --manifesto manifesto.json --saida ensaio/SIM
python scripts/estudos/tcc_camila/pilotos_oficiais.py SIH --manifesto manifesto.json --saida ensaio/SIH
python scripts/estudos/tcc_camila/pilotos_oficiais.py CNES_SIA --manifesto manifesto.json --saida ensaio/CNES_SIA
python scripts/estudos/tcc_camila/confrontar_pilotos.py --pilotos ensaio --referencias referencias.json --saida confrontos
```

A última etapa recebe os quatro agregados homologados exclusivamente depois da geração das saídas. Os hashes constam no [exemplo das referências](../../../scripts/estudos/tcc_camila/exemplo_referencias_2024.json). Igualdade inteira das contagens é obrigatória; apenas proporções de ponto flutuante admitem tolerância relativa de 1e-12 e absoluta de 1e-10. O fluxo SIH separa residência de atendimento e ano da admissão de competência de processamento. O universo do piloto mensal de ECG parte dos CNES do ST. Em dezembro de 2024, todos os selecionados estavam no ST e o universo coincidiu com a matriz mensal de referência. Essa verificação não autoriza assumir igualdade em outros meses.

A contraprova R/SQL usa Rscript em PATH ou a variável OBS_RSCRIPT apontando para um runtime isolado. Rode `python -m pytest -q -rs tests/python/test_contraprova_sih_sql.py`. As saídas detalhadas dos ensaios são de auditoria privada. As contagens da candidata acadêmica anterior foram preservadas.
