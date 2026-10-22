# Reutiliza preparadores/contratos existentes; não reimplementa regras em Python.
# Uso: Rscript scripts/conferir_paridade_parquet_r.R CSV_RESTITUIDO SAIDA_NOVA REFERENCIA EVIDENCIAS
source("src/transform/preparar_estabelecimentos_cnes.R")
source("src/transform/preparar_habilitacoes_cnes.R")
source("src/validation/conferir_contrato_snapshot_cnes.R")
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 4L, !dir.exists(args[2]), dir.exists(args[3]), dir.exists(args[4]))
est <- preparar_estabelecimentos_cnes("data_raw/cnes", dir_interim = args[2], arquivo_estabelecimentos = args[1])
hab <- preparar_habilitacoes_cnes(dir_interim = args[2])
est <- ler_snapshot_cnes(file.path(args[2], "estabelecimentos/cnes_estabelecimentos_es_202601.csv"))
hab <- ler_snapshot_cnes(file.path(args[2], "habilitacoes/cnes_habilitacoes_es_202601.csv"))
ref_est <- ler_snapshot_cnes(file.path(args[3], "estabelecimentos/cnes_estabelecimentos_es_202601.csv"))
ref_hab <- ler_snapshot_cnes(file.path(args[3], "habilitacoes/cnes_habilitacoes_es_202601.csv"))
comparacoes <- data.frame(produto = c("estabelecimentos", "habilitacoes"),
  linhas_referencia = c(nrow(ref_est), nrow(ref_hab)), linhas_novas = c(nrow(est), nrow(hab)),
  campos_ordem_valores_identicos = c(identical(est, ref_est), identical(hab, ref_hab)))
write.csv(comparacoes, file.path(args[4], "paridade_r.csv"), row.names = FALSE)
checks <- conferir_contrato_snapshot_cnes(est, hab,
  ler_snapshot_cnes("metadata/cnes/classificacao_habilitacoes_cnes.csv", ";"),
  ler_schema_snapshot_cnes("metadata/cnes/schema_estabelecimentos_cnes.csv"),
  ler_schema_snapshot_cnes("metadata/cnes/schema_habilitacoes_cnes.csv"))
write.csv(checks, file.path(args[4], "contrato_r.csv"), row.names = FALSE)
stopifnot(all(comparacoes$campos_ordem_valores_identicos), all(checks$estado == "passou"))
print(comparacoes)
cat("Contrato:", nrow(checks), "verificações aprovadas.\n")
