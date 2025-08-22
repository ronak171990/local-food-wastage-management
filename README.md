# 🍲 Food Donation Data Analytics

This project analyzes **food donation and distribution data** using **PostgreSQL, Python (pandas + SQLAlchemy), and Power BI**.  
The goal is to uncover insights such as **top donated food items, receiver statistics, food variety distribution, and donor–receiver relationships**.

---

## 📊 Project Objectives
- Clean, prepare, and integrate raw CSV data into PostgreSQL.
- Perform **SQL-based exploratory data analysis (EDA)**.
- Generate key metrics such as:
  - Top donated food types by quantity.
  - Receivers with the highest food variety received.
  - Donor–receiver matching efficiency.
- Build an **interactive Power BI dashboard** for visualization.

---

## 🗂️ Dataset Information
The project uses three core tables:

1. **`food_listings_data`**
   - `Food_ID`
   - `Meal_Type`
   - `Quantity`
   - `Donor_ID`

2. **`consumption_data`**
   - `Consumption_ID`
   - `Receiver_ID`
   - `Food_ID`
   - `Quantity_Consumed`

3. **`receivers_data`**
   - `Receiver_ID`
   - `Name`
   - `Location`

---

## 🛠️ Tech Stack
- **Database**: PostgreSQL  
- **Programming**: Python 3.13, pandas, SQLAlchemy  
- **Visualization**: Power BI  
- **Version Control**: Git & GitHub  

---

## ⚙️ Setup Instructions
1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/food-donation-analytics.git
   cd food-donation-analytics

Create PostgreSQL tables & import CSVs:

CREATE TABLE food_listings_data (...);
CREATE TABLE consumption_data (...);
CREATE TABLE receivers_data (...);


Install dependencies:

pip install pandas sqlalchemy psycopg2


Update your database connection string in Python:

engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/food_db")

🔍 Sample Analysis
Top 10 Donated Foods by Quantity
SELECT f."Meal_Type" AS food_name,
       SUM(f."Quantity") AS total_quantity
FROM food_listings_data f
GROUP BY f."Meal_Type"
ORDER BY total_quantity DESC
LIMIT 10;

Top 10 Receivers by Food Variety
SELECT r."Name" AS receiver_name, 
       COUNT(DISTINCT f."Meal_Type") AS food_type_variety
FROM consumption_data c
JOIN receivers_data r
     ON c."Receiver_ID" = r."Receiver_ID"
JOIN food_listings_data f
     ON c."Food_ID" = f."Food_ID"
GROUP BY r."Name"
ORDER BY food_type_variety DESC
LIMIT 10;

📈 Power BI Dashboard

The dashboard provides:

KPIs: total food donated, total receivers, variety count.

Donor vs receiver insights.

Drill-down into specific food categories.

🚀 Future Enhancements

Predict food demand using ML models.

Automate ETL pipeline with Airflow.

Add geospatial mapping of donations & receivers.

👨‍💻 Author

Ronak Patel
📧 ronakpatel171990@gmail.com
🌐 https://ronakpatel.online/

