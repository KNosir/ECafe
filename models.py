from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase
from connection import engine


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    description = Column(String)
    status = Column(String)  # ready, not ready
    price = Column(Float)
    is_deleted = Column(Boolean, default=False)
    author_id = Column(Integer)


class Personal(Base):
    __tablename__ = 'personal'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    salary = Column(Float)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    created_at = Column(DateTime)
    fired_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    author_id = Column(Integer)


class TableManagement(Base):
    __tablename__ = 'table_management'
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    author_id = Column(Integer)


class OrderManagement(Base):
    __tablename__ = 'order_management'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, unique=True)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    amount = Column(Integer)
    price = Column(Integer)
    total = Column(Integer)
    order_status = Column(String, default='not completed')
    table_id = Column(Integer, ForeignKey('table_management.id'))
    personal_id = Column(Integer, ForeignKey('personal.id'), nullable=False)
    created_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    author_id = Column(Integer)


Base.metadata.create_all(bind=engine)
