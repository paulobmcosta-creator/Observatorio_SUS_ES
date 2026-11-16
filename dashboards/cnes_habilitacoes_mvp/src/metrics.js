export const ALL = "Todos";

export const MAP_METRICS = {
  selectedRecords: { label: "Registros de habilitação", short: "registros" },
  distinctEstablishments: { label: "Estabelecimentos distintos", short: "estabelecimentos" },
  distinctQualificationTypes: { label: "Tipos de habilitação", short: "tipos" },
  validationRate: { label: "% de registros validados", short: "% validado" },
};

function uniqueCount(records, field) {
  return new Set(records.map((record) => record[field])).size;
}

export function summarizeRecords(records) {
  const selectedRecords = uniqueCount(records, "chave");
  const validatedRecords = records.filter((record) => record.status === "Validado").length;
  const reviewRecords = records.filter((record) => record.status === "Revisar").length;
  return {
    selectedRecords,
    distinctEstablishments: uniqueCount(records, "cnes"),
    distinctMunicipalities: uniqueCount(records, "municipioCodigo"),
    distinctQualificationTypes: uniqueCount(records, "tipoChave"),
    validatedRecords,
    reviewRecords,
    validationRate: selectedRecords ? (100 * validatedRecords) / selectedRecords : null,
  };
}

export function filterRecords(records, filters) {
  return records.filter(
    (record) =>
      (filters.status === ALL || record.status === filters.status) &&
      (filters.line === ALL || record.linha === filters.line) &&
      (filters.region === ALL || record.regiaoIntermediaria === filters.region) &&
      (filters.municipality === ALL || record.municipioCodigo === filters.municipality),
  );
}

function groupBy(records, field) {
  const groups = new Map();
  records.forEach((record) => {
    const key = record[field];
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  });
  return groups;
}

export function deriveViewModel(data, filters) {
  const selected = filterRecords(data.registros, filters);
  const careGroups = groupBy(selected, "linha");
  const regionGroups = groupBy(selected, "regiaoIntermediaria");
  const municipalityGroups = groupBy(selected, "municipioCodigo");

  const byCareLine = data.dominios.linhas
    .map((name) => ({ name, ...summarizeRecords(careGroups.get(name) ?? []) }))
    .sort((a, b) => b.selectedRecords - a.selectedRecords || a.name.localeCompare(b.name, "pt-BR"));

  const byIntermediateRegion = data.dominios.regioesIntermediarias.map((name) => ({
    name,
    ...summarizeRecords(regionGroups.get(name) ?? []),
  }));

  const byMunicipality = data.municipios.map((municipality) => ({
    ...municipality,
    ...summarizeRecords(municipalityGroups.get(municipality.codigo) ?? []),
  }));

  const ranking = byMunicipality
    .filter((item) => item.selectedRecords > 0)
    .sort(
      (a, b) =>
        b.selectedRecords - a.selectedRecords || a.nome.localeCompare(b.nome, "pt-BR"),
    )
    .slice(0, 6);

  return {
    selected,
    global: summarizeRecords(selected),
    byCareLine,
    byIntermediateRegion,
    byMunicipality,
    ranking,
  };
}

export function metricValue(metrics, metric) {
  if (!Object.hasOwn(MAP_METRICS, metric)) throw new Error(`Métrica de mapa desconhecida: ${metric}`);
  return metrics[metric];
}

export function metricBand(value, metric) {
  if (value === null || value === undefined) return 0;
  if (metric === "validationRate") {
    if (value < 25) return 1;
    if (value < 50) return 2;
    if (value < 75) return 3;
    return 4;
  }
  if (value === 0) return 0;
  if (value <= 2) return 1;
  if (value <= 5) return 2;
  if (value <= 10) return 3;
  return 4;
}

export function mapViewBox(municipalities, fullExtent = false) {
  // Enquadramento visual de subpolígonos M/L/Z gerados pelo pipeline original.
  // Não altera geometrias, filtros ou contagens; ilhas afastadas continuam no SVG.
  const bounds = municipalities.flatMap((m) => (m.path?.match(/M[^M]+/g) ?? []).map((part) => {
    const numbers = (part.match(/-?\d+(?:\.\d+)?/g) ?? []).map(Number);
    const xs = numbers.filter((_, i) => i % 2 === 0);
    const ys = numbers.filter((_, i) => i % 2 === 1);
    return { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) };
  })).filter((b) => Object.values(b).every(Number.isFinite));
  if (!bounds.length) return "0 0 430 560";
  const merge = (a, b) => ({ x0: Math.min(a.x0, b.x0), x1: Math.max(a.x1, b.x1), y0: Math.min(a.y0, b.y0), y1: Math.max(a.y1, b.y1) });
  let b;
  if (fullExtent) b = bounds.reduce(merge);
  else {
    const groups = [];
    for (const item of bounds.sort((a, b) => a.x0 - b.x0)) {
      const last = groups.at(-1);
      if (last && item.x0 <= last.x1 + 0.05) groups[groups.length - 1] = merge(last, item);
      else groups.push(item);
    }
    b = groups.reduce((a, b) => (a.x1 - a.x0) * (a.y1 - a.y0) >= (b.x1 - b.x0) * (b.y1 - b.y0) ? a : b);
  }
  const pad = Math.max(b.x1 - b.x0, b.y1 - b.y0) * 0.04 || 1;
  return `${b.x0 - pad} ${b.y0 - pad} ${b.x1 - b.x0 + 2 * pad} ${b.y1 - b.y0 + 2 * pad}`;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

