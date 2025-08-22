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
    A user can have many posts.

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


class posts(Base):
    """
    The posts class model.
    This is a one to many relationship. With a foreign key from
    the users table.
    A post can only have one creator, and a user can have many
    posts.

    Args:
        Base (declaritive): The sqlalchemy base declarative.
    """

    __tablename__ = "posts"
    postId = Column("postId", String, primary_key=True, default=generate_uuid)
    userId = Column("userId", String, ForeignKey("users.userID"))
    postContent = Column("postContent", String)

    def __init__(self, userId, postContent):
        self.userId = userId
        self.postContent = postContent


class likes(Base):
    """
    Class representing likes in the db.

    Args:
        Base (declaritive): The sqlalchemy base declarative.
    """

    __tablename__ = "likes"
    likeId = Column("likedId", String, primary_key=True, default=generate_uuid)
    userId = Column("userId", String, ForeignKey("users.userID"))
    postId = Column("postId", String, ForeignKey("posts.postId"))

    def __init__(self, userId, postId):
        self.userId = userId
        self.postId = postId


def addUser(session, firstName, lastName, profileName, email):
    """
    Adds a user to the db.

    Args:
        session (sqlalchemy): The sqlalchemy session.
        firstName (str): The first name.
        lastName (str): The lastt name.
        profileName (str): The profile name.
        email (str): The email.
    """

    # Seaches all user's email addresses and sees if it
    # matches user we are creating and it exists.
    exist = session.query(users).filter(users.email == email).all()

    # Don't create db entry of email already exists.
    if len(exist) > 0:
        print("Email address already exists!")
    else:
        # Creating a user
        user = users(firstName, lastName, profileName, email)

        # Add/Commit users to db
        session.add(user)
        session.commit()
        print("user added to db...")


def addPost(session, userId, postContent):
    """
    Adds a post to the database.

    Args:
        session (sqlalchemy): The sqlalchemy session.
        userId (str): The user id.
        postContent (str): The post content.
    """
    newPost = posts(userId, postContent)
    session.add(newPost)
    session.commit()
    print("post added to db...")


def addLike(userId, postId):
    like = likes(userId, postId)
    session.add(like)
    session.commit()
    print("like added to db...")


# Create the database
db = "sqlite:///socialDB.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

# Sample User data:
# firstName = "Jane"
# lastName = "DoeAdear"
# profileName = "JaneTheDeer"
# email = "janeBigBuckHunter@gmail.com"
# addUser(session, firstName, lastName, profileName, email)


# Sample Post data for user 1
# userId = "07186c6a-cb99-4615-ba61-050256fcde61"
# postContent = "Who let the dogs out!"
# addPost(session, userId, postContent)

# Sample Post data for user 2
# userId = "ab1c46e9-83a0-4953-9b2f-d488aa1b1606"
# postContent = "Let's put the smack down on the beach!"
# addPost(session, userId, postContent)

# Sample Post data for user 3
# userId = "0d588e1b-d3ac-478c-ad73-9d98b80aa2aa"
# postContent = "Let's meet at 5pm"
# addPost(session, userId, postContent)

# Get all the post from a specific user
userId = "0d588e1b-d3ac-478c-ad73-9d98b80aa2aa"
allPosts = session.query(posts).filter(posts.userId == userId)
# Using for loop
postsFilteredByUser = []
for post in allPosts:
    postsFilteredByUser.append(post.postContent)
print("All posts for user: ", postsFilteredByUser)

# Could also use a list comprehension
# [p.postContent for p in allPosts]

# Liking a post
# We will use postId 'e7a26fd2-bd14-4e53-b591-f74dbb57e7ed'
# as a sample post to like:
# userIdDoingLike1 = "ab1c46e9-83a0-4953-9b2f-d488aa1b1606"
# postId1 = "e7a26fd2-bd14-4e53-b591-f74dbb57e7ed"
# addLike(userIdDoingLike1, postId1)

# More sample data of adding a like:
# userIdDoingLike2 = "07186c6a-cb99-4615-ba61-050256fcde61"
# postId2 = "e7a26fd2-bd14-4e53-b591-f74dbb57e7ed"

# addLike(userIdDoingLike2, postId2)

# Get all users who liked a post:
postId = "e7a26fd2-bd14-4e53-b591-f74dbb57e7ed"
postLikes = session.query(likes).filter(likes.postId == postId).all()
print(len(postLikes))

# all user names who liked a post with a JOIN
usersLikedPost = (
    session.query(users, likes)
    .filter(likes.postId == postId)
    .filter(likes.userId == users.userID)
    .all()
)


for u in usersLikedPost:
    print("***********************************")
    print(u[0].email)
    print(u[0].firstName)
    print(u[0].lastName)
    print(u[0].profileName)
    print("************************************")
    print(" ")
