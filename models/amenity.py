#!/usr/bin/python3
"""modukes that holds class Amenity"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ amenity class"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       back_populates='amenities')
