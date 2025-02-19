#!/usr/bin/python3
""" unittest module for amenities.py """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import os


class test_Amenity(test_basemodel):
    """ test class for amenity """

    def __init__(self, *args, **kwargs):
        """ initiates the test class """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ name testing """
        new = self.value()
        self.assertEqual(type(new.name), str) if
                        os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                        type(None))
