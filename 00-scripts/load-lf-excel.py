import pandas as pd
import os
import argparse
import sys
import re


def parse_filename(filename):
    """
    Parse filename to extract year, month, and LF number.
    Example: '25.12.LF2.xlsx' -> year=2025, month=12, lf=2
    """
    basename = os.path.basename(filename)
    # Pattern: YY.MM.LFXX.xlsx
    pattern = r'(\d{2})\.(\d{1,2})\.LF(\d+)'
    match = re.search(pattern, basename, re.IGNORECASE)
    
    if match:
        year = 2000 + int(match.group(1))  # Convert YY to YYYY
        month = int(match.group(2))
        lf_number = int(match.group(3))
        return year, month, lf_number
    else:
        print(f"Warning: Could not parse filename '{basename}'. Using defaults.")
        return None, None, None

def process_file(input_path):
    """
    Process LF Excel file and return a DataFrame.
    Extracts year, month, and LF number from filename.
    """
    if not os.path.exists(input_path):
        print(f"Warning: File '{input_path}' not found. Skipping.")
        return None

    print(f"Processing file: {input_path}")
    
    # Parse filename for metadata
    source_year, source_month, source_lf = parse_filename(input_path)

    # Define column names
    cols = [
        'stt', 'ngay', 'Ca', 'me_tinh_luyen_so', 'mac_thep_yeu_cau',
        'thoi_gian_vao_tinh_luyen', 'bat_dau', 'ket_thuc', 'thoi_gian_len_duc',
        'thung_lf', 'lan_luyen_thu', 'nhiet_do_vao_tl', 'C_truoc', 'Si_truoc',
        'Mn_truoc', 'S_truoc', 'P_truoc', 'khoi_luong_thung_thep', 'FeSi', 'FeMn',
        'SiMn', 'than', 'FeCr', 'FeV', 'Niken', 'FeP', 'Cu', 'khac', 'huynh_thach',
        'nhom_thoi', 'voi_song', 'dolomite', 'quaczit', 'day_feca', 'day_casi',
        'day_ca_dac', 'xi_bao_on', 'thoi_gian_danh_dien', 'tieu_thu_dien', 'C_sau',
        'Si_sau', 'Mn_sau', 'S_sau', 'P_sau', 'Al', 'Canxi', 'nhiet_do_lan_1',
        'nhiet_do_ra_thep', 'nhiet_do_duc_yeu_cau', 'nhiet_do_do_tren_duc',
        'thoi_gian_dinh_tre', 'ly_do_dinh_tre', 'ghi_chu_1',
        'thoi_gian_bat_dau_thoi_mem', 'thoi_gian_ket_thu_thoi_mem', 'tong_thoi_gian_thoi_mem',
        'tinh_trang_xi_lo_thoi_qua_tinh_luyen', 'tinh_trang_xi', 'ghi_chu'
    ]

    try:
        # Read excel file
        df = pd.read_excel(input_path, skiprows=4, header=None, names=cols)
        
        # Initial cleanup: drop rows where all elements are NaN
        df = df.dropna(how='all')
        
        # Drop rows where 'me_tinh_luyen_so' is NaN
        df = df.dropna(subset=['me_tinh_luyen_so'])
        
        # Filter for 'SAE1006' in 'mac_thep_yeu_cau'
        df = df[df['mac_thep_yeu_cau'].str.contains('SAE1006', na=False)]
        
        # Drop 'stt' column
        if 'stt' in df.columns:
            df = df.drop(columns=['stt'])
        
        # Add source metadata columns
        df['source_year'] = source_year
        df['source_month'] = source_month
        df['source_lf'] = source_lf

        # --- DATA CLEANING: Force numeric conversion for technical columns ---
        # List of columns that are NOT numeric (identifiers, timestamps, notes)
        non_numeric_cols = ['ngay',
                            'Ca',
                            'me_tinh_luyen_so',
                            'mac_thep_yeu_cau',
                            'thoi_gian_vao_tinh_luyen',
                            'bat_dau',
                            'ket_thuc',
                            'thoi_gian_len_duc',
                            # 'thung_lf',
                            # 'Si_truoc',
                            # 'S_truoc',
                            # 'P_truoc',
                            # 'khoi_luong_thung_thep',
                            'thoi_gian_danh_dien',
                            # 'tieu_thu_dien',
                            # 'C_sau',
                            # 'Si_sau',
                            # 'S_sau',
                            # 'P_sau',
                            # 'nhiet_do_lan_1',
                            # 'nhiet_do_duc_yeu_cau',
                            # 'nhiet_do_do_tren_duc',
                            # 'thoi_gian_dinh_tre',
                            'ly_do_dinh_tre',
                            'ghi_chu_1',
                            'thoi_gian_bat_dau_thoi_mem',
                            'thoi_gian_ket_thu_thoi_mem',
                            'tong_thoi_gian_thoi_mem',
                            'tinh_trang_xi_lo_thoi_qua_tinh_luyen',
                            'tinh_trang_xi',
                            'ghi_chu'
        ]
        
        # Identify numeric columns (all columns in df that are NOT in the exclusion list)
        numeric_cols = [c for c in df.columns if c not in non_numeric_cols]
        
        # Apply numeric conversion to all identified columns
        # errors='coerce' will turn 'a', 'b', 'error' into NaN automatically
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        print(f"  -> Extracted {len(df)} valid rows. (Year: {source_year}, Month: {source_month}, LF: {source_lf})")
        print(f"  -> Auto-corrected format for {len(numeric_cols)} numeric columns.")
        return df

    except Exception as e:
        print(f"Error processing file {input_path}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple LF Excel files into a single CSV.")
    parser.add_argument("input_files", nargs="+", help="Paths to the input Excel files")
    parser.add_argument("-o", "--output", default="merged_lf_data.csv", help="Path to the output CSV file")
    
    args = parser.parse_args()
    
    all_dfs = []
    for file_path in args.input_files:
        df = process_file(file_path)
        if df is not None and not df.empty:
            all_dfs.append(df)
    
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df.to_csv(args.output, index=False)
        print(f"\nSuccessfully merged {len(all_dfs)} files into: {args.output}")
        print(f"Total rows: {len(merged_df)}")
    else:
        print("\nNo data was processed.")
