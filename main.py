import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype

# variables month and year
month = 3
year = 2023
day = 10

# file paths
hc_geral = "/mnt/c/Users/luizl/repos/spar/pdi_rv_project/hc/hc_geral_adm.xlsx"
cargos = "/mnt/c/Users/luizl/repos/spar/pdi_rv_project/hc/cargos_de_para.xlsx"


#save file
save = "/mnt/c/Users/luizl/repos/spar/pdi_rv_project/hc/teste.csv"

# HC Clean
df = pd.read_excel(hc_geral, engine="openpyxl", sheet_name=0)
df_cargos = pd.read_excel(cargos, engine="openpyxl", sheet_name=0)

# Create a column ultima data de demissão
df['demissao'] = df.apply(lambda x : x['DATA DESLIGAMENTO CLT'] if x['STATUS'] == 'DESLIGADO' and pd.notnull(x['DATA DESLIGAMENTO CLT']) else 
                            x['DATA DESLIGAMENTO TEMP.'] if x['STATUS'] == 'DESLIGADO' and pd.notnull(x['DATA DESLIGAMENTO TEMP.']) else
                            np.nan, axis=1)

# remove unused columns
df = df.iloc[:,[0, 1, 4, 9, 19, 20, 21, 22, 25, 29, 32, -1]]

# remove - and . from CPF column
df['CPF'] = df['CPF'].str.replace(".", '', regex= False)
df['CPF'] = df['CPF'].str.replace("-", '', regex= False)

# remove extra regions
df['MICRO REGIONAL'] = df['MICRO REGIONAL'].apply(
    lambda x : 
    x[:x.find(',')] if x.find(',') > 0 else x
)

# remove extra cargo
df['CARGO'] = df['CARGO'].apply(
    lambda x : 
    x[:x.find('/')] if x.find('/') > 0 else x
)

# trim all columns
for columns in df.columns:
    if is_string_dtype(df[columns]):
        df[columns] = df[columns].str.strip()
    else:
        df[columns] = df[columns]

df = df.merge(
    df_cargos, how='left', left_on='CARGO', right_on='CARGOS NOVOS', suffixes=(False, False)
)

df.to_csv(save, encoding='utf-8-sig', sep=';')