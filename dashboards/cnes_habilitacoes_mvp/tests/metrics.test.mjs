import assert from "node:assert/strict";
import test from "node:test";
import { summarizeRecords } from "../src/metrics.js";

test("subconjunto vazio preserva zero e percentual NA", () => {
  assert.deepEqual(summarizeRecords([]), {
    selectedRecords: 0,
    distinctEstablishments: 0,
    distinctMunicipalities: 0,
    distinctQualificationTypes: 0,
    validatedRecords: 0,
    reviewRecords: 0,
    validationRate: null,
  });
});

test("percentual usa registros como denominador", () => {
  const records = [
    { chave: "1", cnes: "A", municipioCodigo: "M", tipoChave: "T", status: "Validado" },
    { chave: "2", cnes: "A", municipioCodigo: "M", tipoChave: "U", status: "Revisar" },
  ];
  const result = summarizeRecords(records);
  assert.equal(result.selectedRecords, 2);
  assert.equal(result.distinctEstablishments, 1);
  assert.equal(result.validationRate, 50);
});
