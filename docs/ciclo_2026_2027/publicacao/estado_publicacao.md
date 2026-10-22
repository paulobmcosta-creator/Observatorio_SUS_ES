# Publicação das entregas — 22/10/2026

O usuário autorizou criar os commits, enviar a branch e abrir um pull request. O envio Git foi concluído com a autenticação existente:

- `e75e81c`: contratos, cache, configuração, código, testes e workflows — 42 arquivos.
- `47bc932`: dossiês, planos, matrizes, avaliações e evidências — 114 arquivos.

Branch: [feat/ciclo-2026-2027-transicao](https://github.com/paulobmcosta-creator/Observatorio_SUS_ES/tree/feat/ciclo-2026-2027-transicao). O Git confirmou a criação remota e o vínculo de upstream. Esta nota e a atualização do índice/continuidade constituem um complemento documental; não mudam as regras nem os resultados.

## Pull request e bloqueio

O pull request **ainda não foi criado**. As consultas `gh pr list` e `gh api repos/paulobmcosta-creator/Observatorio_SUS_ES` receberam `403 Forbidden`. A política de rede vigente permite Git HTTPS em `github.com`, mas não inclui `api.github.com`. O diagnóstico do CLI sobre token inválido não comprova defeito da credencial enquanto a API está bloqueada. Não foi solicitada uma credencial nova nem contornada a política.

A [descrição completa](descricao_pull_request.md) está pronta. Título proposto: **feat: iniciar ciclo 2026–2027 com reconciliação metodológica e pipeline verificável**.

Após liberação legítima da API nas configurações do ambiente, conferir a identidade e a existência de um PR para esta branch antes de executar:

```bash
gh pr create --repo paulobmcosta-creator/Observatorio_SUS_ES \
  --base main --head feat/ciclo-2026-2027-transicao \
  --title 'feat: iniciar ciclo 2026–2027 com reconciliação metodológica e pipeline verificável' \
  --body-file docs/ciclo_2026_2027/publicacao/descricao_pull_request.md
```

Alternativa manual: [abrir o formulário de pull request](https://github.com/paulobmcosta-creator/Observatorio_SUS_ES/pull/new/feat/ciclo-2026-2027-transicao) com o título e texto acima. Esse link é um formulário, não um PR existente. Quando criado, registrar a URL real e anexá-la à tarefa. Conferir o CI remoto antes de qualquer merge; publicação da branch não significa incorporação à `main`.

## Preservação e verificação

Os 29 hashes do manifesto da complementação DataHub foram conferidos antes da publicação. O código e os resultados não foram alterados nesta etapa. As cópias dos anexos mantêm seus bytes, inclusive finais de linha; o exame de whitespace permitiu CRLF em CSV e excluiu as transcrições/originais preservados. Não se reescreveu documento de origem para satisfazer formatação.

Os manifestos históricos descrevem os instantes em que foram gerados. O estado anterior do índice e da continuidade, atualizado apenas para registrar o envio, está preservado no commit `47bc932`; não se alteraram os manifestos antigos para ocultar a atualização. Não houve merge, escrita no relatório 2025–2026, inclusão de caches grandes ou modificação de dados brutos/intermediários nesta publicação.
