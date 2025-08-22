from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    func,
)

# ------------------ Setup and engine creation ------------------ #
engine = create_engine("sqlite:///mydatabase.db", echo=True)
meta = MetaData()

# ------------------ Create people table ------------------ #
people = Table(
    "people",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer),
)

# ------------------ Create things table w/ Foreign Key ------------------ #
# people can have many things (Many to Many relationship)
things = Table(
    "things",
    meta,
    Column("id", Integer, primary_key=True),
    Column("description", String, nullable=False),
    Column("value", Float),
    Column("owner", Integer, ForeignKey("people.id")),
)


# ------------------ Creates the dB ------------------ #
meta.create_all(engine)

conn = engine.connect()

# ------------------ Inserting Data ------------------ #
# insert_statement = people.insert().values(name="Chris", age=48)
# result = conn.execute(insert_statement)
# conn.commit()

# ------------------ Updating Data ------------------ #
# update_statement = people.update().where(people.c.name == "Mike").values(age=50)
# result = conn.execute(update_statement)
# conn.commit()

# ------------------ Deleting Data ------------------ #
# delete_statement = people.delete().where(people.c.name == "Mike")
# result = conn.execute(delete_statement)
# conn.commit()

# ------------------ Inserting Sample data ------------------ #
# ------------------ Inserting people data ------------------ #
# insert_statement = people.insert().values(
#     [
#         {"name": "Mike", "age": 30},
#         {"name": "Bob", "age": 35},
#         {"name": "Anna", "age": 38},
#         {"name": "John", "age": 50},
#         {"name": "Clara", "age": 42},
#     ]
# )

# result = conn.execute(insert_statement)
# conn.commit()

# ------------------ Inserting things data ------------------ #
# insert_things_statement = things.insert().values(
#     [
#         {"owner": 2, "description": "laptop", "value": 800.50},
#         {"owner": 2, "description": "Mouse", "value": 50.50},
#         {"owner": 2, "description": "Keyboard", "value": 100.50},
#         {"owner": 3, "description": "Book", "value": 30},
#         {"owner": 4, "description": "Bottle", "value": 10.50},
#         {"owner": 5, "description": "Speakers", "value": 80.50},
#     ]
# )


# result = conn.execute(insert_things_statement)
# conn.commit()

# ------------------ Joining Data ------------------ #
# join on the primary and foreign key .id and .owner
# regular join
join_statement = people.join(things, people.c.id == things.c.owner)

# left outer join (Includes even people who do not own anything)
# join_statement = people.outerjoin(things, people.c.id == things.c.owner)

select_join_statement = (
    people.select()
    .with_only_columns(people.c.name, things.c.description)  # The columns to show
    .select_from(join_statement)  # Using join_statement above
)
result_join = conn.execute(select_join_statement)

for row in result_join.fetchall():
    print(row)


# ------------------ Aggregating/Grouping Data ------------------ #
# Sum up value of things for each owner
# things.c.owner is how to get "by owner", and things.c.value is what is summed
group_by_statement = (
    things.select()
    .with_only_columns(things.c.owner, func.sum(things.c.value))
    .group_by(things.c.owner)
)

# Same as above but only if over 50
# group_by_statement = (
#     things.select()
#     .with_only_columns(things.c.owner, func.sum(things.c.value))
#     .group_by(things.c.owner)
#     .having(func.sum(things.c.value) > 50)
# )

result_group_by = conn.execute(group_by_statement)

print("********************** Aggregate Group by *****************")
for row in result_group_by.fetchall():
    print(row)

# ------------------ Selecting Data ------------------ #
# ------------------ Selecting people data ------------------ #
# select_statement = people.select().where(people.c.age > 20)
select_statement = people.select()
result = conn.execute(select_statement)

for row in result.fetchall():
    print(row)

# ------------------ Selecting things data ------------------ #
select_statement_things = things.select()
result_things = conn.execute(select_statement_things)

for row in result_things.fetchall():
    print(row)
