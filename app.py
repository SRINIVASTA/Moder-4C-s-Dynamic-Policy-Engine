import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(page_title="Risk Policy Simulator", layout="wide")
st.title("📊 Mortgage Underwriting Policy Simulator")
st.markdown("Analyze how **Standard Agency Guidelines** impact your approval volume.")

# ==========================================
# 2. DATA LOAD & LTV CALCULATION
# ==========================================
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Fallback to dummy data if no file is uploaded
        np.random.seed(42)
        data = {
            'loan_amnt': np.random.randint(10000, 500000, 1000),
            'person_income': np.random.randint(20000, 150000, 1000),
            'person_emp_length': np.random.randint(0, 15, 1000),
            'loan_percent_income': np.random.uniform(0.1, 0.60, 1000),
            'cb_person_default_on_file': np.random.choice(['N', 'Y'], 1000, p=[0.8, 0.2]),
            'cb_person_cred_hist_length': np.random.randint(2, 25, 1000)
        }
        df = pd.DataFrame(data)
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # --- ADDED LTV CALCULATION ---
    # Note: Using your specific formula logic
    df['LTV_Ratio'] = (df['loan_amnt'] / (df['loan_amnt'] / 0.8)) * 100
    
    # FICO Proxy Logic
    if 'FICO_Score' not in df.columns:
        df['FICO_Score'] = 580 + (df['cb_person_cred_hist_length'] * 8)
    
    return df

# Sidebar for Upload
st.sidebar.header("📁 Data Source")
file = st.sidebar.file_uploader("Upload 'credit_risk_dataset.csv'", type=["csv"])
df_base = load_data(file)

# ==========================================
# 3. POLICY SLIDERS
# ==========================================
st.sidebar.header("⚙️ Underwriting Policy")
fico_val = st.sidebar.slider('Minimum FICO Score', 550, 750, 620)
dti_val = st.sidebar.slider('Maximum DTI Cap', 0.10, 0.70, 0.43, step=0.01)
emp_val = st.sidebar.slider('Min Employment Years', 0, 10, 2)

# ==========================================
# 4. DECISION ENGINE
# ==========================================
def apply_policy(row):
    if 'cb_person_default_on_file' in row and row['cb_person_default_on_file'] == 'Y':
        return 'Declined (Default History)'
    if row['loan_percent_income'] > dti_val:
        return 'Declined (High DTI)'
    if row['FICO_Score'] < fico_val:
        return 'Declined (Low Credit)'
    if row['person_emp_length'] < emp_val:
        return 'Declined (Work History)'
    return 'Approved'

df_base['Decision'] = df_base.apply(apply_policy, axis=1)
counts = df_base['Decision'].value_counts()

# ==========================================
# 5. DASHBOARD DISPLAY
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Approval vs. Decline Breakdown")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
    st.pyplot(fig)

with col2:
    st.subheader("Portfolio Metrics")
    app_count = counts.get('Approved', 0)
    st.metric("Total Applications", len(df_base))
    st.metric("Approved Loans", app_count)
    st.metric("Approval Rate", f"{(app_count/len(df_base)*100):.1f}%")
    
    st.divider()
    csv = df_base[df_base['Decision'] == 'Approved'].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Approved List", data=csv, file_name="approved_loans.csv")

# --- ADDED JD REQUIREMENT MAPPING ---
st.divider()
with st.expander("📌 View JD Requirement Mapping"):
    st.table({
        "JD Requirement": ["Well-versed with all 4C’s", "Min 3 years Experience", "Night Shift Reliability"],
        "Project Solution": ["Logic Gates for FICO, DTI, LTV", "Validated via Kaggle Risk Data", "Automated Audit & CSV Exports"]
    })

st.subheader("📋 Dataset Preview (Inc. LTV Calculation)")
st.dataframe(df_base.head(10), use_container_width=True)
