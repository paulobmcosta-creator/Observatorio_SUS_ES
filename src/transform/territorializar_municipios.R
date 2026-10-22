# Requer sha256_fonte_cnes e conferir_correspondencia_territorial, compartilhados.
#' Ler uma tabela central territorial identificada por hash e versão explícitos.
#' @param arquivo CSV da tabela central, com versão em cada linha.
#' @param versao Identificador da versão selecionada; nunca usa a mais recente por padrão.
#' @param sha256_esperado Hash congelado dos bytes do CSV, fornecido pelo estudo.
#' @return Linhas da versão, preservando todos os códigos como texto.
#' @references Dossiê 1 §7; Dossiê 2 §6; docs/ciclo_2026_2027/reconciliacao_dossies.md
ler_territorio_congelado <- function(arquivo, versao, sha256_esperado) {
  if (length(versao) != 1L || is.na(versao) || !nzchar(versao) ||
      length(sha256_esperado) != 1L || is.na(sha256_esperado) || !grepl("^[0-9a-f]{64}$", sha256_esperado)) {
    stop("Informe versão e SHA-256 congelados; fonte territorial ainda não definida.")
  }
  if (sha256_fonte_cnes(arquivo) != sha256_esperado) stop("Tabela territorial diverge do hash congelado.")
  m <- read.csv(arquivo, colClasses = "character", check.names = FALSE)
  if (!"versao_territorial" %in% names(m) || anyNA(m$versao_territorial)) stop("Tabela sem versão territorial íntegra.")
  m <- m[m$versao_territorial == versao, , drop = FALSE]
  if (!nrow(m)) stop("Versão territorial solicitada não encontrada.")
  m
}

#' Aplicar uma versão central preservando código original e papel territorial.
#' @param codigos Códigos originais textuais; seis ou sete dígitos conforme fonte.
#' @param datas_evento Datas ISO explícitas, uma por registro ou uma comum ao lote.
#' @param tabela Tabela central da versão obtida por ler_territorio_congelado.
#' @param versao Versão exata; o aplicador nunca seleciona outra automaticamente.
#' @param papel residencia, atendimento, municipio_gestor ou localizacao_oferta.
#' @param modo contemporaneo ou retrospectivo_congelado (escolha do estudo).
#' @param data_classificacao Data ISO da classificação congelada; não é a data do evento.
#' @return Uma linha por entrada, com código original, canônico, região e estados explícitos.
#' @details Não certifica a fonte, não infere papéis e não converte dígitos.
territorializar_municipios <- function(codigos, datas_evento, tabela, versao, papel, modo, data_classificacao = NULL) {
  if (!is.character(codigos) || !length(codigos)) stop("Forneça códigos originais textuais não vazios.")
  if (length(papel) != 1L || !papel %in% c("residencia", "atendimento", "municipio_gestor", "localizacao_oferta")) stop("Papel territorial deve ser explícito.")
  if (length(modo) != 1L || !modo %in% c("contemporaneo", "retrospectivo_congelado")) stop("Modo territorial inválido.")
  if (length(versao) != 1L || is.na(versao) || !nzchar(versao) || !"versao_territorial" %in% names(tabela)) stop("Versão territorial obrigatória.")
  if (anyNA(tabela$versao_territorial)) stop("Versão territorial ausente na tabela.")
  m <- tabela[tabela$versao_territorial == versao, , drop = FALSE]
  if (!nrow(m)) stop("Versão territorial não encontrada; não substituir por outra.")
  valido <- function(x) {
    if (!is.character(x) || anyNA(x)) return(FALSE)
    d <- suppressWarnings(as.Date(x, format = "%Y-%m-%d"))
    all(!is.na(d) & grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", x) & format(d, "%Y-%m-%d") == x)
  }
  if (!length(datas_evento) %in% c(1L, length(codigos)) || !valido(datas_evento)) stop("Data do evento inválida.")
  datas_evento <- rep(datas_evento, length.out = length(codigos))
  if (modo == "retrospectivo_congelado") {
    if (length(data_classificacao) != 1L || !valido(data_classificacao)) stop("Data da classificação congelada obrigatória.")
    datas_uso <- rep(data_classificacao, length(codigos))
  } else {
    if (!is.null(data_classificacao)) stop("Não misturar data congelada com modo contemporâneo.")
    datas_uso <- datas_evento
  }
  out <- data.frame(codigo_municipal_original = codigos, cod_municipio_ibge = NA_character_,
    regiao_id = NA_character_, regiao_nome = NA_character_, data_evento = datas_evento,
    data_classificacao = datas_uso, versao_territorial = versao, papel_territorial = papel,
    modo_territorial = modo, estado = "sem_correspondencia", stringsAsFactors = FALSE)
  for (dia in unique(datas_uso)) {
    # Reutiliza o contrato de cardinalidade/vigência, sem herdar seu papel gestor.
    conferir_correspondencia_territorial(unique(m$cod_municipio_cnes), m, dia)
    vigente <- m[m$vigencia_inicio <= dia & m$vigencia_fim >= dia, , drop = FALSE]
    inds <- which(datas_uso == dia)
    for (i in inds) {
      cod <- codigos[i]
      if (is.na(cod) || !grepl("^([0-9]{6}|[0-9]{7})$", cod)) {
        out$estado[i] <- "codigo_ausente_ou_invalido"; next
      }
      campo <- if (nchar(cod) == 6L) "cod_municipio_cnes" else "cod_municipio_ibge"
      j <- match(cod, vigente[[campo]])
      if (is.na(j)) {
        if (cod %in% m[[campo]]) out$estado[i] <- "fora_vigencia"
        next
      }
      out$cod_municipio_ibge[i] <- vigente$cod_municipio_ibge[j]
      out$regiao_id[i] <- vigente$regiao_id[j]
      out$regiao_nome[i] <- vigente$regiao_nome[j]
      out$estado[i] <- "associado_no_contrato_tecnico"
    }
  }
  out
}
