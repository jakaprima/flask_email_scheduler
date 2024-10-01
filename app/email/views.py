import pytz
from flask import request, jsonify, Blueprint, current_app as app, render_template
from .schema import MailSchema
from datetime import datetime
from ..models import Email
from ..responses import wrap_error_message_schema, init_response, process_response
import traceback
from ..tasks import send_mail_task

bp_email = Blueprint('email', __name__, template_folder='templates/email')
sg_timezone = pytz.timezone('Asia/Singapore')

@bp_email.route('/')
def index():
    emails = Email.query.all()
    return render_template('index.html', emails=emails)

@bp_email.route('/send-mail')
def send_mail():
    emails = Email.query.all()
    return render_template('send_mail.html', emails=emails)

@bp_email.route('/api/save_emails', methods=['POST'])
def save_emails():
    response, status_code = init_response(message_code='GENERAL_ERROR_REQUEST')

    try:
        data = request.get_json()
        validated_data = MailSchema().load(data)

        try:
            naive_timestamp = validated_data['timestamp']

            if naive_timestamp.tzinfo is not None:
                naive_timestamp = naive_timestamp.astimezone(pytz.utc).replace(tzinfo=None)
                aware_timestamp = sg_timezone.localize(naive_timestamp)
            else:
                aware_timestamp = sg_timezone.localize(naive_timestamp)

        except (ValueError, OverflowError) as e:
            return jsonify({'error': 'Invalid timestamp format.'}), 400

        validated_data['timestamp'] = aware_timestamp

        emailInstance = Email(**validated_data).save()
        sg_timestamp = emailInstance.timestamp.astimezone(sg_timezone)

        # # Calculate the countdown in seconds
        sg_now = datetime.now(sg_timezone)  # Get current time in UTC as an aware datetime

        countdown = (sg_timestamp - sg_now).total_seconds()
        if app.config.get('ENV') is not 'test':
            send_mail_task.apply_async(args=[emailInstance.id], countdown=countdown)

        return jsonify({'message': 'Email saved and scheduled for sending.'}), 201
    except Exception as e:
        class_exc = type(e).__name__
        if class_exc == 'ValidationError':
            array_resp = wrap_error_message_schema(dict(e.messages))
            response, status_code = process_response(response, action='error',
                                                                    message_code='INVALID_REQUEST_PARAMETER')

            for data in array_resp:
                if data['key'] == 'validate_object':
                    response.put('desc', data['description'])
            response.put("data", array_resp)
        else:
            app.logger.error("-----------------------------------Exception")
            app.logger.error(e)
            app.logger.error(traceback.format_exc())
            app.logger.error("-----------------------------------")
            response, status_code = process_response(response, action='error',
                                                                    message_code='GENERAL_ERROR_REQUEST')
            response.put("data", {'message': str(e)})
        return jsonify(response.stringify_v1()), status_code

