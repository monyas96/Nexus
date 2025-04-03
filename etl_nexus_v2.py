import pandas as pd
import wbgapi as wb
import re
import openpyxl
import xlrd

#WB-PEFA 
#4.1.1.1
#4.1.1.2

# Input: Load the ISO3 country reference list to filter African countries
def load_iso3_country_reference(file_path):
    """Load the ISO3 country reference file to filter African countries."""
    iso3_reference_df = pd.read_csv(file_path)
    # Filter rows where the 'Region Name' column is 'Africa'
    africa_iso3 = iso3_reference_df[iso3_reference_df['Region Name'] == 'Africa'][['iso3', 'Country or Area']]
    return africa_iso3

# Input: Load PEFA data from the uploaded Excel file
def load_pefa_data(file_path):
    """Load PEFA data from an Excel file."""
    pefa_df = pd.read_excel(file_path)
    pefa_df.columns = pefa_df.columns.str.strip() 
    return pefa_df

# Process: Merge PEFA data with African countries data
def process_pefa_data(pefa_df, africa_iso3, indicator_label):
    """Process PEFA data to filter African countries and transform it."""
    # Filter by Indicator (based on the indicator label provided)
    pefa_df = pefa_df[pefa_df['Indicator'] == indicator_label]
    
    # Convert the list of African countries to a DataFrame
    africa_iso3_df = pd.DataFrame(africa_iso3, columns=['iso3', 'Country'])
    
    # Ensure 'Economy ISO3' and 'iso3' columns are string types
    pefa_df['Economy ISO3'] = pefa_df['Economy ISO3'].astype(str).str.strip()  # Remove extra spaces
    africa_iso3_df['iso3'] = africa_iso3_df['iso3'].astype(str).str.strip()  # Remove extra spaces
    
    # Merge the PEFA data with the African countries' DataFrame on 'Economy ISO3' and 'iso3'
    df = pd.merge(pefa_df, africa_iso3_df, how='inner', left_on='Economy ISO3', right_on='iso3')

    # Melt the DataFrame from wide to long format (years as rows)
    df = pd.melt(df, id_vars=['Economy Name', 'Economy ISO3', 'Indicator ID', 'Indicator'], 
                 var_name='Year', value_name='Value')

    # Add the indicator metadata (using the provided indicator label)
    df['IndicatorLabel'] = df['Indicator']

    # Reorder columns to match the desired output structure
    df = df[['Economy ISO3', 'Economy Name', 'Year', 'Value', 'Indicator ID', 'IndicatorLabel']]
    return df

