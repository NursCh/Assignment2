from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

engine = create_engine('postgresql+psycopg2://assignment2db_4lz5_user:saClUJ1FJFJtLB4BulFBmAaG92MN7CJp\@dpg-cledk58lccns73e9ua5g-a/assignment2db_4lz5')

connection = engine.connect()
from sqlalchemy import Column,Integer,String,DateTime,Text,Float, Time
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, backref
from datetime import datetime

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer(), primary_key = True, nullable = False)
    email = Column(String(100), nullable = False, unique = True)
    given_name = Column(String(100), nullable = False)
    surname = Column(String(100), nullable = False)
    city = Column(String(100), nullable = False)
    phone_number = Column(String(100), nullable = False, unique = True)
    profile_description = Column(Text)
    password = Column(String(100), nullable = False)
        
    user_caregiver = relationship('Caregiver', backref = 'user', uselist = False, cascade = 'all, delete-orphan') 
    user_member = relationship('Member', backref = 'user', uselist = False, cascade = 'all, delete-orphan')
class Caregiver(Base):
    __tablename__ = 'caregiver'

    caregiver_user_id = Column(Integer(), ForeignKey('user.user_id' ,ondelete = 'CASCADE' ), primary_key = True) 
    photo = Column(String(100), nullable = False)
    gender = Column(String(20), nullable = False)
    caregiving_type = Column(String(50), nullable = False)
    CheckConstraint(caregiving_type.in_([ 'babysitter', 'caregiver for elderly','playmate for children']), name = "checkforcaretype"),
    hourly_rate = Column(Float(), nullable = False)
    
    caregiver_job_application = relationship('Job_application', backref = 'caregiver',cascade = 'all, delete-orphan')  
    caregiver_job_appointment = relationship('Appointment', backref = 'caregiver',cascade = 'all, delete-orphan')  

class Member(Base):
    __tablename__ = 'member'

    member_user_id = Column(Integer(), ForeignKey('user.user_id' ,ondelete = 'CASCADE' ), nullable = False, primary_key = True)
    house_rules = Column(Text())

    member_address = relationship('Address', backref = 'member', uselist = False) 
    member_job = relationship('Job', backref = 'member') 
    member_job_appointment = relationship('Appointment', backref = 'member', cascade = 'all, delete-orphan')  
class Address(Base):
    __tablename__ = 'address'

    member_user_id = Column(Integer(), ForeignKey('member.member_user_id' ,ondelete = 'CASCADE' ), nullable = False, primary_key = True) 
    house_number = Column(Integer(), nullable = False)
    street = Column(String(100), nullable = False)
    town = Column(String(100), nullable = False)

class Job(Base):
    __tablename__ = 'job'

    job_id = Column(Integer(), primary_key = True, nullable = False)
    member_user_id = Column(Integer(), ForeignKey('member.member_user_id' ,ondelete = 'CASCADE' ), nullable = False )
    required_caregiving_type = Column(String(50), nullable = False)
    CheckConstraint(required_caregiving_type.in_([ 'babysitter', 'caregiver for elderly','playmate for children']), name = "checkforcaretype"),
    other_requirements = Column(Text)
    date_posted = Column(DateTime(), nullable = False)
    job_id_application = relationship('Job_application', backref = 'job', cascade = 'all, delete-orphan') 
class Job_application(Base):
    __tablename__ = 'job_application'

    job_id = Column(Integer(), ForeignKey('job.job_id' ,ondelete = 'CASCADE' ), primary_key = True)
    caregiver_user_id = Column(Integer(), ForeignKey('caregiver.caregiver_user_id' ,ondelete = 'CASCADE' ), primary_key = True)
    date_applied = Column(DateTime(),nullable = False)
