source("src/extract/preparar_cache_cnes.R")
source("src/validation/validar_correspondencia_territorial.R")
source("src/transform/territorializar_municipios.R")
local({
  # Fixture sintética: não contém a regionalização real do ES.
  m <- data.frame(versao_territorial = c("V2024", "V2025"), cod_municipio_cnes = "000001", cod_municipio_ibge = "0000019",
    regiao_id = c("ANTIGA", "NOVA"), regiao_nome = c("Região de teste A", "Região de teste B"),
    vigencia_inicio = c("2024-01-01", "2025-01-01"), vigencia_fim = c("2024-12-31", "2025-12-31"),
    fonte_url = "https://example.invalid/territorio", ato_referencia = "SINTETICO", sha256_fonte = strrep("a", 64))
  tmp <- tempfile(fileext = ".csv"); on.exit(unlink(tmp)); write.csv(m, tmp, row.names = FALSE)
  hash <- sha256_fonte_cnes(tmp)
  pin <- ler_territorio_congelado(tmp, "V2024", hash)
  r <- territorializar_municipios(c("000001", "0000019", "999999", NA_character_), "2015-06-01", pin,
    "V2024", "residencia", "retrospectivo_congelado", "2024-06-01")
  stopifnot(identical(r$regiao_id[1:2], c("ANTIGA", "ANTIGA")), identical(r$codigo_municipal_original[1:2], c("000001", "0000019")),
    all(r$papel_territorial == "residencia"), all(r$data_evento == "2015-06-01"), all(is.na(r$regiao_id[3:4])))
  hist <- territorializar_municipios("000001", "2015-06-01", m, "V2024", "atendimento", "contemporaneo")
  stopifnot(hist$estado == "fora_vigencia", is.na(hist$regiao_id))
  novo <- territorializar_municipios("000001", "2015-06-01", m, "V2024", "residencia", "retrospectivo_congelado", "2024-06-01")
  stopifnot(novo$regiao_id == "ANTIGA")
  falha <- function(expr) stopifnot(inherits(tryCatch({force(expr); NULL}, error = identity), "error"))
  falha(ler_territorio_congelado(tmp, "", hash))
  falha(ler_territorio_congelado(tmp, "V2024", strrep("0",64)))
  falha(territorializar_municipios("000001", "2015-06-01", m, "V9999", "residencia", "retrospectivo_congelado", "2024-06-01"))
  falha(territorializar_municipios("000001", "2015-06-01", m, "V2024", "residencia", "retrospectivo_congelado"))
  m$regiao_nome[1] <- "Alteração após congelamento"; write.csv(m,tmp,row.names=FALSE)
  falha(ler_territorio_congelado(tmp, "V2024", hash))
  message("OK: classificação retrospectiva distinta da vigência do evento; versão/hash congelados; papéis e códigos preservados; lacunas explícitas")
})
