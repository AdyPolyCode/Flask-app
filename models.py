from app import db, myApp, login_manager
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), index=True, unique=True, nullable=False)

    email = db.Column(db.String(64), index=True, unique=True, nullable=False)

    hashed_password = db.Column(db.String(32), index=True, nullable=False)

    profile_picture = db.Column(db.String(20), nullable=False)

    gender = db.Column(db.String(10), nullable=False)

    joined_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_post = db.relationship('Post', backref='user', cascade='all, delete, delete-orphan', lazy=True)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def hash_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def get_reset_token(self, expire=1800):
        s = Serializer(myApp.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(myApp.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return 'User {}\nusername:_{}\nemail:_{}'.format(self.id, self.username, self.email)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(80), index=True, nullable=False)

    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    text = db.Column(db.Text, index=True, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)

    def __repr__(self):
        return 'Post {}\n{}\n{}'.format(self.id, self.title, self.date_posted)
