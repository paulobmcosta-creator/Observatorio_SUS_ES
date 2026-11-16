import assert from "node:assert/strict";
import test from "node:test";
import { ALL, deriveViewModel } from "../src/metrics.js";
import { data } from "./load-data.mjs";

const municipalityCode = new Map(data.municipios.map((item) => [item.nome, item.codigo]));
const cases = [
  ["apenas Validado", { status: "Validado" }, [304, 205, 78, 32, 304, 0]],
  ["apenas Revisar", { status: "Revisar" }, [197, 65, 21, 59, 0, 197]],
  ["linha RUE", { line: "RUE" }, [220, 153, 78, 21, 184, 36]],
  ["linha Oncologia", { line: "Oncologia" }, [41, 23, 8, 14, 4, 37]],
  ["município Vitória", { municipality: municipalityCode.get("Vitória") }, [102, 31, 1, 54, 45, 57]],
  ["região São Mateus", { region: "São Mateus" }, [68, 36, 15, 27, 49, 19]],
  ["RUE + Validado", { line: "RUE", status: "Validado" }, [184, 147, 78, 17, 184, 0]],
  ["São Mateus + RUE", { region: "São Mateus", line: "RUE" }, [39, 26, 15, 8, 33, 6]],
  ["Vitória município + Oncologia", { municipality: municipalityCode.get("Vitória"), line: "Oncologia" }, [21, 10, 1, 11, 1, 20]],
  ["Vitória região + UTI", { region: "Vitória", line: "UTI / cuidado crítico" }, [38, 20, 7, 9, 22, 16]],
];

for (const [name, partialFilters, expected] of cases) {
  test(`filtro: ${name}`, () => {
    const view = deriveViewModel(data, {
      status: ALL,
      line: ALL,
      region: ALL,
      municipality: ALL,
      ...partialFilters,
    });
    assert.deepEqual(
      [
        view.global.selectedRecords,
        view.global.distinctEstablishments,
        view.global.distinctMunicipalities,
        view.global.distinctQualificationTypes,
        view.global.validatedRecords,
        view.global.reviewRecords,
      ],
      expected,
    );
    assert.equal(view.selected.length, view.global.selectedRecords);
    assert.equal(view.byCareLine.reduce((sum, item) => sum + item.selectedRecords, 0), view.global.selectedRecords);
    assert.equal(view.byIntermediateRegion.reduce((sum, item) => sum + item.selectedRecords, 0), view.global.selectedRecords);
    assert.equal(view.byMunicipality.reduce((sum, item) => sum + item.selectedRecords, 0), view.global.selectedRecords);
    for (let index = 1; index < view.ranking.length; index += 1) {
      assert.ok(view.ranking[index - 1].selectedRecords >= view.ranking[index].selectedRecords);
    }
  });
}
