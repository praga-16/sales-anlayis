#  Sales Effectiveness (Lead Category Prediction)

## 1. Project Overview


**Goal:**

1. Perform data exploration and generate **sales effectiveness insights**.  
2. Build an **ML model** to predict the **Lead Category** (High Potential vs Low Potential) based on lead and interaction attributes [file:1][file:68].

---

## 2. Dataset

Source: MySQL database `project_sales`, table `data`, exported as `project_sales_data.csv` [file:1][file:68].

Each row represents a single lead contact or interaction.

Main columns:

- `Created`: Date and time the lead was created (string in `DD-MM-YYYY HH:MM` format).  
- `Product_ID`: Product identifier (numeric, but used as a categorical ID).  
- `Source`: Lead source (Website, Call, Live Chat, Google Organic, Quora, Campaign, JustDial, etc.).  
- `Mobile`: Obfuscated mobile number (used only for presence flag).  
- `EMAIL`: Obfuscated email (used for basic quality features; `#VALUE!` etc. mapped to missing).  
- `Sales_Agent`: Assigned sales agent (Sales-Agent-1, Sales-Agent-2, ...).  
- `Location`: Lead location (Bangalore, Chennai, Delhi, USA, UAE, Other Locations, etc.).  
- `Delivery_Mode`: Interaction mode (Mode-1 to Mode-5, or specific channel types).  
- `Status`: Final/current status of lead: CONVERTED, POTENTIAL, LONG TERM, JUST ENQUIRY, JUNK LEAD, NOT RESPONDING, IN PROGRESS POSITIVE / NEGATIVE, LOST, OPEN, etc. [file:68].

Row count is around 7,400, with some missing values and placeholders like `#VALUE!` in several columns [file:1][file:68].

---

## 3. Problem Formulation

We convert the multi-class `Status` field into a **binary `Lead_Category`** target:

- **High Potential:**  
  - `CONVERTED`  
  - `POTENTIAL`  
  - `LONG TERM`  
  - `IN PROGRESS POSITIVE`

- **Low Potential:**  
  - `OPEN`  
  - `LOST`  
  - `JUST ENQUIRY`  
  - `JUNK LEAD`  
  - `NOT RESPONDING`  
  - `IN PROGRESS NEGATIVE`  

Any rows whose status cannot be mapped are dropped from the training set.

**Task:**  
Given a new lead with fields like source, location, product, created time and basic contact flags, the model predicts whether it is **High** or **Low** potential.

---

## 4. Approach & Workflow

1. **Data Loading**
   - Load `project_sales_data.csv` into a pandas DataFrame.  
   - Standardize column names and handle obvious bad tokens such as `#VALUE!`, `VALUE!`, empty strings, and string `"nan"` [file:68].

2. **Data Cleaning & Feature Engineering**
   - Convert `Created` to `datetime` and derive: `Created_Day`, `Created_Month`, `Created_Year`, `Created_Hour`, `Created_DayOfWeek`.  
   - Normalize `Status` to uppercase text and map to binary `Lead_Category` (High/Low).  
   - Treat `Product_ID` as a categorical feature (`str`).  
   - Derive:
     - `Has_Mobile` (1 if mobile present, else 0)  
     - `Has_Email` (1 if email present, else 0)  
     - `Email_Quality` (Looks_Valid / Suspicious / Missing) based on presence of `@` and `.` and placeholder markers [file:68].  
   - Drop or avoid direct use of `Mobile` and raw `EMAIL` values to prevent overfitting to identifiers.

3. **EDA (Exploratory Data Analysis)**
   - Inspect missing values per column.  
   - Analyze distribution of `Status` and `Lead_Category` (class balance).  
   - Explore lead volume and conversion / high‑potential rates by:
     - Source  
     - Location  
     - Sales_Agent  
     - Delivery_Mode  
     - Time (hour of day, weekday) [file:68].  

4. **Modeling**
   - Features:
     - Categorical: `Product_ID`, `Source`, `Sales_Agent`, `Location`, `Delivery_Mode`, `Created_DayOfWeek`, `Email_Quality`.  
     - Numeric: `Created_Day`, `Created_Month`, `Created_Year`, `Created_Hour`, `Has_Mobile`, `Has_Email`.  
   - Split into train/test using `train_test_split` with stratification on `Lead_Category`.  
   - Preprocessing:
     - Numeric: median imputation + standard scaling.  
     - Categorical: most-frequent imputation + one‑hot encoding.  
   - Train and compare:
     - Logistic Regression (baseline, class_weight="balanced")  
     - Random Forest Classifier (balanced, 200 trees)  
     - Gradient Boosting Classifier  
   - Metrics: Accuracy, Precision, Recall, F1-score, ROC‑AUC, Confusion Matrix.

5. **Model Selection & Interpretation**
   - Select best model based on F1‑score on the test set.  
   - For Random Forest:
     - Extract feature importances and identify the most influential features (e.g., certain sources, locations, modes, time patterns).  

6. **Outputs Saved**
   - `project_sales_cleaned_with_target.csv` – cleaned dataset with `Lead_Category`.  
   - `model_comparison_results.csv` – metrics for each model.  
   - `best_lead_category_model.pkl` – serialized scikit‑learn Pipeline (preprocessing + model).  
   - `feature_importance.csv` – feature importance ranking (if RF is selected as best).

---

## 5. Key Insights (example)

These will depend on your actual EDA and model, but typical insights:

- Certain digital sources (e.g., Website or specific Live Chat types) produce a higher share of **High** potential leads.  
- Specific locations or sales agents show consistently better conversion / high‑potential rates.  
- Time-of-day or day-of-week patterns show when higher-quality leads tend to arrive.  
- Some channels (or `Delivery_Mode` values) correlate with more **Junk Lead** or **Not Responding** statuses [file:68].

You should fill in concrete numbers and charts from your EDA here.

---

## 6. How to Run

### Requirements

- Python 3.8+  
- Packages:
  - `pandas`, `numpy`, `scikit-learn`, `joblib`, `matplotlib`, `seaborn` (optional for plots)

Install:

```bash
pip install pandas numpy scikit-learn joblib matplotlib seaborn
```

### Steps

1. Place `project_sales_data.csv` in the project folder.  
2. Run the Jupyter notebook `Sales_Effectiveness_PRCL_0019.ipynb` (or `main.py` script if you used one).  
3. The notebook will:
   - Load and clean data  
   - Create `Lead_Category`  
   - Train and evaluate models  
   - Save the cleaned dataset and best model artifacts  

4. Use the final cell to pass a new lead’s features to the pipeline and get High / Low prediction plus probability.

---

## 7. Files in This Project

- `project_sales_data.csv` – original exported data [file:68].  
- `Sales_Effectiveness_PRCL_0019.ipynb` – main notebook (EDA + modeling).  
- `project_sales_cleaned_with_target.csv` – cleaned dataset with labels.  
- `model_comparison_results.csv` – evaluation metrics for all models.  
- `best_lead_category_model.pkl` – trained pipeline model.  
- `feature_importance.csv` – feature importance table (if applicable).  
- `README.md` – this documentation.

---


