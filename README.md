# 👥 Employee Attrition Prediction System using Machine Learning and HR Analytics

**Machine Learning • HR Analytics • Streamlit**

A machine learning based HR analytics project that analyzes employee-related information and predicts the likelihood of employee attrition. The system combines data preprocessing, exploratory analysis, machine learning and an interactive Streamlit interface to turn employee data into useful HR insights.

---

## 📌 Project Overview

Employee attrition can be affected by different factors such as job satisfaction, salary, overtime, workload, job role, experience and work-life balance.

This project uses employee HR data to identify patterns related to attrition and build a classification model that predicts whether an employee is likely to **stay or leave**.

The project also includes HR analytics and visualizations to make the data easier to understand and to identify factors that are commonly associated with employee turnover.

---

## 🎯 Objectives

* Analyze employee and HR-related data
* Clean and prepare the dataset for machine learning
* Explore patterns related to employee attrition
* Identify important employee-related factors
* Train classification models for attrition prediction
* Evaluate model performance
* Provide predictions through an interactive Streamlit application

---

## 🔄 Project Workflow

```text
Raw Employee Data
        ↓
Data Cleaning & Preprocessing
        ↓
Exploratory Data Analysis
        ↓
Feature Selection
        ↓
Train / Test Split
        ↓
Machine Learning Models
        ↓
Model Evaluation
        ↓
Selected Model
        ↓
Streamlit Application
        ↓
Employee Attrition Prediction
```

---

## 🧹 Data Processing

The employee dataset is prepared before training the machine learning models.

Main preprocessing steps include:

* Checking missing values
* Removing duplicate or unnecessary records
* Handling categorical variables
* Converting categorical information into numerical form
* Preparing numerical features
* Selecting relevant attributes
* Splitting the data into training and testing sets

---

## 🤖 Machine Learning

The project focuses on employee attrition as a classification problem.

The following algorithms are considered for the prediction task:

| Model               | Purpose                                                   |
| ------------------- | --------------------------------------------------------- |
| Logistic Regression | Provides a simple classification baseline                 |
| Decision Tree       | Learns decision rules from employee attributes            |
| Random Forest       | Combines multiple decision trees                          |
| SVM                 | Separates the attrition classes using a decision boundary |
| KNN                 | Predicts using similar employee records                   |

The trained model is saved and used by the application for making predictions on new employee information.

---

## 📊 HR Analytics

The analytics part of the project focuses on understanding how employee attributes relate to attrition.

Some of the areas analyzed include:

* Job satisfaction
* Overtime
* Monthly income
* Age
* Job role
* Years of experience
* Work-life balance
* Job involvement
* Employee performance

Visualizations are used to make these patterns easier to identify.

---

## 📈 Model Evaluation

The trained models can be evaluated using standard classification metrics:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* ROC-AUC

These metrics help understand how well the model identifies employees belonging to the different attrition classes.

---

## 🖥️ Application

The prediction interface is developed using **Streamlit**.

The application allows the user to enter employee-related information and obtain an attrition prediction without directly interacting with the machine-learning code.

### Application Flow

```text
Employee Details
       ↓
Input Processing
       ↓
Trained ML Model
       ↓
Prediction
       ↓
Stay / Leave Result
```

---

## 📸 Project Preview

<img width="1907" height="978" alt="Screenshot 2026-09-26 143639" src="https://github.com/user-attachments/assets/caa29c5d-b8c6-4aa7-93b3-ae800704b881" />

<img width="1903" height="1022" alt="Screenshot 2026-09-26 143805" src="https://github.com/user-attachments/assets/19e8f5be-8296-4e1a-bf14-923c7ec7061e" />

<img width="1905" height="1008" alt="Screenshot 2026-09-26 143842" src="https://github.com/user-attachments/assets/6108ae1e-b3fc-4c31-9b3a-7b805657d791" />

<img width="1903" height="907" alt="Screenshot 2026-09-26 143904" src="https://github.com/user-attachments/assets/7a5269a9-ab71-419d-bc17-c98f1c852a7b" />

<img width="1877" height="952" alt="Screenshot 2026-09-26 143929" src="https://github.com/user-attachments/assets/8c817704-533b-4843-88ba-fcc1d3570f01" />

---

## 🛠️ Tech Stack

### Programming & Application

* Python
* Streamlit

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Joblib

### Visualization

* Matplotlib
* Seaborn

---

## 💡 Key Insights

The analysis focuses on understanding which employee and workplace factors are associated with attrition.

Some of the important areas examined in the project are:

* Relationship between overtime and attrition
* Effect of job satisfaction
* Salary and income patterns
* Role and department-wise differences
* Experience and years at the company
* Work-life balance
* Employee involvement and performance

These insights complement the prediction model by giving additional context to the HR data.

---

