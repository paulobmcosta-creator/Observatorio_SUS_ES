# Dependências e atribuições de terceiros

A proposta contém referências de instalação para Python 3.12, não incorpora as bibliotecas ou seus binários. O quadro identifica as versões efetivamente instaladas. Atribuir os respectivos projetos. Para redistribuição futura, conservar os textos legais e os avisos específicos de cada distribuição, inclusive dos componentes empacotados.

| Projeto e versão | Regime documentado | Fonte |
|---|---|---|
| colorama 0.4.6 | BSD-3-Clause | [Distribuição](https://pypi.org/project/colorama/0.4.6/) |
| contourpy 1.3.3 | BSD-3-Clause | [Distribuição](https://pypi.org/project/contourpy/1.3.3/) |
| cycler 0.12.1 | BSD-3-Clause | [Distribuição](https://pypi.org/project/cycler/0.12.1/) |
| dbfread 2.0.7 | MIT | [Distribuição](https://pypi.org/project/dbfread/2.0.7/) |
| duckdb 1.4.2 | não verificada | [Distribuição](https://pypi.org/project/duckdb/1.4.2/) |
| fonttools 4.68.0 | MIT | [Distribuição](https://pypi.org/project/fonttools/4.68.0/) |
| iniconfig 2.3.1 | MIT | [Distribuição](https://pypi.org/project/iniconfig/2.3.1/) |
| kiwisolver 1.5.1 | BSD-3-Clause e licenças incluídas | [Distribuição](https://pypi.org/project/kiwisolver/1.5.1/) |
| matplotlib 3.10.7 | Matplotlib License, baseada na PSF, e avisos incluídos | [Distribuição](https://pypi.org/project/matplotlib/3.10.7/) |
| numpy 1.26.4 | BSD-3-Clause e licenças de componentes empacotados | [Distribuição](https://pypi.org/project/numpy/1.26.4/) |
| packaging 26.3 | Apache-2.0 OR BSD-2-Clause | [Distribuição](https://pypi.org/project/packaging/26.3/) |
| pandas 2.2.3 | BSD-3-Clause e avisos incluídos | [Distribuição](https://pypi.org/project/pandas/2.2.3/) |
| pillow 12.3.0 | MIT-CMU | [Distribuição](https://pypi.org/project/pillow/12.3.0/) |
| pluggy 1.7.0 | MIT | [Distribuição](https://pypi.org/project/pluggy/1.7.0/) |
| pyarrow 19.0.1 | Apache-2.0 e avisos incluídos | [Distribuição](https://pypi.org/project/pyarrow/19.0.1/) |
| Pygments 2.21.0 | BSD-2-Clause | [Distribuição](https://pypi.org/project/Pygments/2.21.0/) |
| pyparsing 3.3.3 | MIT | [Distribuição](https://pypi.org/project/pyparsing/3.3.3/) |
| pyreaddbc 2.0.4 | AGPL-3.0 conforme metadados e licença distribuída | [Distribuição](https://pypi.org/project/pyreaddbc/2.0.4/) |
| pytest 8.4.2 | MIT | [Distribuição](https://pypi.org/project/pytest/8.4.2/) |
| python-dateutil 4.0.0 | BSD-3-Clause; componentes históricos conforme LICENSE | [Distribuição](https://pypi.org/project/python-dateutil/4.0.0/) |
| pytz 2026.6 | MIT | [Distribuição](https://pypi.org/project/pytz/2026.6/) |
| tzdata 2026.6 | Apache-2.0 | [Distribuição](https://pypi.org/project/tzdata/2026.6/) |

O descompressor pyreaddbc 2.0.4 declara AGPL-3.0. O piloto o invoca como dependência instalada, em subprocesso local, sem distribuir o binário ou iniciar serviço de rede. Uma futura distribuição combinada ou serviço precisa de exame próprio. O interpretador Python está sujeito à licença PSF e aos avisos inclusos. R 4.6.2 foi utilizado isoladamente para a contraprova SQL e seus termos constam na [documentação do R](https://www.r-project.org/Licenses/). O desenho utiliza Matplotlib e fontes locais. A proposta não inclui arquivos de fonte.
