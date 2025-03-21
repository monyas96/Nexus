import pandas as pd
import wbgapi as wb
import re
import openpyxl
import xlrd

iso3_reference_df = pd.read_csv('iso3_country_reference.csv')
africa_iso3 = list(wb.region.members('AFR'))

africa_m49 = iso3_reference_df[iso3_reference_df['iso3'].isin(africa_iso3)]['m49'].tolist()

# indicator_to_csv
def process_indicator_to_csv(indicator_code, file_name):
    # Step 1: Extract the data for the indicator and reset the index
    df = wb.data.DataFrame(indicator_code, wb.region.members('AFR'), db=67).reset_index()

    # Step 2: Melt the DataFrame from wide to long format
    df = pd.melt(df, id_vars=['classification', 'economy'], var_name='YearMonth', value_name='Value')

    # Step 3: Rename and clean columns
    df = df.rename(columns={'economy': 'Country'})
    df['Year'] = df['YearMonth'].str[2:6]
    df['Month'] = df['YearMonth'].str[6:]
    df = df.drop(columns=['YearMonth'])  # Drop 'YearMonth' column

    # Step 4: Reorder columns and save to CSV
    df = df[['classification', 'Country', 'Year', 'Month', 'Value']]
    df.to_csv(file_name, index=False)
    print(f"Cleaned data saved to '{file_name}'")

# CSV Indicator 4.1.1.1: DONE!
process_indicator_to_csv('PI-01', 'indicator_4_1_1_1.csv')
# CSV indicator 4.1.1.2: DONE!
process_indicator_to_csv('PI-02', 'indicator_4_1_1_2.csv')
# CSV indicator 4.1.1.3: DONE!
process_indicator_to_csv('PI-03', 'indicator_4_1_1_3.csv')

######################################################################################
# indicator 4.2.1.1: DONE!
def get_4_2_1_1():
    indicator4_2_1_1 = wb.data.DataFrame('GC.TAX.TOTL.GD.ZS', wb.region.members('AFR'))
    return indicator4_2_1_1
indicator_4_2_1_1_df = get_4_2_1_1()
indicator_4_2_1_1_df = indicator_4_2_1_1_df.reset_index()

long_df = pd.melt(indicator_4_2_1_1_df, id_vars=['economy'], var_name='Year', value_name='Value')
long_df['Year'] = long_df['Year'].str.replace('YR', '')
long_df['Indicator'] = 'Tax Revenue as Percentage of GDP'
long_df.to_csv('indicator_4_2_1_1.csv', index=False)

########################################################################################
# indicator 4.2.1.2: DONE!

