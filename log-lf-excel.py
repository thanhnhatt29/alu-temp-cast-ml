import pandas as pd
import os
import argparse
import sys

def process_file(input_path):
    """
    Process LF Excel file and save as CSV with the same name.
    """
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    print(f"Processing file: {input_path}")

    # Define column names
    cols = [
        'stt', 'ngay', 'Ca', 'me_tinh_luyen_so', 'mac_thep_yeu_cau', 
        'thoi_gian_vao_tinh_luyen', 'bat_dau', 'ket_thuc', 'thoi_gian_len_duc', 
        'thung_lf', 'lan_luyen_thu', 'nhiet_do_vao_tl', 'C', 'Si', 'Mn', 'S', 
        'P', 'khoi_luong_thung_thep', 'FeSi', 'FeMn', 'SiMn', 'than', 'FeCr', 
        'FeV', 'Niken', 'FeP', 'Cu', 'khac', 'huynh_thach', 'nhom_thoi', 
        'voi_song', 'dolomite', 'quaczit', 'day_feca', 'day_casi', 'day_ca_dac', 
        'xi_bao_on', 'thoi_gian_danh_dien', 'tieu_thu', 'C', 'Si', 'Mn', 'S', 
        'P', 'Al', 'Ca', 'lan_1', 'ra_thep', 'nhiet_do_duc_yeu_cau', 
        'nhiet_do_do_tren_duc', 'thoi_gian_dinh_tre', 'ly_do_dinh_tre', 
        'ghi_chu_1', 'thoi_gian_bat_dau_thoi_mem', 'thoi_gian_ket_thu_thoi_mem', 
        'tong_thoi_gian_thoi_mem', 'tinh_trang_xi_lo_thoi_qua_tinh_luyen', 
        'tinh_trang_xi', 'ghi_chu'
    ]

    try:
        # Read excel file
        # Note: Removing engine='calamine' to use default (usually openpyxl) for compatibility
        # as calamine might not be installed in all environments.
        df = pd.read_excel(input_path, skiprows=4, header=None, names=cols)
        
        # Initial cleanup: drop rows where all elements are NaN
        df = df.dropna(how='all')
        print(f"  -> Loaded {len(df)} rows.")

        # Logic from notebook
        
        # Drop rows where 'me_tinh_luyen_so' is NaN
        df = df.dropna(subset=['me_tinh_luyen_so'])
        
        # Filter for 'SAE1006' in 'mac_thep_yeu_cau'
        df = df[df['mac_thep_yeu_cau'].str.contains('SAE1006', na=False)]
        
        # Drop 'stt' column
        if 'stt' in df.columns:
            df = df.drop(columns=['stt'])

        # Generate output filename
        # "tên file cũ nhưng .csv"
        # Using the same directory and base name
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.csv"

        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"Data saved to: {output_path}")

    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process LF Excel file to CSV.")
    parser.add_argument("input_file", help="Path to the input Excel file")
    
    args = parser.parse_args()
    process_file(args.input_file)
