import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# ==========================================
# 1. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(page_title="Mortgage Underwriting Simulator", layout="wide")
st.title("📊 Mortgage Underwriting Policy Simulator")
st.markdown("Adjust policy sliders to see how risk appetite impacts loan approval volume.")

# ==========================================
# 2. DATA HANDLER
# ==========================================
@st.cache_data # Caches data so it doesn't reload on every slider move
def load_data():
    FILE_PATH = 'credit_risk_dataset.csv'
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        df.columns = df.columns.str.strip()
    else:
        # Generate Dummy Data if file missing
        np.random.seed(42)
        dummy_data = {
            'person_income': np.random.randint(20000, 150000, 1000),
            'person_emp_length': np.random.randint(0, 15, 1000),
            'loan_amnt': np.random.randint(1000, 35000, 1000),
            'loan_percent_income': np.random.uniform(0.1, 0.65, 1000),
            'cb_person_default_on_file': np.random.choice(['N', 'Y'], 1000, p=[0.8, 0.2]),
            'cb_person_cred_hist_length': np.random.randint(2, 25, 1000)
        }
        df = pd.DataFrame(dummy_data)
    
    if 'FICO_Score' not in df.columns:
        df['FICO_Score'] = 580 + (df['cb_person_cred_hist_length'] * 8)
    return df

df_base = load_data()

# ==========================================
# 3. SIDEBAR CONTROLS (The Policy Handlers)
# ==========================================
st.sidebar.header("Policy Thresholds")
fico_val = st.sidebar.slider('Min FICO Score (Credit)', 550, 750, 620)
dti_val = st.sidebar.slider('Max DTI Cap (Capacity)', 0.10, 0.70, 0.43, step=0.01)
emp_val = st.sidebar.slider('Min Employment Years (Stability)', 0, 10, 2)

# ==========================================
# 4. LOGIC ENGINE
# ==========================================
def engine(row):
    if row['cb_person_default_on_file'] == 'Y': return 'Declined (Character)'
    if row['FICO_Score'] < fico_val: return 'Declined (Credit)'
    if row['loan_percent_income'] > dti_val: return 'Declined (Capacity)'
    if row['person_emp_length'] < emp_val: return 'Declined (Stability)'
    return 'Approved'

df_base['Decision'] = df_base.apply(engine, axis=1)
counts = df_base['Decision'].value_counts()

# ==========================================
# 5. VISUALIZATION & OUTPUT
# ==========================================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Approval Distribution")
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, 
           colors=colors[:len(counts)], explode=[0.05]*len(counts))
    st.pyplot(fig)

with col2:
    st.subheader("Key Metrics")
    approved_count = counts.get('Approved', 0)
    st.metric("Total Approved Loans", approved_count)
    st.metric("Approval Rate", f"{(approved_count/len(df_base)*100):.1f}%")
    
    # Download Buttons
    approved_df = df_base[df_base['Decision'] == 'Approved']
    csv = approved_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Approved Batch", data=csv, file_name="approved_loans.csv", mime="text/csv")

st.subheader("Data Preview (Sample)")
st.write(df_base.head(10))
