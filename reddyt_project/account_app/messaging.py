from django.core.mail import send_mail


def email_message(message_dict):
    alt_body = f"To reset your password, click the following link: {message_dict['reset_url']}"
    body = ("<html>"
            "<head></head>"
            "<body>"
            f"<h4>To reset your password, click <a href='{message_dict['reset_url']} '>this link</a></h4>"
            "</body>"
            "</html>"
            )

    send_mail('Password reset', alt_body, settings.EMAIL_HOST_USER,
              [message_dict['email'], ], html_message=body)
