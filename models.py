from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy import asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()
_engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(_engine)
Base.metadata.bind = _engine
_db_session = sessionmaker(bind=_engine)
_session = _db_session()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    items = relationship("Item", back_populates='user',
                         cascade="all, delete, delete-orphan")

    @classmethod
    def create_user(cls, session):
        new_user = User(name=session['name'], email=session['email'])
        try:
            user = _session.query(User).filter_by(email=session['email']).one()
            return user
        except NoResultFound:
            _session.add(new_user)
            _session.commit()
            return new_user


    @classmethod
    def by_id(cls, user_id):
        user = _session.query(User).filter_by(id=user_id).one()
        return user

    @classmethod
    def by_email(cls, email):
        user = _session.query(User).filter_by(email=email).one()
        return user

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)
    description = Column(Text, nullable=False) 
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="items")

    @classmethod
    def by_id(cls, item_id):
        item = _session.query(Item).filter_by(id=item_id).one()
        return item

    @classmethod
    def by_name(cls, name):
        item = _session.query(Item).filter_by(name=name).one()
        return item

    @classmethod
    def by_category(cls, category):
        items = (_session.query(Item)
                    .filter_by(category=category)
                    .order_by(Item.name)
                    .all())
        return items

    @classmethod
    def by_user_id(cls, user_id):
        items = (_session.query(Item)
                    .filter_by(user_id=user_id)
                    .order_by(Item.name)
                    .all())
        return items

    @classmethod
    def get_categories(cls):
        categories = (_session.query(Item)
                        .group_by(Item.category)
                        .order_by(Item.category)
                        .all())
        return [category for category in categories]

    @classmethod
    def create_item(cls, name, description, category, user_id):
        new_item = Item(name=name, description=description,
                        category=category, user_id=user_id)
        _session.add(new_item)
        _session.commit()

        return new_item

    def is_owner(self, user_id):
        return self.user_id == user_id

    def delete(self):
        _session.delete(self)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'user_id': self.user_id
        }



