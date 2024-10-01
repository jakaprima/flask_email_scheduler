from .extensions import db
from .orm import PkModelWithManageAttr

class Email(PkModelWithManageAttr):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    email_subject = db.Column(db.String(255), nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f'<Email {self.id} {self.event_id}>'

# register your table here
register_tables = {
    "Email": Email,
}