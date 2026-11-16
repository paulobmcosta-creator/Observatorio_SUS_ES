from __future__ import annotations

from typing import Any

import pandas as pd


def validation_rate(validated: int, total: int) -> float | None:
    return round(100 * validated / total, 1) if total else None


def _group_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    total = int(frame["chave_registro"].nunique())
    validated = int((frame["situacao_validacao"] == "Validado").sum())
    review = int((frame["situacao_validacao"] == "Revisar").sum())
    return {
        "selectedRecords": total,
        "distinctEstablishments": int(frame["cnes"].nunique()),
        "distinctMunicipalities": int(frame["cod_municipio_ibge_7"].nunique()),
        "distinctQualificationTypes": int(frame["chave_tipo_habilitacao"].nunique()),
        "validatedRecords": validated,
        "reviewRecords": review,
        "validationRate": validation_rate(validated, total),
    }


def derive_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    if frame["chave_registro"].duplicated().any():
        duplicated = frame.loc[frame["chave_registro"].duplicated(), "chave_registro"].iloc[0]
        raise ValueError(f"Duplicate record key in canonical metric input: {duplicated}")

    global_metrics = _group_metrics(frame)

    by_care_line: dict[str, Any] = {}
    for name, subset in frame.groupby("linha_cuidado", sort=True, dropna=False):
        metrics = _group_metrics(subset)
        by_care_line[str(name)] = {
            **metrics,
            "validated": metrics["validatedRecords"],
            "review": metrics["reviewRecords"],
            "total": metrics["selectedRecords"],
        }

    by_region: dict[str, Any] = {}
    for name, subset in frame.groupby("regiao_intermediaria_ibge", sort=True, dropna=False):
        by_region[str(name)] = {**_group_metrics(subset), "total": int(len(subset))}

    by_municipality: dict[str, Any] = {}
    for code, subset in frame.groupby("cod_municipio_ibge_7", sort=True, dropna=False):
        metrics = _group_metrics(subset)
        by_municipality[str(code)] = {
            **metrics,
            "code": str(code),
            "name": str(subset["municipio_ibge"].iloc[0]),
            "intermediateRegion": str(subset["regiao_intermediaria_ibge"].iloc[0]),
            "total": metrics["selectedRecords"],
            "validated": metrics["validatedRecords"],
            "review": metrics["reviewRecords"],
        }

    return {
        "global": global_metrics,
        "byCareLine": by_care_line,
        "byIntermediateRegion": by_region,
        "byMunicipality": by_municipality,
    }
