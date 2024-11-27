from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Patient Model
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'))
    
    bills = relationship('Bill', back_populates='patient')
    location = relationship('Location', back_populates='patients')

# Location Model
class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    patients = relationship('Patient', back_populates='location')

# Doctor Model
class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization_id = Column(Integer, ForeignKey('specializations.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='doctors')
    services = relationship('Service', back_populates='doctor')
    specialization = relationship('Specialization', back_populates='doctors')

# Specialization Model
class Specialization(Base):
    __tablename__ = 'specializations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    doctors = relationship('Doctor', back_populates='specialization')

# Service Model
class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))

    doctor = relationship('Doctor', back_populates='services')
    bills = relationship('Bill', back_populates='service')

# Bill Model
class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    scheme_id = Column(Integer, ForeignKey('schemes.id'))
    amount = Column(Float, nullable=False)
    payment_type_id = Column(Integer, ForeignKey('payment_types.id'))
    date = Column(Date, nullable=False)

    patient = relationship('Patient', back_populates='bills')
    service = relationship('Service', back_populates='bills')
    scheme = relationship('Scheme', back_populates='bills')
    payment_type = relationship('PaymentType', back_populates='bills')

# Scheme Model
class Scheme(Base):
    __tablename__ = 'schemes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    discount_percentage = Column(Float, nullable=False)

    bills = relationship('Bill', back_populates='scheme')

# Payment Type Model
class PaymentType(Base):
    __tablename__ = 'payment_types'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    bills = relationship('Bill', back_populates='payment_type')

# Department Model
class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    doctors = relationship('Doctor', back_populates='department')
    expenses = relationship('Expense', back_populates='department')

# Expense Model
class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    type_id = Column(Integer, ForeignKey('expense_types.id'))
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    department = relationship('Department', back_populates='expenses')
    expense_type = relationship('ExpenseType', back_populates='expenses')

# Expense Type Model
class ExpenseType(Base):
    __tablename__ = 'expense_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Labour, Utilities, Equipment

    expenses = relationship('Expense', back_populates='expense_type')

# Creating the database
engine = create_engine('sqlite:///hospital.db')
Base.metadata.create_all(engine)

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

# Example data to populate the database
location_ny = Location(name='New York')
location_la = Location(name='Los Angeles')
session.add(location_ny)
session.add(location_la)
session.commit()

cardiology = Department(name='Cardiology')
general_surgery = Department(name='General Surgery')
session.add(cardiology)
session.add(general_surgery)
session.commit()

specialization_cardio = Specialization(name='Cardiologist')
specialization_surgeon = Specialization(name='Surgeon')
session.add(specialization_cardio)
session.add(specialization_surgeon)
session.commit()

# Adding doctors
doctor_1 = Doctor(name='Dr. Smith', specialization=specialization_cardio, department=cardiology)
doctor_2 = Doctor(name='Dr. Brown', specialization=specialization_surgeon, department=general_surgery)
session.add(doctor_1)
session.add(doctor_2)
session.commit()

# Adding patients
patient_1 = Patient(name='John Doe', age=45, gender='Male', location=location_ny)
patient_2 = Patient(name='Jane Roe', age=36, gender='Female', location=location_la)
session.add(patient_1)
session.add(patient_2)
session.commit()

# Adding services
service_1 = Service(name='ECG', cost=200, doctor=doctor_1)
service_2 = Service(name='Appendectomy', cost=3000, doctor=doctor_2)
session.add(service_1)
session.add(service_2)
session.commit()

# Adding schemes and payment types
scheme_1 = Scheme(name='HealthFirst', discount_percentage=10)
payment_type_1 = PaymentType(type='Credit Card')
session.add(scheme_1)
session.add(payment_type_1)
session.commit()

# Adding expense types
expense_type_labour = ExpenseType(name='Labour')
expense_type_utilities = ExpenseType(name='Utilities')
expense_type_equipment = ExpenseType(name='Equipment')
session.add(expense_type_labour)
session.add(expense_type_utilities)
session.add(expense_type_equipment)
session.commit()

# Adding bills
bill_1 = Bill(patient=patient_1, service=service_1, scheme=scheme_1, amount=180, payment_type=payment_type_1, date=datetime.strptime('2024-11-25', '%Y-%m-%d').date())
session.add(bill_1)
session.commit()
    