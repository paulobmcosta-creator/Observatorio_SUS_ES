import assert from "node:assert/strict";
import test from "node:test";
import { compareBaseline } from "../src/metrics.js";
import { allView, data, loadJson } from "./load-data.mjs";

test("baseline canônica 202601 reconcilia com as 501 chaves fornecidas", () => {
  const baseline = loadJson("config/baseline_canonical_202601.json");
  assert.deepEqual(compareBaseline(allView, baseline), []);
});

test("totais globais e identidades de validação fecham", () => {
  assert.deepEqual({ ...allView.global, validationRate: undefined }, {
    selectedRecords: 501,
    distinctEstablishments: 238,
    distinctMunicipalities: 78,
    distinctQualificationTypes: 91,
    validatedRecords: 304,
    reviewRecords: 197,
    validationRate: undefined,
  });
  assert.ok(Math.abs(allView.global.validationRate - 60.7) < 0.05);
  assert.equal(allView.global.validatedRecords + allView.global.reviewRecords, 501);
});

test("linhas, regiões e municípios particionam o mesmo conjunto", () => {
  assert.equal(allView.byCareLine.reduce((sum, item) => sum + item.selectedRecords, 0), 501);
  assert.equal(allView.byCareLine.reduce((sum, item) => sum + item.validatedRecords, 0), 304);
  assert.equal(allView.byCareLine.reduce((sum, item) => sum + item.reviewRecords, 0), 197);
  assert.equal(allView.byIntermediateRegion.reduce((sum, item) => sum + item.selectedRecords, 0), 501);
  assert.equal(allView.byMunicipality.reduce((sum, item) => sum + item.selectedRecords, 0), 501);
});

test("join do mapa contém 78 municípios únicos e nenhuma perda", () => {
  assert.equal(data.municipios.length, 78);
  assert.equal(new Set(data.municipios.map((item) => item.codigo)).size, 78);
  assert.ok(data.municipios.every((item) => item.path.startsWith("M ")));
  const mapCodes = new Set(data.municipios.map((item) => item.codigo));
  assert.ok(data.registros.every((record) => mapCodes.has(record.municipioCodigo)));
});

test("baseline agregada solicitada falha de modo explícito, sem alterar registros", () => {
  const requested = loadJson("config/baseline_requested_202601.json");
  const differences = compareBaseline(allView, requested);
  assert.ok(differences.length >= 20);
  assert.ok(differences.some((item) => item.path === "byCareLine.RUE.total"));
  assert.ok(differences.some((item) => item.path === "byIntermediateRegion.Vitória.total"));
  assert.ok(differences.some((item) => item.path === "featuredMunicipalities.Vitória.total"));
});