class Appointment(Base):
    __tablename__ = 'appointment'

    appointment_id = Column(Integer(), nullable = False, primary_key = True)
    caregiver_user_id = Column(Integer(), ForeignKey('caregiver.caregiver_user_id' ,ondelete = 'CASCADE' ), nullable = False)
    member_user_id = Column(Integer(), ForeignKey('member.member_user_id' ,ondelete = 'CASCADE' ), nullable = False)
    appointment_date = Column(DateTime, nullable = False)
    appointment_time = Column(Time, nullable = False)
    work_hours = Column(Float(),nullable = False)
    status = Column(String(30), nullable = False)
    CheckConstraint(status.in_(['confirmed','declined','waiting']))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

user1 = User( 
    email = 'bolat1@gmail.com',
    given_name = 'Jonh',
    surname = 'Bolatov',
    city = 'Astana',
    phone_number = '88005553535',
    profile_description = 'Cool guy',
    password = '123'
)

user2 = User( 
    email = 'email1@gmail.com',
    given_name = 'Bolat',
    surname = 'Familiya',
    city = 'Almaty',
    phone_number = '+77039284955',
    profile_description = 'Very handsome',
    password = '12311111'
)
user3 = User( 
    email = 'email2@gmail.com',
    given_name = 'Askar',
    surname = 'Askarov',
    city = 'Astana',
    phone_number = '+9139120393',
    profile_description = 'Professional footbal player',
    password = '12312312312312'
)
user4 = User(
    email = 'email3@gmail.com',
    given_name = 'Askar',
    surname = 'Bolatov',
    city = 'Astana',
    phone_number = '+9999999999',
    profile_description = 'Bolat bolatov is my brother',
    password = '123111111111111111111'
)

user5 = User(
    email = 'email4@gmail.com',
    given_name = 'Ivan',
    surname = 'Ivanov',
    city = 'Kokshetay',
    phone_number = '+3213219999',
    profile_description = 'Hello i am Ivan',
    password = '1231111113'
)

user6 = User(
    email = 'email5@gmail.com',
    given_name = 'Asem',
    surname = 'Asemova',
    city = 'Astana',
    phone_number = '+7743849523',
    profile_description = 'Where am I',
    password = '12000001'
)
user7 = User(
    email = 'email6@gmail.com',
    given_name = 'Asem',
    surname = 'Bolatov',
    city = 'Almaty',
    phone_number = '+999993123129999',
    profile_description = 'Bolat bolatov is my brother',
    password = '12300001111111111'
)
user8 = User(
    email = 'email7@gmail.com',
    given_name = 'Bolatbeek',
    surname = 'Ashura',
    city = 'Astana',
    phone_number = '+9777832159',
    profile_description = 'Bolat bolatov is not my brother',
    password = '00234511111111'
)
user9 = User(
        email = 'email8@gmail.com',
    given_name = 'Asuka',
    surname = 'Thanos',
    city = 'Astana',
    phone_number = '+111134953',
    profile_description = 'Ok',
    password = '012311110'
)
user10 = User(
    email = 'email9@gmail.com',
    given_name = 'Asuka',
    surname = 'Bolatov',
    city = 'Astana',
    phone_number = '+9999012349',
    profile_description = 'Bolat bolatov is my brother',
    password = '1'
)
user11 = User( 
    email = 'email11@gmail.com',
    given_name = 'Bolat',
    surname = 'Bolatov',
    city = 'Moscow',
    phone_number = '8832323122',
    profile_description = 'I am from Russia',
    password = '1000000000000'
)

user12 = User( 
    email = 'email12@gmail.com',
    given_name = 'JeiJei',
    surname = 'Kennedy',
    city = 'New York',
    phone_number = '+732321321',
    profile_description = 'I like chicken kebab',
    password = '1238806957056'
)
user13 = User( 
    email = 'email13@gmail.com',
    given_name = 'Antio',
    surname = 'Rodriges',
    city = 'Mexico',
    phone_number = '+666666666',
    profile_description = 'Professional dota 2 player',
    password = '12312312312312'
)
user14 = User(
    email = 'email14@gmail.com',
    given_name = 'Anton',
    surname = 'Dyrachyo',
    city = 'Almaty',
    phone_number = '+12345679',
    profile_description = 'Professional Dota 2 player. Major winner. Best carry in the world',
    password = '12301'
)

