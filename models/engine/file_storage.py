#!/usr/bin/python3
"""Module for the FileStorage class"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
try:
    from models.place import Place
except ImportError:
    import sys
    Place = sys.moduile[__package__ + '.Place']
from models.review import Review
from models.state import State
from models.city import City


class FileStorage:
    """Class incharge of serialization/deserialization from/to JSON file"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns dictionary of objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the new obj"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        objects = FileStorage.__objects
        serialized_objects = {}
        for obj in objects.keys():
            serialized_objects[obj] = objects[obj].to_dict()

        with open(FileStorage.__file_path, 'w', encoding="utf-8") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r', encoding="utf-8") as file:
                try:
                    loaded_objects = json.load(file)
                    for key, obj_dict in loaded_objects.items():
                        class_name, obj_id = key.split('.')
                        cls = eval(class_name)
                        obj_instance = cls(**obj_dict)
                        FileStorage.__objects[key] = obj_instance
                except Exception:
                    pass
