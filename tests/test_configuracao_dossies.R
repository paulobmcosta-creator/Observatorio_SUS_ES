ler <- function(p) read.csv(p,colClasses="character",check.names=FALSE,na.strings=NULL)
comum <- ler("config/institucional.csv")
tcc <- ler("config/estudos/tcc_cardiovascular.csv")
valor <- function(d,k) {stopifnot(sum(d$chave==k)==1L);d$valor[d$chave==k]}
stopifnot(valor(comum,"periodo_empirico")=="definido_por_estudo",valor(comum,"filtro_cid")=="definido_por_estudo",
  valor(tcc,"ano_inicio")=="2014",valor(tcc,"ano_fim")=="2024",valor(tcc,"cid_iam")=="",
  valor(comum,"territorio_tabela_central")!=valor(tcc,"territorio_tabela_central"))
source("src/extract/preparar_cache_cnes.R")
source("src/validation/validar_correspondencia_territorial.R")
source("src/transform/territorializar_municipios.R")
cad <- ler_territorio_congelado(valor(tcc,"territorio_tabela_central"), valor(tcc,"territorio_versao"),
                                valor(tcc,"territorio_sha256"))
stopifnot(setequal(strsplit(valor(tcc,"regioes_principais"),";",fixed=TRUE)[[1]],unique(cad$regiao_nome)),
          nrow(cad)==78, identical(as.integer(table(cad$regiao_nome)), c(15L,23L,14L,26L)),
          valor(tcc,"recorte_focal")=="Norte", valor(tcc,"recorte_focal_nivel")=="regiao",
          valor(tcc,"comparacoes_focais")=="Norte:ES", cad$regiao_nome[cad$cod_municipio_cnes=="320330"]=="Central")
for (ano in 2014:2024) {
  reg <- territorializar_municipios(c(cad$cod_municipio_ibge,"329999"), paste0(ano,"-01-01"), cad,
    valor(tcc,"territorio_versao"),"residencia",valor(tcc,"territorio_modo"),valor(tcc,"territorio_data_classificacao"))
  stopifnot(identical(reg$regiao_id[1:78],cad$regiao_id),is.na(reg$regiao_id[79]))
}
message("OK: 78 municípios nas quatro regiões, classificação fixa nos 11 anos")
candidatos <- ler("metadata/estudos/tcc_cardiovascular/candidatos_codigos.csv")
sigtap <- candidatos[candidatos$dominio=="SIGTAP",]
stopifnot(all(grepl("^[0-9]{10}$",sigtap$codigo_normalizado)),all(candidatos$habilitado_selecao_final=="nao"),
  all(candidatos$status_historico=="preliminar_nao_verificado"),all(candidatos$competencia_inicio==""),all(candidatos$competencia_fim==""))
consultas <- sigtap[sigtap$codigo_normalizado=="0301010072",]
stopifnot(nrow(consultas)==2L,all(grepl("procedimento+CBO",consultas$regra_adicional,fixed=TRUE)),
  sigtap$nivel[sigtap$codigo_normalizado=="0406010684"]=="excluido_do_nucleo")
ex <- ler("metadata/estudos/tcc_cardiovascular/motivos_exclusao.csv")
stopifnot(identical(ex$codigo,paste0("EX0",1:7)),all(grepl("analise_especifica",ex$escopo,fixed=TRUE)))
message("OK: zeros SIGTAP preservados; candidatos sem vigência não promovidos; consulta exige CBO; EX01–EX07 por análise")
