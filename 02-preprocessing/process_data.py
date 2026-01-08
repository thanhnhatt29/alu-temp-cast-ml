import pandas as pd
import json

# 1. Đọc 2 file CSV riêng biệt
# Giả sử file không có header chuẩn hoặc cần skip dòng, bạn chỉnh tham số trong read_csv nhé
try:
    df13 = pd.read_csv('data/TSC_dataDuc13.csv') # Tốc độ
    df45 = pd.read_csv('data/TSC_dataDuc45.csv') # Nhiệt độ
    print("Đã đọc file thành công.")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file csv. Hãy kiểm tra lại tên file.")
    exit()

# 2. Hàm làm sạch dữ liệu
def clean_data(df, col_name):
    # Chỉ lấy VALUE_CODE = 1 (Giá trị thực)
    df_clean = df[df['VALUE_CODE'] == 1].copy()
    
    # Chỉ giữ lại PROD_COUNTER và giá trị trung bình
    df_clean = df_clean[['REPORT_COUNTER','PROD_COUNTER', 'AVG_VALUE']]
    
    # Đổi tên cột AVG_VALUE thành tên có nghĩa (speed/temp)
    df_clean.rename(columns={'AVG_VALUE': col_name}, inplace=True)
    return df_clean

# 3. Áp dụng làm sạch
df_speed = clean_data(df13, 'speed')
df_temp = clean_data(df45, 'temperature')

# 4. Gộp 2 bảng lại dựa trên 'PROD_COUNTER'
# Dùng 'outer' join để giữ lại tất cả các phôi, dù 1 trong 2 file bị thiếu dữ liệu
df_final = pd.merge(df_speed, df_temp, on=['REPORT_COUNTER', 'PROD_COUNTER'], how='outer')

# Sắp xếp theo thứ tự phôi
df_final.sort_values(by=['REPORT_COUNTER', 'PROD_COUNTER'], inplace=True)

# Thay thế NaN bằng null để JavaScript hiểu
df_final = df_final.where(pd.notnull(df_final), None)

# 5. Xuất ra file JavaScript (data.js)
# Mẹo: Xuất dưới dạng biến JS để file HTML có thể dùng ngay mà không cần fetch
data_dict = df_final.to_dict(orient='records')
js_content = f"const chartData = {json.dumps(data_dict, indent=4)};"

with open('data/dataDuc.js', 'w') as f:
    f.write(js_content)

print("Xong! Đã tạo file 'data.js'. Bây giờ hãy mở file HTML.")