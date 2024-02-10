#!/usr/bin/python3
"""Module for the base_model"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """class that defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """constructor"""

        if kwargs:
            self.__update(**kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        models.storage.new(self)

    def __update(self, **kwargs):
        """
        Updates updated_at attr
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        for key, value in kwargs.items():
            if key == "__class__":
                continue
            elif key == "created_at" or key == "updated_at":
                setattr(self, key, datetime.strptime(value, time_format))
            else:
                setattr(self, key, value)

    def save(self):
        """
        updates the public instance attribute updated_at with current datetime
        """

        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__ of instance
        """
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()

        return instance_dict

    def __str__(self):
        """
        String Representation of instance
        format: [<class name>] (<self.id>) <self.__dict__>
        """

        class_name = self.__class__.__name__

        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
