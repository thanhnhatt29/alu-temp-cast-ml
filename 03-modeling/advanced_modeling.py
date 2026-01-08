import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import os

def load_and_process_data(file_path):
    # Load data
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path, parse_dates=['CUT_DATE', 'START_DATE'], low_memory=False)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None
    
    # Filter Grade
    target_grade = 'sae1006'
    if 'STEEL_GRADE_NAME' in df.columns:
        df = df[df['STEEL_GRADE_NAME'].str.contains(target_grade, case=False, na=False)].copy()
    else:
        print("Warning: STEEL_GRADE_NAME column not found.")
    
    # Basic Cleaning
    required_cols = ['speed', 'temperature', 'CUT_DATE', 'START_DATE', 'PROD_COUNTER']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns {missing_cols}")
        return None

    df = df.dropna(subset=required_cols)
    df = df[(df['speed'] > 0) & (df['temperature'] >= 1500)]
    
    # Feature Engineering: Time_In_Ladle
    # Ensure datetime conversion worked
    df['CUT_DATE'] = pd.to_datetime(df['CUT_DATE'], errors='coerce')
    df['START_DATE'] = pd.to_datetime(df['START_DATE'], errors='coerce')
    df = df.dropna(subset=['CUT_DATE', 'START_DATE'])
    
    df['Time_In_Ladle'] = (df['CUT_DATE'] - df['START_DATE']).dt.total_seconds() / 60.0
    
    # Filter valid Time_In_Ladle (e.g., positive values)
    df = df[df['Time_In_Ladle'] > 0]
    
    print(f"Data shape after cleaning and feature engineering: {df.shape}")
    return df

def remove_outliers_iqr(df, columns):
    df_out = df.copy()
    for col in columns:
        if col in df_out.columns:
            Q1 = df_out[col].quantile(0.25)
            Q3 = df_out[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df_out = df_out[(df_out[col] >= lower) & (df_out[col] <= upper)]
    return df_out

def train_models(df):
    features = ['temperature', 'PROD_COUNTER', 'Time_In_Ladle']
    target = 'speed'
    
    X = df[features]
    y = df[target]
    
    print(f"Training on features: {features}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Polynomial Regression (Deg 2)": Pipeline([
            ('poly', PolynomialFeatures(degree=2)),
            ('linear', LinearRegression())
        ]),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "XGBoost": xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
    }
    
    results = {}
    for name, model in models.items():
        print(f"\nTraining {name}...")
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            results[name] = {'MSE': mse, 'R2': r2}
            print(f"  MSE: {mse:.4f}, R2: {r2:.4f}")
        except Exception as e:
            print(f"  Error training {name}: {e}")
        
    return results

if __name__ == "__main__":
    # Absolute path based on user context
    file_path = r"e:\OneDrive - hoaphat.com.vn\Code\ai-loss\01-data\TSC_clean.csv"
    
    if os.path.exists(file_path):
        df = load_and_process_data(file_path)
        
        if df is not None and not df.empty:
            cols_to_filter = ['speed', 'temperature', 'Time_In_Ladle']
            df_clean = remove_outliers_iqr(df, cols_to_filter)
            print(f"Data shape after outlier removal: {df_clean.shape}")
            
            if not df_clean.empty:
                train_models(df_clean)
            else:
                print("Dataframe is empty after outlier removal.")
        else:
            print("Dataframe is emtpy or failed to load.")
    else:
        print(f"File not found: {file_path}")
