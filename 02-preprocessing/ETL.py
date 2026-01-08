import pandas as pd

# Đọc dữ liệu (Thay vì read_csv từ file, mình đọc từ chuỗi string ở trên để demo)
# Trong máy bạn, hãy dùng: 
df_var = pd.read_csv('01-data/REP_CCM_PRODUCT_VARS.csv')
df_heat = pd.read_csv('01-data/REP_CCM_HEATS.csv')
df_prod = pd.read_csv('01-data/REP_CCM_PRODUCTS.csv')

# --- BẮT ĐẦU XỬ LÝ JOIN BẢNG ---

# BƯỚC 1: Xử lý bảng VAR (Chuyển từ dòng sang cột)
# Lọc lấy Tốc độ (13) và Nhiệt độ (45), chỉ lấy VALUE_CODE=1 (giá trị thực)
df_speed = df_var[(df_var['VARIABLE_ID'] == 13) & (df_var['VALUE_CODE'] == 1)][['REPORT_COUNTER', 'PROD_COUNTER', 'AVG_VALUE']]
df_speed.rename(columns={'AVG_VALUE': 'speed'}, inplace=True)

df_temp = df_var[(df_var['VARIABLE_ID'] == 45) & (df_var['VALUE_CODE'] == 1)][['REPORT_COUNTER', 'PROD_COUNTER', 'AVG_VALUE']]
df_temp.rename(columns={'AVG_VALUE': 'temperature'}, inplace=True)

# Gộp Speed và Temp lại thành 1 bảng var gọn gàng
# Dùng outer join để giữ lại dữ liệu nếu có speed mà mất temp hoặc ngược lại
df_vars_clean = pd.merge(df_speed, df_temp, on=['REPORT_COUNTER', 'PROD_COUNTER'], how='outer')

# BƯỚC 2: Join với bảng PRODUCT (Đây là bảng xương sống)
# Dùng left join: Ưu tiên giữ lại tất cả các Phôi (Product), sau đó điền speed/temp vào
# KHÓA CHÍNH: [REPORT_COUNTER, PROD_COUNTER]
df_merged_1 = pd.merge(df_prod, df_vars_clean, on=['REPORT_COUNTER', 'PROD_COUNTER'], how='left')

# BƯỚC 3: Join với bảng HEAT (Để lấy thông tin Mẻ)
# Dùng left join: Mỗi phôi sẽ được gắn thông tin của Mẻ tương ứng
# KHÓA CHÍNH: REPORT_COUNTER
df_final = pd.merge(df_merged_1, df_heat, on='REPORT_COUNTER', how='left')

# Sắp xếp lại cho đẹp: Theo Mẻ -> Theo Phôi
df_final.sort_values(by=['REPORT_COUNTER', 'PROD_COUNTER'], inplace=True)

# Xuất ra file CSV
df_final.to_csv('01-data/TSC.csv', index=False)

print("Đã xử lý xong!")