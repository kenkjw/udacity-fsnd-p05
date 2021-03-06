from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import datetime

Base = declarative_base()
_engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = _engine
_db_session = sessionmaker(bind=_engine)
_session = _db_session()


class User(Base):
    """
    Model class representing a user of the catalog.

    Attributes:
        name:   string representing the user's name
        email:  string representing the user's email
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    items = relationship('Item', back_populates='user',
                         cascade='all, delete, delete-orphan')

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
        try:
            user = _session.query(User).filter_by(id=user_id).one()
            return user
        except NoResultFound:
            return None

    @classmethod
    def by_email(cls, email):
        try:
            user = _session.query(User).filter_by(email=email).one()
            return user
        except NoResultFound:
            return None

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Item(Base):
    """
    Model class representing an item in the catalog.

    Attributes:
        name:  string representing the item's name
        email:  string representing the item's category
        description:  text representing the item's description
        user_id:  id of the user model that created the item
        created_date:  date the item was created
        modified_date:  date the item was last modified

    """
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    modified_date = Column(DateTime, onupdate=datetime.datetime.now)

    @classmethod
    def by_id(cls, item_id):
        try:
            item = _session.query(Item).filter_by(id=item_id).one()
            return item
        except NoResultFound:
            return None

    @classmethod
    def by_name(cls, category, name):
        try:
            item = (_session.query(Item)
                    .filter_by(category=category, name=name)
                    .one())
            return item
        except NoResultFound:
            return None

    @classmethod
    def by_category(cls, category):
        try:
            items = (_session.query(Item)
                     .filter_by(category=category)
                     .order_by(Item.name)
                     .all())
            return items
        except NoResultFound:
            return None

    @classmethod
    def by_user_id(cls, user_id):
        try:
            items = (_session.query(Item)
                     .filter_by(user_id=user_id)
                     .order_by(Item.name)
                     .all())
            return items
        except NoResultFound:
            return None

    @classmethod
    def get_categories(cls):
        try:
            items = (_session.query(Item)
                     .group_by(Item.category)
                     .order_by(Item.category)
                     .all())
            return [item.category for item in items]
        except NoResultFound:
            return None

    @classmethod
    def get_latest(cls, limit=10):
        try:
            items = (_session.query(Item)
                     .order_by(Item.modified_date.desc())
                     .limit(limit)
                     .all())
            return items
        except NoResultFound:
            return None

    @classmethod
    def create_item(cls, name, description, category, user_id):
        new_item = Item(name=name, description=description,
                        category=category.lower(), user_id=user_id)
        _session.add(new_item)
        _session.commit()

        return new_item

    def is_owned_by(self, user_id):
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


Base.metadata.create_all(_engine)
