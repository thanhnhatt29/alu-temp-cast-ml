import pandas as pd
import os

# Define file paths
file_paths = [
    r"e:\OneDrive - hoaphat.com.vn\Code\alu-temp-cast-ml\01-data\LF\25.12.LF2.xlsx",
    r"e:\OneDrive - hoaphat.com.vn\Code\alu-temp-cast-ml\01-data\LF\25.12.LF5.xlsx"
]

# Define column names as requested
cols = [
    'stt', 'ngay', 'ca', 'me_tinh_luyen_so', 'mac_thep_yeu_cau', 'thoi_gian_vao_tinh_luyen', 
    'bat_dau', 'ket_thuc', 'thoi_gian_len_duc', 'thung_lf', 'lan_luyen_thu', 'nhiet_do_vao_tl', 
    'c', 'si', 'mn', 's', 'p', 'khoi_luong_thung_thep', 'fesi', 'femn', 'simn', 'than', 
    'fecr', 'fev', 'niken', 'fep', 'cu', 'khac', 'huynh_thach', 'nhom_thoi', 'voi_song', 
    'dolomite', 'quaczit', 'day_feca', 'day_casi', 'day_ca_dac', 'xi_bao_on', 'thoi_gian_danh_dien', 
    'tieu_thu', 'c', 'si', 'mn', 's', 'p', 'al', 'ca', 'lan_1', 'ra_thep', 'nhiet_do_duc_yeu_cau', 
    'nhiet_do_do_tren_duc', 'thoi_gian_dinh_tre', 'ly_do_dinh_tre', 'ghi_chu_1', 'thoi_gian_bat_dau_thoi_mem', 
    'thoi_gian_ket_thu_thoi_mem', 'tong_thoi_gian_thoi_mem', 'tinh_trang_xi_lo_thoi_qua_tinh_luyen', 
    'tinh_trang_xi', 'ghi_chu'
]

# List to hold dataframes
dfs = []

for path in file_paths:
    if os.path.exists(path):
        print(f"Reading {path}...")
        try:
            # Read excel, skipping first 4 rows (index 0-3), so row 5 (index 4) is the start
            # header=None because we provide names.
            # However, if row 5 is the header in the file, it will be read as data if we use header=None.
            # Assuming row 5 contains the data or we want to overwrite whatever is there.
            # read_excel(skiprows=4) reads starting from line 5.
            df = pd.read_excel(path, skiprows=4, header=None, names=cols)
            dfs.append(df)
            print(f"  -> Loaded {len(df)} rows.")
        except Exception as e:
            print(f"  -> Error reading file: {e}")
    else:
        print(f"File not found: {path}")

# Merge and display
if dfs:
    final_df = pd.concat(dfs, ignore_index=True)
    print("\nMerged DataFrame Shape:", final_df.shape)
    print("\nFirst 5 rows:")
    print(final_df.head())
    
    # Optional: Save to verify
    # final_df.to_csv("merged_debug.csv", index=False)
else:
    print("No data loaded.")
