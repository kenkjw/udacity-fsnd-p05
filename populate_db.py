""" Empty the databases and then repopulate with dummy data """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from models import User
from models import Item

_engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = _engine
_db_session = sessionmaker(bind=_engine)
_session = _db_session()

_session.query(User).delete()
_session.query(Item).delete()

_session.commit()

u1 = User.create_user({'name':'Adam','email':'adam@fake.com'})
u2 = User.create_user({'name':'Bob','email':'bob@fake.com'})
u3 = User.create_user({'name':'Carl','email':'carl@fake.com'})

Item.create_item("Stick","A stick","Hockey",u1.id)
Item.create_item("Goggles","Pair of goggles","Snowboarding",u2.id)
Item.create_item("Snowboard","A snowboard","Snowboarding",u3.id)
Item.create_item("Two shinguards","2 shinguards","Soccer",u1.id)
Item.create_item("Shinguards","shinguards","Soccer",u2.id)
Item.create_item("Frizbee","A disc","Frisbee",u3.id)
Item.create_item("Bat","wooden","Baseball",u1.id)
Item.create_item("Glove","mitt","Baseball",u2.id)
Item.create_item("Jersey","Large","Soccer",u3.id)
Item.create_item("Soccer Cleats","Small","Soccer",u1.id)
Item.create_item("Skate","Skates","Skating",u2.id)

