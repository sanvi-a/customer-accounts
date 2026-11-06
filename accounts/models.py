"""Account data model."""
from accounts import db


class DataValidationError(Exception):
    """Raised when incoming data is missing or invalid."""


class Account(db.Model):
    """Customer account."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        """Convert the account to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
        }

    def deserialize(self, data):
        """Populate the account from a dictionary."""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError(f"Invalid account: missing {error.args[0]}") from error
        except (AttributeError, TypeError) as error:
            raise DataValidationError("Invalid account: bad request data") from error
        return self

    def create(self):
        """Persist a new account."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Persist changes to an existing account."""
        db.session.commit()

    def delete(self):
        """Remove the account."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """Return all accounts."""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Return an account by id, or None."""
        return db.session.get(cls, account_id)