# Output: Save processed data to a CSV file with specific file names
def save_to_csv(df, file_name, output_dir):
    """Save the cleaned data to a CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, file_name), index=False)
    print(f"Cleaned data saved to '{file_name}'")

# Main ETL function
def etl_process(indicator_label, input_iso3_file, input_pefa_file, output_dir, file_name):
    """Run the ETL process: input, process, output."""
    # Input: Load the ISO3 reference and PEFA data
    africa_iso3 = load_iso3_country_reference(input_iso3_file)
    pefa_df = load_pefa_data(input_pefa_file)

    # Process: Merge PEFA data with Africa ISO3 and transform
    processed_df = process_pefa_data(pefa_df, africa_iso3, indicator_label)

    # Output: Save the processed data to a CSV file with a specific name
    save_to_csv(processed_df, file_name, output_dir)

# Example usage of the function:
indicators = [
    ('PEFA: PI-1 Aggregate expenditure out-turn', 'indicator_4_1_1_1_WB_PEFA.csv'),
    ('PEFA: PI-3 Revenue outturn', 'indicator_4_1_1_2_WB_PEFA.csv'),
    ('PEFA: PI-2 Expenditure composition outturn', 'indicator_4_1_1_3_WB_PEFA.csv')
]  # PEFA indicator labels and their corresponding output file names
input_iso3_file = 'data/iso3_country_reference.csv'  # Path to the ISO3 reference file
input_pefa_file = 'data/WB-PEFA.xlsx'  # Path to the PEFA data Excel file
output_dir = 'outputs'  # Directory to save the output CSV files

# Step: Process each indicator and save with the specified names
for indicator_label, file_name in indicators:
    etl_process(indicator_label, input_iso3_file, input_pefa_file, output_dir, file_name)

# usage of the function:
indicators = [
    ('WB.PEFA.PI-2016-03', 'PEFA: PI-3 Revenue outturn'),
    ('WB.PEFA.PI-2016-01', 'PEFA: PI-1 Aggregate expenditure out-turn'),
    ('WB.PEFA.PI-2016-02', 'PEFA: PI-2 Expenditure composition outturn')
]  # PEFA indicator codes and their corresponding labels
input_iso3_file = 'data/iso3_country_reference.csv'  # Path to the ISO3 reference file
input_pefa_file = 'data/WB-PEFA.xlsx'  # Path to the PEFA data Excel file
output_dir = 'outputs'  # Directory to save the output CSV files

# Step: Process each indicator
for indicator_code, indicator_label in indicators:
    etl_process(indicator_code, indicator_label, input_iso3_file, input_pefa_file, output_dir)
######################################################################################
# WDI indicator 4.2.1.1: DONE!

def get_4_2_1_1():
    indicator4_2_1_1 = wb.data.DataFrame('GC.TAX.TOTL.GD.ZS', wb.region.members('AFR'))
    return indicator4_2_1_1

indicator_4_2_1_1_df = get_4_2_1_1()
indicator_4_2_1_1_df = indicator_4_2_1_1_df.reset_index()

long_df = pd.melt(indicator_4_2_1_1_df, id_vars=['economy'], var_name='Year', value_name='Value')
long_df['Year'] = long_df['Year'].str.replace('YR', '')
long_df['Indicator'] = 'Tax Revenue as Percentage of GDP'
long_df['IndicatorID'] = 'GC.TAX.TOTL.GD.ZS'

output_dir = 'outputs'
os.makedirs(output_dir, exist_ok=True)

long_df.to_csv(os.path.join(output_dir, 'indicator_4_2_1_1_WB_WDI.csv'), index=False)
########################################################################################
#ATAF: indicator 4.2.1.2: DONE!

# Load the Excel file
file_path = 'data/ATO_RAW_ATAF 2.xlsx'  # This is relative path from my 
xls = pd.ExcelFile(file_path, engine='openpyxl')

# Load the first sheet into a DataFrame
df = pd.read_excel(xls, 'Sheet1')

# Initialize lists to store cleaned data
cleaned_data = []

# Temporary storage for theme and topic
current_theme = None
current_topic = None

# Loop through the DataFrame to organize the data based on themes, topics, and indicators
for index, row in df.iterrows():
    first_col_value = row[0]
    
    # Check if the row indicates a new Theme
    if isinstance(first_col_value, str) and first_col_value.startswith('Theme'):
        current_theme = first_col_value.strip()
        current_topic = None  # Reset topic when a new theme starts
    
    # Check if the row indicates a new Topic
    elif pd.notna(first_col_value) and first_col_value != 'Year':
        current_topic = first_col_value.strip()
    
    # If the row indicates 'Year', extract country and year, then collect indicators
    elif first_col_value == 'Year':
        for col_idx in range(1, len(row)):
            if pd.notna(row[col_idx]):
                country_year = row[col_idx]
                if isinstance(country_year, str) and len(country_year.split()) == 2:
                    country, year = country_year.split()
                    
                    # Collect indicators until the next 'Theme' row
                    indicator_idx = index + 1
                    while indicator_idx < len(df) and not (
                        isinstance(df.iloc[indicator_idx, 0], str) and df.iloc[indicator_idx, 0].startswith('Theme')
                    ):
                        indicator_name = df.iloc[indicator_idx, 0]
                        indicator_value = df.iloc[indicator_idx, col_idx]
                        
                        # Add cleaned data to the list if the indicator name is not NaN
                        if pd.notna(indicator_name):
                            cleaned_data.append({
                                'Theme': current_theme,
                                'Topic': current_topic,
                                'Country': country,
                                'Year': year,
                                'Indicator': indicator_name.strip(),
                                'Value': indicator_value
                            })
                        indicator_idx += 1

# Create a cleaned DataFrame from the collected data
cleaned_df = pd.DataFrame(cleaned_data)

# Filter for 'Domestic revenue from large taxpayers' and indicators containing 'Taxpayers'
filtered_df = cleaned_df[(cleaned_df['Indicator'].str.contains('Domestic revenue from large taxpayers', case=False)) |
                         (cleaned_df['Indicator'].str.contains('Taxpayers', case=False))]

# Display the first few rows of the cleaned DataFrame
print(filtered_df.head())

# Save the filtered DataFrame to a CSV file
filtered_df.to_csv('outputs/indicator_4_2_1_2_ATAF.csv', index=False)
############################################################################################
# USAID indicator 4.2.2.1a  DONE!
# Define the function to get the indicator
usaid_df = pd.read_excel('data/USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
iso3_reference_df = pd.read_csv('data/iso3_country_reference.csv')
africa_iso3_df = iso3_reference_df[iso3_reference_df['Region Name'] == 'Africa']
usaid_df = usaid_df[usaid_df['country_name'].isin(africa_iso3_df['Country or Area'])]
indicator_4_2_2_1a = usaid_df[usaid_df['country_id'].notna()][['country_id', 'country_name', 'year', 'Tax effort (ratio) [tax_eff]']]
indicator_4_2_2_1a = indicator_4_2_2_1a.rename(columns={'Tax effort (ratio) [tax_eff]': 'Value'})
indicator_4_2_2_1a['Indicator'] = 'Tax effort (ratio)'
indicator_4_2_2_1a = indicator_4_2_2_1a[['country_name', 'year', 'Indicator', 'Value']]
indicator_4_2_2_1a.to_csv('outputs/indicator_4_2_2_1a_USAID.csv', index=False)
#World Bank Revenue Dashboard
#4_2_2_1b it has gap cpacity and buoyancy
file_path = 'data/WB_TAX CPACITY AND GAP.csv'
df = pd.read_csv(file_path)
# Define the function to reshape the dataset
def reshape_tax_data(df):
    # Filter for relevant indicators: Buoyancy, Capacity, and Gap
    indicators = ['Buoyancy', 'Capacity', 'Gap']
    reshaped_data = []

    for indicator in indicators:
        # Extract columns that contain the indicator name
        indicator_columns = [col for col in df.columns if indicator in col]
        for col in indicator_columns:
            # Extract the main indicator name and unit if available
            main_indicator = df['indicator name'].iloc[0] if 'indicator name' in df.columns else 'Unknown'
            unit = df['indicator unit'].iloc[0] if 'indicator unit' in df.columns else 'Unknown'
            reshaped_data.append(
                df[['iso3_code', 'Year']]  # Keep common columns
                .assign(Indicator=f"{main_indicator} - {unit} - {indicator}",  # Indicator name with unit and type
                        Value=df[col])  # Indicator value
            )

    reshaped_df = pd.concat(reshaped_data)
    return reshaped_df[['iso3_code', 'Year', 'Indicator', 'Value']]

# Reshape the data
indicator4_2_2_1b = reshape_tax_data(df)

# Save the reshaped DataFrame to a CSV file
indicator4_2_2_1b.to_csv('outputs/indicator_4_2_2_1b_WB_TAXCPA&GAP.csv', index=False)

####################################################################################
#OSAA
# indicator 4.3.1.1
# Define the function to get the indicator
def get_4_3_1_1(output_dir='outputs'):

    # Get market cap and GDP data
    market_cap = wb.data.DataFrame('CM.MKT.LCAP.CD', wb.region.members('AFR'))
    gdp = wb.data.DataFrame('NY.GDP.MKTP.CD', wb.region.members('AFR'))

    # Calculate the indicator (Market capitalization / GDP * 100)
    indicator4_3_1_1 = (market_cap / gdp) * 100
    indicator4_3_1_1 = indicator4_3_1_1.reset_index()
    indicator4_3_1_1_long = pd.melt(indicator4_3_1_1, id_vars=['economy'], var_name='year', value_name='value')
    indicator4_3_1_1_long['year'] = indicator4_3_1_1_long['year'].str.extract(r'(\d{4})')
    indicator4_3_1_1_long['indicator description'] = 'Market capitalization of listed domestic companies (current US$) divided by GDP (current US$)'
    indicator4_3_1_1_long['indicator code'] = 'CM.MKT.LCAP.CD / NY.GDP.MKTP.CD'
    indicator4_3_1_1_long['Indicator label'] = 'Market capitalization in USD as percentage of GDP'
    indicator4_3_1_1_long = indicator4_3_1_1_long.rename(columns={'economy': 'iso3'})
    indicator4_3_1_1_long = indicator4_3_1_1_long[['iso3', 'year', 'indicator description', 'indicator code', 'Indicator label', 'value']]
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'indicator_4_3_1_1_OSAA.csv')
    indicator4_3_1_1_long.to_csv(file_path, index=False)
    return indicator4_3_1_1_long
get_4_3_1_1()

#WB - WDI
#indicator 4_3_1_2
# Call the function and save the data
def get_4_3_1_2(output_dir='outputs'):
    indicator4_3_1_2 = wb.data.DataFrame('DT.NFL.BOND.CD', wb.region.members('AFR')).reset_index()

    # Convert to long format
    indicator4_3_1_2_long = pd.melt(indicator4_3_1_2, id_vars=['economy'], var_name='year', value_name='value')

    # Extract year value from the 'year' column
    indicator4_3_1_2_long['year'] = indicator4_3_1_2_long['year'].str.extract(r'(\d{4})')

    # Add indicator description and code
    indicator4_3_1_2_long['indicator description'] = 'Portfolio investment, bonds (PPG + PNG) (NFL, current US$)'
    indicator4_3_1_2_long['indicator code'] = 'DT.NFL.BOND.CD'
    indicator4_3_1_2_long = indicator4_3_1_2_long.rename(columns={'economy': 'iso3'})
    indicator4_3_1_2_long = indicator4_3_1_2_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'indicator_4_3_1_2_WB_WDI.csv')
    indicator4_3_1_2_long.to_csv(file_path, index=False)
    print(f"Indicator data saved to '{file_path}'")
    return indicator4_3_1_2_long
get_4_3_1_2(output_dir='outputs')

#OSAA
# indicator 4.3.1.3
# Define the function to get the indicator
def get_4_3_1_3(output_dir='outputs'):
    # Get reserves and debt
    reserves = wb.data.DataFrame('BN.RES.INCL.CD', wb.region.members('AFR'))
    debt = wb.data.DataFrame('DT.DOD.DSTC.CD', wb.region.members('AFR'))

    # Calculate the indicator
    indicator4_3_1_3 = reserves / debt
    indicator4_3_1_3 = indicator4_3_1_3.reset_index()

    # Make long format
    indicator4_3_1_3_long = pd.melt(indicator4_3_1_3, id_vars=['economy'], var_name='year', value_name='value')

    # Extract year value
    indicator4_3_1_3_long['year'] = indicator4_3_1_3_long['year'].str.extract(r'(\d{4})')

    # Add indicator code and description
    indicator4_3_1_3_long['indicator description'] = 'Reserves and related items (BoP, current US$) divided by External debt stocks, short-term (DOD, current US$)'
    indicator4_3_1_3_long['indicator code'] = 'BN.RES.INCL.CD / DT.DOD.DSTC.CD'

    # Add the new indicator column
    indicator4_3_1_3_long['Indicator label'] = 'Adequacy of International Reserves'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_3_long = indicator4_3_1_3_long.rename(columns={'economy': 'iso3'})

    # Reorder columns
    indicator4_3_1_3_long = indicator4_3_1_3_long[['iso3', 'year', 'indicator description', 'indicator code', 'Indicator label', 'value']]

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the resulting DataFrame to CSV
    file_path = os.path.join(output_dir, 'indicator_4_3_1_3_OSAA.csv')
    indicator4_3_1_3_long.to_csv(file_path, index=False)
    print(f"Indicator data saved to '{file_path}'")

    return indicator4_3_1_3_long

# Call the function and save the data
get_4_3_1_3(output_dir='outputs')


#OSAA
# indicator 4.3.2.1
def get_4_3_2_1(output_dir='outputs'):

    capital_to_assets = wb.data.DataFrame('FB.BNK.CAPA.ZS', wb.region.members('AFR'))
    liquid_reserves_to_assets = wb.data.DataFrame('FD.RES.LIQU.AS.ZS', wb.region.members('AFR'))
    domestic_credit = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR')) / 100

    def min_max_normalize(df):
        return (df - df.min()) / (df.max() - df.min())

    capital_to_assets = min_max_normalize(capital_to_assets) * 0.4
    liquid_reserves_to_assets = min_max_normalize(liquid_reserves_to_assets) * 0.3
    domestic_credit = min_max_normalize(domestic_credit) * 0.3
    indicator4_3_2_1 = (capital_to_assets + liquid_reserves_to_assets + domestic_credit)
    indicator4_3_2_1 = indicator4_3_2_1.reset_index()

    indicator4_3_2_1_long = pd.melt(indicator4_3_2_1, id_vars=['economy'], var_name='year', value_name='value')
    indicator4_3_2_1_long['year'] = indicator4_3_2_1_long['year'].str.extract(r'(\d{4})')

    indicator4_3_2_1_long['indicator description'] = '(0.4 * Bank capital to assets ratio (%)) + (0.3 * Bank liquid reserves to bank assets ratio (%)) + (0.3 * Domestic credit provided by financial sector (% of GDP))'
    indicator4_3_2_1_long['indicator code'] = '(0.4 * FB.BNK.CAPA.ZS) + (0.3 * FD.RES.LIQU.AS.ZS) + (0.3 * FS.AST.DOMS.GD.ZS)'

    indicator4_3_2_1_long['Indicator label'] = 'Banking Sector Development Index'

    indicator4_3_2_1_long = indicator4_3_2_1_long.rename(columns={'economy': 'iso3'})
    indicator4_3_2_1_long = indicator4_3_2_1_long[['iso3', 'year', 'indicator description', 'indicator code', 'Indicator label', 'value']]

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'indicator_4_3_2_1_OSAA.csv')
    indicator4_3_2_1_long.to_csv(file_path, index=False)

    return indicator4_3_2_1_long

get_4_3_2_1(output_dir='outputs')

#WB - WDI
# indicator 4.3.2.2
def get_4_3_2_2(output_dir='outputs'):
    indicator4_3_2_2 = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR')).reset_index()

    indicator4_3_2_2_long = pd.melt(indicator4_3_2_2, id_vars=['economy'], var_name='year', value_name='value')

    indicator4_3_2_2_long['year'] = indicator4_3_2_2_long['year'].str.extract(r'(\d{4})')

    indicator4_3_2_2_long['indicator description'] = 'Domestic credit provided by financial sector (% of GDP)'
    indicator4_3_2_2_long['indicator code'] = 'FS.AST.DOMS.GD.ZS'

    indicator4_3_2_2_long['Indicator label'] = 'Domestic Credit to GDP Ratio'

    indicator4_3_2_2_long = indicator4_3_2_2_long.rename(columns={'economy': 'iso3'})
    indicator4_3_2_2_long = indicator4_3_2_2_long[['iso3', 'year', 'indicator description', 'indicator code', 'Indicator label', 'value']]

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'indicator_4_3_2_2_WB_WDI.csv')
    indicator4_3_2_2_long.to_csv(file_path, index=False)

    return indicator4_3_2_2_long

get_4_3_2_2(output_dir='outputs')


# TODO: indicator 4.3.3.1
""" FIND SOURCE FOR PENSION / SOVREIGN WEALTH FUNDS - DONT WORRY ABOUT THIS FOR NOW """


# TODO: indicator 4.4.1.1
""" SUM BELOW INDICATORS AS PERCENTAGE OF GDP """



# indicator 4.4.2.1
def get_4_4_2_1():

    # indicator4_4_2_1 = pd.read_excel('data/gfi trade mispricing.xlsx', skiprows=4, engine='openpyxl', sheet_name='Table A')


    # indicator4_4_2_1.columns = ['Index', 'Country', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', 'Average']
    # indicator4_4_2_1 = indicator4_4_2_1.drop(columns=['Index'])
    # indicator4_4_2_1 = indicator4_4_2_1.dropna(subset=['Country']).replace('N/A', pd.NA)
    # indicator4_4_2_1['Country'] = indicator4_4_2_1['Country'].astype(str)
    # indicator4_4_2_1['iso3'] = indicator4_4_2_1['Country'].apply(lambda x: wb.economy.coder(x) if pd.notnull(x) else None)

    # TODO: get trade mis-invoicing and calculate indicator 4.4.2.1 - DONT WORRY ABOUT THIS FOR NOW

#GFI 
#indicator4_4_2_1

def add_indicator_cols(df, code, description):
    df['indicator_code'] = code
    df['indicator_description'] = description
    return df

# Read in the data from the GFI sheets
def process_gfi_table(sheet_name, indicator_code, indicator_description):
    # Read data from the GFI sheet
    gfi_table = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name=sheet_name).drop(columns='Unnamed: 0')
    
    # Rename the country column
    gfi_table = gfi_table.rename(columns={"Unnamed: 1": "country"})
    
    # Filter for African countries
    iso3_reference_df = pd.read_csv('data/iso3_country_reference.csv')
    africa_iso3_df = iso3_reference_df[iso3_reference_df['Region Name'] == 'Africa']
    
    # Filter the table for African countries
    gfi_table = gfi_table[gfi_table['country'].isin(africa_iso3_df['Country or Area'])]
    
    # Melt the data from wide format to long format
    gfi_table_long = pd.melt(gfi_table, id_vars=['country'], var_name='year', value_name='value')
    
    # Add indicator code and description
    gfi_table_long = add_indicator_cols(gfi_table_long, indicator_code, indicator_description)
    
    return gfi_table_long

# Process data for different tables
gfi_table_a_long = process_gfi_table('Table A', "Table A", "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and 36 Advanced Economies, 2009-2018, in USD Millions")
gfi_table_c_long = process_gfi_table('Table C', "Table C", "The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009-2018, as a Percent of Total Trade")
gfi_table_e_long = process_gfi_table('Table E', "Table E", "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and all of their Global Trading Partners, 2009-2018 in USD Millions")
gfi_table_g_long = process_gfi_table('Table G', "Table G", "The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009-2018 as a Percent of Total Trade")

# Concatenate the data from all tables
indicator4_4_2_1 = pd.concat([gfi_table_a_long, gfi_table_c_long, gfi_table_e_long, gfi_table_g_long])

# Output the resulting DataFrame
indicator4_4_2_1.to_csv('outputs/indicator_4_4_2_1_GFI.csv', index=False)

#IMF ISORA
# indicator 4.4.2.2
# Define the function to get the indicator
def get_4_4_2_2(output_dir='outputs'):
    imf_isora_df_1 = pd.read_excel('data/IMF ISORA.xlsx', engine='openpyxl', skiprows=5, skipfooter=3, sheet_name="Registration of personal income").rename(columns={"Unnamed: 0": 'country'})
    imf_isora_df_1_long = pd.melt(imf_isora_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_df_1_long['indicator code'] = imf_isora_df_1_long['year'].apply(
        lambda x: 'PIT_Population' if '.1' in x else 'PIT_Labor_Force'
    )

    imf_isora_df_1_long['indicator description'] = imf_isora_df_1_long['indicator code'].map({
        'PIT_Labor_Force': 'Active taxpayers on PIT register as percentage of Labor Force',
        'PIT_Population': 'Active taxpayers on PIT register as percentage of Population'
    })

    imf_isora_df_1_long['year'] = imf_isora_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_df_2 = pd.read_excel('data/IMF ISORA.xlsx', engine='openpyxl', skiprows=5, skipfooter=3, sheet_name="Percentage inactive taxpayers o").rename(columns={"Unnamed: 0": 'country'})
    imf_isora_df_2_long = pd.melt(imf_isora_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_df_2_long['indicator code'] = imf_isora_df_2_long['year'].apply(
        lambda x: (
            'On CIT register' if '.1' in x else
            'On VAT register' if '.2' in x else
            'On PAYE register' if '.3' in x else
            'On Excise register' if '.4' in x else
            'On PIT register'
        )
    )

    imf_isora_df_2_long['indicator description'] = imf_isora_df_2_long['indicator code'].map({
        'On CIT register': 'On CIT register',
        'On VAT register': 'On VAT register',
        'On PAYE register': 'On PAYE register',
        'On Excise register': 'On Excise register',
        'On PIT register': 'On PIT register'
    })
    imf_isora_df_2_long['year'] = imf_isora_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)
    
    # Concatenate both dataframes
    indicator4_4_2_2 = pd.concat([imf_isora_df_1_long, imf_isora_df_2_long])

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the resulting DataFrame to CSV in the specified output directory
    file_path = os.path.join(output_dir, 'indicator_4_4_2_2_ISORA.csv')
    indicator4_4_2_2.to_csv(file_path, index=False)
    print(f"Indicator data saved to '{file_path}'")

    return indicator4_4_2_2

# Call the function and save the data
get_4_4_2_2(output_dir='outputs')

#OSAA
# indicator 4.4.2.3
def get_4_4_2_3():

    # get drug prices and seizures data
    drug_prices_df = pd.read_excel('data/unodc drug prices.xlsx', skiprows=1, engine='openpyxl', sheet_name='Prices in USD')
    drug_seizures_df = pd.read_excel('data/unodc drug seizures.xlsx', skiprows=1, engine='openpyxl', sheet_name='Export')

    # filter drug prices data and convert units
    filtered_prices_df = drug_prices_df[drug_prices_df['Unit'].isin(['Grams', 'Kilograms'])].copy() #Think of adding units and tablets
    filtered_prices_df.loc[filtered_prices_df['Unit'] == 'Grams', 'Typical_USD'] *= 1000

    # merge drug prices and seizures
    drug_total_df = pd.merge(
        drug_seizures_df, 
        filtered_prices_df, 
        left_on=['Country', 'DrugName', 'Reference year'], 
        right_on=['Country/Territory', 'Drug', 'Year'], 
        how='inner'
    )

    # calculate total drug sales
    drug_total_df['Total_Sale'] = drug_total_df['Kilograms'] * drug_total_df['Typical_USD']

    indicator4_4_2_3 = drug_total_df.groupby(['Country', 'Reference year'])['Total_Sale'].sum().reset_index()
    indicator4_4_2_3.columns = ['Country', 'year', 'Total_Sale']
    indicator4_4_2_3['iso3'] = indicator4_4_2_3['Country'].apply(lambda x: wb.economy.coder(x) if pd.notnull(x) else None)

    indicator4_4_2_3 = indicator4_4_2_3.drop(columns='Country').rename(columns={'Total_Sale': 'value'})
    indicator4_4_2_3['indicator description'] = 'The amount of drugs seized in kilograms multiplied by the drug price in kilograms. Excludes all seizures not measured in grams or kilograms.'
    indicator4_4_2_3['indicator code'] = 'Monetary losses (in USD) to drug sales'

    os.makedirs('outputs', exist_ok=True)
    indicator4_4_2_3.to_csv('outputs/4.4.2.3_OSAA.csv', index=False)
    print("Saved to outputs/4.4.2.3_OSAA.csv")
    return indicator4_4_2_3
   get_4_4_2_3()

#OSAA
# indicator 4.4.2.4 
def get_4_4_2_4():

    wb_corruption_score = wb.data.DataFrame('CC.EST', wb.region.members('AFR'), db=3).reset_index().melt(
        id_vars=['economy'], var_name='year', value_name='wb corruption score'
    ).rename(columns={'economy': 'iso3'})
    wb_corruption_score['year'] = wb_corruption_score['year'].str.replace('YR', '')
    wb_corruption_score['wb normalized corruption score'] = wb_corruption_score.groupby('year')['wb corruption score'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    wb_corruption_score['wb corruption score weight'] = wb_corruption_score['wb normalized corruption score']
    total_weights = wb_corruption_score.groupby('year')['wb corruption score weight'].sum().reset_index()
    total_weights = total_weights.rename(columns={'wb corruption score weight': 'wb corruption score total weight'})
    wb_corruption_score = wb_corruption_score.merge(total_weights, on='year')

    wb_corruption_score['wb corruption score country share'] = (wb_corruption_score['wb corruption score weight'] / wb_corruption_score['wb corruption score total weight']) * 148

    # Save WDI-calculated corruption score
    wb_corruption_score_export = wb_corruption_score[['iso3', 'year', 'wb corruption score country share']].rename(
        columns={'wb corruption score country share': 'value'}
    )
    wb_corruption_score_export['indicator description'] = 'WDI-calculated corruption score share of 148'
    wb_corruption_score_export['indicator code'] = 'CC.EST calculated'
    os.makedirs('outputs', exist_ok=True)
    wb_corruption_score_export.to_csv('outputs/4.4.2.4_OSAA.csv', index=False)
    print("Saved WDI corruption score to outputs/4.4.2.4_OSAA.csv")

    # --- WJP Component ---
    wjp_absence_of_corruption = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[
        ['Country Code', 'Year', 'Factor 2: Absence of Corruption']
    ].rename(columns={'Country Code': 'iso3', 'Year': 'year'})
    wjp_absence_of_corruption['year'] = wjp_absence_of_corruption['year'].astype(str)

    def expand_years(row):
        if '-' in row['year']:
            start, end = map(int, row['year'].split('-'))
            return [{'iso3': row['iso3'], 'year': str(year), 'Factor 2: Absence of Corruption': row['Factor 2: Absence of Corruption']}
                    for year in range(start, end + 1)]
        else:
            return [row]

    wjp_expanded = pd.DataFrame([entry for row in wjp_absence_of_corruption.to_dict(orient='records') for entry in expand_years(row)])

    # Save WJP Absence of Corruption
    wjp_export = wjp_expanded.rename(columns={'Factor 2: Absence of Corruption': 'value'})
    wjp_export['indicator description'] = 'WJP Factor 2: Absence of Corruption'
    wjp_export['indicator code'] = 'WJP_F2'
    wjp_export = wjp_export[['iso3', 'year', 'indicator description', 'indicator code', 'value']]
    wjp_export.to_csv('outputs/4.4.2.4_wb_WJP.csv', index=False)
    print("Saved WJP data to outputs/4.4.2.4_WB_WJP.csv")

get_4_4_2_4()
######################################################################################
#wjp #WDI #MOIbrahim #World Bank ID4D
#WPJ _4_4_3_1b
def get_4_4_3_1b():
    df = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')
    df = df[['Country', 'Year', 'WJP Rule of Law Index: Overall Score']].rename(columns={
        'Country': 'economy',
        'Year': 'year',
        'WJP Rule of Law Index: Overall Score': 'value'
    })
    df['indicator description'] = 'WJP Rule of Law Index: Overall Score'
    df['indicator code'] = 'WJP Rule of Law Index'
    df = df[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/4.4.3.1b_WB_WJP.csv', index=False)
    print("Saved: 4.4.3.1b_WB_WJP.csv")
get_4_4_3_1b()
#Mo Ibraham
# indicator 4.4.3.1c
def get_4_4_3_1c():
    df = pd.read_csv('data/mo ibrahim rule of law - score and rank.csv')
    df_long = pd.melt(df, id_vars=['Location', 'iso2', 'Indicator'], var_name='year', value_name='value')
    df_long = df_long.rename(columns={'Location': 'economy','Indicator': 'indicator description'})
    df_long['indicator code'] = 'Mo Ibrahim Index'
    df_long = df_long[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df_long.to_csv('outputs/4.4.3.1c_MoIbrahim.csv', index=False)
    print("Saved to outputs/4.4.3.1c_MoIbrahim.csv")
get_4_4_3_1c()
#WDI
# indicator 4.4.3.1d
def get_4_4_3_1d():
    df = wb.data.DataFrame('IQ.CPA.PUBS.XQ', wb.region.members('AFR'), db=31).reset_index()
    df_long = pd.melt(df, id_vars=['economy'], var_name='year', value_name='value')
    df_long['year'] = df_long['year'].str.replace('YR', '')
    df_long['indicator description'] = 'CPIA transparency, accountability, and corruption in the public sector rating'
    df_long['indicator code'] = 'IQ.CPA.PUBS.XQ'
    df_long = df_long[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df_long.to_csv('outputs/4.4.3.1d_WB_WDI_CPIA1.csv', index=False)
    print("Saved to outputs/4.4.3.1d_WB_WDI_CPIA1.csv")
get_4_4_3_1d()
#WDI 
# indicator 4.4.3.1e
def get_4_4_3_1e():
    df = wb.data.DataFrame('IQ.CPA.PADM.XQ', wb.region.members('AFR'), db=31).reset_index()
    df_long = pd.melt(df, id_vars=['economy'], var_name='year', value_name='value')
    df_long['year'] = df_long['year'].str.replace('YR', '')
    df_long['indicator description'] = 'Indicator Name	CPIA quality of public administration rating'
    df_long['indicator code'] = 'IQ.CPA.PADM.XQ'
    df_long = df_long[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df_long.to_csv('outputs/4.4.3.1e_WB_WDI_CPIA2.csv', index=False)
    print("Saved to outputs/4.4.3.1e_WB_WDI_CPIA2.csv")
get_4_4_3_1e()
#ID4D (Two indicators)
def get_4_4_3_1fa():
    try:
        df = wb.data.DataFrame('FX.OWN.TOTL.YG.ZS', wb.region.members('AFR')).reset_index()
        df_long = pd.melt(df, id_vars=['economy'], var_name='year', value_name='value')
        df_long['year'] = df_long['year'].str.replace('YR', '')
        df_long['indicator description'] = 'ID ownership, 15 to 24 years old (%)'
        df_long['indicator code'] = 'FX.OWN.TOTL.YG.ZS'
        df_long = df_long[['economy', 'year', 'value', 'indicator description', 'indicator code']]
        os.makedirs('outputs', exist_ok=True)
        df_long.to_csv('outputs/4.4.3.1f_WB_WDI_ID4D1.csv', index=False)
        print("Saved to outputs/4.4.3.1f_WB_WDI_ID4D1.csv")
    except Exception as e:
        print(f"Failed to fetch youth ID ownership data: {e}")

def get_4_4_3_1fb():
    try:
        df = wb.data.DataFrame('FX.OWN.TOTL.OL.ZS', wb.region.members('AFR')).reset_index()
        df_long = pd.melt(df, id_vars=['economy'], var_name='year', value_name='value')
        df_long['indicator description'] = 'ID ownership, 25 and older (%)'
        df_long['indicator code'] = 'FX.OWN.TOTL.OL.ZS'
        df_long = df_long[['economy', 'year', 'value', 'indicator description', 'indicator code']]
        os.makedirs('outputs', exist_ok=True)
        df_long.to_csv('outputs/4.4.3.1f_WB_WDI_ID4D2.csv', index=False)
        print("Saved to outputs/4.4.3.1f_WB_WDI_ID4D2.csv")
    except Exception as e:
        print(f"Failed to fetch adult ID ownership data: {e}")

get_4_4_3_1fa()
get_4_4_3_1fb()

#WJP
# indicator 4.4.3.1g
# indicator 4.4.3.1h
def get_4_4_3_1g():
    df = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')
    df = df[['Country', 'Year', 'Factor 3: Open Government']].copy()
    df = df.rename(columns={
        'Country': 'economy',
        'Factor 3: Open Government': 'value',
        'Year': 'year'
    })
    df['indicator description'] = 'Public Access to Information'
    df['indicator code'] = 'Factor 3: Open Government'
    df = df[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/4.4.3.1g_WJP.csv', index=False)
    print("Saved to outputs/4.4.3.1g_WJP.csv")

def get_4_4_3_1h():
    df = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')
    df = df[['Country', 'Year', 'Factor 5: Order and Security', 'Factor 7: Civil Justice', 'Factor 8: Criminal Justice']].copy()
    df = df.rename(columns={'Country': 'economy', 'Year': 'year'})
    df_long = pd.melt(df, id_vars=['economy', 'year'], var_name='indicator code', value_name='value')
    df_long['indicator description'] = 'Institutions to Combat Crime'
    df_long = df_long[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df_long.to_csv('outputs/4.4.3.1h_WJP.csv', index=False)
    print("Saved to outputs/4.4.3.1h_WJP.csv")

get_4_4_3_1g()
get_4_4_3_1h()

#IMF ISORA
# indicator 4.4.3.2
def get_4_4_3_2():

    # get all IMF ISORA data
    # imf_isora_stakeholder_df = pd.read_excel('data/imf isora stakeholder interactions.xlsx', engine='openpyxl', sheet_name=None)
    # imf_isora_op_metrics_payments_df = pd.read_excel('data/imf isora op metrics payments and arrears.xlsx', engine='openpyxl', sheet_name=None)
    # imf_isora_op_metrics_registration_df = pd.read_excel('data/imf isora op metrics registration and filing.xlsx', engine='openpyxl', sheet_name=None)

    imf_isora_resources_ict_df_1 = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', skiprows=6, engine='openpyxl', sheet_name='Tax administration expenditures').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_resources_ict_df_1_long = pd.melt(imf_isora_resources_ict_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_resources_ict_df_1_long['indicator code'] = imf_isora_resources_ict_df_1_long['year'].apply(
        lambda x: (
            'Salary expenditure - Derived' if '.1' in x else
            'Information and communications technology expenditure - Derived' if '.2' in x else
            'Capital expenditure - Derived' if '.3' in x else
            'Operating expenditure - Derived'
        )
    )
    imf_isora_resources_ict_df_1_long['indicator description'] = imf_isora_resources_ict_df_1_long['indicator code'].map({
        'Salary expenditure - Derived': 'Salary expenditure - Derived',
        'Information and communications technology expenditure - Derived': 'Information and communications technology expenditure - Derived',
        'Capital expenditure - Derived': 'Capital expenditure - Derived',
        'Operating expenditure - Derived': 'Operating expenditure - Derived',
    })
    imf_isora_resources_ict_df_1_long['year'] = imf_isora_resources_ict_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_resources_ict_df_2 = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', skiprows=7, engine='openpyxl', sheet_name='Tax administration staff total ').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_resources_ict_df_2_long = pd.melt(imf_isora_resources_ict_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_resources_ict_df_2_long['indicator code'] = imf_isora_resources_ict_df_2_long['year'].apply(
        lambda x: (
            'FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing' if '.1' in x else
            'FTEs by function of the tax administration-Audit, investigation and other verification' if '.2' in x else
            'FTEs by function of the tax administration-Enforced debt collection and related functions' if '.3' in x else
            'FTEs by function of the tax administration-Other functions' if '.4' in x else
            'Percentage of staff working on headquarter functions' if '.5' in x else
            'Total tax administration FTEs - Derived'
        )
    )
    imf_isora_resources_ict_df_2_long['indicator description'] = imf_isora_resources_ict_df_2_long['indicator code'].map({
        'FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing': 'FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing',
        'FTEs by function of the tax administration-Audit, investigation and other verification': 'FTEs by function of the tax administration-Audit, investigation and other verification',
        'FTEs by function of the tax administration-Enforced debt collection and related functions': 'FTEs by function of the tax administration-Enforced debt collection and related functions',
        'FTEs by function of the tax administration-Other functions': 'FTEs by function of the tax administration-Other functions',
        'Percentage of staff working on headquarter functions': 'Percentage of staff working on headquarter functions',
        'Total tax administration FTEs - Derived': 'Total tax administration FTEs - Derived'
    })
    imf_isora_resources_ict_df_2_long['year'] = imf_isora_resources_ict_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_resources_ict_df_3 = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Operational ICT solutions').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_resources_ict_df_3_long = pd.melt(imf_isora_resources_ict_df_3, id_vars='country', var_name='year', value_name='value')
    imf_isora_resources_ict_df_3_long['indicator code'] = imf_isora_resources_ict_df_3_long['year'].apply(
        lambda x: (
            'Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)' if '.1' in x else
            'Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)' if '.2' in x else
            'Operational ICT solutions of the administration are…-Custom built'
        )
    )
    imf_isora_resources_ict_df_3_long['indicator description'] = imf_isora_resources_ict_df_3_long['indicator code'].map({
        'Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)': 'Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)',
        'Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)': 'Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)',
        'Operational ICT solutions of the administration are…-Custom built': 'Operational ICT solutions of the administration are…-Custom built'
    })
    imf_isora_resources_ict_df_3_long['year'] = imf_isora_resources_ict_df_3_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_resources_ict_df = pd.concat([imf_isora_resources_ict_df_1_long, imf_isora_resources_ict_df_2_long, imf_isora_resources_ict_df_3_long])


    imf_isora_staff_metrics_df_1 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff strength levels').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_1_long = pd.melt(imf_isora_staff_metrics_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_1_long['indicator code'] = imf_isora_staff_metrics_df_1_long['year'].apply(
        lambda x: (
            'Staff strength levels -Departures in FY' if '.1' in x else
            'Staff strength levels -Recruitments in FY' if '.2' in x else
            'Staff strength levels -No. at end of FY' if '.3' in x else
            'Staff strength levels -No. at start of FY'
        )
    )
    imf_isora_staff_metrics_df_1_long['indicator description'] = imf_isora_staff_metrics_df_1_long['indicator code'].map({
        'Staff strength levels -Departures in FY': 'Staff strength levels -Departures in FY',
        'Staff strength levels -Recruitments in FY': 'Staff strength levels -Recruitments in FY',
        'Staff strength levels -No. at end of FY': 'Staff strength levels -No. at end of FY',
        'Staff strength levels -No. at start of FY': 'Staff strength levels -No. at start of FY',
    })
    imf_isora_staff_metrics_df_1_long['year'] = imf_isora_staff_metrics_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df_2 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff academic qualifications').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_2_long = pd.melt(imf_isora_staff_metrics_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_2_long['indicator code'] = imf_isora_staff_metrics_df_2_long['year'].apply(
        lambda x: (
            'Academic qualifications (No. of staff at the end of FY)-Bachelors degree' if '.1' in x else
            'Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)'
        )
    )
    imf_isora_staff_metrics_df_2_long['indicator description'] = imf_isora_staff_metrics_df_2_long['indicator code'].map({
        'Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)': 'Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)',
        'Academic qualifications (No. of staff at the end of FY)-Bachelors degree': 'Academic qualifications (No. of staff at the end of FY)-Bachelors degree',
    })
    imf_isora_staff_metrics_df_2_long['year'] = imf_isora_staff_metrics_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)
    
    imf_isora_staff_metrics_df_3 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff age distribution').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_3_long = pd.melt(imf_isora_staff_metrics_df_3, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_3_long['indicator code'] = imf_isora_staff_metrics_df_3_long['year'].apply(
        lambda x: (
            'Age distribution (No. of staff at the end of FY)-25-34 years' if '.1' in x else
            'Age distribution (No. of staff at the end of FY)-35-44 years' if '.2' in x else
            'Age distribution (No. of staff at the end of FY)-45-54 years' if '.3' in x else
            'Age distribution (No. of staff at the end of FY)-55-64 years' if '.4' in x else
            'Age distribution (No. of staff at the end of FY)-Over 64 years' if '.5' in x else
            'Age distribution (No. of staff at the end of FY)-Under 25 years'
        )
    )
    imf_isora_staff_metrics_df_3_long['indicator description'] = imf_isora_staff_metrics_df_3_long['indicator code'].map({
        'Age distribution (No. of staff at the end of FY)-Under 25 years': 'Age distribution (No. of staff at the end of FY)-Under 25 years',
        'Age distribution (No. of staff at the end of FY)-25-34 years': 'Age distribution (No. of staff at the end of FY)-25-34 years',
        'Age distribution (No. of staff at the end of FY)-35-44 years': 'Age distribution (No. of staff at the end of FY)-35-44 years',
        'Age distribution (No. of staff at the end of FY)-45-54 years': 'Age distribution (No. of staff at the end of FY)-45-54 years',
        'Age distribution (No. of staff at the end of FY)-55-64 years': 'Age distribution (No. of staff at the end of FY)-55-64 years',
        'Age distribution (No. of staff at the end of FY)-Over 64 years': 'Age distribution (No. of staff at the end of FY)-Over 64 years',
    })
    imf_isora_staff_metrics_df_3_long['year'] = imf_isora_staff_metrics_df_3_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df_4 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff length of service').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_4_long = pd.melt(imf_isora_staff_metrics_df_4, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_4_long['indicator code'] = imf_isora_staff_metrics_df_4_long['year'].apply(
        lambda x: (
            'Length of service (No. of staff at the end of FY)-5-9 years' if '.1' in x else
            'Length of service (No. of staff at the end of FY)-10-19 years' if '.2' in x else
            'Length of service (No. of staff at the end of FY)-Over 19 years' if '.3' in x else
            'Length of service (No. of staff at the end of FY)-Under 5 years'
        )
    )
    imf_isora_staff_metrics_df_4_long['indicator description'] = imf_isora_staff_metrics_df_4_long['indicator code'].map({
        'Length of service (No. of staff at the end of FY)-Under 5 years': 'Length of service (No. of staff at the end of FY)-Under 5 years',
        'Length of service (No. of staff at the end of FY)-5-9 years': 'Length of service (No. of staff at the end of FY)-5-9 years',
        'Length of service (No. of staff at the end of FY)-10-19 years': 'Length of service (No. of staff at the end of FY)-10-19 years',
        'Length of service (No. of staff at the end of FY)-Over 19 years': 'Length of service (No. of staff at the end of FY)-Over 19 years',
    })
    imf_isora_staff_metrics_df_4_long['year'] = imf_isora_staff_metrics_df_4_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df_5 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=7, skipfooter=2, engine='openpyxl', sheet_name='Staff gender distribution').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_5_long = pd.melt(imf_isora_staff_metrics_df_5, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_5_long['indicator code'] = imf_isora_staff_metrics_df_5_long['year'].apply(
        lambda x: (
            'Gender distribution (No. of staff at the end of FY)-All staff-Female' if '.1' in x else
            'Gender distribution (No. of staff at the end of FY)-All staff-Other' if '.2' in x else
            'Gender distribution (No. of staff at the end of FY)-Executives only-Male' if '.3' in x else
            'Gender distribution (No. of staff at the end of FY)-Executives only-Female' if '.4' in x else
            'Gender distribution (No. of staff at the end of FY)-Executives only-Other' if '.5' in x else
            'Gender distribution (No. of staff at the end of FY)-All staff-Male'
        )
    )
    imf_isora_staff_metrics_df_5_long['indicator description'] = imf_isora_staff_metrics_df_5_long['indicator code'].map({
        'Gender distribution (No. of staff at the end of FY)-All staff-Male': 'Gender distribution (No. of staff at the end of FY)-All staff-Male',
        'Gender distribution (No. of staff at the end of FY)-All staff-Female': 'Gender distribution (No. of staff at the end of FY)-All staff-Female',
        'Gender distribution (No. of staff at the end of FY)-All staff-Other': 'Gender distribution (No. of staff at the end of FY)-All staff-Other',
        'Gender distribution (No. of staff at the end of FY)-Executives only-Male': 'Gender distribution (No. of staff at the end of FY)-Executives only-Male',
        'Gender distribution (No. of staff at the end of FY)-Executives only-Female': 'Gender distribution (No. of staff at the end of FY)-Executives only-Female',
        'Gender distribution (No. of staff at the end of FY)-Executives only-Other': 'Gender distribution (No. of staff at the end of FY)-Executives only-Other',
    })
    imf_isora_staff_metrics_df_5_long['year'] = imf_isora_staff_metrics_df_5_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df = pd.concat([imf_isora_staff_metrics_df_1_long, imf_isora_staff_metrics_df_2_long, imf_isora_staff_metrics_df_3_long, imf_isora_staff_metrics_df_4_long, imf_isora_staff_metrics_df_5_long])


    imf_isora_op_metrics_audit_df_1 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Audit and verification').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_1_long = pd.melt(imf_isora_op_metrics_audit_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_1_long['indicator code'] = imf_isora_op_metrics_audit_df_1_long['year'].apply(
        lambda x: (
            'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits where a tax adjustment was made' if '.1' in x else
            'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits completed'
        )
    )
    imf_isora_op_metrics_audit_df_1_long['indicator description'] = imf_isora_op_metrics_audit_df_1_long['indicator code'].map({
        'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits completed': 'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits completed',
        'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits where a tax adjustment was made': 'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits where a tax adjustment was made',
    })
    imf_isora_op_metrics_audit_df_1_long['year'] = imf_isora_op_metrics_audit_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)
    
    imf_isora_op_metrics_audit_df_2 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Value of additional assessments').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_2_long = pd.melt(imf_isora_op_metrics_audit_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_2_long['indicator code'] = imf_isora_op_metrics_audit_df_2_long['year'].apply(
        lambda x: (
            'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Electronic compliance checks' if '.1' in x else
            'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Total' if '.2' in x else
            'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-All audits (excluded electronic compliance checks)'
        )
    )
    imf_isora_op_metrics_audit_df_2_long['indicator description'] = imf_isora_op_metrics_audit_df_2_long['indicator code'].map({
        'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-All audits (excluded electronic compliance checks)': 'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-All audits (excluded electronic compliance checks)',
        'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Electronic compliance checks': 'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Electronic compliance checks',
        'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Total': 'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Total',
    })
    imf_isora_op_metrics_audit_df_2_long['year'] = imf_isora_op_metrics_audit_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df_3 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Value of additional assessm_0').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_3_long = pd.melt(imf_isora_op_metrics_audit_df_3, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_3_long['indicator code'] = imf_isora_op_metrics_audit_df_3_long['year'].apply(
        lambda x: (
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Personal income tax' if '.1' in x else
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Value added tax' if '.2' in x else
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Tax withheld by employers from employees		' if '.3' in x else
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax'
        )
    )
    imf_isora_op_metrics_audit_df_3_long['indicator description'] = imf_isora_op_metrics_audit_df_3_long['indicator code'].map({
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax',
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Personal income tax': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Personal income tax',
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Value added tax': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Value added tax',
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Tax withheld by employers from employees': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Tax withheld by employers from employees',
    })
    imf_isora_op_metrics_audit_df_3_long['year'] = imf_isora_op_metrics_audit_df_3_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df_4 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=6, engine='openpyxl', sheet_name='Tax crime investigation').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_4_long = pd.melt(imf_isora_op_metrics_audit_df_4, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_4_long['indicator code'] = imf_isora_op_metrics_audit_df_4_long['year'].apply(
        lambda x: (
            'Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency' if '.1' in x else
            'Role of the administration in tax crime investigations - Other agency conducts investigations' if '.2' in x else
            'No. of tax crime investigation cases referred for prosecution during the fiscal year (where the tax administration has responsibility)' if '.3' in x else
            'Role of the administration in tax crime investigations - Directing and conducting investigations'
        )
    )
    imf_isora_op_metrics_audit_df_4_long['indicator description'] = imf_isora_op_metrics_audit_df_4_long['indicator code'].map({
        'Role of the administration in tax crime investigations - Directing and conducting investigations': 'Role of the administration in tax crime investigations - Directing and conducting investigations',
        'Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency': 'Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency',
        'Role of the administration in tax crime investigations - Other agency conducts investigations': 'Role of the administration in tax crime investigations - Other agency conducts investigations',
        'No. of tax crime investigation cases referred for prosecution during the fiscal year (where the tax administration has responsibility)': 'No. of tax crime investigation cases referred for prosecution during the fiscal year (where the tax administration has responsibility)',
    })
    imf_isora_op_metrics_audit_df_4_long['year'] = imf_isora_op_metrics_audit_df_4_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df_5 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Dispute resolution review proce').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_5_long = pd.melt(imf_isora_op_metrics_audit_df_5, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_5_long['indicator code'] = imf_isora_op_metrics_audit_df_5_long['year'].apply(
        lambda x: (
            'Mechanisms available for taxpayers to challenge assessments-Independent review by external body' if '.1' in x else
            'Mechanisms available for taxpayers to challenge assessments-Independent review by a higher appellate court' if '.2' in x else
            'Taxpayers must first pursue internal review where an internal review is permissible' if '.3' in x else
            'Mechanisms available for taxpayers to challenge assessments-Internal review by tax administration'
        )
    )
    imf_isora_op_metrics_audit_df_5_long['indicator description'] = imf_isora_op_metrics_audit_df_5_long['indicator code'].map({
        'Mechanisms available for taxpayers to challenge assessments-Internal review by tax administration': 'Mechanisms available for taxpayers to challenge assessments-Internal review by tax administration',
        'Mechanisms available for taxpayers to challenge assessments-Independent review by external body': 'Mechanisms available for taxpayers to challenge assessments-Independent review by external body',
        'Mechanisms available for taxpayers to challenge assessments-Independent review by a higher appellate court': 'Mechanisms available for taxpayers to challenge assessments-Independent review by a higher appellate court',
        'Taxpayers must first pursue internal review where an internal review is permissible': 'Taxpayers must first pursue internal review where an internal review is permissible',
    })
    imf_isora_op_metrics_audit_df_5_long['year'] = imf_isora_op_metrics_audit_df_5_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df = pd.concat([imf_isora_op_metrics_audit_df_1_long, imf_isora_op_metrics_audit_df_2_long, imf_isora_op_metrics_audit_df_3_long, imf_isora_op_metrics_audit_df_4_long, imf_isora_op_metrics_audit_df_5_long])

    indicator4_4_3_2 = pd.concat([imf_isora_resources_ict_df, imf_isora_staff_metrics_df, imf_isora_op_metrics_audit_df])

    os.makedirs('outputs', exist_ok=True)
    indicator4_4_3_2.to_csv('outputs/4.4.3.2_IMF_ISORA.csv', index=False)
    print("Saved to outputs/4.4.3.2_IMF_ISORA.csv")
    return indicator4_4_3_2
get_4_4_3_2()


# indicator 4.4.4.2
def get_4_4_4_2():
    tjn_df = pd.read_csv('data/tjn data.csv').rename(columns={'country_name': 'Country'})
    tjn_df_long = pd.melt(tjn_df, id_vars=['Country', 'iso3'], var_name='year', value_name='value')
    tjn_df_long['year'] = tjn_df_long['year'].str.extract(r'(\d{4})')
    tjn_df_long['indicator code'] = 'FSI'
    tjn_df_long['indicator description'] = 'Financial Secrecy Index'
    os.makedirs('outputs', exist_ok=True)
    tjn_df_long.to_csv('outputs/4.4.4.2_TJN.csv', index=False)
    print("Saved to outputs/4.4.4.2_TJN.csv")
    return tjn_df_long
get_4_4_4_2()

#USAID
# indicator 4.4.5.1 
def get_4_4_5_1():   
    usaid_df = pd.read_excel('data/USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    df = usaid_df[['country_name', 'year', 'Tax buoyancy [by_tax]']].rename(columns={
        'country_name': 'economy',
        'Tax buoyancy [by_tax]': 'value'
    })
    df['indicator code'] = 'Tax buoyancy [by_tax]'
    df['indicator description'] = 'Tax buoyancy [by_tax]'
    df = df[['economy', 'year', 'value', 'indicator description', 'indicator code']]
    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/4.4.5.1_USAID.csv', index=False)
    print("Saved to outputs/4.4.5.1_USAID.csv")
    return df
get_4_4_5_1()