# Load the Excel file
file_path = 'ATO_RAW_ATAF 2.xlsx' #this is relative path from my 
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
print(filtered_df .head())
filtered_df .to_csv('indicator_4_2_1_2.csv', index=False)
############################################################################################
# indicator 4.2.2.1 DONE!
# Define the function to get the indicator
def get_4_2_2_1():

    usaid_df = pd.read_excel('USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_2_2_1 = usaid_df[usaid_df['m49'].notna()][['ISO2','country_name', 'year', 'Tax effort (ratio) [tax_eff]']]
    indicator4_2_2_1 = indicator4_2_2_1.rename(columns={'Tax effort (ratio) [tax_eff]': 'Value'})
    indicator4_2_2_1['Indicator'] = 'Tax effort (ratio)'
    return indicator4_2_2_1[['country_name', 'year', 'Indicator', 'Value']]
indicator4_2_2_1 = get_4_2_2_1()
indicator4_2_2_1.to_csv('indicator_4_2_2_1.csv', index=False)
##########################################################################################
# indicator 4.2.2.2 two parts Tax buoyancy [by_tax] + tax cpacity and gap from
#4_2_2_1a
def get_4_2_2_2a():

    usaid_df = pd.read_excel('USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_2_2_2a = usaid_df[usaid_df['m49'].notna()][['ISO2','country_name', 'year', 'Tax buoyancy [by_tax]']]
    indicator4_2_2_2a = indicator4_2_2_1.rename(columns={' Tax buoyancy [by_tax]': 'Value'})
    indicator4_2_2_2a['Indicator'] = 'Tax effort (ratio)'
    return indicator4_2_2_2a[['country_name', 'year', 'Indicator', 'Value']]
indicator4_2_2_2a = get_4_2_2_2a()

indicator4_2_2_1a.to_csv('indicator_4_2_2_1a.csv', index=False)

#4_2_2_1b it has gap cpacity and buoyancy
file_path = 'C:/Users/MYASSIEN/WB_TAX CPACITY AND GAP.csv'
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
indicator4_2_2_1b.to_csv('indicator4_2_2_1b.csv', index=False)

####################################################################################

# indicator 4.3.1.1
def get_4_3_1_1():

    # get market cap and GDP
    market_cap = wb.data.DataFrame('CM.MKT.LCAP.CD', wb.region.members('AFR'))
    gdp = wb.data.DataFrame('NY.GDP.MKTP.CD', wb.region.members('AFR'))

    # calculate indicator
    indicator4_3_1_1 = (market_cap / gdp) * 100
    indicator4_3_1_1 = indicator4_3_1_1.reset_index()

    # make long format
    indicator4_3_1_1_long = pd.melt(indicator4_3_1_1, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_1_1_long['year'] = indicator4_3_1_1_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_1_1_long['indicator description'] = 'Market capitalization of listed domestic companies (current US$) divided by GDP (current US$)'
    indicator4_3_1_1_long['indicator code'] = 'CM.MKT.LCAP.CD / NY.GDP.MKTP.CD'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_1_long = indicator4_3_1_1_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_1_1_long = indicator4_3_1_1_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_1_1_long


# indicator 4.3.1.2
def get_4_3_1_2():
    indicator4_3_1_2 = wb.data.DataFrame('DT.NFL.BOND.CD', wb.region.members('AFR')).reset_index()

    # make long format
    indicator4_3_1_2_long = pd.melt(indicator4_3_1_2, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_1_2_long['year'] = indicator4_3_1_2_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_1_2_long['indicator description'] = 'Portfolio investment, bonds (PPG + PNG) (NFL, current US$)'
    indicator4_3_1_2_long['indicator code'] = 'DT.NFL.BOND.CD'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_2_long = indicator4_3_1_2_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_1_2_long = indicator4_3_1_2_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_1_2_long


# indicator 4.3.1.3
def get_4_3_1_3():

    # get reserves and debt
    reserves = wb.data.DataFrame('BN.RES.INCL.CD', wb.region.members('AFR'))
    debt = wb.data.DataFrame('DT.DOD.DSTC.CD', wb.region.members('AFR'))

    # calculate indicator
    indicator4_3_1_3 = reserves / debt
    indicator4_3_1_3 = indicator4_3_1_3.reset_index()

    # make long format
    indicator4_3_1_3_long = pd.melt(indicator4_3_1_3, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_1_3_long['year'] = indicator4_3_1_3_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_1_3_long['indicator description'] = 'Reserves and related items (BoP, current US$) divided by External debt stocks, short-term (DOD, current US$)'
    indicator4_3_1_3_long['indicator code'] = 'BN.RES.INCL.CD / DT.DOD.DSTC.CD'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_3_long = indicator4_3_1_3_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_1_3_long = indicator4_3_1_3_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_1_3_long


# indicator 4.3.2.1
def get_4_3_2_1():

    # get banking sector indicators
    capital_to_assets = wb.data.DataFrame('FB.BNK.CAPA.ZS', wb.region.members('AFR'))
    liquid_reserves_to_assets = wb.data.DataFrame('FD.RES.LIQU.AS.ZS', wb.region.members('AFR'))
    domestic_credit = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR')) / 100

    # normalize indicators
    def min_max_normalize(df):
        return (df - df.min()) / (df.max() - df.min())

    # calculate banking sector strength score from indicators
    capital_to_assets = min_max_normalize(capital_to_assets) * 0.4
    liquid_reserves_to_assets = min_max_normalize(liquid_reserves_to_assets) * 0.3
    domestic_credit  = min_max_normalize(domestic_credit) * 0.3
    indicator4_3_2_1 = (capital_to_assets + liquid_reserves_to_assets + domestic_credit)
    indicator4_3_2_1 = indicator4_3_2_1.reset_index()

    # make long format
    indicator4_3_2_1_long = pd.melt(indicator4_3_2_1, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_2_1_long['year'] = indicator4_3_2_1_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_2_1_long['indicator description'] = '(0.4 * Bank capital to assets ratio (%)) + (0.3 * Bank liquid reserves to bank assets ratio (%)) + (0.3 * Domestic credit provided by financial sector (% of GDP))'
    indicator4_3_2_1_long['indicator code'] = '(0.4 * FB.BNK.CAPA.ZS) + (0.3 * FD.RES.LIQU.AS.ZS) + (0.3 * FS.AST.DOMS.GD.ZS)'

    # Rename 'economy' column to 'iso3'
    indicator4_3_2_1_long = indicator4_3_2_1_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_2_1_long = indicator4_3_2_1_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]
    
    return indicator4_3_2_1_long


# indicator 4.3.2.2
def get_4_3_2_2():
    indicator4_3_2_2 = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR')).reset_index()

    # make long format
    indicator4_3_2_2_long = pd.melt(indicator4_3_2_2, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_2_2_long['year'] = indicator4_3_2_2_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_2_2_long['indicator description'] = 'Domestic credit provided by financial sector (% of GDP)'
    indicator4_3_2_2_long['indicator code'] = 'FS.AST.DOMS.GD.ZS'

    # Rename 'economy' column to 'iso3'
    indicator4_3_2_2_long = indicator4_3_2_2_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_2_2_long = indicator4_3_2_2_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_2_2_long



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

    def add_indicator_cols(df, code, description):
        df['indicator_code'] = code
        df['indicator_description'] = description
        return df

    gfi_table_a = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table A').drop(columns='Unnamed: 0')
    gfi_table_a_long = pd.melt(gfi_table_a, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_a_long = add_indicator_cols(gfi_table_a_long, "Table A", "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries  and 36 Advanced Economies, 2009-2018, in USD Millions")

    gfi_table_c = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table C').drop(columns='Unnamed: 0')
    gfi_table_c_long = pd.melt(gfi_table_c, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_c_long = add_indicator_cols(gfi_table_c_long, "Table C", "  The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009-2018, as a Percent of Total Trade")
                                      
    gfi_table_e = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table E').drop(columns='Unnamed: 0')
    gfi_table_e_long = pd.melt(gfi_table_e, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_e_long = add_indicator_cols(gfi_table_e_long, "Table E", "  The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries  and all of their Global Trading Partners, 2009-2018 in USD Millions")
                                          
    gfi_table_g = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table G').drop(columns='Unnamed: 0')
    gfi_table_g_long = pd.melt(gfi_table_g, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_g_long = add_indicator_cols(gfi_table_g_long, "Table G", "  The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009-2018 as a Percent of Total Trade")
                                          
    indicator4_4_2_1 = pd.concat([gfi_table_a_long, gfi_table_c_long, gfi_table_e_long, gfi_table_g_long])
    
    return indicator4_4_2_1


# indicator 4.4.2.2
def get_4_4_2_2():
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
    
    indicator4_4_2_2 = pd.concat([imf_isora_df_1_long, imf_isora_df_2_long])

    return indicator4_4_2_2


# indicator 4.4.2.3
def get_4_4_2_3():

    # get druge prices and seizures data
    drug_prices_df = pd.read_excel('data/unodc drug prices.xlsx', skiprows=1, engine='openpyxl', sheet_name='Prices in USD')
    drug_seizures_df = pd.read_excel('data/unodc drug seizures.xlsx', skiprows=1, engine='openpyxl', sheet_name='Export')

    # filter drug prices data and convert units
    filtered_prices_df = drug_prices_df[drug_prices_df['Unit'].isin(['Grams', 'Kilograms'])].copy()
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
    indicator4_4_2_3['indicator description'] = 'The amount of drugs seized in kilograms multiplied by the drug price in kilograms. Exlcludes all siezures not measured in grams or kilograms.'
    indicator4_4_2_3['indicatore code'] = 'Monetary losses (in USD) to drug sales'

    return indicator4_4_2_3


# indicator 4.4.2.4 
def get_4_4_2_4():
    wb_corruption_score = wb.data.DataFrame('CC.EST', wb.region.members('AFR'), db=3).reset_index().melt(id_vars=['economy'], var_name='year', value_name='wb corruption score').rename(columns={'economy': 'iso3'})
    wb_corruption_score['year'] = wb_corruption_score['year'].str.replace('YR', '')
    wb_corruption_score['wb normalized corruption score'] = wb_corruption_score.groupby('year')['wb corruption score'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    wb_corruption_score['wb corruption score weight'] = wb_corruption_score['wb normalized corruption score']
    total_weights = wb_corruption_score.groupby('year')['wb corruption score weight'].sum().reset_index()
    total_weights = total_weights.rename(columns={'wb corruption score weight': 'wb corruption score total weight'})
    wb_corruption_score = wb_corruption_score.merge(total_weights, on='year')

    wb_corruption_score['wb corruption score country share'] = (wb_corruption_score['wb corruption score weight'] / wb_corruption_score['wb corruption score total weight']) * 148

    wjp_absence_of_corruption = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country Code', 'Year', 'Factor 2: Absence of Corruption']].rename(columns={'Country Code': 'iso3', 'Year': 'year'})
    wjp_absence_of_corruption['year'] = wjp_absence_of_corruption['year'].astype(str)

    def expand_years(row):
        if '-' in row['year']:
            start, end = map(int, row['year'].split('-'))
            return [{'iso3': row['iso3'], 'year': year, 'Factor 2: Absence of Corruption': row['Factor 2: Absence of Corruption']}
                    for year in range(start, end + 1)]
        else:
            return [row]
        
    wjp_absence_of_corruption_expanded = pd.DataFrame([entry for row in wjp_absence_of_corruption.to_dict(orient='records') for entry in expand_years(row)])

    """ 
        TODO: add afrobarometer data and calculate indicator 4.4.2.4
        Afrobarometer data is stored as .sav files right now, and I cant figure out how to convert them to csv.
        Theres a command line tool and an online tool but neither have worked for me.
    """

    indicator4_4_2_4 = pd.merge(wb_corruption_score, wjp_absence_of_corruption_expanded, on=['iso3', 'year'], how='left')
    indicator4_4_2_4 = pd.melt(indicator4_4_2_4, id_vars=['iso3', 'year'], var_name='indicator description', value_name='value')

    return indicator4_4_2_4


######################################################################################
# indicator 4.4.3.1 has several indicators
def get_4_4_3_1b():
    wjp_rule_of_law = pd.read_excel('C:/Users/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'WJP Rule of Law Index: Overall Score']]
get_4_4_3_1b()
# Function to get and save Rule of Law & Justice indicator - Mo Ibrahim
def get_4_4_3_1c():
   def get_4_4_3_1c():
    rule_of_law_justice = pd.read_csv('mo ibrahim rule of law - score and rank.csv')[['Country', 'Year', 'Rule of Law & Justice (score and rank)']]
get_4_4_3_1c()
# Function to get and save Reduce Corruption indicator - World Bank CPIA
def get_4_4_3_1d():
    cpia_reduce_corruption = wb.data.DataFrame('IQ.CPA.PUBS.XQ', wb.region.members('AFR'), db=31)
    cpia_reduce_corruption.to_csv('4.4.3.1d_Reduce_Corruption.csv', index=False)
get_4_4_3_1d()
# Function to get and save Sound Institutions indicator - World Bank CPIA
def get_4_4_3_1e():
    cpia_sound_institutions = wb.data.DataFrame('IQ.CPA.TRAN.XQ', wb.region.members('AFR'), db=31)
    cpia_sound_institutions.to_csv('4.4.3.1e_Sound_Institutions.csv', index=False)

# Function to get and save Identity Documentation indicator - World Bank ID4D
def get_4_4_3_1f():
    id4d_identity_documentation = wb.data.DataFrame('SP.REG.BRTH.ZS', wb.region.members('AFR'), db=89)
    id4d_identity_documentation.to_csv('4.4.3.1f_Identity_Documentation.csv', index=False)
get_4_4_3_1f()
# Function to get and save Public Access to Information indicator - World Justice Project
def get_4_4_3_1g():
    public_access_information = pd.read_excel('C:/Users/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 3: Open Government']]
    public_access_information.to_csv('4.4.3.1g_Public_Access_to_Information.csv', index=False)
get_4_4_3_1g()
# Function to get and save Institutions to Combat Crime indicator - World Justice Project
def get_4_4_3_1h():
    institutions_combat_crime = pd.read_excel('C:/Users/wjp rule of law.xlsxx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 5: Order and Security', 'Factor 7: Civil Justice', 'Factor 8: Criminal Justice']]
    institutions_combat_crime.to_csv('4.4.3.1h_Institutions_to_Combat_Crime.csv', index=False)
get_4_4_3_1h()


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
    return indicator4_4_3_2


# indicator 4.4.4.2
def get_4_4_4_2():

    tjn_df = pd.read_csv('data/tjn data.csv').rename(columns={'country_name': 'Country'}).drop(columns=['cthi_2019_score', 'cthi_2021_score', 'cthi_2019_rank', 'cthi_2021_rank', 'cthi_2019_share', 'cthi_2021_share', 'sotj20_loss_corp_musd', 'sotj21_loss_corp_musd', 'sotj23_loss_corp_musd', 'sotj20_loss_total_share_healthexpenses', 'sotj21_loss_total_share_healthexpenses', 'sotj23_loss_total_musd', 'sotj23_loss_total_share_healthexpenses'])
    tjn_df_long = pd.melt(tjn_df, id_vars=['Country', 'iso3'], var_name='year', value_name='value')
    tjn_df_long['year'] = tjn_df_long['year'].str.extract(r'(\d{4})')
    tjn_df_long['indicator code'] = 'FSI'
    tjn_df_long['indicator description'] = 'Financial Secrecy Index'

    return tjn_df_long


# indicator 4.4.5.1 
def get_4_4_5_1():

    # read in data and extract indicators
    usaid_df = pd.read_excel('data/USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_4_5_1 = usaid_df[['country_name', 'country_id', 'year', 'Tax buoyancy [by_tax]']].rename(columns={"country_name": 'country', 'country_id': 'm49', 'Tax buoyancy [by_tax]': 'value'})
    indicator4_4_5_1['indicator code'] = "Tax buoyancy [by_tax]"
    indicator4_4_5_1['indicator description'] = "Tax buoyancy [by_tax]"

    return indicator4_4_5_1


# indicator 4.4.5.2
def get_4_4_5_2():

    # get tax justice network data
    df_unilateralCross_url = "https://data.taxjustice.net/api/data/download?dataset=unilateral_cross&keys=country_name%2Ciso3&variables=fsi_2011_value%2Cfsi_2013_value%2Cfsi_2015_value%2Cfsi_2018_value%2Cfsi_2020_value%2Cfsi_2022_value%2Cfsi_2011_gsw%2Cfsi_2013_gsw%2Cfsi_2015_gsw%2Cfsi_2018_gsw%2Cfsi_2020_gsw%2Cfsi_2022_gsw%2Cfsi_2011_rank%2Cfsi_2013_rank%2Cfsi_2015_rank%2Cfsi_2018_rank%2Cfsi_2020_rank%2Cfsi_2022_rank%2Cfsi_2011_score%2Cfsi_2013_score%2Cfsi_2015_score%2Cfsi_2018_score%2Cfsi_2020_score%2Cfsi_2022_score&format=csv&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ4OTQsInR5cGUiOiJkb3dubG9hZCIsImlhdCI6MTcyNjY5MDE2MSwiZXhwIjoxNzI2NjkxOTYxfQ.Hf8ycDkeciGz6WxNhWXriuFMBL5GZnp52lpeNPFg8Q0"
    df_unilateralCross = pd.read_csv(df_unilateralCross_url)

    # TODO: figure out why Pandas cant parse df

    return df_unilateralCross


# TODO: indicator 4.4.6.1 
""" NEED TO REGISTER WITH GOLD MINING DATABASE - WE DON'T NEED TO WORRY ABOUT THIS ONE FOR NOW """


if __name__ == '__main__':

    # df_4_3_1_1 = get_4_3_1_1().to_csv("indicator_data_files/indicator 4.3.1.1.csv")

    # df_4_3_1_2 = get_4_3_1_2().to_csv("indicator_data_files/indicator 4.3.1.2.csv")

    # df_4_3_1_3 = get_4_3_1_3().to_csv("indicator_data_files/indicator 4.3.1.3.csv")

    # df_4_3_2_1 = get_4_3_2_1().to_csv("indicator_data_files/indicator 4.3.2.1.csv")

    # df_4_3_2_2 = get_4_3_2_2().to_csv("indicator_data_files/indicator 4.3.2.2.csv")

    # df_4_4_2_1 = get_4_4_2_1().to_csv("indicator_data_files/indicator 4.4.2.1.csv")

    # df_4_4_2_2 = get_4_4_2_2().to_csv("indicator_data_files/indicator 4.4.2.2.csv")

    # df_4_4_2_3 = get_4_4_2_3().to_csv("indicator_data_files/indicator 4.4.2.3.csv")

    # df_4_4_2_4 = get_4_4_2_4().to_csv("indicator_data_files/indicator 4.4.2.4.csv")

    # df_4_4_3_2 = get_4_4_3_2().to_csv("indicator_data_files/indicator 4.4.3.2.csv")

    # df_4_4_4_2 = get_4_4_4_2().to_csv("indicator_data_files/indicator 4.4.4.2.csv")

    # df_4_4_5_1 = get_4_4_5_1().to_csv("indicator_data_files/indicator 4.4.5.1.csv")

    exit()