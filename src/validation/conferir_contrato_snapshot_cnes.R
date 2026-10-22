#' Ler um snapshot sem inferir tipos nem reparar identificadores.
#' @param arquivo Caminho CSV UTF-8; sep Separador explícito.
#' @return data.frame com todas as colunas textuais e vazios preservados.
#' @references docs/ciclo_2026_2027/primeiro_incremento.md
ler_snapshot_cnes <- function(arquivo, sep = ",") {
    larguras <- utils::count.fields(arquivo, sep = sep, quote = '"', comment.char = "")
    completas <- !is.na(larguras)
    if (!length(larguras) || any(larguras[completas] != larguras[1])) {
        stop("CSV não retangular: ", arquivo, "; linhas finais de registro divergentes: ",
            paste(which(completas & larguras != larguras[1]), collapse = ";"))
    }
    utils::read.csv(arquivo, sep = sep, colClasses = "character",
                    na.strings = character(), check.names = FALSE,
                    fileEncoding = "UTF-8", stringsAsFactors = FALSE)
}

#' Ler schema estritamente ou conservar o erro como diagnóstico, sem repará-lo.
#' @param arquivo Schema CSV.
#' @return data.frame; atributo erro_csv quando sua estrutura não é interpretável.
#' @references docs/ciclo_2026_2027/primeiro_incremento.md
ler_schema_snapshot_cnes <- function(arquivo) {
    tryCatch(ler_snapshot_cnes(arquivo), error = function(e) {
        structure(data.frame(nome_campo = character(), obrigatorio = character()),
                  erro_csv = conditionMessage(e))
    })
}

