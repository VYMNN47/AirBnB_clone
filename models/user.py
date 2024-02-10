#!/usr/bin/python3
"""Module for user class"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    User class inheriting from BaseModel

    Attributes:
        email: The email address of the user.
        password: The password of the user.
        first_name: The first name of the user.
        last_name: The last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
