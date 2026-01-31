import pandas as pd
import os

# Define file paths
input_file = r'e:\OneDrive - hoaphat.com.vn\Code\alu-temp-cast-ml\01-data\TSC_clean.csv'
output_file = r'e:\OneDrive - hoaphat.com.vn\Code\alu-temp-cast-ml\01-data\TSC_SAE1006AL_2025.csv'

print(f"Reading {input_file}...")
try:
    df = pd.read_csv(input_file)
    print(f"Total rows: {len(df)}")

    # 1. Filter by Steel Grade (Mac Thep) containing 'SAE1006AL'
    # Checking both STEEL_GRADE_NAME and FINAL_STEEL_GRADE_NAME just in case, but usually STEEL_GRADE_NAME is sufficient.
    # User mentioned 'Mac Thep'.
    
    # Ensure string type for filtering logic
    df['STEEL_GRADE_NAME'] = df['STEEL_GRADE_NAME'].astype(str)
    
    # Filter
    grade_mask = df['STEEL_GRADE_NAME'].str.contains('SAE1006AL', case=False, na=False)
    df_filtered_grade = df[grade_mask]
    
    print(f"Rows after grade filter ('SAE1006AL'): {len(df_filtered_grade)}")

    # 2. Filter by Year 2025
    # Using START_DATE as the reference date
    df_filtered_grade['START_DATE'] = pd.to_datetime(df_filtered_grade['START_DATE'], errors='coerce')
    
    # Drop rows where date parsing failed (if any) - optional but good for data integrity
    df_filtered_grade = df_filtered_grade.dropna(subset=['START_DATE'])
    
    year_mask = df_filtered_grade['START_DATE'].dt.year == 2025
    df_final = df_filtered_grade[year_mask]
    
    print(f"Rows after year 2025 filter: {len(df_final)}")

    # 3. Save to file
    if len(df_final) > 0:
        df_final.to_csv(output_file, index=False)
        print(f"Successfully saved {len(df_final)} rows to {output_file}")
    else:
        print("No data found matching criteria. Output file not created.")

except Exception as e:
    print(f"An error occurred: {e}")
