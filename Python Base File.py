
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# In[60]:


# Load the compounds annotation dataset
compounds = pd.read_csv('https://drive.google.com/uc?id=1EQvydk1MxbXF72_zVyUQHHPlvp7slqoN&export=download')


# In[61]:


# Load the GDSC dataset
gdsc = pd.read_csv('https://drive.google.com/uc?id=1DJT1BFqwCjA8uipkSbENFftKU0_O-AK4&export=download',low_memory=False)


# In[62]:


# Load the GDSC2 dataset
gdsc2 = pd.read_csv('https://drive.google.com/uc?id=1e8iHLMOVHrweM_rhKKBi93mOx8tYyMln&export=download',low_memory=False)


# In[63]:


# Load the Cell Line Details Dataset
cell_lines_details = pd.read_csv('https://drive.google.com/uc?id=1ypE6lK8D1LcrG8IrMiRJqTxrBEdZH3LZ&export=download',low_memory=False)


# In[64]:


# Load the Cosmic tissue Classification dataset
cosmic_tissue_classification = pd.read_csv('https://drive.google.com/uc?id=18fe6RRo-DAli112jzCt6OcYIoiAFyvYl&export=download',low_memory=False)


# In[65]:


# Load the Decode sheet dataset
decode_sheet = pd.read_csv('https://drive.google.com/uc?id=1MBJpLBls56JzqXntLyqN0IUQ-AFuyeQs&export=download',header=1,low_memory=False)


# In[66]:


# Converting into DataFrame.
compounds_df = pd.DataFrame(compounds)
gdsc_df = pd.DataFrame(gdsc)
gdsc2_df = pd.DataFrame(gdsc2)
cell_lines_details_df = pd.DataFrame(cell_lines_details)
cosmic_tissue_classification_df = pd.DataFrame(cosmic_tissue_classification)
decode_sheet_df = pd.DataFrame(decode_sheet)


# In[67]:


#Step 1: Check the first few rows of each dataset.
gdsc_df.head()
gdsc2_df.head()
compounds_df.head()   # For compounds annotations
cell_lines_details_df.head()  # For Sheet 1
cosmic_tissue_classification_df.head()  # For Sheet 2
decode_sheet_df.head()   # For Sheet 3


# In[68]:


#Step 2: Check for the data types and basic statistics.
print(gdsc_df.info())
print(gdsc2_df.info())
print(compounds_df.info())
print(cell_lines_details_df.info())
print(cosmic_tissue_classification_df.info())
print(decode_sheet_df.info())


# In[77]:


## Identify missing values
print("Missing values in GDSC DataFrame:\n", gdsc_df.isnull().sum())
print("Missing values in GDSC2 DataFrame:\n", gdsc2_df.isnull().sum())
print("Missing values in Compounds DataFrame:\n", compounds_df.isnull().sum())
print("Missing values in Cell Lines Details DataFrame(Sheet 1):\n", cell_lines_details_df.isnull().sum())
print("Missing values in Cosmic Tissue Classification DataFrame(Sheet 2):\n", cosmic_tissue_classification_df.isnull().sum())
print("Missing values in Decode DataFrame(Sheet 3):\n", decode_sheet_df.isnull().sum())


# In[70]:


# Dropping rows with excessive missing values (e.g., over 50%)
gdsc_df_cleaned = gdsc_df.dropna(thresh=len(gdsc_df.columns) * 0.5)
gdsc2_df_cleaned = gdsc2_df.dropna(thresh=len(gdsc2_df.columns) * 0.5)
compounds_df_cleaned = compounds_df.dropna(thresh=len(compounds_df.columns) * 0.5)
cell_lines_details_df_cleaned = cell_lines_details_df.dropna(thresh=len(cell_lines_details_df.columns) * 0.5)
cosmic_tissue_classification_df_cleaned = cosmic_tissue_classification_df.dropna(thresh=len(cosmic_tissue_classification_df.columns) * 0.5)
decode_sheet_df_cleaned = decode_sheet_df.dropna(thresh=len(decode_sheet_df.columns) * 0.5)


# In[71]:


# Remove duplicates from the cleaned DataFrames
gdsc_df_cleaned = gdsc_df_cleaned.drop_duplicates()
gdsc2_df_cleaned = gdsc2_df_cleaned.drop_duplicates()
compounds_df_cleaned = compounds_df_cleaned.drop_duplicates()
cell_lines_details_df_cleaned = cell_lines_details_df_cleaned.drop_duplicates()
cosmic_tissue_classification_df_cleaned = cosmic_tissue_classification_df_cleaned.drop_duplicates()
decode_sheet_df_cleaned = decode_sheet_df_cleaned.drop_duplicates()


# In[72]:


