ler <- function(p) read.csv(p,colClasses="character",check.names=FALSE,na.strings=NULL)
comum <- ler("config/institucional.csv")
tcc <- ler("config/estudos/tcc_cardiovascular.csv")
valor <- function(d,k) {stopifnot(sum(d$chave==k)==1L);d$valor[d$chave==k]}
stopifnot(valor(comum,"periodo_empirico")=="definido_por_estudo",valor(comum,"filtro_cid")=="definido_por_estudo",
  valor(tcc,"ano_inicio")=="2014",valor(tcc,"ano_fim")=="2024",valor(tcc,"cid_iam")=="",
  valor(comum,"territorio_tabela_central")==valor(tcc,"territorio_tabela_central"))
regioes <- strsplit(valor(tcc,"regioes_principais"),";",fixed=TRUE)[[1]]
stopifnot(setequal(regioes,c("Norte","Central","Metropolitana","Sul")),!valor(tcc,"recorte_focal") %in% regioes,
  valor(tcc,"recorte_focal_nivel")=="subregional",valor(tcc,"territorio_modo")=="retrospectivo_congelado",
  valor(tcc,"territorio_sha256")=="",valor(tcc,"territorio_versao")=="")
message("OK: escolhas TCC isoladas; tabela central compartilhada; Noroeste 1 não é quinta região; referências pendentes explícitas")
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
