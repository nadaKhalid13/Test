import mysql.connector
from faker import Faker
import random

# ✅ 1. Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # your DB has no password
    database="insurance_system"
)
cursor = db.cursor()
fake = Faker()

# ✅ 2. Insert fake clients
def insert_clients(n=20):
    for _ in range(n):
        full_name = fake.name()
        gender = random.choice(['Male', 'Female', 'Other'])
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        contact_number = fake.phone_number()
        city = fake.city()
        join_date = fake.date_time_this_decade()

        cursor.execute("""
            INSERT INTO Clients (full_name, gender, birth_date, contact_number, city, join_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, gender, birth_date, contact_number, city, join_date))
    db.commit()
    print(f"✅ Inserted {n} fake clients.")

# ✅ 3. Insert fake policies
def insert_policies(n=30):
    cursor.execute("SELECT client_id FROM Clients")
    client_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT policy_type_id FROM PolicyTypes")
    policy_type_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        client_id = random.choice(client_ids)
        policy_type_id = random.choice(policy_type_ids)
        policy_number = fake.unique.bothify(text="POL#######")
        start_date = fake.date_between(start_date='-2y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+1y')
        premium_amount = round(random.uniform(2000, 15000), 2)
        status = random.choice(['Active', 'Expired', 'Cancelled'])

        cursor.execute("""
            INSERT INTO Policies (client_id, policy_type_id, policy_number, start_date, end_date, premium_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (client_id, policy_type_id, policy_number, start_date, end_date, premium_amount, status))
    db.commit()
    print(f"✅ Inserted {n} fake policies.")

# ✅ 4. Insert fake claims
def insert_claims(n=25):
    cursor.execute("SELECT policy_id FROM Policies")
    policy_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        policy_id = random.choice(policy_ids)
        claim_date = fake.date_between(start_date='-1y', end_date='today')
        claim_amount = round(random.uniform(500, 5000), 2)
        status = random.choice(['Pending', 'Approved', 'Rejected', 'Paid'])
        description = fake.sentence(nb_words=10)

        cursor.execute("""
            INSERT INTO Claims (policy_id, claim_date, claim_amount, status, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (policy_id, claim_date, claim_amount, status, description))
    db.commit()
    print(f"✅ Inserted {n} fake claims.")

# ✅ 5. Insert fake payments
def insert_payments(n=50):
    cursor.execute("SELECT claim_id FROM Claims WHERE status IN ('Approved', 'Paid')")
    claim_ids = [row[0] for row in cursor.fetchall()]

    # If no eligible claims yet, allow from all
    if not claim_ids:
        cursor.execute("SELECT claim_id FROM Claims")
        claim_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        claim_id = random.choice(claim_ids)
        payment_date = fake.date_between(start_date='-6m', end_date='today')
        payment_amount = round(random.uniform(500, 5000), 2)
        payment_method = random.choice(['Bank Transfer', 'Check', 'Cash'])

        cursor.execute("""
            INSERT INTO Payments (claim_id, payment_date, payment_amount, payment_method)
            VALUES (%s, %s, %s, %s)
        """, (claim_id, payment_date, payment_amount, payment_method))
    db.commit()
    print(f"✅ Inserted {n} fake payments.")

# ✅ 6. Run everything in order
if __name__ == "__main__":
    insert_clients(20)
    insert_policies(30)
    insert_claims(25)
    insert_payments(50)
    print("🎉 Data generation complete.")
