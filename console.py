#!/usr/bin/env python3
"""
Module: console.py

Description:
    This module implements a command-line interface (CLI) for interacting
    with the AirBnB clone project. It provides various commands to create,
    manipulate, and manage instances of different classes such as BaseModel,
    User, State, City, Amenity, Place, and Review.

Usage:
    This Module can be run as a script using:
    $ ./console.py

    Type 'help' to display a list of available commands and their usage.
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


class HBNBCommand(cmd.Cmd):
    """Console Class that deals with all the console command control"""
    prompt = '(hbnb) '
    classes = ["BaseModel", "User", "State", "City",
                            "Amenity", "Place", "Review"]

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """exits the program if End-Of-Line"""
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, line):
        """
        Creates instance of specified class, saves it, and prints the id
        Usage: creatre <class_name>
        """

        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            cls = args[0]
            new_inst = eval(cls)()
            new_inst.save()
            print(new_inst.id)

    def do_show(self, line):
        """
        Prints string representation of instance
        Usage: show <class_name> <class_id>
        """

        args = line.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:

            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])

            if key not in objects:
                print("** no instance found **")
            else:
                print(objects[key])

    def do_destroy(self, line):
        """
        Deletes an instance based on class name and id
        Usage: destroy <class_name>
        """

        args = line.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:

            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])

            if key not in objects:
                print("** no instance found **")
            else:
                del objects[key]
                storage.save()

    def do_all(self, line):
        """
        Prints string representation of all or specific instances
        Usage: all [class_name]
        """

        objects = storage.all()

        args = line.split()

        object_list = []

        if len(args) == 0:
            for key, obj in objects.items():
                object_list.append(str(obj))

            print(object_list)

        elif args[0] not in self.classes:
            print("** class doesn't exist **")

        else:
            for key, obj in objects.items():
                if key.split('.')[0] == args[0]:
                    object_list.append(str(obj))

            print(object_list)

    def do_update(self, line):
        """
        Updates instance based on the class name and id and saves it
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """

        args = line.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])

            if key in objects:
                obj = objects[key]
                setattr(obj, args[2], args[3])
                obj.save()
            else:
                print("** no instance found **")

    def do_count(self, line):
        """prints the number of isntances of a class"""

        args = line.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            count = 0

            objects = storage.all()

            for key in objects.keys():
                if key.split('.')[0] == args[0]:
                    count += 1

            print(count)

    def default(self, line):
        """Handle unrecognized commands"""

        if '.' not in line:
            return super().default(line)

        method_dict = {
                'show': self.do_show,
                'all': self.do_all,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
        }

        args = line.split('.')

        class_name = args[0]
        cmd = args[1].split('(')

        method = cmd[0]
        method_args = cmd[1].split(')')[0]

        if method in method_dict.keys():
            return method_dict[method]("{} {}".format(class_name, method_args.strip('\"')))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
