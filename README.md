# Aluminum Temperature Loss & Casting Speed Prediction with Machine Learning

Dự án Machine Learning này phân tích và dự đoán **tốc độ đúc (Casting Speed)** tối ưu dựa trên nhiệt độ và các thông số vận hành trong quá trình sản xuất thép liên tục (Continuous Casting). Dự án tích hợp nhiều nguồn dữ liệu từ TSC (Tundish Casting), LF (Ladle Furnace), và KCS (Quality Control System) để xây dựng các mô hình dự đoán chính xác.

## 🎯 Mục Tiêu Dự Án

- **Dự đoán tốc độ đúc tối ưu** dựa trên nhiệt độ thép lỏng và các tham số vận hành
- **Chuẩn hóa quy trình đúc** để giảm thiểu sự mất mát nhiệt độ và hàm lượng nhôm
- **Tích hợp dữ liệu đa nguồn** từ các hệ thống TSC, LF, và KCS
- **Phát hiện và làm sạch dữ liệu outlier** để nâng cao độ chính xác mô hình

## 📂 Cấu Trúc Dự Án

```
alu-temp-cast-ml/
│
├── 00-scripts/              # Scripts tiện ích cho data loading
│   ├── get-LF-data-from-api.py        # Lấy dữ liệu LF từ API
│   ├── load-lf-excel.py               # Load dữ liệu LF từ Excel files
│   └── load-lf-excel.ipynb            # Notebook version
│
├── 01-data/                 # Dữ liệu thô và đã xử lý
│   ├── TSC/                 # Dữ liệu Tundish Casting
│   ├── LF/                  # Dữ liệu Ladle Furnace (Excel)
│   ├── LF API/              # Dữ liệu LF từ API
│   ├── KCS/                 # Dữ liệu Quality Control System
│   ├── processed/           # Dữ liệu đã xử lý
│   └── sample/              # Dữ liệu mẫu
│
├── 02-preprocessing/        # Xử lý và làm sạch dữ liệu
│   ├── ETL.py               # Extract, Transform, Load cho TSC data
│   ├── EDA_TSC.ipynb        # Exploratory Data Analysis cho TSC
│   ├── LF-log-analysis.ipynb           # Phân tích LF logs (Oct-Dec 2025)
│   ├── LF-data-preprocessing.ipynb     # Xử lý dữ liệu LF
│   ├── KCS-data-preprocessing.ipynb    # Xử lý dữ liệu KCS
│   ├── merge_kcs_lf_data.ipynb         # Merge KCS và LF data theo heat ID
│   ├── outlier-cleaning/               # Comprehensive outlier detection
│   │   ├── comprehensive_outlier_cleaning.py    # Outlier detector với 3 methods
│   │   ├── clean_temperature_outliers.py
│   │   └── outlier_visualization.png
│   ├── process_data.py      # Utility functions
│   ├── run_eda.py           # Automated EDA script
│   └── filter_script.py     # Filter data by criteria
│
├── 03-modeling/             # Xây dựng và đánh giá mô hình
│   ├── multiple-vars-modeling.ipynb    # Multi-variable models (main)
│   ├── mono-var-modeling.ipynb         # Single-variable experiments
│   ├── advanced_modeling.py            # Advanced ML algorithms
│   └── time_series.png                 # Time series visualization
│
├── LF-Log.csv               # LF log data (consolidated)
├── merged_lf_data.csv       # Merged LF data from multiple sources
├── merged_lf_data_cleaned.csv          # Cleaned merged data
├── outlier_summary_report.csv          # Outlier analysis report
├── requirements.txt         # Python dependencies
└── README.md
```

## 🛠️ Cài Đặt

### Yêu Cầu Hệ Thống

- **Python**: 3.8 hoặc cao hơn
- **OS**: Windows / Linux / macOS
- **RAM**: Tối thiểu 4GB (khuyên nghị 8GB cho xử lý dữ liệu lớn)

### Các Bước Cài Đặt

1. **Clone repository:**
   ```bash
   git clone <repo_url>
   cd alu-temp-cast-ml
   ```

