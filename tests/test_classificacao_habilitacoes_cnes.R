# Testes do Ciclo 1 - classificação de habilitações CNES

arquivo <- file.path("metadata", "cnes", "classificacao_habilitacoes_cnes.csv")

if (!file.exists(arquivo)) stop("Arquivo metadata/cnes/classificacao_habilitacoes_cnes.csv não encontrado.")

ler_tentativa <- function(encoding) {
  tryCatch(
    read.csv2(arquivo, stringsAsFactors = FALSE, fileEncoding = encoding, check.names = FALSE),
    error = function(e) NULL
  )
}

classificacao <- ler_tentativa("UTF-8")
if (is.null(classificacao)) classificacao <- ler_tentativa("Latin1")
if (is.null(classificacao)) stop("Falha ao ler arquivo de classificação (encoding).")

colunas_obrigatorias <- c(
  "codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao", "origem_habilitacao",
  "linha_cuidado", "sublinha_cuidado", "componente_rede", "nivel_complexidade",
  "usar_observatorio", "prioridade", "fonte_cnes", "fonte_normativa",
  "criterio_classificacao", "status_validacao", "observacao"
)

faltantes <- setdiff(colunas_obrigatorias, names(classificacao))
if (length(faltantes) > 0) stop("Colunas obrigatórias ausentes: ", paste(faltantes, collapse = ", "))

if (any(is.na(classificacao$codigo_habilitacao) | trimws(classificacao$codigo_habilitacao) == "")) stop("codigo_habilitacao vazio encontrado.")
if (any(is.na(classificacao$tipo_habilitacao) | trimws(classificacao$tipo_habilitacao) == "")) stop("tipo_habilitacao vazio encontrado.")

chave <- paste(classificacao$codigo_habilitacao, classificacao$tipo_habilitacao, sep = "__")
if (any(duplicated(chave))) stop("Duplicidade encontrada na chave composta codigo_habilitacao + tipo_habilitacao.")

linhas_validas <- c(
  "Oncologia", "Cardiovascular", "RUE", "UTI / cuidado crítico", "Nefrologia",
  "Saúde mental", "Outras habilitações estratégicas", "Fora do escopo inicial", "Revisar"
)
if (length(setdiff(unique(classificacao$linha_cuidado), linhas_validas)) > 0) stop("linha_cuidado contém valor não permitido.")

if (length(setdiff(unique(classificacao$usar_observatorio), c("Sim", "Não"))) > 0) stop("usar_observatorio inválido.")
if (length(setdiff(unique(classificacao$prioridade), c("Alta", "Média", "Baixa"))) > 0) stop("prioridade inválida.")


status_validacao_validos <- c("revisar", "validado")
if (length(setdiff(unique(classificacao$status_validacao), status_validacao_validos)) > 0) stop("status_validacao inválido.")

sel_sim <- classificacao$usar_observatorio == "Sim"
req_sim <- c("linha_cuidado", "sublinha_cuidado", "criterio_classificacao", "status_validacao")
for (c in req_sim) {
  if (any(is.na(classificacao[sel_sim, c]) | trimws(classificacao[sel_sim, c]) == "")) {
    stop("Registros com usar_observatorio == 'Sim' possuem campos obrigatórios vazios: ", c)
  }
}

sel_alta <- classificacao$prioridade == "Alta"
if (any(is.na(classificacao$criterio_classificacao[sel_alta]) | trimws(classificacao$criterio_classificacao[sel_alta]) == "")) {
  stop("Registros com prioridade == 'Alta' devem ter criterio_classificacao preenchido.")
}

message("OK: testes de classificação de habilitações CNES passaram.")



source(file.path("src", "transform", "classificar_habilitacoes_cnes.R"))

base_teste <- classificacao[1:2, c("codigo_habilitacao", "tipo_habilitacao")]
resultado_teste <- classificar_habilitacoes_cnes(base_teste, classificacao)
campos_esperados_funcao <- c("nivel_complexidade", "criterio_classificacao", "status_validacao")
if (length(setdiff(campos_esperados_funcao, names(resultado_teste))) > 0) {
  stop("Função classificar_habilitacoes_cnes não retornou todos os campos adicionais esperados.")
}
