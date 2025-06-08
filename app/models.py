from app import db, jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import rq


@jwt.user_lookup_loader
def user_loader_callback(jwt_header: dict, jwt_data: dict) -> object:
    """
    HUser loader function which uses the JWT identity to retrieve a user object.
    Method is called on protected routes

    Parameters
    ----------
    jwt_header : dictionary
        header data of the JWT
    jwt_data : dictionary
        payload data of the JWT

    Returns
    -------
    object
        Returns a users object containing the user information
    """
    return Users.query.filter_by(id=jwt_data["sub"]).first()

class Members(db.Model):
    """
    Members table to store the information of members in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_url = db.Column(db.String(2048), nullable=True)
    followers = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    active = db.Column(db.Boolean, default=True)
    
    def delete(self):
        """
        Helper function to delete a member from the database
        """
        self.active = False
        db.session.commit()
    
# defines the Users database table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def set_password(self, password: str):
        """
        Helper function to generate the password hash of a user

        Parameters
        ----------
        password : str
            The password provided by the user when registering
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Helper function to verify the password hash agains the password provided
        by the user when logging in

        Parameters
        ----------
        password : str
            The password provided by the user when logging in

        Returns
        -------
        bool
            Returns True if the password is a match. If not False is returned
        """
        return check_password_hash(self.password_hash, password)

    

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(2048))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    active = db.Column(db.Boolean, default=True)
    
    def delete(self):
        """
        Helper function to delete a comment from the database
        """
        self.active = False
        db.session.commit()
    

class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    date_revoked = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def add(self):
        """
        Helper function to add a JWT to the table
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti: str) -> bool:
        """
        Helper function to check if a JWT is in the Revoked Token table

        Parameters
        ----------
        jti : str
            The JWT unique identifier

        Returns
        -------
        bool
            Return True if the JWT is in the Revoked Token table
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