user15 = User(
    email = 'email15@gmail.com',
    given_name = 'Jessy',
    surname = 'Pinkman',
    city = 'Kokshetay',
    phone_number = '+3221312312',
    profile_description = 'Hello. I know chemistry',
    password = '13'
)

user16 = User(
    email = 'email16@gmail.com',
    given_name = 'Saul',
    surname = 'Goodman',
    city = 'Astana',
    phone_number = '+2227743849523',
    profile_description = 'Where am I',
    password = '9'
)
user17 = User(
    email = 'email17@gmail.com',
    given_name = 'Korol',
    surname = 'Arthas',
    city = 'Almaty',
    phone_number = '+99129999',
    profile_description = 'Best in the world',
    password = '12345678'
)
user18 = User(
    email = 'email18@gmail.com',
    given_name = 'Wraith',
    surname = 'King',
    city = 'Astana',
    phone_number = '+9772159',
    profile_description = 'Arthas is my brother',
    password = '00234511111'
)
user19 = User(
    email = 'email19@gmail.com',
    given_name = 'Rost1k',
    surname = 'Earth',
    city = 'Astana',
    phone_number = '+111111134953',
    profile_description = 'NS',
    password = '0120'
)
user20 = User(
    email = 'email20@gmail.com',
    given_name = 'Nix',
    surname = 'Fruit',
    city = 'Astana',
    phone_number = '+012349',
    profile_description = 'I eat only fruits',
    password = '19')

caregiver1 = Caregiver(
    user = user1,
    photo = "abpba1",
    gender = "male",
    caregiving_type = "babysitter",
    hourly_rate = 0.5
    )
caregiver2 = Caregiver(
    user = user2,
    photo = "abpba2",
    gender = "male",
    caregiving_type = "babysitter",
    hourly_rate = 1.5
    )
caregiver3 = Caregiver(
    user = user3,
    photo = "abpba3",
    gender = "female",
    caregiving_type = "babysitter",
    hourly_rate = 0.9
    )
caregiver4 = Caregiver(
    user = user4,
    photo = "abpba4",
    gender = "female",
    caregiving_type = "babysitter",
    hourly_rate = 2.0
    )
caregiver5 = Caregiver(
    user = user5,
    photo = "abpba5",
    gender = "male",
    caregiving_type = "caregiver for elderly",
    hourly_rate = 3.0
    )
caregiver6 = Caregiver(
    user = user6,
    photo = "abpba6",
    gender = "female",
    caregiving_type = "caregiver for elderly",
    hourly_rate = 4.0
    )
caregiver7 = Caregiver(
    user = user7,
    photo = "abpba7",
    gender = "female",
    caregiving_type = "caregiver for elderly",
    hourly_rate = 0.1
    )
caregiver8 = Caregiver(
    user = user8,
    photo = "abpba8",
    gender = "male",
    caregiving_type = "playmate for children",
    hourly_rate = 8.6
    )
caregiver9 = Caregiver(
    user = user9,
    photo = "abpba9",
    gender = "female",
    caregiving_type = "playmate for children",
    hourly_rate = 9.1
    )
caregiver10 = Caregiver(
    user = user10,
    photo = "abpba10",
    gender = "male",
    caregiving_type = "playmate for children",
    hourly_rate = 20.0
    )
member1 = Member(
        user = user11,
        house_rules = 'No pets. No food'
        )
member2 = Member(
        user = user12,
        house_rules = 'Be clean. Be gentle. Be smart'
        )

member3 = Member(
        user = user13,
        house_rules = 'No pets allowed in the house'
        )
member4 = Member(
        user = user14,
        house_rules = 'Yes pets please i like cats.'
        )
member5 = Member(
        user = user15,
        house_rules = 'I love pets, especially dogs'
        )
member6 = Member(
        user = user16,
        house_rules = 'No music'
        )
member7 = Member(
        user = user17,
        house_rules = 'Be quite'
        )
member8 = Member(
        user = user18,
        house_rules = 'MAKE SOME NOISE'
        )