#' Conferir contratos atuais contra snapshots históricos, sem transformá-los.
#' @param estabelecimentos,habilitacoes,classificacao data.frames textuais.
#' @param schema_estabelecimentos,schema_habilitacoes Schemas versionados.
#' @param competencia Competência única esperada, texto AAAAMM.
#' @return data.frame de verificações: escopo, regra, estado, ocorrencias, detalhe.
#'   Estados: passou, falhou, nao_executado. Não é validação sanitária.
#' @references metadata/cnes/schema_estabelecimentos_cnes.csv;
#'   metadata/cnes/schema_habilitacoes_cnes.csv;
#'   docs/cnes/base_estabelecimentos_cnes.md; docs/cnes/base_habilitacoes_cnes.md.
conferir_contrato_snapshot_cnes <- function(estabelecimentos, habilitacoes,
        classificacao, schema_estabelecimentos, schema_habilitacoes,
        competencia = "202601") {
    if (!is.character(competencia) || length(competencia) != 1L ||
        is.na(competencia) || !grepl("^[0-9]{4}(0[1-9]|1[0-2])$", competencia)) {
        stop("competencia deve ser texto AAAAMM com mês válido.")
    }
    resultado <- list()
    registrar <- function(escopo, regra, n, detalhe = "") {
        resultado[[length(resultado) + 1L]] <<- data.frame(
            escopo = escopo, regra = regra,
            estado = if (is.na(n)) "nao_executado" else if (n == 0) "passou" else "falhou",
            ocorrencias = as.integer(n), detalhe = detalhe,
            stringsAsFactors = FALSE)
    }
    vazio <- function(x) is.na(x) | trimws(x) == ""
    checar_base <- function(dados, schema, escopo) {
        stopifnot(is.data.frame(dados), is.data.frame(schema),
                  all(c("nome_campo", "obrigatorio") %in% names(schema)))
        registrar(escopo, "base_nao_vazia", as.integer(nrow(dados) == 0))
        registrar(escopo, "colunas_sem_duplicacao", sum(duplicated(names(dados))))
        erro_schema <- attr(schema, "erro_csv")
        registrar(escopo, "estrutura_csv_schema", as.integer(!is.null(erro_schema)),
                  if (is.null(erro_schema)) "" else erro_schema)
        if (is.null(erro_schema)) {
            faltantes <- setdiff(schema$nome_campo, names(dados))
            registrar(escopo, "colunas_do_schema", length(faltantes), paste(faltantes, collapse = ";"))
        } else registrar(escopo, "colunas_do_schema", NA_integer_, "Schema malformado; comparação completa não executada")
        # Núcleo também definido na documentação de chaves, independente do CSV de schema.
        nucleo <- c("competencia", "co_unidade", "cnes", "cod_municipio", "uf")
        faltantes <- setdiff(nucleo, names(dados))
        registrar(escopo, "colunas_nucleo", length(faltantes), paste(faltantes, collapse = ";"))
        obrigatorios <- unique(c(nucleo, schema$nome_campo[schema$obrigatorio == "sim"]))
        for (campo in intersect(unique(c(nucleo, schema$nome_campo)), names(dados))) {
            registrar(escopo, paste0("tipo_textual:", campo), as.integer(!is.character(dados[[campo]])))
        }
        for (campo in intersect(obrigatorios, names(dados))) {
            registrar(escopo, paste0("preenchimento:", campo), sum(vazio(dados[[campo]])))
        }
        for (campo in c("competencia", "cnes", "uf")) {
            if (!campo %in% names(dados)) {
                registrar(escopo, paste0("dominio:", campo), NA_integer_, "Campo ausente")
                next
            }
            x <- dados[[campo]]
            valido <- switch(campo,
                competencia = !vazio(x) & x == competencia,
                cnes = !vazio(x) & grepl("^[0-9]{7}$", x),
                uf = !vazio(x) & x == "ES")
            registrar(escopo, paste0("dominio:", campo), sum(!valido))
        }
        # Nenhuma conversão 6→7 dígitos ou suposição de região/município de atendimento.
        chaves <- if (escopo == "estabelecimentos") c("competencia", "co_unidade") else
            c("competencia", "co_unidade", "codigo_habilitacao", "tipo_habilitacao")
        if (all(chaves %in% names(dados))) {
            registrar(escopo, "chave_unica", sum(duplicated(dados[chaves])))
        } else registrar(escopo, "chave_unica", NA_integer_, "Chave contratual ausente; não substituir por cnes")
    }
    checar_base(estabelecimentos, schema_estabelecimentos, "estabelecimentos")
    checar_base(habilitacoes, schema_habilitacoes, "habilitacoes")

    campos_class <- c("codigo_habilitacao", "tipo_habilitacao", "usar_observatorio", "status_validacao", "linha_cuidado")
    stopifnot(is.data.frame(classificacao))
    registrar("classificacao", "base_nao_vazia", as.integer(nrow(classificacao) == 0))
    registrar("classificacao", "colunas_requeridas", length(setdiff(campos_class, names(classificacao))))
    if (all(campos_class %in% names(classificacao))) {
        for (campo in campos_class) {
            registrar("classificacao", paste0("tipo_textual:", campo), as.integer(!is.character(classificacao[[campo]])))
            registrar("classificacao", paste0("preenchimento:", campo), sum(vazio(classificacao[[campo]])))
        }
        registrar("classificacao", "chave_unica", sum(duplicated(classificacao[c("codigo_habilitacao", "tipo_habilitacao")])))
        registrar("classificacao", "dominio:usar_observatorio", sum(!classificacao$usar_observatorio %in% c("Sim", "Não")))
        registrar("classificacao", "dominio:status_validacao", sum(!classificacao$status_validacao %in% c("validado", "revisar")))
    }
    # Relação muitos-para-um pela chave operacional, nunca pelo rótulo cnes legado.
    campos_rel <- c("competencia", "co_unidade", "cnes", "cod_municipio")
    relacao_disponivel <- all(campos_rel %in% names(estabelecimentos)) &&
        all(campos_rel %in% names(habilitacoes)) &&
        !any(duplicated(estabelecimentos[c("competencia", "co_unidade")])) &&
        !any(vazio(estabelecimentos$co_unidade)) && !any(vazio(habilitacoes$co_unidade))
    if (relacao_disponivel) {
        # merge por múltiplas colunas evita colisões artificiais de chaves concatenadas.
        rel <- merge(habilitacoes[campos_rel], estabelecimentos[campos_rel],
            by = c("competencia", "co_unidade"), all.x = TRUE, suffixes = c("_hab", "_est"))
        registrar("relacao", "habilitacoes_estabelecimentos", sum(is.na(rel$cnes_est)))
        for (campo in c("cnes", "cod_municipio")) {
            a <- rel[[paste0(campo, "_hab")]]; b <- rel[[paste0(campo, "_est")]]
            registrar("relacao", paste0("igualdade:", campo), sum(is.na(a) | is.na(b) | a != b, na.rm = TRUE))
        }
    } else registrar("relacao", "habilitacoes_estabelecimentos", NA_integer_, "Chave ausente, vazia ou não única; relação não comprovada")

    class_disponivel <- all(campos_class %in% names(habilitacoes)) &&
        all(campos_class %in% names(classificacao)) &&
        !any(duplicated(classificacao[c("codigo_habilitacao", "tipo_habilitacao")])) &&
        !any(vazio(classificacao$codigo_habilitacao)) && !any(vazio(classificacao$tipo_habilitacao))
    if (class_disponivel) {
        rel <- merge(habilitacoes[campos_class], classificacao[campos_class],
            by = c("codigo_habilitacao", "tipo_habilitacao"), all.x = TRUE, suffixes = c("_hab", "_class"))
        for (campo in c("usar_observatorio", "status_validacao", "linha_cuidado")) {
            a <- rel[[paste0(campo, "_hab")]]; b <- rel[[paste0(campo, "_class")]]
            registrar("relacao", paste0("classificacao:", campo), sum(is.na(a) | is.na(b) | a != b, na.rm = TRUE))
        }
    } else registrar("relacao", "classificacao", NA_integer_, "Campos ausentes ou classificação sem chave única preenchida")
    do.call(rbind, resultado)
}
