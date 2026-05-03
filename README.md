# 🏦 Moder 4C’s Dynamic Policy Engine & Simulator 🚀

**Autonomous Underwriting Decision Engine for US Residential Mortgage Portfolios.**

This project is a custom-built, cloud-hosted solution designed to meet the specific requirements of the **Moder Underwriter / Sr. Underwriter** role. It automates the complex audit of the **4C's of Underwriting** using Python and Streamlit.

🔗 **Live App:** [Click Here to View App](https://moder-4c-s-dynamic-policy-engine-am7fzqxlcyxmxyqxsfpugp.streamlit.app/)

---

## 🎯 Strategic Alignment with Moder JD


| Moder JD Requirement | My Project Solution |
| :--- | :--- |
| **Well-versed with all 4C’s** | Integrated logic gates for **Credit** (FICO), **Capacity** (DTI), **Collateral** (LTV), and **Capital** (Stability). |
| **Min 3 years Experience** | Validated against **32,000+ records** of US Credit Risk data to ensure production-grade accuracy. |
| **Night Shift Reliability** | Features **Automated Batch Export** (CSV) and Audit Logs for efficient high-volume night-shift operations. |
| **Live Underwriting Expertise** | Interactive **Policy Sandbox** with real-time sliders to stress-test agency guidelines (620 FICO / 43% DTI). |

---

## 🛠️ Key Features
*   **⚙️ Dynamic Policy Handlers:** Adjust Minimum FICO, Maximum DTI, and Employment Stability via interactive sliders to see instant portfolio impact.
*   **📊 3D Health Analytics:** High-impact visualizations demonstrating the distribution of Approvals vs. specific Decline reasons.
*   **🧪 Live Data Sandbox:** Supports direct upload of `credit_risk_dataset.csv` with automated data sanitization and header cleaning.
*   **📥 Automated Audit Exports:** One-click generation of `Approved_Batch.csv` to streamline the transition from underwriting to loan funding.

---

## 🎓 4C's Logic Implementation
*   **Character (Credit):** Evaluates FICO scores and prior default history.
*   **Capacity:** Calculates Debt-to-Income (DTI) ratios against the 43% QM benchmark.
*   **Collateral:** Automated Loan-to-Value (LTV) calculation to assess property equity risk.
*   **Capital/Stability:** Verifies Continuity of Income through employment history length filters.

---

## 💻 Tech Stack
- **Frontend:** Streamlit (Interactive Dashboard)
- **Data Engine:** Pandas & NumPy (Vectorized logic for high-speed processing)
- **Visualization:** Matplotlib
- **Deployment:** Streamlit Cloud

---

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy matplotlib
   ```
3. Launch the app:
   ```bash


---

### 👨‍💻 Developed by Srinivasta
**Data Scientist** | *Focused on Automating the Future of Underwriting.*

   streamlit run app.py
   ```
