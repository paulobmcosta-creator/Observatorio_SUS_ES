-- Entradas previamente validadas e únicas por competência e estabelecimento.
CREATE TABLE matriz AS
WITH k AS (SELECT mes,cnes FROM cadastro UNION SELECT mes,cnes FROM rsum UNION SELECT mes,cnes FROM amb UNION SELECT mes,cnes FROM hosp)
SELECT k.*,coalesce(s.municipio,a.municipio,h.municipio,r.municipio) municipio,
 s.mes IS NOT NULL cadastrado,s.VINC_SUS,s.TP_UNID,s.NAT_JUR,s.TPGESTAO,s.ATENDAMB,s.ATENDHOS,
 coalesce(r.especifico,false) recurso_especifico,coalesce(r.estrutura_hosp,false) estrutura_hosp,
 coalesce(r.sr,false) servico,coalesce(r.hab,false) habilitacao,
 coalesce(a.especificas,0) aprovadas,coalesce(a.apresentadas,0) apresentadas,
 coalesce(a.contextuais,0) contextuais,coalesce(h.aih,0) aih,
 coalesce(a.especificas,0)>0 tem_pa,coalesce(h.aih,0)>0 tem_sih,
 CASE WHEN tem_pa AND tem_sih THEN 'ambos' WHEN tem_pa THEN 'apenas_PA' WHEN tem_sih THEN 'apenas_SIH' ELSE 'nenhum' END situacao,
 (s.municipio IS DISTINCT FROM a.municipio AND s.municipio IS NOT NULL AND a.municipio IS NOT NULL) OR
 (s.municipio IS DISTINCT FROM h.municipio AND s.municipio IS NOT NULL AND h.municipio IS NOT NULL) OR
 (a.municipio IS DISTINCT FROM h.municipio AND a.municipio IS NOT NULL AND h.municipio IS NOT NULL) conflito_territorial
FROM k LEFT JOIN cadastro s USING(mes,cnes) LEFT JOIN rsum r USING(mes,cnes) LEFT JOIN amb a USING(mes,cnes) LEFT JOIN hosp h USING(mes,cnes);
