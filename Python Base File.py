#!/usr/bin/env python
# coding: utf-8

# In[15]:



# In[16]:


import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# In[17]:


# Load the compounds annotation dataset
compounds = pd.read_csv('https://drive.google.com/uc?id=1EQvydk1MxbXF72_zVyUQHHPlvp7slqoN&export=download')


# In[18]:


# Load the GDSC dataset
gdsc = pd.read_csv('https://drive.google.com/uc?id=1DJT1BFqwCjA8uipkSbENFftKU0_O-AK4&export=download',low_memory=False)


# In[19]:


# Load the GDSC2 dataset
gdsc2 = pd.read_csv('https://drive.google.com/uc?id=1e8iHLMOVHrweM_rhKKBi93mOx8tYyMln&export=download',low_memory=False)


# In[20]:


# Load the Cell Line Details Dataset
cell_lines_details = pd.read_csv('https://drive.google.com/uc?id=1ypE6lK8D1LcrG8IrMiRJqTxrBEdZH3LZ&export=download',low_memory=False)


# In[21]:


# Load the Cosmic tissue Classification dataset
cosmic_tissue_classification = pd.read_csv('https://drive.google.com/uc?id=18fe6RRo-DAli112jzCt6OcYIoiAFyvYl&export=download',low_memory=False)


# In[22]:


# Load the Decode sheet dataset
decode_sheet = pd.read_csv('https://drive.google.com/uc?id=1MBJpLBls56JzqXntLyqN0IUQ-AFuyeQs&export=download',header=1,low_memory=False)


# In[23]:


# Converting into DataFrame.
compounds_df = pd.DataFrame(compounds)
gdsc_df = pd.DataFrame(gdsc)
gdsc2_df = pd.DataFrame(gdsc2)
cell_lines_details_df = pd.DataFrame(cell_lines_details)
cosmic_tissue_classification_df = pd.DataFrame(cosmic_tissue_classification)
decode_sheet_df = pd.DataFrame(decode_sheet)


# In[25]:


#Step 2: Check for the data types and basic statistics.
print(gdsc_df.info())
print(gdsc2_df.info())
print(compounds_df.info())
print(cell_lines_details_df.info())
print(cosmic_tissue_classification_df.info())
print(decode_sheet_df.info())


# In[26]:


## Identify missing values
print("Missing values in GDSC DataFrame:\n", gdsc_df.isnull().sum())
print("Missing values in GDSC2 DataFrame:\n", gdsc2_df.isnull().sum())
print("Missing values in Compounds DataFrame:\n", compounds_df.isnull().sum())
print("Missing values in Cell Lines Details DataFrame(Sheet 1):\n", cell_lines_details_df.isnull().sum())
print("Missing values in Cosmic Tissue Classification DataFrame(Sheet 2):\n", cosmic_tissue_classification_df.isnull().sum())
print("Missing values in Decode DataFrame(Sheet 3):\n", decode_sheet_df.isnull().sum())


# In[27]:


# Dropping rows with excessive missing values (e.g., over 50%)
gdsc_df_cleaned = gdsc_df.dropna(thresh=len(gdsc_df.columns) * 0.5)
gdsc2_df_cleaned = gdsc2_df.dropna(thresh=len(gdsc2_df.columns) * 0.5)
compounds_df_cleaned = compounds_df.dropna(thresh=len(compounds_df.columns) * 0.5)
cell_lines_details_df_cleaned = cell_lines_details_df.dropna(thresh=len(cell_lines_details_df.columns) * 0.5)
cosmic_tissue_classification_df_cleaned = cosmic_tissue_classification_df.dropna(thresh=len(cosmic_tissue_classification_df.columns) * 0.5)
decode_sheet_df_cleaned = decode_sheet_df.dropna(thresh=len(decode_sheet_df.columns) * 0.5)


# In[28]:


# Filling missing numeric values with median
gdsc_df_cleaned.loc[:, 'LN_IC50'] = gdsc_df_cleaned['LN_IC50'].fillna(gdsc_df_cleaned['LN_IC50'].median())
gdsc_df_cleaned.loc[:, 'AUC'] = gdsc_df_cleaned['AUC'].fillna(gdsc_df_cleaned['AUC'].median())

gdsc2_df_cleaned.loc[:, 'LN_IC50'] = gdsc2_df_cleaned['LN_IC50'].fillna(gdsc2_df_cleaned['LN_IC50'].median())
gdsc2_df_cleaned.loc[:, 'AUC'] = gdsc2_df_cleaned['AUC'].fillna(gdsc2_df_cleaned['AUC'].median())


# In[29]:


# Remove duplicates from the cleaned DataFrames
gdsc_df_cleaned = gdsc_df_cleaned.drop_duplicates()
gdsc2_df_cleaned = gdsc2_df_cleaned.drop_duplicates()
compounds_df_cleaned = compounds_df_cleaned.drop_duplicates()
cell_lines_details_df_cleaned = cell_lines_details_df_cleaned.drop_duplicates()
cosmic_tissue_classification_df_cleaned = cosmic_tissue_classification_df_cleaned.drop_duplicates()
decode_sheet_df_cleaned = decode_sheet_df_cleaned.drop_duplicates()


# In[30]:


# Optionally, We can check the number of duplicates removed
print(f"Duplicates removed from gdsc_df_cleaned: {gdsc_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from gdsc2_df_cleaned: {gdsc2_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from compounds_df_cleaned: {compounds_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from cell_lines_details_cleaned: {cell_lines_details_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from cosmic_tissue_classification_df_cleaned: {cosmic_tissue_classification_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from decode_sheet_df_cleaned: {decode_sheet_df_cleaned.duplicated().sum()}")


