from flask_app.config.mysqlconnection import connectToMySQL
import re
# from flask_app.models.recipe import Recipe
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recepies = []

    
    @staticmethod
    def validate(data):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe').query_db(query,data)

        # Validate name
        if len(data['first_name']) < 3:
            flash("Name must be at least 3 characters.","register")
            is_valid = False
        # Validate email
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.", "register")
            is_valid = False
        if len(results) >= 1:
            flash("Email address already exist", "register")
            is_valid = False
        # Validate password
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, email, password) VALUES (%(first_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipe').query_db(query, data)

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('recipe').query_db(query, data)
        return cls(result[0])
