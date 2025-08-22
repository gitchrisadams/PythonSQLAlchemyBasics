# How to use sqlAlchemy with pure SQL:
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///mydatabase.db", echo=True)

conn = engine.connect()

conn.execute(text("create table if not exists people (name str, age int)"))

conn.commit()

# How to use sqlAlchemy with ORM but still use Pure SQL:
from sqlalchemy.orm import Session

session = Session(engine)

session.execute(text('insert into people (name, age) values("Mike", 30);'))

session.commit()