member9 = Member(
        user = user19,
        house_rules = 'No pets no '
        )
member10 = Member(
        user = user20,
        house_rules = 'THERE IS NO RULES!!!'
        )
address1 = Address(
        member = member1,
        house_number = '1',
        street = 'Buran street',
        town = 'Astana',
        )
address2 = Address(
        member = member2,
        house_number = '2',
        street = 'Buran street',
        town = 'Astana',
        )
address3 = Address(
        member = member3,
        house_number = '3',
        street = 'Turan street',
        town = 'Astana',
        )
address4 = Address(
        member = member4,
        house_number = '4',
        street = 'Kabanbay Batyr street',
        town = 'Astana',
        )
address5 = Address(
        member = member5,
        house_number = '5',
        street = 'Kabanbay Batyr street',
        town = 'Almaty',
        )
address6 = Address(
        member = member6,
        house_number = '6',
        street = 'Pushikina street',
        town = 'Moscow',
        )
address7 = Address(
        member = member7,
        house_number = '7',
        street = 'Orynbor street',
        town = 'Astana',
        )
address8 = Address(
        member = member8,
        house_number = '8',
        street = 'Saryarka street',
        town = 'Astana',
        )
address9 = Address(
        member = member9,
        house_number = '9',
        street = 'Mangyluk street',
        town = 'Astana',
        )

address10 = Address(
        member = member10,
        house_number = '10',
        street = 'Mangyluk street',
        town = 'Astana',
        )
job1 = Job(
        member = member1,
        required_caregiving_type = 'babysitter',
        other_requirements = 'Be gentle, be smart. be good',
        date_posted = datetime(2023,11,18,1,2,3)
        )

job2 = Job(
        member = member1,
        required_caregiving_type = 'caregiver for elderly',
        other_requirements = 'Beware we have gentle dogs',
        date_posted = datetime(2023,11,19,4,5,6)
        )

job3 = Job(
        member = member1,
        required_caregiving_type = 'playmate for children',
        other_requirements = 'Know how to play instrument',
        date_posted = datetime(2023,10,18,12,13,14)
        )
job4 = Job(
        member = member1,
        required_caregiving_type = 'babysitter',
        other_requirements = 'Do not scream at the baby',
        date_posted = datetime(2023,11,10,15,24,26)
        )
job5 = Job(
        member = member2,
        required_caregiving_type = 'babysitter',
        other_requirements = 'Be gentle with the child',
        date_posted = datetime(2023,11,1,5,35,40)
        )
job6 = Job(
        member = member3,
        required_caregiving_type = 'caregiver for elderly',
        other_requirements = 'Be gentle be dog',
        date_posted = datetime(2023,11,8,7,43,35)
        )
job7 = Job(
        member = member4,
        required_caregiving_type = 'babysitter',
        other_requirements = 'WE HATE DOGS',
        date_posted = datetime(2023,1,13,7,10,23)
        )
job8 = Job(
        member = member2,
        required_caregiving_type = 'playmate for children',
        other_requirements = 'He is adopted, be nice',
        date_posted = datetime(2023,5,10,2,42,40)
        )
job9 = Job(
        member = member3,
        required_caregiving_type = 'caregiver for elderly',
        other_requirements = 'He is very artistic, be patient',
        date_posted = datetime(2023,4,5)
        )
job10 = Job(
        member = member2,
        required_caregiving_type = 'babysitter',
        other_requirements = 'Be gentle, be smart. be good',
        date_posted = datetime(2023,3,7)
        )
job_application1 = Job_application(
        caregiver = caregiver1,
        job = job1,
        date_applied = datetime(2024,1,2)
        )
job_application2 = Job_application(
        caregiver = caregiver1,
        job = job2,
        date_applied = datetime(2024,1,5)
        )
job_application3 = Job_application(
        caregiver = caregiver1,
        job = job3,
        date_applied = datetime(2024,1,6)
        )
job_application4 = Job_application(
        caregiver = caregiver2,
        job = job6,
        date_applied = datetime(2024,1,8)
        )