# Optionally, We can check the number of duplicates removed
print(f"Duplicates removed from gdsc_df_cleaned: {gdsc_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from gdsc2_df_cleaned: {gdsc2_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from compounds_df_cleaned: {compounds_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from cell_lines_details_cleaned: {cell_lines_details_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from cosmic_tissue_classification_df_cleaned: {cosmic_tissue_classification_df_cleaned.duplicated().sum()}")
print(f"Duplicates removed from decode_sheet_df_cleaned: {decode_sheet_df_cleaned.duplicated().sum()}")


# In[75]:


# Function to replace NaN values and show the replaced values
def replace_nan_and_show_replacements(df):
    replaced_values = {}
    for column in df.columns:
        # Identify rows where NaN values are present in the column
        replaced_rows = df[df[column].isna()].copy()
        
        # Store the first 5 rows of replaced values and what they are replaced with
        if not replaced_rows.empty:
            replaced_rows[f"Replaced with"] = f"Unknown ({column})"
            replaced_values[column] = replaced_rows[[column]].head(5)
        
        # Replace NaN values with "Unknown (Column header)"
        df[column] = df[column].fillna(f"Unknown {column}")
    
    return df, replaced_values

# Apply the function and store the replaced values
replaced_values_all = {}

gdsc_df_cleaned, replaced_values_gdsc = replace_nan_and_show_replacements(gdsc_df_cleaned)
replaced_values_all['gdsc_df_cleaned'] = replaced_values_gdsc

gdsc2_df_cleaned, replaced_values_gdsc2 = replace_nan_and_show_replacements(gdsc2_df_cleaned)
replaced_values_all['gdsc2_df_cleaned'] = replaced_values_gdsc2

compounds_df_cleaned, replaced_values_compounds = replace_nan_and_show_replacements(compounds_df_cleaned)
replaced_values_all['compounds_df_cleaned'] = replaced_values_compounds

cell_lines_details_df_cleaned, replaced_values_cell_lines = replace_nan_and_show_replacements(cell_lines_details_df_cleaned)
replaced_values_all['cell_lines_details_df_cleaned'] = replaced_values_cell_lines

cosmic_tissue_classification_df_cleaned, replaced_values_cosmic = replace_nan_and_show_replacements(cosmic_tissue_classification_df_cleaned)
replaced_values_all['cosmic_tissue_classification_df_cleaned'] = replaced_values_cosmic

decode_sheet_df_cleaned, replaced_values_decode = replace_nan_and_show_replacements(decode_sheet_df_cleaned)
replaced_values_all['decode_sheet_df_cleaned'] = replaced_values_decode

# Print 5 replaced values from each column along with what they were replaced with
for df_name, replaced_values in replaced_values_all.items():
    print(f"Replaced values in {df_name}:\n")
    for column, values in replaced_values.items():
        print(f"Column: {column}")


# In[79]:


## Identify missing values
print("Missing values in GDSC DataFrame:\n", gdsc_df_cleaned.isnull().sum())
print("Missing values in GDSC2 DataFrame:\n", gdsc2_df_cleaned.isnull().sum())
print("Missing values in Compounds DataFrame:\n", compounds_df_cleaned.isnull().sum())
print("Missing values in Cell Lines Details DataFrame(Sheet 1):\n", cell_lines_details_df_cleaned.isnull().sum())
print("Missing values in Cosmic Tissue Classification DataFrame(Sheet 2):\n", cosmic_tissue_classification_df_cleaned.isnull().sum())
print("Missing values in Decode DataFrame(Sheet 3):\n", decode_sheet_df_cleaned.isnull().sum())




# In[33]:


# Optionally, We can check the number of duplicates removed


# In[34]:



from dotenv import load_dotenv
import os
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
load_dotenv()

# Connection parameters
host = os.getenv("HOST")  # Change if you're connecting remotely
user = os.getenv("USER")  # Your MySQL username
password = os.getenv("PASSWORD")  # Your MySQL password
database = os.getenv("DATABASE")  # The database name you want to connect to

tables = {
    "gdsc": gdsc_df_cleaned,
    "gdsc2": gdsc2_df_cleaned,
    "Compund": compounds_df_cleaned,
    "Cell_lines": cell_lines_details_df_cleaned,
    "Cosmic_tissue_classification": cosmic_tissue_classification_df_cleaned,
    "decode": decode_sheet_df_cleaned
}

# Create engine
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Using a context manager to handle the connection and transactions
try:
    with engine.begin() as connection:  # use begin() for transactional support
        for table_name, df in tables.items():
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
except sqlalchemy.exc.SQLAlchemyError as e:
    # SQLAlchemyError is a base exception for sqlalchemy-related errors
    print(f"An error occurred: {e}")