2. **Tạo môi trường ảo (Khuyến nghị):**
   ```bash
   python -m venv venv
   
   # Trên Windows
   venv\Scripts\activate
   
   # Trên Linux/macOS
   source venv/bin/activate
   ```

3. **Cài đặt dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Thư Viện Chính

- **Data Processing**: `pandas`, `numpy`, `openpyxl`
- **Visualization**: `matplotlib`, `seaborn`
- **Machine Learning**: `scikit-learn`, `xgboost`
- **Statistical Analysis**: `scipy`
- **Web Framework**: `Flask` (cho deployment)
- **Database**: `pymysql`, `sqlalchemy`, `mysql-connector-python`

## 🚀 Hướng Dẫn Sử Dụng

### 1. Thu Thập Dữ Liệu

#### Từ API (LF Data)
```bash
cd 00-scripts
python get-LF-data-from-api.py
```

#### Từ Excel Files (LF Logs)
```bash
cd 00-scripts
python load-lf-excel.py
# Hoặc sử dụng notebook: load-lf-excel.ipynb
```

### 2. Chuẩn Bị Dữ Liệu (ETL)

#### ETL cho TSC Data
```bash
cd 02-preprocessing
python ETL.py
```
Script này sẽ:
- Đọc dữ liệu từ `REP_CCM_PRODUCT_VARS.csv`, `REP_CCM_HEATS.csv`, `REP_CCM_PRODUCTS.csv`
- Join các bảng theo `REPORT_COUNTER` và `PROD_COUNTER`
- Trích xuất `speed` (VARIABLE_ID=13) và `temperature` (VARIABLE_ID=45)
- Xuất file tổng hợp `TSC.csv`

### 3. Phân Tích Khám Phá Dữ Liệu (EDA)

#### EDA Tự Động
```bash
cd 02-preprocessing
python run_eda.py
```

#### EDA Chi Tiết (Notebooks)
- **TSC Data**: Mở `02-preprocessing/EDA_TSC.ipynb`
- **LF Logs**: Mở `02-preprocessing/LF-log-analysis.ipynb`
- **KCS Data**: Mở `02-preprocessing/KCS-data-preprocessing.ipynb`

Các notebook này cung cấp:
- Phân tích phân bố dữ liệu
- Ma trận tương quan giữa các biến
- Phát hiện outliers
- Visualizations (histograms, scatter plots, box plots)

### 4. Làm Sạch Outliers

Dự án cung cấp **3 phương pháp** phát hiện outliers:

#### a) IQR Method (Interquartile Range)
Phương pháp thống kê cơ bản sử dụng khoảng tứ phân vị.

#### b) Z-Score Method
Phương pháp dựa trên độ lệch chuẩn (standard deviation).

#### c) Domain-Specific Thresholds (Khuyến nghị)
Phương pháp dựa trên kiến thức ngành và ngưỡng kỹ thuật.

**Sử dụng:**
```python
from outlier_cleaning.comprehensive_outlier_cleaning import OutlierDetector

# Load data
df = pd.read_csv('merged_lf_data.csv')

# Initialize detector
detector = OutlierDetector(df)

# Analyze all numeric columns
detector.analyze_all_numeric_columns()

# Generate summary report
detector.generate_summary_report()

# Clean using domain-specific method (recommended)
df_cleaned = detector.clean_data_domain()

# Visualize outliers
detector.visualize_outliers(top_n=10)

# Save cleaned data
df_cleaned.to_csv('merged_lf_data_cleaned.csv', index=False)
```

### 5. Merge Dữ Liệu Từ Nhiều Nguồn

```bash
# Sử dụng notebook để merge KCS và LF data
jupyter notebook 02-preprocessing/merge_kcs_lf_data.ipynb
```

Notebook này:
- Parse heat IDs từ `BilletLotCode` (KCS) và `me_tinh_luyen_so` (LF)
- Merge theo heat key (furnace + heat number)
- Phân tích trùng lặp thành phần hóa học (C, Si, Mn, S, P, Al, Ca)

### 6. Huấn Luyện Mô Hình

