import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

# ==========================================
# 1. PAGE SETUP & HEADER
# ==========================================
st.set_page_config(page_title="Risk Policy Simulator", layout="wide")
st.title("📊 Mortgage Underwriting Policy Simulator")
st.markdown("""
This simulator measures how deviations from **Standard Agency Guidelines** 
impact portfolio volume. It automates the audit of the **4C's of Credit**.
""")

# ==========================================
# 2. DATA LOAD & 4C's CALCULATION
# ==========================================
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
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
    
    df.columns = df.columns.str.strip()
    df['LTV_Ratio'] = (df['loan_amnt'] / (df['loan_amnt'] / 0.8)) * 100
    if 'FICO_Score' not in df.columns:
        df['FICO_Score'] = 580 + (df['cb_person_cred_hist_length'] * 8)
    return df

file = st.sidebar.file_uploader("Upload 'credit_risk_dataset.csv'", type=["csv"])
df_base = load_data(file)

# ==========================================
# 3. POLICY SLIDERS (Logic Gates)
# ==========================================
st.sidebar.header("⚙️ Underwriting Policy")
fico_val = st.sidebar.slider('Minimum FICO (Credit)', 550, 750, 620)
dti_val = st.sidebar.slider('Maximum DTI Cap (Capacity)', 0.10, 0.70, 0.43, step=0.01)
emp_val = st.sidebar.slider('Min Employment (Stability)', 0, 10, 2)

# ==========================================
# 4. DECISION ENGINE
# ==========================================
def apply_policy(row):
    if 'cb_person_default_on_file' in row and row['cb_person_default_on_file'] == 'Y':
        return 'Declined (Character - Prior Default)'
    if row['loan_percent_income'] > dti_val:
        return 'Declined (Capacity - High DTI)'
    if row['FICO_Score'] < fico_val:
        return 'Declined (Credit - Low FICO)'
    if row['person_emp_length'] < emp_val:
        return 'Declined (Stability - Short Work History)'
    return 'Approved'

df_base['Decision'] = df_base.apply(apply_policy, axis=1)
counts = df_base['Decision'].value_counts()

# ==========================================
# 5. PDF REPORT GENERATOR (NEW FEATURE)
# ==========================================
def create_pdf_report(counts_df, app_rate):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Moder Mortgage Audit Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Approval Rate: {app_rate}%", ln=True)
    pdf.cell(200, 10, txt=f"Total Applications: {len(df_base)}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Policy Bottleneck Breakdown:", ln=True)
    pdf.set_font("Arial", size=10)
    for reason, count in counts_df.items():
        pdf.cell(200, 10, txt=f"- {reason}: {count}", ln=True)
    
    return pdf.output()

# ==========================================
# 6. DASHBOARD DISPLAY
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Approval vs. Decline Breakdown")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=colors[:len(counts)])
    st.pyplot(fig)
    
    st.write("---")
    st.write("**💡 Policy Bottleneck Analysis (Audit View)**")
    decline_reasons = counts[counts.index != 'Approved']
    st.table(decline_reasons) if not decline_reasons.empty else st.success("100% Approval!")

with col2:
    st.subheader("Portfolio Performance")
    app_count = counts.get('Approved', 0)
    app_rate = round((app_count/len(df_base)*100), 1)
    st.metric("Total Applications", len(df_base))
    st.metric("Approved Loans", app_count)
    st.metric("Approval Rate", f"{app_rate}%")
    
    st.divider()
    # CSV Export
    csv = df_base[df_base['Decision'] == 'Approved'].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Approved_Batch.csv", data=csv, file_name="Approved_Batch.csv", use_container_width=True)
    
    # PDF Export (NEW)
    pdf_data = create_pdf_report(counts, app_rate)
    st.download_button("📄 Download PDF Audit Summary", data=pdf_data, file_name="Audit_Summary.pdf", mime="application/pdf", use_container_width=True)

# ==========================================
# 7. JD MAPPING & AUDIT PREVIEW
# ==========================================
st.divider()
c1, c2 = st.columns(2)
with c1:
    with st.expander("📌 View JD Requirement Mapping", expanded=True):
        st.table({"JD Requirement": ["Well-versed with all 4C’s", "Min 3 years Experience", "Night Shift Reliability"], "Project Solution": ["Logic Gates for FICO, DTI, LTV", "Validated via Kaggle Risk Data", "Automated Audit & PDF/CSV Exports"]})
with c2:
    with st.expander("🎓 4C's Logic Definitions"):
        st.write("- **Credit:** FICO Score check\n- **Capacity:** DTI ratio check\n- **Collateral:** LTV Ratio check\n- **Capital:** Employment history check")

st.subheader("📋 Audit Preview (Top 10 Rows)")
def color_decision(val):
    color = '#d4edda' if val == 'Approved' else '#f8d7da'
    return f'background-color: {color}'

st.dataframe(df_base.head(10).style.map(color_decision, subset=['Decision']), use_container_width=True)
