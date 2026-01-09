# Aluminum/Steel Casting Speed Prediction with Machine Learning

Dự án này sử dụng các kỹ thuật Machine Learning để phân tích và dự đoán tốc độ đúc (Casting Speed) tối ưu dựa trên nhiệt độ và các thông số vận hành khác, đặc biệt tập trung vào mác thép **sae1006**. Mục tiêu là chuẩn hóa quy trình đúc và kiểm soát giảm nhiệt.

## 📂 Cấu Trúc Dự Án

*   **`01-data/`**: Chứa dữ liệu thô và dữ liệu đã qua xử lý.
    *   `TSC.csv`: Dữ liệu sạch được tổng hợp từ ETL.
*   **`02-preprocessing/`**: Các script và notebook để làm sạch và chuẩn bị dữ liệu.
    *   `ETL.py`: Quy trình trích xuất, chuyển đổi và tải dữ liệu từ các báo cáo thô.
    *   `EDA_TSC.ipynb`: Phân tích khám phá dữ liệu (Exploratory Data Analysis).
    *   `process_data.py`: Các hàm xử lý dữ liệu bổ trợ.
*   **`03-modeling/`**: Xây dựng và đánh giá mô hình.
    *   `multiple-vars-modeling.ipynb`: Notebook chính để huấn luyện các mô hình đa biến (Linear, Polynomial, Random Forest, XGBoost).
    *   `mono-var-modeling.ipynb`: Mô hình đơn biến (thử nghiệm ban đầu).
    *   `time_series.png`: Biểu đồ chuỗi thời gian mẫu.

## 🛠️ Cài Đặt

Dự án yêu cầu Python 3.8+ và các thư viện trong `requirements.txt`.

1.  **Clone repo:**
    ```bash
    git clone <repo_url>
    cd alu-temp-cast-ml
    ```

2.  **Tạo môi trường ảo (Khuyến nghị):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3.  **Cài đặt dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Hướng Dẫn Sử Dụng

### 1. Chuẩn bị dữ liệu (ETL)
Chạy script ETL để gộp các file dữ liệu thô thành file tổng hợp `TSC.csv`.
```bash
cd 02-preprocessing
python ETL.py
```

### 2. Khám phá dữ liệu (EDA)
Mở notebook `02-preprocessing/EDA_TSC.ipynb` để xem các biểu đồ phân bố, tương quan biến và phân tích outlier.

### 3. Huấn luyện mô hình
Mở notebook `03-modeling/multiple-vars-modeling.ipynb` để chạy quy trình huấn luyện:
*   **Feature Engineering**: Tính toán `Time_In_Ladle` (thời gian trong thùng).
*   **Outlier Removal**: Sử dụng IQR hoặc Z-score để lọc nhiễu.
*   **Model Training**:
    *   Linear Regression
    *   Polynomial Regression (Degree 2, 3)
    *   Random Forest Regressor
    *   XGBoost Regressor
*   **Evaluation**: Đánh giá bằng MSE, RMSE, R2 Score.

## 📊 Các Tính Năng Chính (Features)
Mô hình sử dụng các đặc trưng đầu vào (features) sau để dự đoán `speed`:
*   `temperature`: Nhiệt độ thép lỏng.
*   `time_in_ladle`: Thời gian chờ trong thùng (tính từ lúc cắt đến lúc bắt đầu đúc).
*   `PROD_COUNTER`: Bộ đếm sản phẩm (liên quan đến thứ tự đúc).

## 📈 Kết Quả
Dự án so sánh hiệu quả giữa các mô hình tuyến tính và phi tuyến tính để tìm ra giải pháp dự đoán chính xác nhất cho bài toán thực tế tại nhà máy.
