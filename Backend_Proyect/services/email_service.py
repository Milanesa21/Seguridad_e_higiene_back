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
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
        <h2 style="color: #4CAF50;">Hola {full_name},</h2>
        <p>Recibimos una solicitud para cambiar tu contraseña.</p>
        <p>Si fuiste tú, usa el siguiente enlace para cambiar tu contraseña:</p>
        <p><a href="{link}" style="color: #4CAF50; text-decoration: none; font-weight: bold;">Cambiar Contraseña</a></p>
        <p>O copia y pega este enlace en tu navegador:</p>
        <p style="background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd;">{link}</p>
        <p>Si no solicitaste este cambio, por favor ignora este mensaje.</p>
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

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Cambio de Contraseña'
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = email

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

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


def send_create_company(data):
    nombre_empresa = data['nombre_empresa']
    nombre_dueno = data['nombre_dueno']
    email = data['email']
    telefono = data['telefono']

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
        <h2 style="color: #4CAF50;">Nueva Empresa Registrada</h2>
        <p style="margin-bottom: 20px; font-size: 16px;">
            La empresa <strong>{nombre_empresa}</strong> ha mostrado interés en unirse a Centinela.
        </p>
        <p style="font-size: 14px; margin-bottom: 10px;"><strong>Detalles de la Empresa:</strong></p>
        <p><strong>Nombre:</strong> {nombre_empresa}</p>
        <p><strong>Dueño:</strong> {nombre_dueno}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Teléfono:</strong> {telefono}</p>
    </body>
    </html>
    """

    text_content = f"""\
    Nueva Empresa Registrada:
    La empresa {nombre_empresa} ha mostrado interés en unirse a Centinela.
    Detalles de la Empresa:
    Nombre: {nombre_empresa}
    Dueño: {nombre_dueno}
    Email: {email}
    Teléfono: {telefono}
    """

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Nuevo Registro de Empresa'
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = 'iv4npz001@gmail.com'  # Dirección fija para el registro de empresas

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
            server.sendmail(os.getenv('EMAIL_SENDER'), 'iv4npz001@gmail.com', msg.as_string())
        print(f"Correo de registro de empresa enviado a: iv4npz001@gmail.com")
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación: verifique las credenciales del correo.")
    except smtplib.SMTPConnectError:
        print("Error de conexión: no se pudo conectar al servidor SMTP.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
