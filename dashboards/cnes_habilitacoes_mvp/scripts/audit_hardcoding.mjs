import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const app = fs.readFileSync(path.join(root, "src", "App.jsx"), "utf8");
const metrics = fs.readFileSync(path.join(root, "src", "metrics.js"), "utf8");
const processor = fs.readFileSync(path.join(root, "scripts", "process_data.py"), "utf8");

for (const value of ["501", "238", "304", "197", "220", "263", "102"]) {
  assert.equal(new RegExp(`\\b${value}\\b`).test(app), false, `Valor de baseline ${value} não pode estar no frontend.`);
}
for (const category of ["RUE", "Oncologia", "Nefrologia", "Cardiovascular", "São Mateus"]) {
  assert.equal(app.includes(`\"${category}\"`), false, `Categoria ${category} não pode ser enumerada no componente.`);
}
assert.ok(app.includes("deriveViewModel"), "App deve consumir a camada canônica de métricas.");
assert.equal(app.includes("new Set("), false, "App não deve reimplementar contagens distintas.");
assert.equal(app.includes(".filter((record)"), false, "App não deve reimplementar filtros de registros.");
assert.equal(metrics.includes("deriveViewModel"), true, "Camada canônica ausente.");
assert.equal(processor.includes("cnes_habilitacoes_es_202601.csv"), false, "Nome de arquivo de entrada não pode fixar a competência.");
assert.equal(processor.includes("line_order"), false, "Ordem estática de linhas não permitida.");

console.log(JSON.stringify({ status: "APROVADO", checks: 17 }, null, 2));
