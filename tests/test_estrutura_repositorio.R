# Teste mínimo de integridade estrutural do repositório.
# Usa apenas funções do pacote base de R para evitar dependências externas.

arquivos_obrigatorios <- c(
  "README.md",
  "AGENTS.md",
  "docs/convensoes_metodologicas.md",
  "docs/governanca_codigo.md",
  "docs/fluxo_trabalho.md",
  "config/dependencias_r.csv"
)

diretorios_obrigatorios <- c(
  "src/extract",
  "src/transform",
  "src/indicators",
  "tests",
  "metadata"
)

arquivos_ausentes <- arquivos_obrigatorios[!file.exists(arquivos_obrigatorios)]
diretorios_ausentes <- diretorios_obrigatorios[!dir.exists(diretorios_obrigatorios)]

if (length(arquivos_ausentes) > 0) {
  stop(
    "Arquivos obrigatórios ausentes: ",
    paste(arquivos_ausentes, collapse = ", "),
    call. = FALSE
  )
}

if (length(diretorios_ausentes) > 0) {
  stop(
    "Diretórios obrigatórios ausentes: ",
    paste(diretorios_ausentes, collapse = ", "),
    call. = FALSE
  )
}
