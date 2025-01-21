# censor.py
from flask import current_app
from flask_login import UserMixin
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from __init__ import app, db

""" Database Models """


class Censor(db.Model, UserMixin):
    """
    Censor Model

    This class represents the Censor model, which is used to manage actions in the 'censor' table of the database. It is an
    implementation of Object Relational Mapping (ORM) using SQLAlchemy, allowing for easy interaction with the database
    using Python code. The Censor model includes various fields and methods to support user management, authentication,
    and profile management functionalities.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database.
        id (Column): The primary key, an integer representing the unique identifier for the censor.
        _name (Column): A string representing the censor's name. It is not unique and cannot be null.
        _uid (Column): A unique string identifier for the censor, cannot be null.
        _password (Column): A string representing the hashed password of the censor. It is not unique and cannot be null.
        _role (Column): A string representing the censor's role within the application. Defaults to "Censor".
        _pfp (Column): A string representing the path to the censor's profile picture. It can be null.
    """
    __tablename__ = 'censor'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    submission_text = db.Column(db.Text, nullable=True)
    censored_text = db.Column(db.Text, nullable=True)
    submission_date = db.Column(db.Date, nullable=False, default=date.today)
    flagged_words = db.Column(db.String(255), nullable=True)


    def __init__(self, name, uid, submission_text="", censored_text="", flagged_words="", submission_date=None):
        """
        Constructor, 1st step in object creation.
       
        Args:
            name (str): The name of the censor.
            uid (str): The unique identifier for the censor.
            submission_text (str): The text that was submitted for censorship.
            censored_text (str): The censored version of the submission text.
            flagged_words (str): A comma-separated list of flagged words.
            submission_date (str): The date the submission was made.
        """
        self.name = name
        self.uid = uid
        self.submission_text = submission_text
        self.censored_text = censored_text
        self.flagged_words = flagged_words
        if submission_date:
            self.submission_date = submission_date


    def get_id(self):
        """
        Returns the censor's ID as a string.
       
        Returns:
            str: The censor's ID.
        """
        return str(self.id)


    def create(self, inputs=None):
        """
        Adds a new record to the table and commits the transaction.
       
        Args:
            inputs (dict, optional): Additional data to update the censor with.
       
        Returns:
            Censor: The created censor object, or None on error.
        """
        try:
            db.session.add(self)  # add prepares to persist censor object to Censor table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            if inputs:
                self.update(inputs)
            return self
        except IntegrityError:
            db.session.rollback()
            return None


    def read(self):
        """
        Converts the censor object to a dictionary.
       
        Returns:
            dict: A dictionary representation of the censor object.
        """
        data = {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "submission_text": self.submission_text,
            "censored_text": self.censored_text,
            "submission_date": self.submission_date,
            "flagged_words": self.flagged_words
        }
        return data


    def update(self, inputs):
        """
        Updates the censor object with new data.
       
        Args:
            inputs (dict): A dictionary containing the new data for the censor.
       
        Returns:
            Censor: The updated censor object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self


        submission_text = inputs.get("submission_text", "")
        censored_text = inputs.get("censored_text", "")
        flagged_words = inputs.get("flagged_words", "")


        # Update table with new data
        if submission_text:
            self.submission_text = submission_text
        if censored_text:
            self.censored_text = censored_text
        if flagged_words:
            self.flagged_words = flagged_words


        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self

    def delete(self):
        """
        Removes the censor object from the database and commits the transaction.
       
        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return None

def initCensor():

    with app.app_context():

        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
       
        c1 = Censor(
            name='John Doe',
            uid='johndoe123',
            submission_text='This is a test message with inappropriate content.',
            censored_text='This is a test message with ******** content.',
            submission_date=datetime.strptime('2025-01-17', '%Y-%m-%d').date(),  # Convert string to date object
            flagged_words='inappropriate'
        )
        c2 = Censor(
            name='Jane Smith',
            uid='janesmith456',
            submission_text='Hello! This is an example of another submission.',
            censored_text='Hello! This is an example of another submission.',
            submission_date=datetime.strptime('2025-01-17', '%Y-%m-%d').date(),  # Convert string to date object
            flagged_words=''
        )
        c3 = Censor(
            name='Alice Brown',
            uid='alicebrown789',
            submission_text='Some inappropriate language here!',
            censored_text='Some ******** language here!',
            submission_date=datetime.strptime('2025-01-17', '%Y-%m-%d').date(),  # Convert string to date object
            flagged_words='inappropriate'
        )
        c4 = Censor(
            name='Bob White',
            uid='bobwhite101',
            submission_text='This is a clean message with no issues.',
            censored_text='This is a clean message with no issues.',
            submission_date=datetime.strptime('2025-01-17', '%Y-%m-%d').date(),  # Convert string to date object
            flagged_words=''
        )

        censors = [c1, c2, c3, c4]
       
        for censor in censors:
            try:
                censor.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
