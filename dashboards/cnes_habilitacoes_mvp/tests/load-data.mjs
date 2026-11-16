import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ALL, deriveViewModel, validateDataContract } from "../src/metrics.js";

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const data = validateDataContract(
  JSON.parse(fs.readFileSync(path.join(root, "public", "data", "mvp-data.json"), "utf8")),
);
export const allFilters = { status: ALL, line: ALL, region: ALL, municipality: ALL };
export const allView = deriveViewModel(data, allFilters);

export function loadJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}
