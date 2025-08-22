from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# sqlalchemy setup
engine = create_engine("sqlite:///mydatabaseOrm.db", echo=True)
Base = declarative_base()


# ------------------ DB Models ------------------ #
class Person(Base):
    """
    Person class to create the people table.

    Args:
        Base (declarative): The SQLAlchemy declarative
    """

    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    # Establish relationship that a person has things
    things = relationship("Thing", back_populates="person")


class Thing(Base):
    """
    Thing class to create the things table.

    Args:
        Base (declarative): The SQLAlchemy declarative
    """

    __tablename__ = "things"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    # Setup foreign key relationship to people table
    owner = Column(Integer, ForeignKey("people.id"))

    # Establish relationship with all things a person owns
    person = relationship("Person", back_populates="things")


# ------------------ sqlalchemy setup and Session ------------------ #
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# ------------------ Add a new person to the db ------------------ #
# new_person = Person(name="Karen", age=44)
# session.add(new_person)

# ------------------ Flush DB before commit ------------------ #
# This will temporarily give us the person we created
# above without needing to commit, we will then have the
# id we can use in the new thing insert below.
# --------------------------------------------------------------- #
# session.flush()

# ------------------ Add a new thing to the db ------------------ #
# owner = new_person.id allows us to not specify an id but to
# use the id we just created above for the new person.
# --------------------------------------------------------------- #
# new_thing = Thing(description="Ipod", value=10, owner=new_person.id)
# session.add(new_thing)
# session.commit()

# ------------------ Accessing table data ------------------ #
# print([t.description for t in new_person.things])
# print(new_thing.person.name)

# ------------------ Selecting/Querying for data ------------------ #
result_people = session.query(Person).all()
result_things = session.query(Thing).all()
print([p.name for p in result_people])
print([t.description for t in result_things])

result_age_filter = session.query(Person).filter(Person.age > 70).all()
print([p.name for p in result_age_filter])

# Could also do .delete() and .update() vs .all() at end
result_things_filter = session.query(Thing).filter(Thing.value < 50).all()
print([t.description for t in result_things_filter])

result_all = session.query(Person.name).all()
print(result_all)

# ------------------ Joins ------------------ #
result_join = session.query(Person.name, Thing.description).join(Thing).all()
print(result_join)

# ------------------ Aggregation / Groupby ------------------ #
result_agg = (
    session.query(Thing.owner, func.sum(Thing.value)).group_by(Thing.owner).all()
)
print(result_agg)

# ------------------ Closing the session ------------------ #
session.close()
