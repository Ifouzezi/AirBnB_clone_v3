#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    _FileStorage__file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    _FileStorage__objects = {}

    def all(self, cls=None):
        """returns the dictionary _FileStorage__objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self._FileStorage__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self._FileStorage__objects

    def get(self, cls, id):
        """retrieves an object of a class with id"""
        if cls is not None:
            res = list(
                filter(
                    lambda x: type(x) is cls and x.id == id,
                    self._FileStorage__objects.values()
                )
            )
            if res:
                return res[0]
        return None

    def count(self, cls=None):
        """retrieves the number of objects of a class or all (if cls==None)"""
        return len(self.all(cls))

    def new(self, obj):
        """sets in _FileStorage__objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self._FileStorage__objects[key] = obj

    def save(self):
        """serializes _FileStorage__objects to the JSON file (path: _FileStorage__file_path)"""
        json_objects = {}
        for key in self._FileStorage__objects:
            json_objects[key] = self._FileStorage__objects[key].to_dict()
        with open(self._FileStorage__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to _FileStorage__objects"""
        try:
            with open(self._FileStorage__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self._FileStorage__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from _FileStorage__objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self._FileStorage__objects:
                del self._FileStorage__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
