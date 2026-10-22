# Uso na raiz: Rscript scripts/auditar_territorio_habilitacoes.R ID_COMPARACAO ID_AUDITORIA RESPONSAVEL
source("src/extract/preparar_cache_cnes.R")
source("src/validation/conferir_contrato_snapshot_cnes.R")
source("src/validation/validar_correspondencia_territorial.R")
source("src/validation/preparar_fila_revisao_habilitacoes.R")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L || any(!grepl("^[A-Za-z0-9_-]+$", args[1:2])) || !nzchar(trimws(args[3]))) stop("Informe ID_COMPARACAO ID_AUDITORIA RESPONSAVEL.")
origem <- file.path(".cache/cnes/execucoes", args[1])
saida <- file.path("metadata/ciclo_2026_2027/execucoes", args[2])
if (file.exists(saida)) stop("Destino existente; não sobrescrever evidências.")
insumos <- c(
  file.path(origem, "estabelecimentos/cnes_estabelecimentos_es_202601.csv"),
  file.path(origem, "habilitacoes/cnes_habilitacoes_es_202601.csv"),
  "metadata/cnes/classificacao_habilitacoes_cnes.csv",
  "metadata/territorio/correspondencia_municipio_regiao_pendente.csv",
  "src/extract/preparar_cache_cnes.R", "src/validation/conferir_contrato_snapshot_cnes.R",
  "src/validation/validar_correspondencia_territorial.R", "src/validation/preparar_fila_revisao_habilitacoes.R",
  "scripts/auditar_territorio_habilitacoes.R")
hashes <- vapply(insumos, sha256_fonte_cnes, character(1))
manifesto_origem <- file.path("metadata/ciclo_2026_2027/execucoes", args[1], "produtos_sha256.csv")
produtos_origem <- read.csv(manifesto_origem, colClasses = "character")
idx <- match(insumos[1:2], produtos_origem$arquivo)
if (anyNA(idx) || !all(hashes[1:2] == produtos_origem$sha256[idx])) stop("Bases divergem dos produtos da comparação de origem.")
est <- ler_snapshot_cnes(insumos[1]); hab <- ler_snapshot_cnes(insumos[2])
if (!nrow(est) || !nrow(hab) || anyNA(est$competencia) || anyNA(hab$competencia) ||
    any(est$competencia != "202601") || any(hab$competencia != "202601")) stop("Exige bases não vazias da competência 202601.")
classif <- ler_snapshot_cnes(insumos[3], ";")
mapa <- read.csv(insumos[4], colClasses = "character")
if (nrow(mapa)) stop("Este executor registra lacuna documental; mapa preenchido requer revisão do escopo.")
# Data apenas para o teste negativo de correspondência vazia; não fixa regra temporal analítica.
territorio <- conferir_correspondencia_territorial(sort(unique(est$cod_municipio)), mapa, "2026-01-31")
territorio$municipio_no_snapshot <- vapply(territorio$cod_municipio_gestor, function(k) {
  nomes <- unique(est$municipio[est$cod_municipio == k])
  if (length(nomes) != 1L) stop("Nomes conflitantes no snapshot municipal.")
  nomes
}, character(1))
territorio$n_estabelecimentos_snapshot <- vapply(territorio$cod_municipio_gestor, function(k) sum(est$cod_municipio == k), integer(1))
fila <- preparar_fila_revisao_habilitacoes(classif, hab)
resumo <- aggregate(cbind(n_registros_observados, n_estabelecimentos_observados) ~ linha_cuidado + usar_observatorio + status_validacao,
  data = fila, FUN = sum)
# Soma de estabelecimentos por habilitação não é número de estabelecimentos distintos da linha.
names(resumo)[names(resumo) == "n_estabelecimentos_observados"] <- "soma_vinculos_estabelecimento_habilitacao"
resumo$n_combinacoes_classificacao <- vapply(seq_len(nrow(resumo)), function(i) sum(fila$linha_cuidado == resumo$linha_cuidado[i] & fila$usar_observatorio == resumo$usar_observatorio[i] & fila$status_validacao == resumo$status_validacao[i]), integer(1))
stopifnot(sum(fila$n_registros_observados) == nrow(hab), sum(territorio$n_estabelecimentos_snapshot) == nrow(est),
  identical(hashes, vapply(insumos, sha256_fonte_cnes, character(1))))
dir.create(saida, recursive = TRUE)
gravar <- function(x, nome) write.csv(x, file.path(saida, nome), row.names = FALSE, na = "", fileEncoding = "UTF-8")
gravar(territorio, "inventario_territorial.csv")
gravar(fila, "fila_revisao_habilitacoes.csv")
gravar(resumo, "resumo_revisao_habilitacoes.csv")
gravar(data.frame(arquivo = c(insumos, manifesto_origem), sha256 = c(unname(hashes), sha256_fonte_cnes(manifesto_origem))), "insumos_sha256.csv")
gravar(data.frame(instante_utc = format(Sys.time(), tz = "UTC", usetz = TRUE), responsavel = args[3], competencia = "202601",
  execucao_origem = args[1], versao_r = as.character(getRversion()), status_r06 = "pendente_fonte_oficial", status_r07 = "triagem_concluida_normas_pendentes",
  resultado = "diagnostico_de_lacunas_sem_homologacao"), "execucao.csv")
produtos <- list.files(saida, full.names = TRUE)
gravar(data.frame(arquivo = produtos, sha256 = vapply(produtos, sha256_fonte_cnes, character(1))), "produtos_sha256.csv")
cat("Inventário:", nrow(territorio), "códigos; sem correspondência oficial:", sum(territorio$estado == "sem_correspondencia"), "\n")
cat("Fila:", nrow(fila), "combinações; selecionadas:", sum(fila$usar_observatorio == "Sim"), "; registros reconciliados:", sum(fila$n_registros_observados), "\n")
cat("Diagnóstico concluído. R06/R07 continuam pendentes de fontes oficiais e revisão metodológica.\n")
