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