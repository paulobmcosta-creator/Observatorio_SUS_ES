-- dominio_municipal deve corresponder à época. O instrumento e sua vigência clínica são pré-requisitos.
SELECT e.*,g.regiao regiao_destino,rg.regiao regiao_residencia,
CASE WHEN instrumento='C' THEN '2_referencia_prestador'
     WHEN instrumento IN ('I','P','S') AND dm.codigo IS NULL THEN '3_ignorada_invalida'
     WHEN instrumento IN ('I','P','S') THEN '1_residencia_identificavel'
     WHEN instrumento IN ('A','B') THEN '4_instrumento_nao_elegivel'
     ELSE '5_historica_indeterminada' END situacao_residencia
FROM elegivel e LEFT JOIN dominio_municipal dm ON dm.codigo=e.residencia
LEFT JOIN geo g ON g.municipio=e.municipio LEFT JOIN geo rg ON rg.municipio=e.residencia
