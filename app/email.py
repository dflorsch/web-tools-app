from flask_mail import Message

from app import mail


def send_credentials_email(user, user_pw):
    msg = Message('Your credentials for MyApp', sender='', recipients=[user.e_mail])
    msg.body = f"Hello {user.username},\n\n" \
               f"Your username is {user.username} and your temporary password is {user_pw}.\n" \
               f"Please log in to MyApp and change your password.\n\n" \
               f"Thanks,\n" \
               f"The MyApp Team"

    mail.send(msg)
