"""
Script để phát hiện và xử lý outliers trong dữ liệu nhiệt độ LF
"""

import pandas as pd
import numpy as np

# Load data
file_path = 'merged_lf_data.csv'
df = pd.read_csv(file_path)

print("=" * 80)
print("PHÂN TÍCH VÀ XỬ LÝ OUTLIERS - NHIET_DO_RA_THEP")
print("=" * 80)

# 1. Phân tích trước khi clean
print("\n1. TRƯỚC KHI CLEAN:")
print(f"   Mean: {df['nhiet_do_ra_thep'].mean():.2f}°C")
print(f"   Median: {df['nhiet_do_ra_thep'].median():.2f}°C")
print(f"   Std: {df['nhiet_do_ra_thep'].std():.2f}°C")
print(f"   Min: {df['nhiet_do_ra_thep'].min():.2f}°C")
print(f"   Max: {df['nhiet_do_ra_thep'].max():.2f}°C")

# 2. Tìm outliers
print("\n2. OUTLIERS PHÁT HIỆN:")

# Outliers theo ngưỡng hợp lý (nhiệt độ LF thường 1400-1700°C)
temp_min_threshold = 1400
temp_max_threshold = 1700

outliers_low = df[df['nhiet_do_ra_thep'] < temp_min_threshold]
outliers_high = df[df['nhiet_do_ra_thep'] > temp_max_threshold]

print(f"\n   a) Giá trị QUÁ THẤP (< {temp_min_threshold}°C): {len(outliers_low)} mẫu")
if len(outliers_low) > 0:
    print("\n   Chi tiết:")
    print(outliers_low[['me_tinh_luyen_so', 'ngay', 'nhiet_do_vao_tl', 
                        'nhiet_do_ra_thep', 'source_month']].head(10).to_string())

print(f"\n   b) Giá trị QUÁ CAO (> {temp_max_threshold}°C): {len(outliers_high)} mẫu")
if len(outliers_high) > 0:
    print("\n   Chi tiết:")
    print(outliers_high[['me_tinh_luyen_so', 'ngay', 'nhiet_do_vao_tl',
                         'nhiet_do_ra_thep', 'source_month']].sort_values(
                         'nhiet_do_ra_thep', ascending=False).head(10).to_string())

# 3. Xử lý outliers
print("\n" + "=" * 80)
print("3. XỬ LÝ OUTLIERS")
print("=" * 80)

# Tạo copy để xử lý
df_cleaned = df.copy()

# Option 1: Replace outliers với NaN
print("\n   Option 1: Replace outliers với NaN")
mask_outliers = (df_cleaned['nhiet_do_ra_thep'] < temp_min_threshold) | \
                (df_cleaned['nhiet_do_ra_thep'] > temp_max_threshold)
df_cleaned.loc[mask_outliers, 'nhiet_do_ra_thep'] = np.nan

print(f"   Đã thay thế {mask_outliers.sum()} giá trị outliers bằng NaN")

# 4. Kết quả sau khi clean
print("\n4. SAU KHI CLEAN:")
print(f"   Mean: {df_cleaned['nhiet_do_ra_thep'].mean():.2f}°C")
print(f"   Median: {df_cleaned['nhiet_do_ra_thep'].median():.2f}°C")
print(f"   Std: {df_cleaned['nhiet_do_ra_thep'].std():.2f}°C")
print(f"   Min: {df_cleaned['nhiet_do_ra_thep'].min():.2f}°C")
print(f"   Max: {df_cleaned['nhiet_do_ra_thep'].max():.2f}°C")
print(f"   Count non-null: {df_cleaned['nhiet_do_ra_thep'].count()}")
print(f"   Count NaN: {df_cleaned['nhiet_do_ra_thep'].isna().sum()}")

# 5. Kiểm tra các cột nhiệt độ khác
print("\n" + "=" * 80)
print("5. KIỂM TRA CÁC CỘT NHIỆT ĐỘ KHÁC")
print("=" * 80)

temp_columns = ['nhiet_do_vao_tl', 'nhiet_do_lan_1', 'nhiet_do_ra_thep']
for col in temp_columns:
    if col in df.columns:
        outliers_count = ((df[col] < 1400) | (df[col] > 1700)).sum()
        print(f"\n   {col}:")
        print(f"   - Mean: {df[col].mean():.2f}°C")
        print(f"   - Min: {df[col].min():.2f}°C")
        print(f"   - Max: {df[col].max():.2f}°C")
        print(f"   - Outliers (< 1400 hoặc > 1700): {outliers_count}")

# 6. Lưu file đã clean
output_file = 'merged_lf_data_cleaned.csv'
df_cleaned.to_csv(output_file, index=False)
print("\n" + "=" * 80)
print(f"✅ Đã lưu dữ liệu cleaned vào: {output_file}")
print("=" * 80)

# 7. Recalculate temp_loss với dữ liệu cleaned
if 'nhiet_do_vao_tl' in df_cleaned.columns:
    df_cleaned['temp_loss'] = df_cleaned['nhiet_do_vao_tl'] - df_cleaned['nhiet_do_ra_thep']
    print(f"\n📊 Temp loss sau khi clean:")
    print(df_cleaned['temp_loss'].describe())
    
    # Save again với temp_loss updated
    df_cleaned.to_csv(output_file, index=False)
    print(f"\n✅ Đã cập nhật temp_loss và lưu lại file")