export function validateDataContract(data) {
  assert(data?.schemaVersion === "2.0.0", "Versão de contrato de dados incompatível.");
  assert(Array.isArray(data.registros), "Contrato inválido: registros ausentes.");
  assert(Array.isArray(data.municipios), "Contrato inválido: municípios ausentes.");
  assert(Array.isArray(data.dominios?.linhas), "Contrato inválido: domínio de linhas ausente.");
  assert(Array.isArray(data.dominios?.regioesIntermediarias), "Contrato inválido: domínio regional ausente.");

  const recordKeys = data.registros.map((record) => record.chave);
  assert(new Set(recordKeys).size === recordKeys.length, "Contrato inválido: chave de registro duplicada.");
  const municipalityCodes = data.municipios.map((municipality) => municipality.codigo);
  assert(new Set(municipalityCodes).size === municipalityCodes.length, "Contrato inválido: município duplicado.");
  const municipalitySet = new Set(municipalityCodes);
  const domain = data.dominios.regioesIntermediarias;
  assert(domain.length > 0 && new Set(domain).size === domain.length && domain.every((v) => typeof v === "string" && v.trim()), "Contrato inválido: domínio regional vazio/duplicado.");
  const municipalityByCode = new Map(data.municipios.map((m) => [m.codigo, m]));
  assert(data.municipios.every((m) => domain.includes(m.regiaoIntermediaria)), "Contrato inválido: município fora do domínio regional.");
  assert(data.registros.every((r) => domain.includes(r.regiaoIntermediaria) && municipalityByCode.get(r.municipioCodigo)?.regiaoIntermediaria === r.regiaoIntermediaria), "Contrato inválido: região do registro divergente do domínio/município.");
  assert(data.registros.every((r) => !r.regiaoSaude) && data.municipios.every((m) => !m.regiaoSaude), "Região de saúde requer novo contrato e fonte validada; não preencher no contrato 2.0.0.");
  assert(
    data.registros.every((record) => municipalitySet.has(record.municipioCodigo)),
    "Contrato inválido: registro sem município no mapa.",
  );
  assert(
    data.registros.every((record) => data.dominios.linhas.includes(record.linha)),
    "Contrato inválido: linha de cuidado desapareceu do domínio.",
  );
  assert(
    data.registros.every((record) => ["Validado", "Revisar"].includes(record.status)),
    "Contrato inválido: status de validação desconhecido.",
  );

  const actual = summarizeRecords(data.registros);
  assert(data.resumoCanonico && typeof data.resumoCanonico === "object", "Resumo canônico obrigatório ausente.");
  assert(Object.keys(actual).sort().join("|") === Object.keys(data.resumoCanonico).sort().join("|"), "Resumo canônico obrigatório incompleto ou com campos desconhecidos.");
  for (const [key, expected] of Object.entries(data.resumoCanonico)) {
    const value = actual[key];
    if (typeof expected === "number" && key === "validationRate") {
      assert(Math.abs(value - expected) < 0.05, `Resumo canônico divergente em ${key}.`);
    } else {
      assert(value === expected, `Resumo canônico divergente em ${key}.`);
    }
  }
  return data;
}

export function exportRecordsCsv(records) {
  const fields = ["competencia", "chave", "cnes", "estabelecimento", "municipioCodigo", "municipio", "regiaoIntermediaria", "regiaoSaude", "linha", "codigoHabilitacao", "tipoHabilitacao", "tipoChave", "status"];
  const cell = (v) => `"${String(v ?? "").replaceAll('"', '""')}"`;
  return [fields.map(cell).join(","), ...records.map((r) => fields.map((f) => cell(r[f])).join(","))].join("\r\n") + "\r\n";
}

export function compareBaseline(view, baseline) {
  const differences = [];
  const compareValue = (path, actual, expected, tolerance = 0) => {
    if (actual === null || Math.abs(actual - expected) > tolerance) {
      differences.push({ path, actual, expected });
    }
  };

  Object.entries(baseline.global).forEach(([key, expected]) => {
    compareValue(`global.${key}`, view.global[key], expected, key === "validationRate" ? 0.05 : 0);
  });

  const lines = new Map(view.byCareLine.map((item) => [item.name, item]));
  Object.entries(baseline.byCareLine).forEach(([name, expected]) => {
    const actual = lines.get(name);
    compareValue(`byCareLine.${name}.validated`, actual?.validatedRecords ?? null, expected.validated);
    compareValue(`byCareLine.${name}.review`, actual?.reviewRecords ?? null, expected.review);
    compareValue(`byCareLine.${name}.total`, actual?.selectedRecords ?? null, expected.total);
  });

  const regions = new Map(view.byIntermediateRegion.map((item) => [item.name, item]));
  Object.entries(baseline.byIntermediateRegion).forEach(([name, expected]) => {
    const actual = regions.get(name);
    compareValue(`byIntermediateRegion.${name}.total`, actual?.selectedRecords ?? null, expected.total);
    compareValue(
      `byIntermediateRegion.${name}.validationRate`,
      actual?.validationRate ?? null,
      expected.validationRate,
      0.05,
    );
  });

  const municipalities = new Map(view.byMunicipality.map((item) => [item.nome, item]));
  Object.entries(baseline.featuredMunicipalities).forEach(([name, expected]) => {
    const actual = municipalities.get(name);
    compareValue(`featuredMunicipalities.${name}.total`, actual?.selectedRecords ?? null, expected.total);
    compareValue(`featuredMunicipalities.${name}.validated`, actual?.validatedRecords ?? null, expected.validated);
    compareValue(
      `featuredMunicipalities.${name}.validationRate`,
      actual?.validationRate ?? null,
      expected.validationRate,
      0.05,
    );
  });

  return differences;
}