Mở notebook chính cho multi-variable modeling:
```bash
jupyter notebook 03-modeling/multiple-vars-modeling.ipynb
```

#### Quy Trình Modeling

**a) Feature Engineering**
- `time_in_ladle`: Thời gian chờ trong thùng (từ lúc cắt đến lúc đúc)
- `temperature`: Nhiệt độ thép lỏng
- `PROD_COUNTER`: Thứ tự phôi trong mẻ đúc

**b) Outlier Removal**
- IQR method
- Z-score method
- Domain-specific filtering

**c) Model Training**
- **Linear Regression**: Baseline model
- **Polynomial Regression**: Degree 2 và 3 để capture non-linear relationships
- **Random Forest Regressor**: Ensemble method với feature importance
- **XGBoost Regressor**: Gradient boosting cho accuracy cao

**d) Model Evaluation**
Các metrics:
- **MSE** (Mean Squared Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**: Độ phù hợp của mô hình
- **MAE** (Mean Absolute Error)

**e) Visualizations**
- Scatter plots: Actual vs Predicted
- Residual plots: Phân tích sai số
- Feature importance charts
- Perfect prediction line comparison

## 📊 Các Features (Biến Đầu Vào)

Mô hình sử dụng các đặc trưng chính sau:

### TSC Features
- `temperature`: Nhiệt độ thép lỏng tại thùng đúc (°C)
- `speed`: Tốc độ đúc (target variable)
- `PROD_COUNTER`: Thứ tự phôi trong mẻ (1, 2, 3...)
- `STEEL_GRADE_NAME`: Mác thép (e.g., SAE1006AL)

### LF Features
- `nhiet_do_lan_1`, `nhiet_do_lan_2`: Nhiệt độ đo tại LF
- `Al_lan_1`, `Al_lan_2`: Hàm lượng nhôm (%)
- `thoi_gian_bat_dau`, `thoi_gian_ket_thuc`: Timestamps
- Chemical composition: C, Si, Mn, S, P, Cr, Ni, Cu, etc.

### KCS Features
- `BilletLotCode`: Mã lô phôi (chứa heat ID)
- Chemical analysis results
- Quality control metrics

### Engineered Features
- `time_in_ladle`: Calculated time duration
- Temperature loss rate
- Aluminum loss rate

## 📈 Kết Quả và So Sánh Mô Hình

Dự án so sánh hiệu quả giữa các mô hình:
- **Linear models** vs **Non-linear models**
- **Tree-based models** vs **Polynomial regression**
- **Feature importance analysis** để xác định các yếu tố chính ảnh hưởng đến tốc độ đúc

Kết quả được visualize qua:
- Scatter plots với perfect prediction line
- Residual histograms
- Feature importance bar charts
- Time series analysis

## 📝 Ghi Chú Quan Trọng

### Data Sources
- **TSC**: Continuous Casting Machine data
- **LF**: Ladle Furnace operation logs (Oct-Dec 2025)
- **KCS**: Quality Control System measurements
- **API**: Real-time LF data endpoint

### Known Issues & Solutions
1. **Missing dates in LF logs**: Sử dụng `source_year` và `source_month` columns để reconstruct dates
2. **Non-numeric values**: Type conversion handling trong data loading
3. **Heat ID parsing**: Different formats giữa KCS và LF require custom parsing logic

### Best Practices
- Luôn sử dụng **domain-specific thresholds** cho outlier cleaning (phù hợp nhất với ngành thép)
- Kiểm tra **data type consistency** trước khi modeling
- Validate **heat ID parsing** khi merge data sources
- Backup dữ liệu gốc trước khi cleaning

## 🔬 Phân Tích Nâng Cao

### Outlier Detection Results
File `outlier_summary_report.csv` chứa:
- Số lượng outliers phát hiện theo từng method
- % outliers trong tổng data
- Statistical summary (mean, std, min, max, Q1, Q3)

### Visualization Outputs
- `outlier_visualization.png`: Box plots và distribution plots
- `eda_histograms.png`: Phân bố các biến chính
- `time_series.png`: Xu hướng theo thời gian
