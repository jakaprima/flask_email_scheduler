from ..extensions import ma
from ..models import Email
from marshmallow import fields, ValidationError
from datetime import datetime

class CustomDateTime(fields.DateTime):
    def _deserialize(self, value, attr, obj, **kwargs):
        try:
            return datetime.strptime(value, "%d %b %Y %H:%M")
        except ValueError:
            raise ValidationError("Not a valid datetime.")

class MailSchema(ma.Schema):
    event_id = fields.Int(required=True)
    email_subject = fields.Str(required=True)
    email_content = fields.Str(required=True)
    timestamp = CustomDateTime(required=True)