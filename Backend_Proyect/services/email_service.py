import smtplib
from email.mime.text import MIMEText


def send_email(email,full_name):
    link = '/changePassword/{full_name}'
    body = f'Hola,\n\n Se quiere cambiar de contraseña, si no fuiste tu, por favor ignora este mensaje.\n\n Link para cambiar contraseña: {link}'

    msg = MIMEText(body)
    msg['Subject'] = 'Cambio de contraseña'
    msg['From'] = ''
    msg['To'] = email
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('', '')

        server.sendmail('', email, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()


