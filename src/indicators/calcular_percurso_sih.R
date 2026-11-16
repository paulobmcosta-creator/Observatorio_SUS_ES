#' Calcular S03/S04 sobre RD já lido e aprovado, preservando registros repetidos.
#' @param rd Tabela com campos originais textuais; não é leitor/decodificador DBC.
#' @param contrato Lista com competencia, ident_elegivel, ident_dominio, municipios_es,
#' municipios_destino_conhecidos e gates documentais/operacionais. Sem valores padrão científicos.
#' @param mapa Correspondência central congelada v2, ou NULL para S03 sem região.
#' @param modo empirico (gates obrigatórios) ou fixture_sintetica (nunca resultado real).
#' @return Tabelas S03/S04/matriz e perdas mutuamente exclusivas; sem dados individuais.
#' @references mandato integrado §§7/10; primeiro_percurso_analitico.md; D1 §§7/8.
calcular_percurso_sih <- function(rd, contrato, mapa = NULL, modo = "empirico") {
  if (!modo %in% c("empirico", "fixture_sintetica")) stop("Modo inválido.")
  if (modo == "empirico") {
    if (!exists("validar_vinculos_sih", mode = "function")) stop("Gates empíricos exigem o verificador de evidências vinculadas.")
    validar_vinculos_sih(rd, contrato)
  }
  parametros <- c("competencia", "ident_elegivel", "ident_dominio", "municipios_es", "municipios_destino_conhecidos")
  if (!all(parametros %in% names(contrato)) || any(vapply(contrato[parametros], function(x) !is.character(x) || !length(x) || anyNA(x), logical(1)))) stop("Contrato SIH incompleto.")
  if (length(contrato$competencia) != 1L || !grepl("^[0-9]{4}(0[1-9]|1[0-2])$", contrato$competencia) ||
      !all(contrato$ident_elegivel %in% contrato$ident_dominio)) stop("Competência/domínio incoerente.")
  if (any(!grepl("^32[0-9]{4}$", contrato$municipios_es)) || anyDuplicated(contrato$municipios_es) ||
      !all(contrato$municipios_es %in% contrato$municipios_destino_conhecidos) ||
      any(!grepl("^[0-9]{6}$", contrato$municipios_destino_conhecidos))) stop("Catálogo municipal inválido.")
  if (modo == "empirico" && length(contrato$municipios_es) != 78L) stop("Catálogo ES deve conter 78 municípios.")
  campos <- c("IDENT", "MUNIC_RES", "MUNIC_MOV", "N_AIH", "ANO_CMPT", "MES_CMPT", "DT_INTER", "DT_SAIDA")
  if (!all(campos %in% names(rd)) || !all(vapply(rd[campos], is.character, logical(1)))) stop("Campos SIH obrigatórios devem ser texto.")
  if (!nrow(rd)) stop("Universo SIH obrigatório vazio.")
  mes <- ifelse(nchar(rd$MES_CMPT) == 1L, paste0("0", rd$MES_CMPT), rd$MES_CMPT)
  competencia <- paste0(rd$ANO_CMPT, mes)
  motivo <- rep("elegivel", nrow(rd))
  motivo[is.na(rd$ANO_CMPT) | is.na(rd$MES_CMPT) | competencia != contrato$competencia] <- "fora_competencia"
  selecionar <- function(condicao, valor) motivo[which(motivo == "elegivel" & condicao)] <<- valor
  selecionar(is.na(rd$IDENT) | !rd$IDENT %in% contrato$ident_dominio, "ident_ignorado_ou_nao_resolvido")
  selecionar(!rd$IDENT %in% contrato$ident_elegivel, "ident_nao_elegivel")
  selecionar(is.na(rd$MUNIC_RES) | !rd$MUNIC_RES %in% contrato$municipios_destino_conhecidos, "residencia_ignorada_ou_invalida")
  selecionar(!rd$MUNIC_RES %in% contrato$municipios_es, "residente_fora_es")
  motivos <- c("fora_competencia", "ident_ignorado_ou_nao_resolvido", "ident_nao_elegivel", "residencia_ignorada_ou_invalida", "residente_fora_es", "elegivel")
  perdas <- data.frame(motivo = motivos, registros = as.integer(table(factor(motivo, levels = motivos))))
  stopifnot(sum(perdas$registros) == nrow(rd))
  # Domínios novos não são silenciosamente tratados como AIH normal.
  if (modo == "empirico" && any(motivo == "ident_ignorado_ou_nao_resolvido")) stop("Domínio IDENT não resolvido; revisar coorte antes de agregar.")
  coorte <- rd[motivo == "elegivel", , drop = FALSE]
  origem <- rep("NAO_REGIONALIZADA", nrow(coorte))
  destino_regiao <- rep(NA_character_, nrow(coorte))
  if (!is.null(mapa)) {
    if (modo == "empirico") validar_vinculo_territorio_sih(mapa, contrato)
    if (!"versao_territorial" %in% names(mapa) || !length(contrato$territorio_versao)) stop("Versão territorial explícita obrigatória.")
    mapa <- mapa[which(mapa$versao_territorial == contrato$territorio_versao), , drop = FALSE]
    if (!nrow(mapa)) stop("Versão territorial não encontrada.")
    dia <- paste0(substr(contrato$competencia, 1, 4), "-", substr(contrato$competencia, 5, 6), "-01")
    # Selecionar papel antes da cardinalidade; versões antigas não formam o domínio de saída.
    mapas_papel <- lapply(c("residencia", "atendimento"), function(papel) {
      m <- mapa
      if ("papel_territorial" %in% names(m)) m <- m[which(m$papel_territorial == papel), , drop = FALSE]
      conferir_correspondencia_territorial(unique(m$cod_municipio_cnes), m, dia)
      m[which(m$vigencia_inicio <= dia & m$vigencia_fim >= dia), , drop = FALSE]
    })
    names(mapas_papel) <- c("residencia", "atendimento")
    for (papel in c("residencia", "atendimento")) {
      codigos <- if (papel == "residencia") coorte$MUNIC_RES else coorte$MUNIC_MOV
      if (!length(codigos) || !nrow(mapas_papel[[papel]])) next
      aplicado <- territorializar_municipios(codigos, dia,
        mapas_papel[[papel]], contrato$territorio_versao, papel, "contemporaneo")
      if (papel == "residencia") origem[!is.na(aplicado$regiao_id)] <- aplicado$regiao_id[!is.na(aplicado$regiao_id)]
      else destino_regiao <- aplicado$regiao_id
    }
  }
  regioes <- sort(unique(c(if (!is.null(mapa)) mapas_papel$residencia$regiao_id, origem)))
  s03 <- data.frame(regiao_residencia = c("TOTAL_ES", regioes),
    registros_elegiveis = c(nrow(coorte), as.integer(table(factor(origem, levels = regioes)))))
  categorias <- c("propria_regiao", "outra_regiao_es", "fora_es", "ignorado", "es_sem_comparacao_regional")
  categoria <- rep("ignorado", nrow(coorte))
  conhecido <- !is.na(coorte$MUNIC_MOV) & coorte$MUNIC_MOV %in% contrato$municipios_destino_conhecidos
  categoria[conhecido & !coorte$MUNIC_MOV %in% contrato$municipios_es] <- "fora_es"
  categoria[conhecido & coorte$MUNIC_MOV %in% contrato$municipios_es] <- "es_sem_comparacao_regional"
  categoria[conhecido & origem != "NAO_REGIONALIZADA" & !is.na(destino_regiao) & destino_regiao == origem] <- "propria_regiao"
  categoria[conhecido & origem != "NAO_REGIONALIZADA" & !is.na(destino_regiao) & destino_regiao != origem] <- "outra_regiao_es"
  matriz <- as.data.frame(table(regiao_residencia = factor(origem, levels = regioes),
    categoria_destino = factor(categoria, levels = categorias)), stringsAsFactors = FALSE)
  names(matriz)[3] <- "registros"
  stopifnot(sum(matriz$registros) == nrow(coorte))
  destino_tipo <- rep("ignorado", nrow(coorte))
  destino_id <- rep("IGNORADO", nrow(coorte))
  externo <- conhecido & !coorte$MUNIC_MOV %in% contrato$municipios_es
  destino_tipo[externo] <- "uf_externa"
  destino_id[externo] <- paste0("UF_IBGE_", substr(coorte$MUNIC_MOV[externo], 1, 2))
  es <- conhecido & coorte$MUNIC_MOV %in% contrato$municipios_es
  destino_tipo[es] <- "es_sem_regiao_resolvida"
  destino_id[es] <- "ES_REGIAO_NAO_RESOLVIDA"
  mapeado <- es & !is.na(destino_regiao)
  destino_tipo[mapeado] <- "regiao_es"
  destino_id[mapeado] <- paste0("REGIAO_", destino_regiao[mapeado])
  od <- data.frame(origem_regiao = origem, destino_tipo = destino_tipo, destino_id = destino_id, registros = rep(1L, nrow(coorte)))
  if (nrow(od)) od <- aggregate(registros ~ origem_regiao + destino_tipo + destino_id, od, sum)
  stopifnot(sum(od$registros) == nrow(coorte))
  s04 <- NULL
  if (!is.null(mapa)) {
    linhas <- lapply(setdiff(regioes, "NAO_REGIONALIZADA"), function(regiao) {
      selecao <- origem == regiao
      denominador <- sum(selecao & categoria %in% c("propria_regiao", "outra_regiao_es", "fora_es"))
      numerador <- sum(selecao & categoria %in% c("outra_regiao_es", "fora_es"))
      data.frame(regiao_residencia = regiao, total_elegivel = sum(selecao), numerador = numerador,
        denominador = denominador, destino_ignorado = sum(selecao & categoria == "ignorado"),
        es_sem_comparacao_regional = sum(selecao & categoria == "es_sem_comparacao_regional"),
        percentual_fora = if (denominador == 0L) NA_real_ else 100 * numerador / denominador)
    })
    s04 <- do.call(rbind, linhas)
  }
  list(s03 = s03, s04 = s04, matriz = matriz, matriz_origem_destino = od, perdas = perdas,
    divulgacao_fluxos = "BLOQUEADA_ATE_POLITICA_DE_PEQUENAS_CELULAS; saida_local_controlada",
    origem_nao_regionalizada = sum(origem == "NAO_REGIONALIZADA"),
    perfil_ident = as.data.frame(table(rd$IDENT, useNA = "always")), modo = modo,
    status = if (modo == "fixture_sintetica") "SINTETICO_NAO_EMPIRICO" else "CALCULO_LOCAL_SUJEITO_A_REVISAO")
}
