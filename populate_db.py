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

Item.create_item("Stick","Lorem ipsum dolor sit amet, consectetur adipiscing elit.","Hockey",u1.id)
Item.create_item("Goggles","Mauris et ante feugiat, laoreet felis id, convallis nunc.","Snowboarding",u2.id)
Item.create_item("Snowboard","Mauris venenatis turpis non justo scelerisque maximus.","Snowboarding",u3.id)
Item.create_item("Two shinguards","Mauris placerat ipsum eget ligula facilisis posuere.","Soccer",u1.id)
Item.create_item("Shinguards","Curabitur cursus mauris vitae tortor varius porta.","Soccer",u2.id)
Item.create_item("Frizbee","Phasellus suscipit metus ac purus pretium feugiat.","Frisbee",u3.id)
Item.create_item("Bat","Aenean pulvinar nibh non arcu interdum rhoncus.","Baseball",u1.id)
Item.create_item("Glove","Nunc ullamcorper mi euismod viverra consectetur.","Baseball",u2.id)
Item.create_item("Jersey","Proin quis turpis nec lacus molestie vestibulum.","Soccer",u3.id)
Item.create_item("Skate","Nullam sit amet ipsum eu est facilisis euismod.","Skating",u2.id)

