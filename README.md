# 🏦 Moder 4C’s Dynamic Policy Engine & Simulator 🚀

**Autonomous Underwriting Decision Engine for US Residential Mortgage Portfolios.**

This project is a custom-built, cloud-hosted solution designed to meet the specific requirements of the **Moder Underwriter / Sr. Underwriter** role. It automates the complex audit of the **4C's of Underwriting** using Python and Streamlit.

🔗 **Live App:** [Click Here to View App](https://moder-4c-s-dynamic-policy-engine-am7fzqxlcyxmxyqxsfpugp.streamlit.app/)

---

## 🎯 Strategic Alignment with Moder JD


| Moder JD Requirement | My Project Solution |
| :--- | :--- |
| **Well-versed with all 4C’s** | Integrated logic gates for **Credit** (FICO), **Capacity** (DTI), **Collateral** (LTV), and **Capital** (Stability). |
| **Min 3 years Experience** | Validated against **US Credit Risk data** to ensure production-grade accuracy. |
| **Night Shift Reliability** | Features **Automated PDF Audit Reports** and CSV Exports for high-volume shift handovers. |
| **Live Underwriting Expertise** | Interactive **Policy Sandbox** with real-time sliders to stress-test agency guidelines. |

---

## 🛠️ Key Features
*   **⚙️ Dynamic Policy Handlers:** Adjust Minimum FICO, Maximum DTI, and Employment Stability via interactive sliders to see instant portfolio impact.
*   **📊 Policy Bottleneck Analysis:** High-impact tables demonstrating exactly which policy (e.g., High DTI) is driving the most declines.
*   **📄 Executive PDF Reporting:** One-click generation of professional Audit Summaries for compliance and management review.
*   **📥 Automated Audit Exports:** One-click generation of `Approved_Batch.csv` to streamline the transition from underwriting to loan funding.

---

## 🛡️ Advanced Risk Insights
*   **📉 Sensitivity Testing:** Measure how small changes in FICO requirements impact overall portfolio approval rates.
*   **⚖️ Compliance Mapping:** Every decision is logged and mapped to **Standard Agency Guidelines** (Fannie Mae/Freddie Mac).
*   **🟢 Visual Audit Trail:** Real-time, color-coded data previews (Green for Approved / Red for Declined) for fast manual spot-checks.

---

## 💻 Tech Stack
- **Frontend:** Streamlit (Interactive Dashboard)
- **Data Engine:** Pandas & NumPy (Vectorized logic)
- **Reporting:** FPDF2 (Automated PDF Generation)
- **Visualization:** Matplotlib & Plotly
- **Deployment:** Streamlit Cloud

---

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy matplotlib fpdf2
   ```
3. Launch the app:
   ```bash
   streamlit run app.py
   ```

---

### 👨‍💻 Developed by Srinivasta
**Data Scientist** | *Focused on Automating the Future of Underwriting.*
