from sqlalchemy import create_engine, ForeignKey, String, Integer, Column

# Allows use to use Classes/Models and sessions
from sqlalchemy.orm import sessionmaker, declarative_base

import uuid  # Creating unique identifiers

# Create database model
Base = declarative_base()


def generate_uuid():
    """
    Generates a unique id

    Returns:
        str: The generated unique id
    """
    return str(uuid.uuid4())


class users(Base):
    """
    The users class model.

    Args:
        Base (declaritive): The sqlalchemy base declarative.
    """

    __tablename__ = "users"
    userID = Column("userID", String, primary_key=True, default=generate_uuid)
    firstName = Column("firstName", String)
    lastName = Column("lastName", String)
    profileName = Column("profileName", String)
    email = Column("email", String)

    def __init__(self, firstName, lastName, profileName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.profileName = profileName
        self.email = email


# Create the database
db = "sqlite:///socialDB.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

# Creating a user
firstName = "chris"
lastName = "Adams"
profileName = "chrisadams"
email = "chrismichaeladams@gmail.com"
user = users(firstName, lastName, profileName, email)

# Add/Commit user to db
session.add(user)
session.commit()
print("user added to db...")
