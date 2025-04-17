import os
import pandas as pd
from pipeline.base_pipeline import BasePipeline

class IndicatorPipeline(BasePipeline):
    def __init__(self, file_path, country_ref):
        super().__init__(file_path, country_ref)

    def clean_column_names(self):
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )
        return self

    def detect_label_and_description(self):
        if "indicator_label" not in self.df.columns:
            self.df["indicator_label"] = self.df["indicator_code"]
        if "indicator_description" not in self.df.columns:
            self.df["indicator_description"] = self.df["indicator_label"]
        return self

    def detect_indicator_code(self):
        if "indicator_code" not in self.df.columns:
            candidates = [col for col in self.df.columns if "indicator" in col and "id" in col]
            if candidates:
                self.df.rename(columns={candidates[0]: "indicator_code"}, inplace=True)
            else:
                self.df["indicator_code"] = self._extract_code_from_filename()
        return self

    def standardize_structure(self):
        expected_cols = [
            "iso3", "country_name", "value",
            "indicator_code", "indicator_label", "indicator_description", "nexus_code"
        ]

        filename = os.path.basename(self.file_path)

        if filename == "master_obt.csv":
            print(f"⚠️ Skipping {filename}: this is the master output file.")
            raise ValueError("Master file skipped")

        self.df = self.df.loc[:, ~self.df.columns.duplicated()].copy()

        column_mapping = {
            "economy_iso3": "iso3",
            "economy": "iso3",
            "iso3_code": "iso3",
            "country": "country_name",
            "country_or_area": "country_name",
            "economy_name": "country_name",
            "value": "value",
            "indicator": "indicator_label",
            "indicatorlabel": "indicator_label",
            "indicator_id": "indicator_code",
            "indicatorid": "indicator_code"
        }

        for old, new in column_mapping.items():
            if old in self.df.columns and new not in self.df.columns:
                self.df.rename(columns={old: new}, inplace=True)

        if "indicator_code" not in self.df.columns:
            self.df["indicator_code"] = self._extract_code_from_filename()
        if "indicator_label" not in self.df.columns:
            self.df["indicator_label"] = self.df["indicator_code"]
        if "indicator_description" not in self.df.columns:
            self.df["indicator_description"] = self.df["indicator_label"]

        if "country_name" in self.df.columns and "iso3" in self.df.columns:
            self.df.drop(columns=["country_name"], inplace=True)

        if "country_name" not in self.df.columns:
            ref = self.country_ref[["iso3", "Country or Area"]].rename(columns={"Country or Area": "country_name"})
            self.df = self.df.merge(ref, on="iso3", how="left")

        # ✅ Add nexus_code based on file name
        self.df["nexus_code"] = self._extract_code_from_filename()

        if set(expected_cols).issubset(set(self.df.columns)):
            self.df = self.df[expected_cols].copy()
            return self

        raise ValueError(f"{filename}: columns don't match expected structure")

    def _extract_code_from_filename(self):
        base = os.path.basename(self.file_path)
        return base.replace(".csv", "").replace(".xlsx", "").replace(".xls", "")
