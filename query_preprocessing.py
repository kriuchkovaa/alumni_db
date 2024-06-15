""" Use this script to pre-process Peoplesoft queries """

# MAKE SURE YOU UPDATE sbm_pref AND unsorted_pref AS NEED ARISES

# Load required dependencies
import pandas as pd 

# Read the xlsx file 
df = pd.read_excel("1213 query.xlsx", header = 1)

# Specify acceptable values for SBM degrees
sbm_pref = ["5BAM", "5BSCJ", "5BSHA", "5BSPM", "7MSHA", "7BA", "7PM", "7PA", "7DBA", "7MACC", "7MSML"]

# Specify values that need to be verified 
unsorted_pref = ["1CT", "3AS", "5BS", "6CT", "7MS"]

# Filter out required degree values
df = df.loc[df['Degree'].isin(sbm_pref) | df['Degree'].isin(unsorted_pref)]

# Merge emails for each unique name
fun = {'Email': ', '.join}
df = df.groupby(['Name', 'Degree'], as_index = False).aggregate(fun)

# Verify if there are any duplicates
duplicates = df[df.duplicated(subset = ['Name'])]
print(df[df['Name'].isin(duplicates.Name).values])

# Replace degree codes with comprehensive names
degrees = {'1CT': 'UGCert', '6CT': 'GradCert', '3AS': 'Associate unspecified', 
           '5BS': 'BS unspecified', '7MS': 'MS unspecified', '5BAM': 'BAM', 
           '5BSCJ': 'BSCJ', '5BSHA': 'BSHA', '7MSHA': 'MSHA', '7BA': 'MBA',
           '7PM': 'MSPM', '7PA': 'MPA', '7DBA': 'DBA', '5BSPM': 'BSPM', '7MACC': 'MPA', 
           '7MSML': 'MSML'}

df['Degree'] = df['Degree'].replace(degrees)

# Customize and save to Excel
writer = pd.ExcelWriter('./Adjusted/1213 updated.xlsx')                    
df.to_excel(writer, sheet_name = 'Clean Data', index = False, na_rep = 'NaN')

for column in df:
    column_width = max(df[column].astype(str).map(len).max(), len(column))
    col_idx = df.columns.get_loc(column)
    writer.sheets['Clean Data'].set_column(col_idx, col_idx, column_width)

writer.save()
