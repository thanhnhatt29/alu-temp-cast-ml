"""
COMPREHENSIVE OUTLIER DETECTION AND CLEANING FOR LF LOG DATA
=============================================================

This script provides multiple methods for outlier detection and cleaning:
1. IQR (Interquartile Range) method - Statistical approach
2. Z-score method - Standard deviation approach  
3. Domain-specific thresholds - Industry knowledge based

Author: AI Assistant
Date: 2026-01-30
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class OutlierDetector:
    """Comprehensive outlier detection and cleaning"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.outlier_report = {}
        
    def detect_iqr_outliers(self, column, factor=1.5):
        """Detect outliers using IQR method"""
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        outliers = (self.df[column] < lower_bound) | (self.df[column] > upper_bound)
        
        return {
            'method': 'IQR',
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_count': outliers.sum(),
            'outlier_indices': self.df[outliers].index.tolist()
        }
    
    def detect_zscore_outliers(self, column, threshold=3):
        """Detect outliers using Z-score method"""
        z_scores = np.abs(stats.zscore(self.df[column].dropna()))
        outliers = pd.Series(False, index=self.df.index)
        outliers.loc[self.df[column].notna()] = z_scores > threshold
        
        return {
            'method': 'Z-score',
            'threshold': threshold,
            'outlier_count': outliers.sum(),
            'outlier_indices': self.df[outliers].index.tolist()
        }
    
    def get_domain_thresholds(self):
        """Domain-specific thresholds for LF process data"""
        return {
            # Temperature columns (°C)
            'nhiet_do_vao_tl': (1400, 1700),
            'nhiet_do_ra_thep': (1400, 1700),
            'nhiet_do_lan_1': (1400, 1700),
            'nhiet_do_duc_yeu_cau': (1400, 1700),
            'nhiet_do_do_tren_duc': (1400, 1700),
            
            # Chemical composition (%)
            'C_truoc': (0, 0.15),
            'C_sau': (0, 0.15),
            'Si_truoc': (0, 0.05),
            'Si_sau': (0, 0.05),
            'Mn_truoc': (0, 0.5),
            'Mn_sau': (0, 0.5),
            'S_truoc': (0, 0.05),
            'S_sau': (0, 0.05),
            'P_truoc': (0, 0.05),
            'P_sau': (0, 0.05),
            
            # Al, Ca (ppm)
            'Al': (0, 1000),
            'Canxi': (0, 200),
            
            # Additives (kg)
            'FeSi': (0, 500),
            'FeMn': (0, 500),
            'SiMn': (0, 500),
            'than': (0, 200),
            'voi_song': (0, 2000),
            'nhom_thoi': (0, 1000),
            'day_ca_dac': (0, 1000),
            'huynh_thach': (0, 500),
            
            # Time (minutes)
            'processing_time_min': (0, 180),
            'wait_time_min': (-200, 200),
            'thoi_gian_dinh_tre': (0, 300),
            'tieu_thu_dien': (0, 10000),
            
            # Temperature loss (°C)
            'temp_loss': (-100, 100),
        }
    
    def detect_domain_outliers(self, column):
        """Detect outliers using domain-specific thresholds"""
        thresholds = self.get_domain_thresholds()
        
        if column not in thresholds:
            return None
        
        lower, upper = thresholds[column]
        outliers = (self.df[column] < lower) | (self.df[column] > upper)
        
        return {
            'method': 'Domain-specific',
            'lower_bound': lower,
            'upper_bound': upper,
            'outlier_count': outliers.sum(),
            'outlier_indices': self.df[outliers].index.tolist()
        }
    
    def analyze_column(self, column, methods=['domain', 'iqr', 'zscore']):
        """Comprehensive analysis of a column"""
        if self.df[column].dtype not in [np.float64, np.int64]:
            return None
        
        results = {
            'column': column,
            'total_count': len(self.df),
            'non_null_count': self.df[column].count(),
            'null_count': self.df[column].isna().sum(),
            'mean': self.df[column].mean(),
            'median': self.df[column].median(),
            'std': self.df[column].std(),
            'min': self.df[column].min(),
            'max': self.df[column].max(),
            'methods': {}
        }
        
        if 'domain' in methods:
            domain_result = self.detect_domain_outliers(column)
            if domain_result:
                results['methods']['domain'] = domain_result
        
        if 'iqr' in methods:
            try:
                results['methods']['iqr'] = self.detect_iqr_outliers(column)
            except:
                pass
        
        if 'zscore' in methods and self.df[column].count() > 3:
            try:
                results['methods']['zscore'] = self.detect_zscore_outliers(column)
            except:
                pass
        
        return results
    
    def analyze_all_numeric_columns(self):
        """Analyze all numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        print("=" * 100)
        print(f"ANALYZING {len(numeric_cols)} NUMERIC COLUMNS")
        print("=" * 100)
        
        for col in numeric_cols:
            result = self.analyze_column(col)
            if result:
                self.outlier_report[col] = result
        
        return self.outlier_report
    
    def generate_summary_report(self):
        """Generate summary report"""
        print("\n" + "=" * 100)
        print("OUTLIER DETECTION SUMMARY REPORT")
        print("=" * 100)
        
        summary_data = []
        
        for col, report in self.outlier_report.items():
            row = {
                'Column': col,
                'Non-Null': report['non_null_count'],
                'Mean': f"{report['mean']:.2f}" if not np.isnan(report['mean']) else 'N/A',
                'Median': f"{report['median']:.2f}" if not np.isnan(report['median']) else 'N/A',
            }
            
            for method_name, method_data in report['methods'].items():
                row[f'{method_name.upper()}_outliers'] = method_data['outlier_count']
            
            summary_data.append(row)
        
        summary_df = pd.DataFrame(summary_data)
        print("\n", summary_df.to_string(index=False))
        
        return summary_df
    
    def clean_data_domain(self):
        """Clean data using domain-specific thresholds (recommended)"""
        df_cleaned = self.df.copy()
        thresholds = self.get_domain_thresholds()
        
        cleaned_count = 0
        
        for col, (lower, upper) in thresholds.items():
            if col in df_cleaned.columns:
                mask = (df_cleaned[col] < lower) | (df_cleaned[col] > upper)
                count = mask.sum()
                if count > 0:
                    df_cleaned.loc[mask, col] = np.nan
                    cleaned_count += count
                    print(f"   {col}: Replaced {count} outliers with NaN")
        
        print(f"\n✅ Total cleaned: {cleaned_count} values")
        return df_cleaned
    
    def clean_data_iqr(self, factor=1.5):
        """Clean data using IQR method"""
        df_cleaned = self.df.copy()
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        
        cleaned_count = 0
        
        for col in numeric_cols:
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower = Q1 - factor * IQR
            upper = Q3 + factor * IQR
            
            mask = (df_cleaned[col] < lower) | (df_cleaned[col] > upper)
            count = mask.sum()
            if count > 0:
                df_cleaned.loc[mask, col] = np.nan
                cleaned_count += count
        
        return df_cleaned
    
    def visualize_outliers(self, columns=None, top_n=10):
        """Visualize outliers for specified columns"""
        if columns is None:
            # Select top N columns with most outliers
            outlier_counts = {}
            for col, report in self.outlier_report.items():
                if 'domain' in report['methods']:
                    outlier_counts[col] = report['methods']['domain']['outlier_count']
            
            columns = sorted(outlier_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
            columns = [col for col, _ in columns]
        
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for idx, col in enumerate(columns):
            if col in self.df.columns:
                axes[idx].boxplot(self.df[col].dropna(), vert=True)
                axes[idx].set_title(f'{col}\n({self.outlier_report[col]["methods"].get("domain", {}).get("outlier_count", 0)} outliers)')
                axes[idx].set_ylabel('Value')
                axes[idx].grid(True, alpha=0.3)
        
        # Hide unused subplots
        for idx in range(len(columns), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig('outlier_visualization.png', dpi=150, bbox_inches='tight')
        print("\n📊 Saved visualization to: outlier_visualization.png")
        plt.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🔍 COMPREHENSIVE OUTLIER DETECTION AND CLEANING")
    print("=" * 100)
    
    # Load data
    file_path = 'merged_lf_data.csv'
    df = pd.read_csv(file_path)
    print(f"\n✅ Loaded data: {len(df)} rows, {len(df.columns)} columns")
    
    # Initialize detector
    detector = OutlierDetector(df)
    
    # Analyze all numeric columns
    print("\n" + "=" * 100)
    print("STEP 1: ANALYZING ALL NUMERIC COLUMNS")
    print("=" * 100)
    detector.analyze_all_numeric_columns()
    
    # Generate summary report
    print("\n" + "=" * 100)
    print("STEP 2: SUMMARY REPORT")
    print("=" * 100)
    summary_df = detector.generate_summary_report()
    summary_df.to_csv('outlier_summary_report.csv', index=False)
    print("\n✅ Saved summary to: outlier_summary_report.csv")
    
    # Visualize top outliers
    print("\n" + "=" * 100)
    print("STEP 3: VISUALIZATION")
    print("=" * 100)
    try:
        detector.visualize_outliers(top_n=12)
    except Exception as e:
        print(f"⚠️ Visualization skipped: {e}")
    
    # Clean data using domain-specific thresholds
    print("\n" + "=" * 100)
    print("STEP 4: CLEANING DATA (Domain-specific thresholds)")
    print("=" * 100)
    df_cleaned = detector.clean_data_domain()
    
    # Recalculate derived columns
    if 'nhiet_do_vao_tl' in df_cleaned.columns and 'nhiet_do_ra_thep' in df_cleaned.columns:
        df_cleaned['temp_loss'] = df_cleaned['nhiet_do_vao_tl'] - df_cleaned['nhiet_do_ra_thep']
        print("\n✅ Recalculated temp_loss")
    
    # Save cleaned data
    output_file = 'merged_lf_data_cleaned.csv'
    df_cleaned.to_csv(output_file, index=False)
    print(f"\n✅ Saved cleaned data to: {output_file}")
    
    # Before/After comparison
    print("\n" + "=" * 100)
    print("STEP 5: BEFORE/AFTER COMPARISON")
    print("=" * 100)
    
    comparison_cols = ['nhiet_do_vao_tl', 'nhiet_do_ra_thep', 'temp_loss', 
                      'Al', 'Canxi', 'processing_time_min']
    
    print("\n{:<25} {:>15} {:>15} {:>15}".format(
        "Column", "Before (mean)", "After (mean)", "Difference"
    ))
    print("-" * 70)
    
    for col in comparison_cols:
        if col in df.columns:
            before = df[col].mean()
            after = df_cleaned[col].mean()
            diff = after - before
            print("{:<25} {:>15.2f} {:>15.2f} {:>15.2f}".format(
                col, before, after, diff
            ))
    
    print("\n" + "=" * 100)
    print("✅ OUTLIER CLEANING COMPLETED SUCCESSFULLY!")
    print("=" * 100)
    print(f"\n📁 Output files:")
    print(f"   - {output_file}")
    print(f"   - outlier_summary_report.csv")
    print(f"   - outlier_visualization.png")
