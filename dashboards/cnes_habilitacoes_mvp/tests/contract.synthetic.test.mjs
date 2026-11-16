import assert from "node:assert/strict";
import test from "node:test";
import { validateDataContract, summarizeRecords, deriveViewModel, ALL, exportRecordsCsv, metricBand, mapViewBox } from "../src/metrics.js";

function fixture() {
  const registros = [{ competencia: "202601", chave: "001", cnes: "0000123", municipioCodigo: "3200102", municipio: "Fixture", regiaoIntermediaria: "Região fixture", regiaoSaude: "", linha: "RUE", tipoChave: "cod|tipo", status: "Revisar" }];
  return { schemaVersion: "2.0.0", registros, municipios: [{ codigo: "3200102", regiaoIntermediaria: "Região fixture", regiaoSaude: "" }], dominios: { linhas: ["RUE"], regioesIntermediarias: ["Região fixture"] }, resumoCanonico: summarizeRecords(registros) };
}
test("resumo canônico é obrigatório e completo", () => {
  const d = fixture(); delete d.resumoCanonico; assert.throws(() => validateDataContract(d), /obrigatório/);
  const e = fixture(); delete e.resumoCanonico.selectedRecords; assert.throws(() => validateDataContract(e), /incompleto/);
});
test("domínio regional cobre registro e município, sem converter em região de saúde", () => {
  const d = fixture(); d.registros[0].regiaoIntermediaria = "Inventada"; assert.throws(() => validateDataContract(d), /região do registro/);
  const e = fixture(); e.registros[0].regiaoSaude = "Não homologada"; assert.throws(() => validateDataContract(e), /Região de saúde/);
});
test("resumo divergente é recusado antes de exibir cartões", () => {
  const d = fixture(); d.resumoCanonico.distinctEstablishments = 99; assert.throws(() => validateDataContract(d), /divergente/);
});
test("export usa exatamente o subconjunto e preserva identificadores textuais", () => {
  const d = validateDataContract(fixture());
  const v = deriveViewModel(d, { status: "Revisar", line: ALL, region: ALL, municipality: ALL });
  assert.equal(v.global.selectedRecords, 1); assert.match(exportRecordsCsv(v.selected), /"0000123"/);
  const vazio = deriveViewModel(d, { status: "Validado", line: ALL, region: ALL, municipality: ALL });
  assert.equal(vazio.global.validationRate, null); assert.equal(exportRecordsCsv(vazio.selected).split("\r\n").length, 2);
});
test("zero por cento com registros tem faixa própria e não significa ausência de registro", () => {
  assert.equal(metricBand(0, "validationRate"), 1);
  assert.equal(metricBand(null, "validationRate"), 0);
  assert.equal(metricBand(0, "selectedRecords"), 0);
});
test("enquadramento continental conserva dados e permite extensão completa", () => {
  const municipios = [{ path: "M 0 0 L 20 0 L 20 30 Z M 100 0 L 101 0 L 101 1 Z" }];
  const antes = JSON.stringify(municipios);
  assert.ok(Number(mapViewBox(municipios).split(" ")[2]) < 30);
  assert.ok(Number(mapViewBox(municipios, true).split(" ")[2]) > 100);
  assert.equal(JSON.stringify(municipios), antes);
});
