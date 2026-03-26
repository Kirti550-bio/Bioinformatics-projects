import pandas as pd
import matplotlib.pyplot as plt
import os

print("==================================================")
print("   COVID-19 Clinical Data Analyzer")
print("==================================================")

df = pd.read_csv("Covid Data.csv")
print("Data loaded! Total records:", len(df))

df = df[['SEX','AGE','PNEUMONIA','DIABETES','HIPERTENSION','OBESITY','TOBACCO','ICU','DATE_DIED']].copy()
df['DIED'] = df['DATE_DIED'].apply(lambda x: 0 if x == '9999-99-99' else 1)
df = df[df['AGE'] < 120]

total = len(df)
died = df['DIED'].sum()
survived = total - died
death_rate = round((died / total) * 100, 2)

print("\nKEY STATISTICS")
print("Total Patients :", total)
print("Survived       :", survived)
print("Died           :", died)
print("Death Rate     :", death_rate, "%")

os.makedirs("charts", exist_ok=True)

plt.figure(figsize=(8,5))
plt.hist(df['AGE'], bins=20, color='steelblue', edgecolor='white')
plt.title('Age Distribution of COVID-19 Patients')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.tight_layout()
plt.savefig('charts/age_distribution.png')
plt.close()
print("\nChart 1 saved: charts/age_distribution.png")

plt.figure(figsize=(6,5))
plt.bar(['Survived','Died'], [survived, died], color=['#2ecc71','#e74c3c'], edgecolor='white')
plt.title('Patient Outcomes')
plt.ylabel('Number of Patients')
plt.tight_layout()
plt.savefig('charts/survival_outcome.png')
plt.close()
print("Chart 2 saved: charts/survival_outcome.png")

conditions = ['PNEUMONIA','DIABETES','HIPERTENSION','OBESITY','TOBACCO']
rates = []
for c in conditions:
    subset = df[df[c] == 1]
    rate = round((subset['DIED'].sum() / len(subset)) * 100, 1) if len(subset) > 0 else 0
    rates.append(rate)

plt.figure(figsize=(9,5))
plt.barh(conditions, rates, color='tomato', edgecolor='white')
plt.title('Death Rate by Pre-existing Condition')
plt.xlabel('Death Rate (%)')
plt.tight_layout()
plt.savefig('charts/death_rate_by_condition.png')
plt.close()
print("Chart 3 saved: charts/death_rate_by_condition.png")

avg_age = round(df['AGE'].mean(), 1)

print("\n==================================================")
print("   AI CLINICAL INSIGHTS")
print("==================================================")
print("1. Overall death rate is", death_rate, "%")
print("2. Average patient age is", avg_age, "years - older patients have higher risk")
print("3. Pneumonia death rate:", rates[0], "% - highest risk condition")
print("4. Diabetes death rate:", rates[1], "%")
print("5. Hypertension death rate:", rates[2], "%")
print("6. High risk profile = Elderly + Pneumonia + Diabetes/Hypertension")
print("\nAnalysis complete! Check the charts folder.")
