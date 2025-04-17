import pandas as pd
import os

class BasePipeline:
    def __init__(self, file_path, country_ref):
        self.file_path = file_path
        self.country_ref = country_ref
        self.df = None
#dictanory for the function
    def load_data(self):
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == ".csv":
            self.df = pd.read_csv(self.file_path, low_memory=False)
        elif ext in [".xlsx", ".xls"]:
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        return self

    def detect_country_column(self):
        possible_columns = [
            "iso3", "economy", "country_code", "Country",
            "Country or Area", "country", "Economy ISO3", "country_name", "iso3_code", "m49"
        ]
        for col in possible_columns:
            if col in self.df.columns:
                self.df.rename(columns={col: "iso3"}, inplace=True)
                break
        if "iso3" not in self.df.columns:
            raise ValueError("Country column not found")
        return self

    def detect_value_column(self):
        possible_value_cols = ["value", "Value", "score", "estimate"]
        for col in possible_value_cols:
            if col in self.df.columns:
                self.df.rename(columns={col: "value"}, inplace=True)
                break
        if "value" not in self.df.columns:
            for col in self.df.columns:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df.rename(columns={col: "value"}, inplace=True)
                    break
        if "value" not in self.df.columns:
            raise ValueError("Value column not found")
        return self

    def merge_country_name(self):
        if "country_name" not in self.df.columns:
            ref = self.country_ref[["iso3", "Country or Area"]].rename(columns={"Country or Area": "country_name"})
            self.df = self.df.merge(ref, on="iso3", how="left")
        return self

    def standardize_columns(self):
        rename_map = {
            "Indicator": "indicator_label",
            "IndicatorLabel": "indicator_label",
            "Indicator ID": "indicator_code",
            "IndicatorID": "indicator_code"
        }
        self.df.rename(columns=rename_map, inplace=True)
        return self

    def clean_duplicates(self):
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]
        return self
