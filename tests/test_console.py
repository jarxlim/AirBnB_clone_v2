#!/usr/bin/python3
"""
module testing for console.py
"""

import sys
import unittest
from unittest.mock import patch
from io import StringIO
import console
from console import HBNBCommand
from models import storage

class TestConsole(unittest.TestCase):
    """ unittest for console """
    @classmethod
    def setUpClass(cls):
        """set up class for the test"""
        cls.console = HBNBCommand()

    @classmethod
    def teardown(cls):
        """tears down the class at the end of the test"""
        del cls.console

    def test_empty(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """Test quit command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            with self.assertRaises(SystemExit):
                self.console.onecmd("quit")
            self.assertEqual('', f.getvalue())

     def test_module_class_methods_docstrings(self):
        """Test that module, class and methods have docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)

    def test_HBNBCommand_create_new_instances_with_pars(self):
        """Test creation of new instances with parameters"""
        clases = ['BaseModel', 'User', 'Place', 'City',
                  'State', 'Review', 'Amenity']

        for m in clases:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('''create {}
                    city_id="0001" user_id="0001" name="My_little_house"
                    number_rooms=4 number_bathrooms=2 max_guest=10
                    price_by_night=300 latitude=37.773972 longitude=-122.431297
                                     '''.format(m))

                new_key = m + "." + f.getvalue().strip()
                self.assertIn(new_key, storage.all().keys())

    def test_show(self):
        """Test cmdline output: show"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show City abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_create_error_messages(self):
        """Test that the create comand prints the correct error messages"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create')
            self.assertEqual("** class name missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_create_new_instances(self):
        """Test the creation of new instances of different classes"""

        clases = ['BaseModel', 'User', 'Place', 'City',
                  'State', 'Review', 'Amenity']
        for m in clases:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('create {}'.format(m))
                new_key = m + "." + f.getvalue().strip()
                self.assertIn(new_key, storage.all().keys())

    def test_all_error_messages(self):
        """Test that the all comand prints the correct error messages"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_all_existing_instances(self):
        """Test the creation of new instances of different classes"""

        objs = storage.all()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all')
            for key, value in objs.items():
                inst_key = key.split(".")[1]
                self.assertIn(inst_key, f.getvalue().strip())

    def test_update(self):
        """Test cmd output: update"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_destroy(self):
        """Test cmd output: destroy"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    if __name__ == "__main__":
        unittest.main()
