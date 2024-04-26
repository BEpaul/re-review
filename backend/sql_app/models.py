from sqlalchemy import Column, TEXT, INT, BIGINT, VARCHAR, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Review_info(Base):
    __tablename__ = "review_info"

    id = Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    product_name = Column(VARCHAR(100), nullable=False)
    image_url = Column(TEXT, nullable=False)
    product_url = Column(TEXT, nullable=False)
    rate = Column(Float, nullable=False)
    keyword = Column(VARCHAR(30))

class Test(Base):
    __tablename__ = "test"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(TEXT, nullable=False)
    number = Column(INT, nullable=False)