from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class MusicChat(db.Model):
    __tablename__ = 'musicChats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _message = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, message, user_id):
        self._message = message
        self._user_id = user_id

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            'id': self.id,
            'message': self._message,
            'user_id': self._user_id
        }


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
