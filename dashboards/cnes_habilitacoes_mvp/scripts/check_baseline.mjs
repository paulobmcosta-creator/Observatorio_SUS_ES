import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ALL, compareBaseline, deriveViewModel, validateDataContract } from "../src/metrics.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const baselinePath = path.resolve(root, process.argv[2] ?? "config/baseline_canonical_202601.json");
const dataPath = path.join(root, "public", "data", "mvp-data.json");
const baseline = JSON.parse(fs.readFileSync(baselinePath, "utf8"));
const data = validateDataContract(JSON.parse(fs.readFileSync(dataPath, "utf8")));
const view = deriveViewModel(data, { status: ALL, line: ALL, region: ALL, municipality: ALL });
const differences = compareBaseline(view, baseline);

const result = {
  baseline: baseline.id,
  status: differences.length === 0 ? "APROVADO" : "REPROVADO",
  differences,
};
console.log(JSON.stringify(result, null, 2));
if (differences.length) process.exitCode = 1;