job_application5 = Job_application(
        caregiver = caregiver2,
        job = job4,
        date_applied = datetime(2024,1,21)
        )
job_application6 = Job_application(
        caregiver = caregiver3,
        job = job3,
        date_applied = datetime(2024,1,19)
        )
job_application7 = Job_application(
        caregiver = caregiver3,
        job = job4,
        date_applied = datetime(2024,1,14)
        )
job_application8 = Job_application(
        caregiver = caregiver4,
        job = job8,
        date_applied = datetime(2024,1,13)
        )
job_application9 = Job_application(
        caregiver = caregiver4,
        job = job5,
        date_applied = datetime(2024,1,1)
        )
job_application10 = Job_application(
        caregiver = caregiver5,
        job = job5,
        date_applied = datetime(2024,1,2)
        )
appointment1 = Appointment(
    caregiver = caregiver1,
    member = member1,
    appointment_date = datetime(2024,2,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 1,
    status = 'confirmed'
        )
appointment2 = Appointment(
    caregiver = caregiver1,
    member = member2,
    appointment_date = datetime(2024,2,1),
    appointment_time = datetime.time(datetime(2024,2,1,13,0,0)),    
    work_hours = 2,
    status = 'confirmed'
        )
appointment3 = Appointment(
    caregiver = caregiver1,
    member = member3,
    appointment_date = datetime(2024,2,1),
    appointment_time = datetime.time(datetime(2024,2,1,14,0,0)),    
    work_hours = 3,
    status = 'confirmed'
        )
appointment4 = Appointment(
    caregiver = caregiver2,
    member = member1,
    appointment_date = datetime(2024,2,1),
    appointment_time = datetime.time(datetime(2024,2,1,15,0,0)),    
    work_hours = 5,
    status = 'confirmed'
        )
appointment5 = Appointment(
    caregiver = caregiver2,
    member = member2,
    appointment_date = datetime(2024,4,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 1,
    status = 'declined'
        )
appointment6 = Appointment(
    caregiver = caregiver2,
    member = member3,
    appointment_date = datetime(2024,4,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 4,
    status = 'declined'
        )
appointment7 = Appointment(
    caregiver = caregiver3,
    member = member4,
    appointment_date = datetime(2024,3,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 7,
    status = 'confirmed'
        )
appointment8 = Appointment(
    caregiver = caregiver4,
    member = member5,
    appointment_date = datetime(2024,3,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 13,
    status = 'declined'
        )
appointment9 = Appointment(
    caregiver = caregiver4,
    member = member6,
    appointment_date = datetime(2024,3,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 4,
    status = 'confirmed'
        )
appointment10 = Appointment(
    caregiver = caregiver5,
    member = member4,
    appointment_date = datetime(2024,2,1),
    appointment_time = datetime.time(datetime(2024,2,1,12,0,0)),    
    work_hours = 1,
    status = 'confirmed'
        )

session.add_all([user1,user2,user3,user4,user5,user6,user7,user8,user9,user10,user11,user12,user13,user14,user15,user16,user17,user18,user19,user20])
session.add_all([caregiver1,caregiver2,caregiver3,caregiver4,caregiver5,caregiver6,caregiver7,caregiver8,caregiver9,caregiver10])
session.add_all([member1,member2,member3,member4,member5,member6,member7,member8,member9,member10])
session.add_all([address1,address2,address3,address4,address5,address6,address7,address8,address9,address10])
session.add_all([job1,job2,job3,job4,job5,job6,job7,job8,job9,job10])
session.add_all([job_application1,job_application2,job_application3,job_application4,job_application5,job_application6,job_application7,job_application8,job_application9,job_application10])
session.add_all([appointment1])
session.commit()

from sqlalchemy import select
print("Before:")
askar_user = session.query(User).\
        filter(User.given_name == 'Askar', User.surname == 'Askarov').all()
for x in askar_user:
    print(x.phone_number)

askar_user = session.query(User).\
        filter(User.given_name == 'Askar', User.surname == 'Askarov').\
        update({'phone_number' : '+77771010001'})
session.commit()
print("After:")
askar_user = session.query(User).\
        filter(User.given_name == 'Askar', User.surname == 'Askarov').all()
for x in askar_user:
    print(x.phone_number)
print("Before:")
Caregivers_fee = session.query(Caregiver).\
        filter(Caregiver.hourly_rate < 9).all()
for x in Caregivers_fee:
    print(x.hourly_rate)
Caregivers_fee = session.query(Caregiver).\
        filter(Caregiver.hourly_rate > 9).all()
for x in Caregivers_fee:
    print(x.hourly_rate)

Caregivers_fee = session.query(Caregiver).\
        filter(Caregiver.hourly_rate > 9).\
        update({'hourly_rate': Caregiver.hourly_rate *1.1})
Caregivers_fee = session.query(Caregiver).\
        filter(Caregiver.hourly_rate < 9).\
        update({'hourly_rate': Caregiver.hourly_rate + 0.5})
session.commit()
print("After")
Caregivers_fee = session.query(Caregiver).\
        filter(Caregiver.hourly_rate < 9).all()
for x in Caregivers_fee:
    print(x.hourly_rate)
Caregivers_fee = session.query(Caregiver).\
        filter(Caregiver.hourly_rate > 9).all()
for x in Caregivers_fee:
    print(x.hourly_rate)

print("Before:")
Bolat = session.query(Job).\
        filter(Job.member_user_id == Member.member_user_id, Member.member_user_id == User.user_id, User.given_name == 'Bolat', User.surname == 'Bolatov' ).all()
for x in Bolat:
    print(x)

Bolat = session.query(Job_application).\
        filter(Job_application.job_id == Job.job_id, Job.member_user_id == Member.member_user_id, Member.member_user_id == User.user_id, User.given_name == 'Bolat', User.surname == 'Bolatov' ).\
        delete()

Bolat = session.query(Job).\
        filter(Job.member_user_id == Member.member_user_id, Member.member_user_id == User.user_id, User.given_name == 'Bolat', User.surname == 'Bolatov' ).\
        delete()
session.commit()

print("After: ")
Bolat = session.query(Job).\
        filter(Job.member_user_id == Member.member_user_id, Member.member_user_id == User.user_id, User.given_name == 'Bolat', User.surname == 'Bolatov' ).all()
for x in Bolat:
    print(x)

print("Before:")
Turan = session.query(Member).\
        filter(Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').all()
for x in Turan:
    print(x)


Turan = session.query(Appointment).\
        filter(Appointment.member_user_id == Member.member_user_id, Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').\
        delete()
Turan = session.query(Job_application).\
        filter(Job_application.job_id == Job.job_id, Job.member_user_id == Member.member_user_id, Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').\
        delete()
Turan = session.query(Job).\
        filter(Job.member_user_id == Member.member_user_id, Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').\
        delete()
Turan = session.query(Address).\
        filter(Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').\
        delete()
Turan = session.query(Member).\
        filter(Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').\
        delete()
session.commit()
print("After:")
Turan = session.query(Member).\
        filter(Member.member_user_id == Address.member_user_id, Address.street == 'Turan street').all()
for x in Turan:
    print(x)
print("Simple queries")
print("Caregiver and member names:")
caregiver_n_member = session.query(Caregiver, Member).\
        filter(Appointment.member_user_id == Member.member_user_id, Appointment.caregiver_user_id == Caregiver.caregiver_user_id, Appointment.status == 'confirmed').all()
for x in caregiver_n_member:
    print("Caregiver: " + x[0].user.given_name + " " + x[0].user.given_name)
    print("Member: " + x[1].user.given_name + " " + x[1].user.surname)

print('Job ids: ')
job_gentle = session.query(Job).\
        filter(Job.other_requirements.match("%gentle%")).all()

for x in job_gentle:
    print(x.job_id)

babysitter_hours = session.query(Appointment).\
        filter(Job.member_user_id == Appointment.member_user_id, Job.required_caregiving_type == 'babysitter').all()
    
print("work hours")
for x in babysitter_hours:
    print(x.work_hours)

member_no_pets = session.query(Member).\
        filter(Member.house_rules.match("%No pets%")).all()
print("member with no pets:")
for x in member_no_pets:
    print(x)
from sqlalchemy import func


stmt = select(Member,Job).join_from(Member,Job)


print("NumberofApplicants: ")
for row in session.execute(stmt):
    number = session.query(Job,Job_application).filter(row[1].job_id == Job_application.job_id).join(Job_application).count()
    print("Member_id: {} Job_id: {} Number: {}".format(row[0].member_user_id, row[1].job_id, number ))


stmt = select(Caregiver, Appointment).join_from(Caregiver,Appointment).filter(Appointment.status == 'confirmed')



print("Total_work_hours: ")

for row in session.execute(stmt):
    print("Caregiver_id: {} work_hours: {} ".format(row[0].caregiver_user_id, row[1].work_hours))


sum_query = select(func.sum(Appointment.work_hours), Appointment.caregiver_user_id).filter(Appointment.status == 'confirmed').group_by(Appointment.caregiver_user_id)

for row in session.execute(sum_query).fetchall():
    print ("Caregiver id: {}, Sum: {}".format(row[1], row[0]))

print("Average: ")

sum_query = select(func.avg(Caregiver.hourly_rate*Appointment.work_hours)).filter(Appointment.status == 'confirmed', Appointment.caregiver_user_id == Caregiver.caregiver_user_id)

print (session.execute(sum_query).all())

sum_query = select(Caregiver.hourly_rate, Appointment.work_hours,Caregiver.caregiver_user_id).filter(Appointment.status == 'confirmed', Appointment.caregiver_user_id == Caregiver.caregiver_user_id)

for row in session.execute(sum_query):
    print ("Caregiver id:{}  Rate: {}  Work_hours: {}".format(row[2], row[0],row[1]))

print("Who earn > average: ")

sub_query = select(func.avg(Caregiver.hourly_rate*Appointment.work_hours)).join_from(Caregiver,Appointment).filter(Appointment.status == 'confirmed', Appointment.caregiver_user_id == Caregiver.caregiver_user_id).scalar_subquery().correlate()
above_query = select(Caregiver).join_from(Caregiver,Appointment).filter(Caregiver.caregiver_user_id == Appointment.caregiver_user_id, Appointment.status == 'confirmed', Caregiver.hourly_rate * Appointment.work_hours > sub_query)


for row in session.execute(above_query):
    print(row[0].caregiver_user_id)

sum_query = select(func.sum(Caregiver.hourly_rate*Appointment.work_hours)).filter(Appointment.status == 'confirmed', Appointment.caregiver_user_id == Caregiver.caregiver_user_id)

print(session.execute(sum_query).all())


view_query = select(Job_application, Caregiver).join_from(Job_application, Caregiver)

for row in session.execute(view_query):
    print( "Job_application: {} Applicant: {}".format(row[0].job_id,row[1].caregiver_user_id))

#from sqlalchemy.ext.compiler import compiles
#from sqlalchemy.sql.expression import Executable, ClauseElement

#createview = CreateView('job_and_applicants', Job.select().where(Job.job_id == Job_application.job_id), Caregiver.select().where(Job_application.caregiver_user_id == Caregiver.caregiver_user_id))

#session.execute(createview)

#view = Table('job_and_applicants', metadata, autoload = True)
#for row in engine.execute(view.select()):
#    print (row)

#session.query(Caregiver,Appointment).\
#        filter(Appointment.status == 'confirmed', Caregiver.caregiver_user_id == Appointment.caregiver_user_id).\
#        func.sum(Appointment.work_hours)

#NumberofApplicants = session.query(Member,Job,func.count(Job_application.caregiver_user_id)).\
 #       join(Job).\
  #      join(Job_application).\
   #     group_by(Member).\
    #    group_by(Job)

#for row in NumberofApplicants.select_from(Member.member_user_id):
 #   print(row)

