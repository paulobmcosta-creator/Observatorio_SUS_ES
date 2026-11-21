# Deliberação de divulgação integral e interpretação dos dados — v3.5.1

**Escopo:** 318 arquivos originais, incluindo 13 de maior granularidade, incluídos na v3.5.1 com os bytes originais.

## Decisão do responsável pela pesquisa

Em 21/11/2026 foi determinada a inclusão integral dos 13 originais que a prévia v3.5.0 havia substituído por versões agregadas. O objetivo é permitir reprodução e reutilização de todas as dimensões científicas homologadas. As agregações de v3.5.0 permanecem como produtos complementares.

## Verificação técnica e riscos residuais

- Nos cabeçalhos dos 11 CSV compactados não foram observados campos nominais de pacientes, CPF ou CNS; as unidades são óbitos agregados, AIHs, procedimentos e cadastros de estabelecimentos. Os dois Parquet foram verificados estruturalmente e reconciliados com as margens de referência; contêm informação longitudinal de estabelecimentos por CNES, não tabelas de pacientes.
- A ausência de identificador pessoal direto **não é garantia absoluta de anonimato**: município, período, diagnóstico, faixa etária, código de prestador e cruzamentos com fontes externas podem possibilitar inferências. A presença de contagens 1–4 não constitui, isoladamente, comprovação de identificação nem regra automática de supressão.
- CNES identifica estabelecimentos; certos estabelecimentos podem pertencer a pessoas naturais, exigindo interpretação contextual. O campo `aih` contabiliza autorizações hospitalares, não indivíduos únicos; procedimentos não equivalem a pacientes nem demonstram funcionamento efetivo.
- Matrizes SIM distinguem causa básica original, final e menções; diferenças de seleção/codificação não demonstram causalidade administrativa. A geografia por PDR/ES 2024 foi aplicada retrospectivamente à série histórica para comparabilidade.
- A publicação conjunta de conjuntos granulares continua permitindo análises de inferência; pesquisadores devem observar a legislação aplicável e evitar tentativas de identificação de pessoas naturais.

## Condições editoriais

Acesse o [catálogo integral dos 318](CATALOGO_RESULTADOS_318.csv) e a [matriz de 13 originais restaurados](MATRIZ_ABERTURA_INTEGRAL_13.csv). Os hashes dos originais são preservados. Os produtos de terceiros e a geometria cartográfica devem ser creditados segundo [fontes e direitos](FONTES_E_DIREITOS.md). As licenças de terceiros continuam aplicáveis. A comprovação da competência patrimonial para relicenciamento ficou fora do escopo da preparação.

Em 21/11/2026, o pesquisador aprovou a inclusão dos 13 arquivos na edição. A decisão abrangeu o conteúdo científico. A autorização de envio remoto e a competência para relicenciamento têm registros próprios quando formalizadas.
