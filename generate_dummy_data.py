from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hospital_management import Base, Location, Department, Specialization, Doctor, Patient, Service, Bill, Scheme, PaymentType, Expense, ExpenseType
from faker import Faker
import random
from datetime import datetime

# Create the database engine
engine = create_engine('sqlite:///hospital.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Faker
fake = Faker()

# Generate Dummy Data
def generate_dummy_data(num_records=1000):
    # Step 1: Generate Locations
    locations = []
    city_names = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami']
    for city_name in city_names:
        location = Location(name=city_name)
        session.add(location)
        locations.append(location)
    session.commit()
    
    # Step 2: Generate Departments
    departments = []
    department_names = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Surgery']
    for dept_name in department_names:
        department = Department(name=dept_name)
        session.add(department)
        departments.append(department)
    session.commit()

    # Step 3: Generate Specializations
    specializations = []
    specialization_names = ['Cardiologist', 'Neurologist', 'Orthopedic Surgeon', 'Pediatrician', 'General Surgeon']
    for specialization_name in specialization_names:
        specialization = Specialization(name=specialization_name)
        session.add(specialization)
        specializations.append(specialization)
    session.commit()

    # Step 4: Generate Doctors
    doctors = []
    for _ in range(20):  # Create 20 doctors
        doctor = Doctor(
            name=fake.name(),
            specialization=random.choice(specializations),
            department=random.choice(departments)
        )
        session.add(doctor)
        doctors.append(doctor)
    session.commit()

    # Step 5: Generate Patients
    patients = []
    for _ in range(num_records):  # Create num_records patients
        patient = Patient(
            name=fake.name(),
            age=random.randint(1, 90),  # Set realistic age range
            gender=random.choice(['Male', 'Female']),
            location=random.choice(locations)
        )
        session.add(patient)
        patients.append(patient)
    session.commit()

    # Step 6: Generate Services
    services = []
    service_names = ['ECG', 'MRI Scan', 'X-Ray', 'Blood Test', 'Physical Therapy']
    for _ in range(20):  # Generate 20 services
        service = Service(
            name=random.choice(service_names),
            cost=random.uniform(100, 500),  # Realistic service costs
            doctor=random.choice(doctors)
        )
        session.add(service)
        services.append(service)
    session.commit()

    # Step 7: Generate Schemes
    schemes = []
    scheme_names = ['HealthFirst', 'CarePlus', 'WellnessPlan']
    for scheme_name in scheme_names:
        scheme = Scheme(
            name=scheme_name,
            discount_percentage=random.uniform(5, 20)
        )
        session.add(scheme)
        schemes.append(scheme)
    session.commit()

    # Step 8: Generate Payment Types
    payment_types = []
    payment_types_list = ['Credit Card', 'Debit Card', 'Cash', 'Insurance']
    for payment_type_name in payment_types_list:
        payment_type = PaymentType(type=payment_type_name)
        session.add(payment_type)
        payment_types.append(payment_type)
    session.commit()

    # Step 9: Generate Bills
    for _ in range(num_records):  # Create num_records bills
        service = random.choice(services)
        discount = random.choice(schemes).discount_percentage
        original_cost = service.cost
        discounted_amount = original_cost - (original_cost * discount / 100)

        bill = Bill(
            patient=random.choice(patients),
            service=service,
            scheme=random.choice(schemes),
            amount=discounted_amount,
            payment_type=random.choice(payment_types),
            date=fake.date_between(start_date='-1y', end_date='today')
        )
        session.add(bill)
    session.commit()

    print(f"{num_records} patient records, services, and bills generated successfully!")

# Run the function to generate the dummy data
if __name__ == "__main__":
    generate_dummy_data(num_records=1000)
