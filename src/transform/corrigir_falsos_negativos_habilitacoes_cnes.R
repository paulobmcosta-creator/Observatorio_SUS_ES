# Correção pontual de falsos negativos na classificação de habilitações CNES (Ciclo 3C)

corrigir_falsos_negativos_habilitacoes_cnes <- function(
  caminho_classificacao = file.path("metadata", "cnes", "classificacao_habilitacoes_cnes.csv")
) {
  if (!file.exists(caminho_classificacao)) stop("Arquivo de classificação não encontrado: ", caminho_classificacao)

  classif <- utils::read.csv2(caminho_classificacao, stringsAsFactors = FALSE, fileEncoding = "UTF-8", check.names = FALSE)

  oficiais <- c("codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao", "origem_habilitacao")
  analiticos <- c("linha_cuidado", "sublinha_cuidado", "componente_rede", "nivel_complexidade", "usar_observatorio", "prioridade", "criterio_classificacao", "status_validacao")
  if ("observacao" %in% names(classif)) analiticos <- c(analiticos, "observacao")

  faltantes <- setdiff(c(oficiais, analiticos), names(classif))
  if (length(faltantes) > 0) stop("Colunas ausentes: ", paste(faltantes, collapse = ", "))

  classif$codigo_habilitacao <- trimws(as.character(classif$codigo_habilitacao))
  classif$tipo_habilitacao <- trimws(as.character(classif$tipo_habilitacao))
  chave <- paste(classif$codigo_habilitacao, classif$tipo_habilitacao, sep = "__")
  if (any(duplicated(chave))) stop("Duplicidade na chave composta antes da correção.")

  oficiais_antes <- classif[, oficiais, drop = FALSE]

  correcoes <- data.frame(
    codigo_habilitacao = c("1706","1707","1712","3202","3203","3807","8212","8213","8214","8210","8271","8272","815","8116","8117","2101","2102","2802","2803"),
    tipo_habilitacao = c("H","H","H","H","H","H","I","I","I","I","I","I","H","I","I","H","H","H","H"),
    linha_cuidado = c("Oncologia","Oncologia","Oncologia","Oncologia","Oncologia","Oncologia","RUE","RUE","RUE","RUE","RUE","RUE","Cardiovascular","Nefrologia","Nefrologia","UTI / cuidado crítico","UTI / cuidado crítico","UTI / cuidado crítico","UTI / cuidado crítico"),
    sublinha_cuidado = c("UNACON","UNACON com radioterapia","CACON","Diagnóstico oncológico / colo do útero","Qualidade diagnóstica em citopatologia / colo do útero","Radioterapia","Porta hospitalar de urgência","Porta hospitalar de urgência","Porta hospitalar de urgência","Atendimento ao AVC","Retaguarda hospitalar","Retaguarda hospitalar","Cardiologia intervencionista / TAVI","Doença renal crônica / categoria I","Doença renal crônica / categoria II","Queimados","Queimados","Cuidado intermediário neonatal","Cuidado intermediário neonatal"),
    componente_rede = c("Atenção oncológica de alta complexidade","Atenção oncológica com radioterapia","Atenção oncológica de alta complexidade","Diagnóstico citopatológico do colo do útero","Monitoramento externo da qualidade diagnóstica","Acesso à radioterapia","Atenção hospitalar de urgência","Atenção hospitalar de urgência","Atenção hospitalar de urgência","Leito/cuidado integral ao AVC","Enfermaria clínica de retaguarda","Enfermaria clínica de retaguarda","Atenção cardiovascular de alta complexidade","Atenção à doença renal crônica","Atenção à doença renal crônica","Centro de referência em assistência a queimados","Centro de referência em assistência a queimados","Unidade de cuidado intermediário neonatal convencional","Unidade de cuidado intermediário neonatal canguru"),
    nivel_complexidade = c("Alta complexidade","Alta complexidade","Alta complexidade","Atenção especializada / diagnóstico","Atenção especializada / diagnóstico","Alta complexidade","Urgência/emergência","Urgência/emergência","Urgência/emergência","Urgência/emergência","Atenção hospitalar / RUE","Atenção hospitalar / RUE","Alta complexidade","Atenção especializada","Atenção especializada","Média complexidade","Alta complexidade","Cuidado intermediário","Cuidado intermediário"),
    usar_observatorio = rep("Sim", 19),
    prioridade = c("Alta","Alta","Alta","Média","Média","Alta","Alta","Alta","Alta","Alta","Média","Média","Alta","Média","Média","Média","Alta","Média","Média"),
    criterio_classificacao = c(
      "Descrição oficial explicita UNACON, componente da atenção oncológica especializada.",
      "Descrição oficial explicita UNACON com serviço de radioterapia.",
      "Descrição oficial explicita CACON.",
      "Descrição oficial vincula a habilitação ao diagnóstico citopatológico do colo do útero, relevante para a linha oncológica.",
      "Descrição oficial vincula a habilitação ao monitoramento da qualidade de exames citopatológicos do colo do útero, relevante para a linha oncológica, mas não equivalente a CACON/UNACON.",
      "Descrição oficial explicita componente de acesso à radioterapia, relevante para a linha oncológica.",
      "Descrição oficial explicita porta de entrada hospitalar de urgência.",
      "Descrição oficial explicita porta de entrada hospitalar de urgência.",
      "Descrição oficial explicita porta de entrada hospitalar de urgência.",
      "Descrição oficial explicita cuidado integral ao paciente com AVC, componente relevante para RUE.",
      "Descrição oficial indica enfermaria clínica de retaguarda, componente associado à organização da resposta hospitalar; manter revisão por não explicitar isoladamente porta de urgência.",
      "Descrição oficial indica enfermaria clínica de retaguarda, componente associado à organização da resposta hospitalar; manter revisão por não explicitar isoladamente porta de urgência.",
      "Descrição oficial explicita procedimento cardiovascular estrutural/intervencionista.",
      "Sigla DRC é interpretada no contexto da habilitação CNES como doença renal crônica; manter revisão por depender de confirmação normativa específica da categoria.",
      "Sigla DRC é interpretada no contexto da habilitação CNES como doença renal crônica; manter revisão por depender de confirmação normativa específica da categoria.",
      "Descrição oficial explicita centro de referência em assistência a queimados; incluído por aderência ao eixo de cuidado crítico/queimados, com revisão metodológica.",
      "Descrição oficial explicita centro de referência em assistência a queimados de alta complexidade; incluído por aderência ao eixo de cuidado crítico/queimados.",
      "Descrição oficial explicita unidade de cuidados intermediários neonatal; incluída no eixo UTI/cuidado crítico por proximidade com cuidado neonatal de maior complexidade, sem equiparar a UTI neonatal.",
      "Descrição oficial explicita unidade de cuidados intermediários neonatal canguru; incluída no eixo UTI/cuidado crítico por proximidade com cuidado neonatal de maior complexidade, sem equiparar a UTI neonatal."
    ),
    status_validacao = c("validado","validado","validado","revisar","revisar","revisar","validado","validado","validado","validado","revisar","revisar","validado","revisar","revisar","revisar","revisar","revisar","revisar"),
    stringsAsFactors = FALSE
  )

  chave_cor <- paste(correcoes$codigo_habilitacao, correcoes$tipo_habilitacao, sep = "__")
  if (any(duplicated(chave_cor))) stop("Tabela de correções com chave duplicada.")

  idx <- match(chave_cor, chave)
  if (any(is.na(idx))) stop("Há chaves de correção ausentes na classificação: ", paste(chave_cor[is.na(idx)], collapse = ", "))

  for (i in seq_len(nrow(correcoes))) {
    j <- idx[i]
    for (campo in setdiff(names(correcoes), c("codigo_habilitacao", "tipo_habilitacao"))) {
      classif[j, campo] <- correcoes[i, campo]
    }
  }

  oficiais_depois <- classif[, oficiais, drop = FALSE]
  if (!identical(oficiais_antes, oficiais_depois)) stop("Campos oficiais foram alterados indevidamente.")

  chave2 <- paste(classif$codigo_habilitacao, classif$tipo_habilitacao, sep = "__")
  if (any(duplicated(chave2))) stop("Duplicidade na chave composta após correção.")

  valid_linha <- c("Oncologia", "Cardiovascular", "RUE", "UTI / cuidado crítico", "Nefrologia", "Saúde mental", "Outras habilitações estratégicas", "Fora do escopo inicial", "Revisar")
  if (length(setdiff(unique(classif$linha_cuidado), valid_linha)) > 0) stop("Domínio inválido em linha_cuidado.")
  if (length(setdiff(unique(classif$usar_observatorio), c("Sim", "Não"))) > 0) stop("Domínio inválido em usar_observatorio.")
  if (length(setdiff(unique(classif$prioridade), c("Alta", "Média", "Baixa"))) > 0) stop("Domínio inválido em prioridade.")
  if (length(setdiff(unique(classif$status_validacao), c("revisar", "validado"))) > 0) stop("Domínio inválido em status_validacao.")

  utils::write.table(classif, caminho_classificacao, sep = ";", row.names = FALSE, fileEncoding = "UTF-8", quote = TRUE)
  invisible(classif)
}
