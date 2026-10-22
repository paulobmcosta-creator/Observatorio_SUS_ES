# Executar na raiz do checkout. Sem escrita nas camadas de dados.
# Uso: Rscript scripts/conferir_snapshot_cnes.R DIRETORIO_NOVO RESPONSAVEL
source("src/validation/conferir_contrato_snapshot_cnes.R")

#' Calcular SHA-256 de um arquivo, exigindo utilitário verificável.
#' @param arquivo Caminho de arquivo existente.
#' @return Hash SHA-256 textual; falha se o utilitário não estiver disponível.
#' @references docs/ciclo_2026_2027/primeiro_incremento.md
sha256_arquivo <- function(arquivo) {
    comando <- Sys.which("sha256sum")
    if (!nzchar(comando)) stop("sha256sum é necessário para registrar a execução.")
    saida <- system2(comando, c("--", shQuote(arquivo)), stdout = TRUE)
    if (!is.null(attr(saida, "status"))) stop("Falha no cálculo SHA-256.")
    hash <- substr(saida[1], 1, 64)
    if (!grepl("^[0-9a-f]{64}$", hash)) stop("SHA-256 inválido.")
    hash
}

#' Registrar uma nova conferência do snapshot 202601, sem reconstruí-lo.
#' @param diretorio_saida Diretório novo sob metadata/ciclo_2026_2027/execucoes.
#' @param responsavel Identificação verdadeira de quem executa (inclusive automação).
#' @return TRUE se todos os checks passaram; grava evidência também em reprovação.
#' @references docs/ciclo_2026_2027/primeiro_incremento.md
registrar_conferencia_snapshot <- function(diretorio_saida, responsavel) {
    if (!nzchar(trimws(responsavel))) stop("Identifique o responsável real pela execução.")
    if (file.exists(diretorio_saida)) stop("Destino existente: não sobrescrever evidências.")
    pai <- normalizePath(dirname(diretorio_saida), mustWork = TRUE)
    permitido <- normalizePath("metadata/ciclo_2026_2027/execucoes", mustWork = TRUE)
    if (pai != permitido || basename(diretorio_saida) %in% c(".", "..")) {
        stop("Use um novo subdiretório imediato de metadata/ciclo_2026_2027/execucoes.")
    }
    arquivos <- c(
        estabelecimentos = "data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv",
        habilitacoes = "data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv",
        classificacao = "metadata/cnes/classificacao_habilitacoes_cnes.csv",
        schema_estabelecimentos = "metadata/cnes/schema_estabelecimentos_cnes.csv",
        schema_habilitacoes = "metadata/cnes/schema_habilitacoes_cnes.csv",
        auditoria = "metadata/cnes/auditoria_fora_escopo_habilitacoes_cnes_202601.csv",
        codigo = "src/validation/conferir_contrato_snapshot_cnes.R",
        executor = "scripts/conferir_snapshot_cnes.R",
        teste = "tests/test_conferir_contrato_snapshot_cnes.R")
    hashes <- vapply(arquivos, sha256_arquivo, character(1))
    est <- ler_snapshot_cnes(arquivos[["estabelecimentos"]])
    hab <- ler_snapshot_cnes(arquivos[["habilitacoes"]])
    classif <- ler_snapshot_cnes(arquivos[["classificacao"]], ";")
    se <- ler_schema_snapshot_cnes(arquivos[["schema_estabelecimentos"]])
    sh <- ler_schema_snapshot_cnes(arquivos[["schema_habilitacoes"]])
    checks <- conferir_contrato_snapshot_cnes(est, hab, classif, se, sh)
    auditoria <- ler_snapshot_cnes(arquivos[["auditoria"]])
    resumo <- data.frame(
        medida = c("linhas_estabelecimentos", "municipios_codigos_observados",
            "linhas_habilitacoes", "valores_distintos_campo_cnes_legado_habilitacoes",
            "combinacoes_classificacao", "combinacoes_classificacao_no_escopo",
            "registros_habilitacao_no_escopo", "registros_no_escopo_status_validado_interno",
            "registros_no_escopo_status_revisar", "registros_fora_escopo",
            "linhas_auditoria", "soma_registros_auditoria"),
        valor = c(nrow(est), length(unique(est$cod_municipio)), nrow(hab),
            length(unique(hab$cnes)), nrow(classif), sum(classif$usar_observatorio == "Sim"),
            sum(hab$usar_observatorio == "Sim"),
            sum(hab$usar_observatorio == "Sim" & hab$status_validacao == "validado"),
            sum(hab$usar_observatorio == "Sim" & hab$status_validacao == "revisar"),
            sum(hab$usar_observatorio == "Não"), nrow(auditoria), sum(as.integer(auditoria$n_registros))),
        stringsAsFactors = FALSE)
    # A estabilidade do insumo entre leitura e gravação é parte da evidência.
    stopifnot(identical(hashes, vapply(arquivos, sha256_arquivo, character(1))))
    if (!dir.create(diretorio_saida)) stop("Não foi possível criar destino novo.")
    escrever <- function(dados, nome) utils::write.csv(dados, file.path(diretorio_saida, nome),
        row.names = FALSE, fileEncoding = "UTF-8", na = "NA")
    escrever(checks, "verificacoes.csv")
    escrever(resumo, "contagens_observadas.csv")
    escrever(data.frame(papel = names(arquivos), caminho = unname(arquivos),
        sha256 = unname(hashes), bytes = file.info(arquivos)$size), "insumos_sha256.csv")
    aprovado <- all(checks$estado == "passou")
    commit <- system2("git", c("rev-parse", "HEAD"), stdout = TRUE)
    if (!is.null(attr(commit, "status"))) stop("Falha ao identificar commit.")
    escrever(data.frame(campo = c("tipo_execucao", "instante_utc", "responsavel",
        "commit_base", "codigo_executado", "r_versao", "competencia", "filtros",
        "origem_local", "fonte_declarada", "url_extracao_original", "instante_extracao_original",
        "campos_estabelecimentos", "campos_habilitacoes", "resultado"),
        valor = c("nova_conferencia_local_nao_extracao", format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
            responsavel, commit, "Arquivos desta rodada identificados por SHA-256 em insumos_sha256.csv",
            R.version.string, "202601", "Nenhum filtro de linhas; leitura integral dos snapshots locais",
            "Checkout Git; origens locais em insumos_sha256.csv", "CNES conforme metadados do repositório",
            "não disponível no snapshot; não inferida", "não disponível; data_processamento não é extração",
            paste(names(est), collapse = ";"), paste(names(hab), collapse = ";"),
            if (aprovado) "contrato_conferido_no_escopo_tecnico" else "bloqueado_por_contrato")), "execucao.csv")
    produtos <- list.files(diretorio_saida, full.names = TRUE)
    escrever(data.frame(arquivo = basename(produtos), sha256 = vapply(produtos, sha256_arquivo, character(1))),
        "produtos_sha256.csv")
    message("Conferência: ", sum(checks$estado == "passou"), " passou; ",
        sum(checks$estado == "falhou"), " falhou; ", sum(checks$estado == "nao_executado"), " não executado.")
    aprovado
}

if (sys.nframe() == 0L) {
    args <- commandArgs(trailingOnly = TRUE)
    if (length(args) != 2L) stop("Uso: Rscript scripts/conferir_snapshot_cnes.R DIRETORIO_NOVO RESPONSAVEL")
    if (!registrar_conferencia_snapshot(args[1], args[2])) quit(status = 1L)
}
