import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your database
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password="",        # no password as you said
    database="insurance_system"
)
cursor = conn.cursor()

# Helper function to run queries and show results as tables
def run_query(query, description):
    print(f"\n📊 {description}")
    df = pd.read_sql(query, conn)
    print(df.head(10))  # show top 10 rows
    print("-" * 60)

# Load all claims and policies for visualization
claims = pd.read_sql("SELECT * FROM Claims", conn)
policies = pd.read_sql("""
    SELECT p.*, pt.type_name
    FROM Policies p
    JOIN PolicyTypes pt ON p.policy_type_id = pt.policy_type_id
""", conn)

# Query 1: Total Claims and Payments per Client
query1 = """
SELECT 
    c.client_id,
    c.full_name,
    COUNT(DISTINCT cl.claim_id) AS total_claims,
    SUM(p.payment_amount) AS total_paid
FROM Clients c
LEFT JOIN Policies po ON c.client_id = po.client_id
LEFT JOIN Claims cl ON po.policy_id = cl.policy_id
LEFT JOIN Payments p ON cl.claim_id = p.claim_id
GROUP BY c.client_id, c.full_name
ORDER BY total_paid DESC;
"""
run_query(query1, "Total Claims and Payments per Client")

# Query 2: Average Claim Amount per Policy Type
query2 = """
SELECT 
    pt.type_name AS policy_type,
    ROUND(AVG(c.claim_amount), 2) AS avg_claim_amount,
    COUNT(c.claim_id) AS total_claims
FROM PolicyTypes pt
JOIN Policies p ON pt.policy_type_id = p.policy_type_id
JOIN Claims c ON p.policy_id = c.policy_id
GROUP BY pt.type_name
ORDER BY avg_claim_amount DESC;
"""
run_query(query2, "Average Claim Amount per Policy Type")

# Query 3: Top 5 Policies by Total Claim Amount
query3 = """
SELECT 
    p.policy_number,
    c.claim_id,
    c.claim_amount,
    p.status AS policy_status
FROM Policies p
JOIN Claims c ON p.policy_id = c.policy_id
ORDER BY c.claim_amount DESC
LIMIT 5;
"""
run_query(query3, "Top 5 Policies by Total Claim Amount")



# Example: Total claims by status
claims_by_status = claims.groupby("status")["claim_id"].count()

claims_by_status.plot(kind="bar", color=["orange", "green", "red", "blue"])
plt.title("Number of Claims by Status")
plt.xlabel("Status")
plt.ylabel("Number of Claims")
plt.show()

# Example: Average premium by policy type
avg_premium = merged.groupby("type_name")["premium_amount"].mean()
avg_premium.plot(kind="barh", title="Average Premium by Policy Type")
plt.xlabel("Average Premium")
plt.ylabel("Policy Type")
plt.show()

# Clean up
cursor.close()
conn.close()
print("✅ All analyses completed.")



