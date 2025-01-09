from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class MusicChat(db.Model): # defiintion for data table 
    __tablename__ = 'musicChats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # parameter 1
    _message = db.Column(db.String(255), nullable=False) #parameter 2
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id')) # pearameter 3

    def __init__(self, message, user_id):
        """
        Constructor, 1st step in object creation.
        
        Args:
            message (str): The message content.
            user_id (int): The user ID of the person who sent the message.
        """
        self._message = message
        self._user_id = user_id

    @property
    def message(self):
        return self._message

    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the music chat data.
        """
        return {
            'id': self.id,
            'message': self._message,
            'user_id': self._user_id,
        }
