import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(email, full_name, temporal_token):
    # Construye la URL de restablecimiento de contraseña
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    link = f"{frontend_url}/PasswordChange/{temporal_token}"

    # HTML y texto en formato seguro
    html_content = f"""
    <html>
    <body>
        <p>Hola {full_name},</p>
        <p>Recibimos una solicitud para cambiar tu contraseña.</p>
        <p>Si fuiste tú, usa el siguiente enlace para cambiar tu contraseña:</p>
        <p><a href="{link}">Cambiar Contraseña</a></p>
        <p>O copia y pega este enlace en tu navegador: {link}</p>
        <p>Si no solicitaste este cambio, por favor ignora este mensaje.</p>
        <br>
        <p>Saludos,<br>Equipo de soporte</p>
    </body>
    </html>
    """

    text_content = f"""\
    Hola {full_name},
    Recibimos una solicitud para cambiar tu contraseña.
    Si fuiste tú, puedes cambiar tu contraseña usando el siguiente enlace: {link}
    Si no solicitaste este cambio, por favor ignora este mensaje.
    Saludos,
    Equipo de soporte
    """

    # Configuración del mensaje
    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Cambio de Contraseña'
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = email

    # Adjunta el contenido en texto y HTML
    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    # Envía el correo electrónico
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
            server.sendmail(os.getenv('EMAIL_SENDER'), email, msg.as_string())
        print(f"Correo de recuperación enviado a: {email}")
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación: verifique las credenciales del correo.")
    except smtplib.SMTPConnectError:
        print("Error de conexión: no se pudo conectar al servidor SMTP.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")