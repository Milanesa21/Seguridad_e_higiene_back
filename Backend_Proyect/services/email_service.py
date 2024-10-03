import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(email, full_name, temporal_token):
    # URL con el token incluido
    link = f"http://127.0.0.1:8000/reset-password/{temporal_token}"

    # Formato HTML para el correo
    html = f"""
    <html>
    <body>
        <p>Hola {full_name},</p>
        <p>Recibimos una solicitud para cambiar tu contraseña.</p>
        <p>Si fuiste tú, puedes cambiar tu contraseña usando el siguiente enlace:</p>
        <a href="{link}">Cambiar Contraseña</a>
        <p>Si no fuiste tú, por favor ignora este mensaje.</p>
        <br>
        <p>Saludos,</p>
        <p>Tu equipo de soporte</p>
    </body>
    </html>
    """

    # Parte de texto plano
    text = f"""\
    Hola {full_name},
    Recibimos una solicitud para cambiar tu contraseña.
    Si fuiste tú, puedes cambiar tu contraseña usando el siguiente enlace: {link}
    Si no fuiste tú, por favor ignora este mensaje.
    Saludos,
    Tu equipo de soporte
    """

    # Configuración del mensaje
    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Cambio de Contraseña'
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = email

    # Agregar las partes de texto
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        # Configuración del servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))

        # Envío del correo
        server.sendmail(os.getenv('EMAIL_SENDER'), email, msg.as_string())
        print(f"Correo enviado a {email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()
