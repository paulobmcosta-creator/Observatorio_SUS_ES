# Funcionamento operacional dos estabelecimentos

**Situação de uso: não mensurável com os campos validados neste estudo.** Foram examinados os esquemas e os campos efetivamente lidos nas 132 competências do CNES/ST. O arquivo campos_st_por_competencia.json permite consultar ambos por mês. ATIVIDAD, DT_ATUAL e os atributos cadastrais de atendimento, quando presentes, não documentam abertura física, continuidade diária ou disponibilidade efetiva de atendimento.

| Conceito | Regra no estudo | Fonte e unidade |
|---|---|---|
| Cadastro | Presença de CNES distinto na competência | ST_CAD, estabelecimentos por mês |
| Vínculo SUS | Presença e marca VINC_SUS igual a 1 | ST_SUS, estabelecimentos por mês |
| Produção observada | CNES com quantidade aprovada positiva do recorte específico, deduplicado no território e período | SIA/PA e SIGTAP; F23 por região e ano |
| Funcionamento efetivo | Medida indisponível; não há critério operacional validado nestes campos | Sem estimativa e sem imputação de zero |

O indicador de produção depende dos procedimentos selecionados e da janela de movimento. A atividade de outras especialidades e o funcionamento durante dias sem produção registrada permanecem desconhecidos.
