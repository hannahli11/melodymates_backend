from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class MusicChat(db.Model):
    """
    MusicChat Model

    Represents a music chat message.
    
    Attributes:
        id (db.Column): The primary key, an integer.
        _message (db.Column): A string representing the message content.
        _user_id (db.Column): A foreign key referencing the user ID.
    """
    __tablename__ = 'musicChats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _message = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, message, user_id):
        """
        Constructor to initialize a MusicChat object.
        
        Args:
            message (str): The message content.
            user_id (int): The user ID of the sender.
        """
        self._message = message
        self._user_id = user_id

    def __repr__(self):
        """
        String representation of the object.
        
        Returns:
            str: The string representation of the object.
        """
        return f"MusicChat(id={self.id}, message='{self._message}', user_id={self._user_id})"

    def create(self):
        """
        Adds the object to the database and commits the transaction.
        
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
        Retrieves the object data and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the music chat data.
        """
        return {
            'id': self.id,
            'message': self._message,
            'user_id': self._user_id,
        }
        
    @staticmethod
    def restore(data):
        """
        Synchronizes the provided data with the musicChat database.
        Updates existing records or creates new ones.
        """
        restored_records = []
        for music_chat in data:
            id = music_chat.get("id")  # Fetch the id from the provided data
            record = musicChat.query.filter_by(id=id).first()

            if record:
                # Update the existing record
                record.update(music_chat)
                restored_records.append(record.read())
            else:
                # Create a new record if it doesn't exist
                try:
                    new_record = musicChat(
                        name=music_chat.get("name"),
                        uid=music_chat.get("uid"),
                        favorites=music_chat.get("favorites", [])
                    )
                    new_record.create()
                    restored_records.append(new_record.read())
                except IntegrityError as e:
                    db.session.rollback()  # Rollback the session in case of any error
                    print(f"Error restoring record with uid {art_data.get('uid')}: {e}")
        return restored_records


def initMusicChats():
    """
    The initMusicChats function creates the MusicChat table and adds tester data to the table.

    Uses:
        The db ORM methods to create the table.

    Instantiates:
        MusicChat objects with tester data.

    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        mc1 = MusicChat(message="This song is amazing!", user_id=1)
        mc2 = MusicChat(message="Anyone got suggestions for new tracks?", user_id=2)
        mc3 = MusicChat(message="Loving this playlist!", user_id=3)
        mc4 = MusicChat(message="Does anyone know the lyrics to this song?", user_id=4)
        mc5 = MusicChat(message="Check out the latest release from my favorite artist!", user_id=5)
        messages = [mc1, mc2, mc3, mc4, mc5]

        for message in messages:
            try:
                message.create()
            except IntegrityError:
                """Fails with bad or duplicate data"""
                db.session.remove()

