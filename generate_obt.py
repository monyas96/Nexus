import os
import pandas as pd
from pipeline.indicator_pipeline import IndicatorPipeline

# ----------------------------
# CONFIGURATION
# ----------------------------
OUTPUTS_DIR = "outputs"
COUNTRY_REF_PATH = "data/iso3_country_reference.csv"
MASTER_OBT_PATH = "outputs/master_obt.csv"
SUPPORTED_FORMATS = (".csv", ".xlsx", ".xls")


# ----------------------------
# PIPELINE MANAGER
# ----------------------------

class PipelineManager:
    def __init__(self, data_dir, country_ref_file):
        self.data_dir = data_dir
        self.country_ref = pd.read_csv(country_ref_file)
        self.indicator_files = self._list_files()
        self.failed_files = []
        self.cleaned_dfs = []
        self.skipped_files = []

    def _list_files(self):
        print("🔍 Scanning output folder for files...")
        files = [f for f in os.listdir(self.data_dir) if f.endswith(SUPPORTED_FORMATS)]
        print(f"✅ Found {len(files)} files.")
        return files

    def process_all_files(self):
        for file in self.indicator_files:
            full_path = os.path.join(self.data_dir, file)
            print(f"⚙️ Processing: {file}")
            try:
                pipeline = IndicatorPipeline(full_path, self.country_ref)
                pipeline.load_data()\
                        .clean_duplicates()\
                        .detect_country_column()\
                        .detect_value_column()\
                        .merge_country_name()\
                        .standardize_columns()\
                        .detect_indicator_code()\
                        .detect_label_and_description()\
                        .standardize_structure()

                self.cleaned_dfs.append(pipeline.df)
                print(f"✅ Finished: {file}")

            except ValueError as ve:
                # Specifically catch column structure mismatches or master file skip
                if "columns don't match" in str(ve) or "Master file skipped" in str(ve):
                    print(f"⚠️ Skipping {file}: {ve}")
                    self.skipped_files.append(file)
                else:
                    print(f"❌ Failed to process {file}: {ve}")
                    self.failed_files.append((file, str(ve)))

            except Exception as e:
                print(f"❌ Failed to process {file}: {e}")
                self.failed_files.append((file, str(e)))

    def export_master_table(self, output_path):
        if not self.cleaned_dfs:
            print("🚫 No dataframes to export. All files may have failed or been skipped.")
            return

        print("📦 Combining all cleaned data...")
        master_df = pd.concat(self.cleaned_dfs, ignore_index=True)
        master_df.to_csv(output_path, index=False)
        print(f"✅ Master OBT saved to: {output_path}")

    def run(self, output_path):
        self.process_all_files()
        self.export_master_table(output_path)
        self._print_summary()

    def _print_summary(self):
        print("\n📊 Pipeline Summary")
        print("-------------------")
        print(f"Total files scanned: {len(self.indicator_files)}")
        print(f"✅ Successfully processed: {len(self.cleaned_dfs)}")
        print(f"⚠️ Skipped due to bad structure: {len(self.skipped_files)}")
        print(f"❌ Failed to process: {len(self.failed_files)}")

        if self.failed_files:
            print("\n❗ Failed Files:")
            for file, error in self.failed_files:
                print(f"- {file}: {error}")

        if self.skipped_files:
            print("\n⚠️ Skipped Files (structural mismatch):")
            for file in self.skipped_files:
                print(f"- {file}")


# ----------------------------
# EXECUTION
# ----------------------------

if __name__ == "__main__":
    print("🚀 Starting OBT generation pipeline...\n")
    manager = PipelineManager(OUTPUTS_DIR, COUNTRY_REF_PATH)
    manager.run(MASTER_OBT_PATH)
