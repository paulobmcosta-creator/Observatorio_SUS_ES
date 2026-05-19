# Setup local para execução do pipeline CNES em R

## Objetivo

Descrever o preparo mínimo de ambiente para validar o pipeline piloto CNES fora do sandbox atual, incluindo instalação/verificação do runtime R, disponibilidade do `Rscript`, instalação de dependências e execução de testes.

## Pré-requisitos

- R (recomendado: versão 4.3 ou superior, mesma versão configurada no GitHub Actions)
- `Rscript` disponível no PATH
- Git

O `Rscript` é instalado junto com o R e permite executar scripts `.R` diretamente no terminal, sem abrir uma sessão interativa do R ou o RStudio.

### Instalação do R/Rscript

Em ambientes Ubuntu/Debian, uma instalação local típica pode ser feita com:

```bash
sudo apt-get update
sudo apt-get install r-base
```

Em macOS com Homebrew:

```bash
brew install r
```

Em Windows, instale o R pelo CRAN e garanta que o diretório `bin` da instalação esteja no `PATH` para que `Rscript.exe` possa ser chamado pelo terminal.

### Verificação rápida

Antes de executar qualquer teste, confirme que `R` e `Rscript` estão disponíveis:

```bash
which R
which Rscript
R --version
Rscript --version
Rscript -e 'sessionInfo()'
```

Se `Rscript: command not found` aparecer, o runtime R não está instalado ou o executável não está no `PATH`. Nesse caso, corrija a instalação local antes de rodar os testes.


## Sequência padrão de validação local (passo a passo)

Execute a sequência abaixo, sempre na raiz do repositório:

1. Verificar runtime R e `Rscript` no ambiente.
2. Instalar/preparar dependências do projeto.
3. Executar a bateria de testes unitários e de integração CNES.
4. (Opcional) Executar manualmente o pipeline piloto com arquivos válidos em `data_raw/cnes/`.

Essa ordem reduz falsos negativos e melhora rastreabilidade da validação.

## Instalação/preparo de dependências

A partir da raiz do repositório, execute:

```bash
Rscript scripts/instalar_dependencias_r.R
```

## Testes locais do módulo CNES

Execute os testes abaixo, também a partir da raiz do repositório:

```bash
Rscript tests/test_estrutura_repositorio.R
Rscript tests/test_metadata_cnes.R
Rscript tests/test_ler_arquivos_cnes.R
Rscript tests/test_padronizar_cnes_interim.R
Rscript tests/test_validar_pipeline_cnes.R
Rscript tests/test_executar_pipeline_piloto_cnes.R
Rscript tests/teste_pipeline_piloto_cnes.R
```

Os testes unitários usam diretórios temporários para evitar gravação de saídas reais em `data_interim/` ou `data_processed/`. O arquivo `tests/teste_pipeline_piloto_cnes.R` permanece como teste de integração do pipeline completo.

## Execução manual do pipeline piloto

Com arquivos CSV válidos disponíveis em `data_raw/cnes/`, o pipeline pode ser executado com:

```bash
Rscript src/transform/executar_pipeline_piloto_cnes.R
```

Essa execução manual usa os caminhos padrão documentados no contrato de dados do piloto CNES.


## Troubleshooting rápido

- **`Rscript: command not found`**: instalar R e garantir `Rscript` no `PATH`; reabrir o terminal e repetir a verificação rápida.
- **Falha ao instalar pacotes**: revisar conectividade de rede/permissões e repetir `Rscript scripts/instalar_dependencias_r.R`.
- **Falha em testes por caminho**: confirmar execução a partir da raiz do repositório e existência dos diretórios esperados.


## Execução em GitHub Actions

O workflow `.github/workflows/validar_pipeline_cnes_r.yml` configura explicitamente o R com `r-lib/actions/setup-r@v2` antes de qualquer chamada a `Rscript`. Em seguida, há um step de verificação com `which R`, `which Rscript`, `R --version`, `Rscript --version` e `sessionInfo()` para diagnosticar problemas de ambiente antes da preparação de dependências e da execução dos testes.

## Limitação de ambientes sem R

Alguns sandboxes de desenvolvimento, incluindo ambientes efêmeros de agentes, podem não permitir ou não trazer a instalação local de R/Rscript. Nesses casos, a ausência de `Rscript` é uma limitação do ambiente local de execução, não uma substituição do runtime do projeto. A validação completa deve ocorrer em um ambiente com R instalado ou no GitHub Actions configurado para provisionar R automaticamente.