# In[31]:
### Merging

#1. Merge gdsc_df_cleaned with gdsc2_df_cleaned:
#Common columns: DRUG_ID, COSMIC_ID
#We'll use an inner join to keep only matching entries.

merged_df = pd.merge(gdsc_df_cleaned, gdsc2_df_cleaned, on=['DRUG_ID', 'COSMIC_ID'], how='inner')
print(f"Merged gdsc_df_cleaned and gdsc2_df_cleaned shape: {merged_df.shape}")


# In[32]:


#2.Merge the result with compounds_df_cleaned:
# Common column: DRUG_ID
# We'll use an inner join to merge based on DRUG_ID.

merged_df = pd.merge(merged_df, compounds_df_cleaned, on='DRUG_ID', how='inner')
print(f"Merged with compounds_df_cleaned shape: {merged_df.shape}")


# In[33]:


#3. Merge with cell_lines_details_cleaned:
# Common columns: COSMIC_ID (you mentioned 'COSMIC identifier')
# We'll match on COSMIC_ID from previous merges and COSMIC identifier in cell_lines_details_cleaned.

merged_df = pd.merge(merged_df, cell_lines_details_df_cleaned, left_on='COSMIC_ID', right_on='COSMIC identifier', how='inner')
print(f"Merged with cell_lines_details_df_cleaned shape: {merged_df.shape}")


# In[34]:


#4. Merge with cosmic_tissue_classification_df_cleaned:
# Common column: COSMIC_ID
# We'll match on COSMIC_ID.

merged_df = pd.merge(merged_df, cosmic_tissue_classification_df_cleaned, on='COSMIC_ID', how='inner')
print(f"Merged with cosmic_tissue_classification_df_cleaned shape: {merged_df.shape}")


# In[35]:


#5. Merge with decode_clean_sheet
# Common column: TCGA label
# We will match on 'TCGA label'

merged_df = pd.merge(merged_df, decode_sheet_df_cleaned, left_on='TCGA_DESC_x', right_on='TCGA Label', how='left')
print(f"Merged with decode_sheet_df_cleaned shape: {merged_df.shape}")


# In[37]:


# Check for duplicates
duplicate_count = merged_df.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")

# Check for NaN values
nan_counts = merged_df.isna().sum()
print("NaN values in each column:\n", nan_counts)


# In[38]:


#1. Replace null values in the TARGET_x & TARGET_y column with "Unknown Target"
merged_df['TARGET_x'] = merged_df['TARGET_x'].fillna('Unknown Target')
merged_df['TARGET_y'] = merged_df['TARGET_y'].fillna('Unknown Target')


# In[39]:


# Replace null values in the GDSC Tissue descriptor 1 & GDSC Tissue descriptor 2 column with "Unknown Target"
merged_df['GDSC Tissue descriptor 1'] = merged_df['GDSC Tissue descriptor 1'].fillna('Unknown Tissue Origin')
merged_df['GDSC Tissue descriptor 2'] = merged_df['GDSC Tissue descriptor 2'].fillna(' Tissue Orgin')


# In[40]:


# Merge the two specified columns into a single columns
merged_df['TCGA_Label_1 (Description)'] = merged_df['Cancer Type (matching TCGA label)'].fillna(merged_df['TCGA_DESC_x'])

# Drop the old columns
merged_df.drop(columns=['TCGA_DESC_x', 'Cancer Type (matching TCGA label)'], inplace=True)

# Display the updated DataFrame to see the new merged column
print(merged_df.head())


# In[41]:


# Merge the specified columns into a new column
merged_df['TCGA_Label_2 (Description)'] = merged_df['Cancer Type\n(matching TCGA label)'].fillna(merged_df['TCGA_DESC_y'])

# Drop the old columns
merged_df.drop(columns=['TCGA_DESC_y', 'Cancer Type\n(matching TCGA label)'], inplace=True)

# Display the updated DataFrame to see the new merged column
print(merged_df.head()) 


# In[42]:


# Drop the SYNONYMS column
merged_df = merged_df.drop(columns=['SYNONYMS'])


# In[43]:


# Replace null values in specified columns
merged_df['Microsatellite instability Status (MSI)'].fillna("Unknown MSI", inplace=True)
merged_df['Screen Medium_x'].fillna("Unknown Screen Medium", inplace=True)
merged_df['Growth Properties_x'].fillna("Unknown Growth Properties", inplace=True)
merged_df['CNA'].fillna("Unknown CNA", inplace=True)
merged_df['Gene Expression_x'].fillna("Unknown Gene Expression", inplace=True)
merged_df['Methylation_x'].fillna("Unknown Methylation", inplace=True)
merged_df['Microsatellite \ninstability Status (MSI)'].fillna("Unknown MSI", inplace=True)
merged_df['TCGA Label'].fillna("Unknown TCGA Label", inplace=True)
merged_df['Definition'].fillna("Unknown Definition", inplace=True)
merged_df['TCGA_Label_1 (Description)'].fillna("Unknown TCGA_Label_1 (Description)", inplace=True)
merged_df['TCGA_Label_2 (Description)'].fillna("Unknown TCGA_Label_2 (Description)", inplace=True)

# Display the updated DataFrame to verify changes
print(merged_df.head())


# In[44]:


# Checking the Percentage of Missing Values
# Percentage of missing values for each column

missing_percentage = merged_df.isnull().mean() * 100
print(missing_percentage[missing_percentage > 0])


# In[45]:


# Remove '_x' and '_y' from column names
merged_df.columns = merged_df.columns.str.replace('_x', '', regex=False).str.replace('_y', '', regex=False)

# Display the updated DataFrame columns
print(merged_df.columns.tolist())

