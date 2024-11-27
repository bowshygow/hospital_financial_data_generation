from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hospital_management import Base, Location, Department, Specialization, Doctor, Patient, Service, Bill, Scheme, PaymentType, Expense, ExpenseType

# Creating the database engine
engine = create_engine('sqlite:///hospital.db')

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

# Clear all data from tables
def clear_tables():
    session.query(Bill).delete()
    session.query(Service).delete()
    session.query(Doctor).delete()
    session.query(Patient).delete()
    session.query(Location).delete()
    session.query(Department).delete()
    session.query(Specialization).delete()
    session.query(Scheme).delete()
    session.query(PaymentType).delete()
    session.query(Expense).delete()
    session.query(ExpenseType).delete()
    session.commit()
    print("All tables have been cleared.")

# Run the function to clear the tables
if __name__ == "__main__":
    confirm = input("Are you sure you want to clear all tables? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_tables()
    else:
        print("Operation canceled.")