# from sqlalchemy import Column, Integer, String
# from database import Base

# class Category(Base):
#     __tablename__ = "Categories"
#     category_id = Column("CategoryID", Integer, primary_key=True, index=True)
#     category_name = Column("CategoryName", String, nullable=False)
#     description = Column("Description", String, nullable=True)
from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, Date, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, String, Unicode
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Categories(Base):
    __tablename__ = 'Categories'
    __table_args__ = (
        PrimaryKeyConstraint('CategoryID', name='PK__Categori__19093A2BFB989CE2'),
    )

    CategoryID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    CategoryName: Mapped[str] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Description: Mapped[Optional[str]] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Products: Mapped[list['Products']] = relationship('Products', back_populates='Categories_')


class Orders(Base):
    __tablename__ = 'Orders'
    __table_args__ = (
        PrimaryKeyConstraint('OrderID', name='PK__Orders__C3905BAFD6E8DEB1'),
    )

    OrderID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    CustomerName: Mapped[str] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    OrderDate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    TotalAmount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    OrderDetails: Mapped[list['OrderDetails']] = relationship('OrderDetails', back_populates='Orders_')


class EFMigrationsHistory(Base):
    __tablename__ = '__EFMigrationsHistory'
    __table_args__ = (
        PrimaryKeyConstraint('MigrationId', name='PK___EFMigrationsHistory'),
    )

    MigrationId: Mapped[str] = mapped_column(Unicode(150, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    ProductVersion: Mapped[str] = mapped_column(Unicode(32, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class Products(Base):
    __tablename__ = 'Products'
    __table_args__ = (
        ForeignKeyConstraint(['CategoryID'], ['Categories.CategoryID'], name='FK__Products__Catego__3B75D760'),
        PrimaryKeyConstraint('ProductID', name='PK__Products__B40CC6EDF4042A6C')
    )

    ProductID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    ProductName: Mapped[str] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    StockQuantity: Mapped[int] = mapped_column(Integer, nullable=False)
    CategoryID: Mapped[Optional[int]] = mapped_column(Integer)

    Categories_: Mapped[Optional['Categories']] = relationship('Categories', back_populates='Products')
    OrderDetails: Mapped[list['OrderDetails']] = relationship('OrderDetails', back_populates='Products_')


class OrderDetails(Base):
    __tablename__ = 'OrderDetails'
    __table_args__ = (
        ForeignKeyConstraint(['OrderID'], ['Orders.OrderID'], ondelete='CASCADE', name='FK__OrderDeta__Order__403A8C7D'),
        ForeignKeyConstraint(['ProductID'], ['Products.ProductID'], name='FK__OrderDeta__Produ__412EB0B6'),
        PrimaryKeyConstraint('OrderDetailID', name='PK__OrderDet__D3B9D30C5747DC46')
    )

    OrderDetailID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    UnitPrice: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    OrderID: Mapped[Optional[int]] = mapped_column(Integer)
    ProductID: Mapped[Optional[int]] = mapped_column(Integer)

    Orders_: Mapped[Optional['Orders']] = relationship('Orders', back_populates='OrderDetails')
    Products_: Mapped[Optional['Products']] = relationship('Products', back_populates='OrderDetails')
