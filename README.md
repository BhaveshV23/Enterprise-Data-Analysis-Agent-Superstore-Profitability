# 🚀 Enterprise Data Analysis Agent – Superstore Profitability

**Autonomous AI-Powered Business Intelligence Platform for Deep Profitability Analysis**

| Status | Value |
| :--- | :--- |
| **Python** | `3.10+` |
| **Agent Core** | `Gemini API (google-genai)` |
| **License** | `MIT` |
| **Platform** | `Kaggle` |

---

## 💡 Overview

This project delivers an enterprise-grade **AI Data Analysis Agent** designed to serve as a virtual Business Intelligence (BI) analyst. Utilizing the Gemini API, the agent autonomously executes a full data analysis lifecycle, from data quality checks and feature engineering to multi-modal reporting and strategic recommendation generation.

* **What it does:** The agent ingests raw transactional data (Superstore), conducts automated Exploratory Data Analysis (EDA), performs deep profitability breakdowns, and generates a structured, executive-ready report (PDF or Markdown).
* **Who it is for:** Senior managers, business analysts, and strategists requiring fast, accurate, and actionable insights into complex sales and profit data.
* **Why it is useful:** It bypasses manual analysis, translating raw data and visual evidence into clear, concise, and strategic business decisions, significantly reducing the time-to-insight.

---

## ✨ Features

The agent system is built around custom **Function Calling** tools, enabling robust and intelligent decision-making.

* **Autonomous EDA:** Executes a full EDA suite, generating key visualizations (e.g., Sales Distribution, Discount vs. Profit Scatter).
* **Profitability Agent Core:** Focuses specifically on synthesizing metrics to provide Category-wise and Region-wise profitability breakdowns.
* **Data Quality Checks:** Integrates custom tools to perform statistical checks, such as Interquartile Range (IQR) analysis for outlier detection in `Profit` and `Sales`.
* **Custom Tool Integration:** Uses three modular Python tools (`data_summary`, `automated_eda`, `check_for_outliers`) exposed to the LLM via Function Calling.
* **Multi-Modal Reporting:** Analyzes **textual data summaries** and **visual charts (`.png` files)** simultaneously to generate a cohesive report.
* **Executive Report Generation:** Automatically compiles all findings, charts, and recommendations into a professional, multi-page **PDF document** (Cell 20).
* **Actionable Recommendations:** Extracts KPIs and generates specific, data-driven recommendations for discount policy and low-margin mitigation.

---

## 💻 Tech Stack

The project leverages modern data science and generative AI tooling for optimal performance and integration.

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Core AI** | Gemini API (`google-genai`) | Large Language Model backbone for reasoning and text generation. |
| **Agent Framework**| Custom Sequential/Two-Step Agent | Manages multi-turn conversation and tool dispatching logic. |
| **Data Processing** | Python, Pandas, NumPy | Data cleaning, feature engineering, and statistical analysis. |
| **Visualization** | Matplotlib/Pyplot | Generation of all custom EDA charts (`.png` files). |
| **Reporting** | FPDF2 | Assembly and generation of the final PDF business report. |
| **Environment** | Kaggle Notebook | Execution and testing environment. |

---

## 📊 Dataset Information

| Detail | Value |
| :--- | :--- |
| **Dataset** | Superstore Sales Data |
| **Key Columns** | `Sales`, `Profit` (Synthetically engineered), `Discount`, `Category`, `Region` |
| **Source** | Public Kaggle Superstore Datasets |
| **Usage Note** | The required `Profit` and `Discount` columns were **synthetically engineered** (Cell 5) to enable advanced profitability analysis, ensuring high data fidelity and analytical value. |

---

## 🧠 Architecture

The EDAA operates as a central AI controller that mediates between the user request and the data processing tools. 

1.  **Input:** User provides a natural language query (e.g., "Generate the profitability report").
2.  **Reasoning:** The Gemini LLM determines that the query requires data analysis and issues a **Function Call** (`automated_eda` or `check_for_outliers`).
3.  **Execution:** The Python dispatcher executes the corresponding tool in the local environment, generating raw statistical data or chart files.
4.  **Synthesis:** The LLM receives the results (text + chart files), synthesizes the findings, and formats the output according to the System Instruction.
5.  **Output:** The final professional report is delivered.

---

## ⚙️ Installation

To replicate this project, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/BhaveshV23/Enterprise-Data-Analysis-Agent-Superstore-Profitability.git
    cd Enterprise-Data-Analysis-Agent-Superstore-Profitability
    ```

2.  **Create Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # .\venv\Scripts\activate # On Windows
    ```

3.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration

1.  **Gemini API Key:** Obtain a Gemini API Key from Google AI Studio.
2.  **Environment Variable:** Set the key as an environment variable named `GEMINI_API_KEY` (or `GOOGLE_API_KEY`).
    * *Kaggle Users:* Store the key securely as a **Kaggle Secret** and reference it in Cell 2.
    * *Local Users:* Export the key in your terminal: `export GEMINI_API_KEY='YOUR_API_KEY'`

## ▶️ Usage

The project is designed to be executed sequentially within a Jupyter or Kaggle Notebook.

1.  Open the main notebook: `superstore_analysis_agent.ipynb`
2.  Run all cells sequentially (Cells 1-20).
3.  The final output is generated by running the PDF assembly function (Cell 20).

**Example Execution (From the Notebook):**

```python
# Run the official Function Calling agent for a specific KPI
print(enterprise_agent("Check the 'profit' column for any significant outliers."))

# Generate the full final report
generate_business_report_v3(df)
```

## ✅ Results
The agent successfully generated a comprehensive report identifying key profitability drivers and risks:

Profitability Risk: Discounts over 20% consistently lead to negative profit margins.

KPI Summary: Technology is the primary profit driver; Furniture is the lowest margin category, posing the highest risk to sustained profitability.

Data Quality: Identified 12.53% of transactions as statistical outliers (extreme gains or extreme losses) requiring further investigation.

## 🚀 Future Enhancements
Dynamic Data Sources: Integrate RAG for live data fetching via built-in tools (e.g., Google Search for market context).

Advanced Agents: Implement a hierarchical system where a Planning Agent delegates tasks to specialized EDA and Reporting Agents.

Web Dashboard: Deploy a simple Streamlit or Gradio interface for interactive, non-code analysis.

## 🙏 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## 📄 License
This project is licensed under the MIT License.

## 🧑‍💻 Author Details
**Name:** Bhavesh Vadnere

**Role:** AI & Data Analytics Student

**LinkedIn:** https://www.linkedin.com/in/bhavesh-vadnere/

**Kaggle:** https://www.kaggle.com/bhaveshv23

**Email:** bhaveshvadnere8888@gmail.com

#AI #GenAI #DataAnalysis #EDA #Profitability #Python #OpenAI #LangChain #Superstore
