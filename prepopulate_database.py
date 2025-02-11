from database import db
from database import app
ctx = app.app_context()
ctx.push()
db.create_all()
from database import Creatures, Humans, Animals, Quotes

creature1 = Creatures(
    name="Bob",
    age=33,
    type="green alien",
    special_force="dancing",
)
human1 = Humans(
    name="Kevin",
    age=54,
    relation="neighbour",
    hobby="collecting stamps",
)
animal1 = Animals(
    name="galactiCat",
    age=3,
    species="cat",
    environment="floating in a far away galaxy",
)
quote1 = Quotes(
    quote="The rhythm of the universe is inside you, dance like gravity can't hold you down!",
    mood=5,
    creatures=creature1,
)


db.session.add(creature1)
db.session.add(human1)
db.session.add(animal1)
db.session.add(quote1)
db.session.commit()

print(vars(Creatures.query.first()))
bob_quotes = list(Creatures.query.first().quotes)
print([{"id": q.id, "quote": q.quote} for q in bob_quotes])
print(vars(Quotes.query.first()))


