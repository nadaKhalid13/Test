import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
NUM_DRUGS = 50
NUM_SCIENTISTS = 20
NUM_PARTNERS = 25
NUM_TRIALS = 100
NUM_REVENUES = 200
NUM_COMPETITORS = 40
NUM_REGULATORY = 30
SEED = 42

faker = Faker()
random.seed(SEED)
np.random.seed(SEED)

# ----------------------------
# Helper Lists
# ----------------------------
therapeutic_areas = ["Oncology", "Cardiology", "Neurology", "Immunology", "Endocrinology"]
drug_types = ["Small Molecule", "Biologic", "Vaccine", "Gene Therapy"]
authorities = ["FDA", "EMA", "TGA", "PMDA", "MHRA"]
regions = ["US", "EU", "Asia", "LATAM", "MEA"]
stage_names = ["Discovery", "Preclinical", "Phase I", "Phase II", "Phase III"]

# ----------------------------
# Table 1: Scientists
# ----------------------------
scientists = []
for i in range(1, NUM_SCIENTISTS + 1):
    scientists.append({
        "ScientistID": i,
        "FullName": faker.name(),
        "Specialty": random.choice(therapeutic_areas),
        "Department": random.choice(["Pharmacology", "Molecular Biology", "Clinical Research"]),
        "Country": faker.country(),
        "YearsOfExperience": random.randint(3, 25)
    })
df_scientists = pd.DataFrame(scientists)

# ----------------------------
# Table 2: Drugs
# ----------------------------
drugs = []
for i in range(1, NUM_DRUGS + 1):
    drugs.append({
        "DrugID": i,
        "ScientistID": random.randint(1, NUM_SCIENTISTS),
        "DrugName": faker.lexify(text=random.choice(["Onco????", "Cardio????", "Neuro????", "Immuno????", "Endo????"])).capitalize(),
        "TherapeuticArea": random.choice(therapeutic_areas),
        "DrugType": random.choice(drug_types),
        "PatentStatus": random.choice(["Pending", "Granted", "Expired"])
    })
df_drugs = pd.DataFrame(drugs)

# ----------------------------
# Table 3: Regulatory
# ----------------------------
regulatory = []
for i in range(1, NUM_REGULATORY + 1):
    sub_date = faker.date_between("-2y", "-1y")
    approval_date = faker.date_between(sub_date, "today")
    regulatory.append({
        "SubmissionID": i,
        "Authority": random.choice(authorities),
        "SubmissionDate": sub_date,
        "ApprovalDate": approval_date,
        "Status": random.choice(["Pending", "Approved", "Rejected"]),
        "Comments": faker.sentence()
    })
df_regulatory = pd.DataFrame(regulatory)

# ----------------------------
# Table 4: Competitors
# ----------------------------
competitors = []
for i in range(1, NUM_COMPETITORS + 1):
    competitors.append({
        "CompetitorID": i,
        "DrugID": random.randint(1, NUM_DRUGS),
        "CompetitorDrugName": faker.lexify(text="????Drug"),
        "CompanyName": faker.company(),
        "City": faker.city(),
        "Country": faker.country()
    })
df_competitors = pd.DataFrame(competitors)

# ----------------------------
# Table 5: Partners
# ----------------------------
partners = []
for i in range(1, NUM_PARTNERS + 1):
    partners.append({
        "PartnerID": i,
        "PartnerName": faker.company(),
        "PartnershipType": random.choice(["Co-Development", "Licensing", "Funding"]),
        "Contribution": f"{random.randint(10, 60)}% Funding"
    })
df_partners = pd.DataFrame(partners)

# ----------------------------
# Table 6: Revenues
# ----------------------------
revenues = []
for i in range(1, NUM_REVENUES + 1):
    revenues.append({
        "RevenueID": i,
        "DrugID": random.randint(1, NUM_DRUGS),
        "Date": faker.date_between("-3y", "today"),
        "ForecastRevenueUSD": round(np.random.uniform(1e6, 5e8), 2),
        "ProbabilityAdjustedRevenueUSD": round(np.random.uniform(5e5, 3e8), 2),
        "MarketRegion": random.choice(regions)
    })
df_revenues = pd.DataFrame(revenues)

# ----------------------------
# Table 7: Clinical Trials
# ----------------------------
trials = []
for i in range(1, NUM_TRIALS + 1):
    start_date = faker.date_between("-3y", "-1y")
    end_date = faker.date_between(start_date, "today")
    trials.append({
        "TrialID": i,
        "DrugID": random.randint(1, NUM_DRUGS),
        "StageID": random.randint(1, 5),
        "TrialName": f"Trial_{i}",
        "Location": faker.city(),
        "NumberOfPatients": random.randint(50, 2000),
        "StartDate": start_date,
        "EndDate": end_date,
        "Result": random.choice(["Positive", "Negative", "Ongoing", "Terminated"])
    })
df_trials = pd.DataFrame(trials)

# ----------------------------
# Table 8: Pipeline Stages
# ----------------------------
pipeline_stages = []
for drug in df_drugs.itertuples():
    start_date = faker.date_between("-4y", "-2y")
    for s in stage_names:
        duration_months = random.randint(6, 24)
        expected_end = start_date + timedelta(days=30 * duration_months)
        actual_end = expected_end + timedelta(days=random.choice([0, 30, 60]))
        pipeline_stages.append({
            "StageID": len(pipeline_stages) + 1,
            "DrugID": drug.DrugID,
            "StartDate": start_date,
            "EndDate": expected_end,
            "StageName": s,
            "Notes": f"{s} completed successfully",
            "ActualEndDate": actual_end,
            "Category": random.choice(["R&D", "Clinical", "Regulatory", "Manufacturing"]),
            "DateIncurred": faker.date_between(start_date, actual_end),
            "Status": random.choice(["Completed", "Delayed"]),
            "AmountUSD": round(np.random.uniform(1e5, 3e7), 2),
            "Cost": round(np.random.uniform(5e4, 2e7), 2)
        })
        start_date = actual_end
df_pipeline_stages = pd.DataFrame(pipeline_stages)

# ----------------------------
# Table 9: Drug-Regulatory Relationship
# ----------------------------
drug_reg = []
for drug_id in range(1, NUM_DRUGS + 1):
    drug_reg.append({
        "DrugID": drug_id,
        "SubmissionID": random.randint(1, NUM_REGULATORY)
    })
df_drug_reg = pd.DataFrame(drug_reg)

# ----------------------------
# Table 10: Drug-Partners Relationship
# ----------------------------
drug_partners = []
for drug_id in range(1, NUM_DRUGS + 1):
    drug_partners.append({
        "DrugID": drug_id,
        "PartnerID": random.randint(1, NUM_PARTNERS)
    })
df_drug_partners = pd.DataFrame(drug_partners)

# ----------------------------
# EXPORT ALL TABLES
# ----------------------------
output_path = "pharma_dataset_normalized/"
os.makedirs(output_path, exist_ok=True)

tables = {
    "Scientists": df_scientists,
    "Drugs": df_drugs,
    "Regulatory": df_regulatory,
    "Competitors": df_competitors,
    "Partners": df_partners,
    "Revenues": df_revenues,
    "ClinicalTrials": df_trials,
    "PipelineStages": df_pipeline_stages,
    "Drug_Regulatory": df_drug_reg,
    "Drug_Partners": df_drug_partners
}

for name, df in tables.items():
    df.to_csv(f"{output_path}{name}.csv", index=False)

print(f"✅ Generated {len(tables)} normalized tables in '{output_path}'")