# AI Employee Feedback & Attrition Risk Assessment System

A premium, modular Streamlit-based web application providing organization-wide telemetry on workplace culture, sentiment trends, and predictive employee attrition risk indices.

---

## 🛰️ Key Features

1. **Organization Health Dashboard (`app.py`)**: Real-time summary metrics (Active interventions count, positive sentiment ratio, job satisfaction indices) and dynamic Plotly layouts.
2. **Textual Sentiment Analytics (`pages/1_📊_Feedback_Analytics.py`)**: Natural Language theme matching, keyword extraction, and filterable sentiment reviews by department or category.
3. **Attrition Predictor & Diagnostics (`pages/2_🔮_Attrition_Risk.py`)**: Weighted risk scoring (0-100%) highlighting critical risk flags, risk heatmaps, registry files, and automated manager intervention roadmaps.
4. **Survey Submission Portal (`pages/3_📝_Survey_Submission.py`)**: Form to dynamically submit telemetry and write to the feedback database with automatic recalculations.
5. **System Settings (`pages/4_⚙️_Settings.py`)**: Model weight customization parameters, LLM API keys toggles, and database recovery tools.

---

## 📂 Project Structure

```
EmployeeFeedbackAI/
├── .gitignore                  # Git tracking exclusion list
├── README.md                   # System documentation & usage instructions
├── requirements.txt            # Python dependencies lists
├── app.py                      # Landing dashboard entrypoint
├── assets/
│   └── custom.css              # Custom styling (glassmorphism, badge UI)
├── data/
│   ├── feedback.csv            # Running feedback database (auto-initialized)
│   └── feedback_template.csv   # Master bootstrap dataset
├── pages/                      # Streamlit Multi-page App
│   ├── 1_📊_Feedback_Analytics.py
│   ├── 2_🔮_Attrition_Risk.py
│   ├── 3_📝_Survey_Submission.py
│   └── 4_⚙️_Settings.py
└── src/                        # Python helper modules
    ├── __init__.py
    ├── components.py           # Shared UI cards, headers, and footer components
    ├── data_loader.py          # Data read, write, and template copy routines
    ├── model_predictor.py      # Statistical logic assessing attrition metrics
    └── sentiment_analyzer.py   # Natural language rules categorizing text comments
```

---

## 🚀 Setup & Installation

Follow these steps to set up and run the application locally:

### 1. Initialize Python Environment
If you don't have a virtual environment set up, create one:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (cmd):
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
Install the required packages listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 3. Launch the Application
Run the Streamlit server from the project root:
```powershell
streamlit run app.py
```
This will launch the app in your default web browser (usually at `http://localhost:8501`).

---

## 🎨 Design System

The app utilizes a custom styling sheet (`assets/custom.css`) to enforce premium web designs over the default Streamlit theme:
- **Glassmorphism Containers** (`.glass-card`): Translucent borders, backdrop filters, and hover offsets.
- **Visual Alert Channels**: Linear-gradient left borders mapping metrics directly to organization status states (`success` green, `warning` amber, `danger` red).
- **Badge Indicators**: Risk & Sentiment tags styled using custom paddings and borders for tables and feeds.

---

## Result

<img width="1907" height="978" alt="Screenshot 2026-09-26 143639" src="https://github.com/user-attachments/assets/d4dd9a8f-d9bf-441e-8a77-f4dd0526510a" />

<img width="1903" height="1022" alt="Screenshot 2026-09-26 143805" src="https://github.com/user-attachments/assets/6ba99baf-b393-4bdb-b452-55dd2fdefd43" />

<img width="1905" height="1008" alt="Screenshot 2026-09-26 143842" src="https://github.com/user-attachments/assets/81056b71-f0d2-4570-8b1c-b9791df5dcee" />

<img width="1903" height="907" alt="Screenshot 2026-09-26 143904" src="https://github.com/user-attachments/assets/32d66823-e33c-4cad-85cd-fd740c236557" />

<img width="1877" height="952" alt="Screenshot 2026-09-26 143929" src="https://github.com/user-attachments/assets/fc648eaf-4e09-4e21-a20a-0194784eb979" />

---
