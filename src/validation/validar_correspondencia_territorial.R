# Contrato técnico de uma correspondência explicitamente fornecida; não valida a norma.

#' Conferir associação do município gestor a uma região em uma data explícita.
#' @param codigos Códigos municipais CNES textuais observados, sem conversão.
#' @param correspondencia Tabela com o schema metadata/territorio/schema_correspondencia.csv.
#' @param data_referencia Data ISO YYYY-MM-DD deliberada pelo responsável metodológico.
#' @return Uma linha por código observado, inclusive ausências e códigos não associados.
#' @references docs/ciclo_2026_2027/rodada_03_territorio_habilitacoes.md
#' @details Exige chaves textuais, intervalos não sobrepostos e referência documental.
#' A presença de URL/hash/ato não comprova autenticidade, vigência legal ou revisão humana.
#' Sem correspondência, devolve NA e sem_correspondencia, nunca região inferida.
conferir_correspondencia_territorial <- function(codigos, correspondencia, data_referencia) {
  campos <- c("cod_municipio_cnes", "cod_municipio_ibge", "regiao_id", "regiao_nome",
    "vigencia_inicio", "vigencia_fim", "fonte_url", "ato_referencia", "sha256_fonte")
  if (!is.character(codigos)) stop("Códigos municipais devem ser texto.")
  if (!all(campos %in% names(correspondencia))) stop("Correspondência sem campos obrigatórios.")
  if (!all(vapply(correspondencia[campos], is.character, logical(1)))) stop("Correspondência deve preservar campos textuais.")
  data_iso <- function(x) {
    d <- suppressWarnings(as.Date(x, format = "%Y-%m-%d"))
    !is.na(x) & grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", x) & !is.na(d) & format(d, "%Y-%m-%d") == x
  }
  if (length(data_referencia) != 1L || !is.character(data_referencia) || !isTRUE(data_iso(data_referencia))) {
    stop("Informe uma data de referência ISO válida e explícita.")
  }
  m <- correspondencia
  if (nrow(m)) {
    if (any(vapply(m[campos], function(x) any(is.na(x) | trimws(x) == ""), logical(1)))) {
      stop("Correspondência com campo obrigatório vazio.")
    }
    if (any(!grepl("^[0-9]{6}$", m$cod_municipio_cnes)) || any(!grepl("^[0-9]{7}$", m$cod_municipio_ibge))) {
      stop("Formato territorial inválido; não truncar nem completar códigos.")
    }
    if (any(!data_iso(m$vigencia_inicio)) || any(!data_iso(m$vigencia_fim)) || any(m$vigencia_inicio > m$vigencia_fim)) {
      stop("Intervalo de vigência inválido; início e fim são obrigatórios.")
    }
    if (any(!grepl("^https://[^/[:space:]]+", m$fonte_url)) || any(!grepl("^[0-9a-f]{64}$", m$sha256_fonte))) {
      stop("Referência documental incompleta: URL HTTPS e SHA-256 exigidos.")
    }
    # Inclusive nos extremos: dois atos não podem atribuir duas regiões no mesmo dia.
    for (codigo in unique(m$cod_municipio_cnes)) {
      g <- m[m$cod_municipio_cnes == codigo, , drop = FALSE]
      g <- g[order(g$vigencia_inicio), , drop = FALSE]
      inicios <- as.numeric(as.Date(g$vigencia_inicio))
      fins <- as.numeric(as.Date(g$vigencia_fim))
      if (nrow(g) > 1L && any(inicios[-1] <= head(cummax(fins), -1))) {
        stop("Vigências sobrepostas para o mesmo município.")
      }
    }
  }
  vigente <- m[m$vigencia_inicio <= data_referencia & m$vigencia_fim >= data_referencia, , drop = FALSE]
  if (anyDuplicated(vigente$cod_municipio_ibge)) stop("Correspondência municipal não é um-para-um na data.")
  for (id in unique(vigente$regiao_id)) {
    if (length(unique(vigente$regiao_nome[vigente$regiao_id == id])) != 1L) stop("Região com nomes conflitantes na data.")
  }
  codigos <- unique(codigos)
  idx <- match(codigos, vigente$cod_municipio_cnes)
  estado <- ifelse(is.na(idx), "sem_correspondencia", "associado_no_contrato_tecnico")
  estado[is.na(idx) & codigos %in% m$cod_municipio_cnes] <- "fora_vigencia"
  estado[is.na(codigos) | !grepl("^[0-9]{6}$", codigos)] <- "codigo_ausente_ou_invalido"
  data.frame(cod_municipio_gestor = codigos, cod_municipio_ibge = vigente$cod_municipio_ibge[idx],
    regiao_do_municipio_gestor = vigente$regiao_id[idx], nome_regiao = vigente$regiao_nome[idx],
    data_referencia = data_referencia, papel_territorial = "municipio_gestor",
    estado = estado, stringsAsFactors = FALSE)
}
