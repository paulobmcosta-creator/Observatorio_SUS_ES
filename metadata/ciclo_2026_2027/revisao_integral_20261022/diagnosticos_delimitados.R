# Executar da raiz. Casos sintéticos para decidir correções futuras; sem alterar
# fixtures, código produtivo, bases históricas ou relatório encerrado.
source("src/transform/preparar_estabelecimentos_cnes.R")
source("src/indicators/calcular_indicadores_cnes_oferta.R")
local({
  destino <- commandArgs(trailingOnly = TRUE)
  stopifnot(length(destino) == 1L, !file.exists(destino))
  tmp <- tempfile("revisao_integral_"); dir.create(tmp)
  on.exit(unlink(tmp, recursive = TRUE))
  raw <- file.path(tmp, "raw"); dir.create(raw)
  dir.create(file.path(raw, "202602"))
  for (f in list.files("tests/fixtures/cnes/202601", full.names = TRUE)) {
    file.copy(f, file.path(raw, "202602", sub("202601", "202602", basename(f))))
  }
  caminho <- file.path(raw, "202602", "tbEstabelecimento202602.csv")
  dados <- read.csv2(caminho, colClasses = "character", check.names = FALSE)
  # Município alternativo diferente do gestor; não atribui automaticamente
  # semântica física a um nome de coluna sem dicionário oficial.
  dados$CO_MUNICIPIO <- rev(dados$CO_MUNICIPIO_GESTOR)
  write.table(dados, caminho, sep = ";", row.names = FALSE, na = "")
  resultado <- preparar_estabelecimentos_cnes(raw, competencia = "202602", dir_interim = file.path(tmp, "saida"))
  stopifnot(nrow(resultado) == 1L)
  indicadores <- calcular_indicadores_cnes_oferta(data.frame(
    competencia_aaaamm = c("202601", "202602", "202602", "202602"),
    co_municipio_gestor = rep("3200102", 4),
    co_cnes = c("0000001", "0000001", "", NA_character_)))
  registros <- data.frame(
    id = c("DI01", "DI02", "DI03"),
    duvida = c("Proveniência acompanha competência?", "Qual coluna municipal prevalece?", "Distinct exclui branco e separa meses?"),
    material = c("Fixture renomeada para 202602 em temporário", "Gestor=3200102; CO_MUNICIPIO=3304557 na mesma fixture", "Quatro linhas; CNES repetido em dois meses; branco; NA"),
    criterio_antes = c("competencia=202602 e arquivo_origem=tbEstabelecimento202602", "Identificar seleção; uso físico exige regra/layout explícitos", "Para medida substantiva, branco não é estabelecimento e recorte mensal é explícito"),
    observado = c(paste(resultado$competencia, resultado$arquivo_origem, sep = ";"),
                  paste(resultado$cod_municipio, resultado$uf, sep = ";"),
                  paste0("distinct=", indicadores$valor[indicadores$indicador == "total_estabelecimentos_distintos"], ";competencias=", indicadores$valor[indicadores$indicador == "total_competencias_distintas"])),
    decisao = c("Corrigir metadado antes de outra competência; tarefa R22", "Não promover gestor a localização; tarefa R23", "Manter controle técnico com limite; não usar como indicador substantivo sem adaptação R22"),
    limite = "Sintético; não valida série ou semântica do cadastro oficial",
    stringsAsFactors = FALSE)
  stopifnot(resultado$arquivo_origem == "tbEstabelecimento202601",
            resultado$cod_municipio == "3200102",
            indicadores$valor[indicadores$indicador == "total_estabelecimentos_distintos"] == 2)
  write.csv(registros, destino, row.names = FALSE, fileEncoding = "UTF-8")
  cat("Três comportamentos reproduzidos; limitações confirmadas, nenhuma correção produtiva aplicada.\n")
})
