import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from functools import partial
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String, CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import uuid
Base = declarative_base()


class Measurement(Base):
    __tablename__ = "measurements"
    # f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")
    measurement_id = Column("measurement_id", String, primary_key=True)
    ven_id = Column("ven_id", String)
    measurement = Column("measurement", String)
    value = Column("value", Float)
    time = Column("time", String)
    resource_id = Column("resource_id", String)

    def __init__(self, measurement_id, ven_id, measurement, value, time, resource_id):
        self.measurement_id = measurement_id
        self.ven_id = ven_id
        self.measurement = measurement
        self.value = value
        self.time = time
        self.resource_id = resource_id

    def __repr__(self):
        return f"({self.measurement_id} {self.ven_id} {self.measurement} {self.value} {self.time} {self.resource_id})"

# class Person(Base):
#     __tablename__ = "people"
#     # Column
#     ssn = Column("ssn", Integer, primary_key=True)
#     firstname = Column("firstname", String)
#     lastname = Column("lastname", String)
#     gender = Column("gender", CHAR)
#     age = Column("age", Integer)

#     def __init__(self, ssn, first, last, gender, age):
#         self.ssn = ssn
#         self.firstname = first
#         self.lastname = last
#         self.gender = gender
#         self.age = age

#     def __repr__(self):
#         return f"({self.ssn} {self.firstname} {self.lastname} {self.gender} {self.age})"


# db environments
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/books'

print(f"DATABASE_URL  {DATABASE_URL}")


enable_default_logging()

# db
# db connection


def create_db_session(engine):
    Session = sessionmaker(bind=engine)

    session = Session()
    return session


def db_connection():
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("*************************")
        print("Connected db successfully")
        print("*************************")
        return engine

    except Exception as e:
        print(f"Connected to db failed {e}")


db_engine = db_connection()
db_session = create_db_session(db_engine)


async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    if registration_info['ven_name'] == 'ven123':
        ven_id = 'ven_id_123'
        registration_id = 'reg_id_123'
        return ven_id, registration_id
    else:
        return False


async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    callback = partial(on_update_report, ven_id=ven_id,
                       resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval


async def on_update_report(data, ven_id, resource_id, measurement):
    """
    Callback that receives report data from the VEN and handles it.
    """
    for time, value in data:
        print("--------------")
        print(
            f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")
        print("--------------")
        try:
            measurement_id = str(uuid.uuid4())
            measurement = Measurement(
                measurement_id=measurement_id, ven_id=ven_id, measurement=measurement, value=value, time=time, resource_id=resource_id)
            db_session.add(measurement)
            db_session.commit()
        except Exception as e:
            print(f"commit session failed :{e}")
    result = db_session.query(Measurement).all()
    print("--------------------")
    print(f"result: {result}")
    print("--------------------")


async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    print(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")


# Create the server object
server = OpenADRServer(vtn_id='myvtn',
                       http_host='0.0.0.0')

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration',
                   on_create_party_registration)

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

# Add a prepared event for a VEN that will be picked up when it polls for new messages.
server.add_event(ven_id='ven_id_123',
                 signal_name='simple',
                 signal_type='level',
                 intervals=[{'dtstart': datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                             'duration': timedelta(minutes=10),
                             'signal_payload': 1}],
                 callback=event_response_callback)

# Run the server on the asyncio event loop
loop = asyncio.get_event_loop()
loop.create_task(server.run())
loop.run_forever()
