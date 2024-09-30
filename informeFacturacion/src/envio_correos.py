import os
import smtplib
import locale
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config.directories import REPORTS_DIRECTORY
from config.smtp_config import *

def envioCorreos(fechaPeriodo, flujo, logger):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    mes_periodo  = fechaPeriodo.strftime('%B').capitalize()
    año_periodo = fechaPeriodo.strftime('%Y')
    if flujo == 'MFT':
    # Definir el patrón del nombre del archivo con el formato MFT-XXXXXX (donde X son dígitos)
        regex_pattern = r"MFT-\d{6}\.txt"  # Patrón para archivos como MFT-072024.txt

    if flujo == 'WEB':
        regex_pattern = r"WEB-\d{6}\.txt"

    # Buscar directamente el primer archivo que coincida con el patrón
    matching_file = next((f for f in os.listdir(REPORTS_DIRECTORY) 
                          if os.path.isfile(os.path.join(REPORTS_DIRECTORY, f)) 
                          and re.match(regex_pattern, f)), None)
    
    if not matching_file:
        print("No se encontró ningún archivo que coincida con el patrón.")
        logger.info("No se encontró archivo que coincida con el patrón.")
        raise ValueError("No se encontró archivo que coincida con el patrón.")

    # Ruta completa del archivo encontrado
    file_path = os.path.join(REPORTS_DIRECTORY, matching_file)

    # Configuración de la cuenta SMTP de Brevo
    smtp_server = SMTPSERVER
    smtp_port = SMTPPORT
    smtp_user = SMTPUSER
    smtp_password = SMTPPASSWORD

    # Dirección del remitente y destinatario
    from_email = FROMEMAIL
    to_emails = destinatarios

    # Asunto y cuerpo del correo
    subject = f"Archivo facturación {flujo} período {mes_periodo}-{año_periodo}"

    # Crear el mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    html_body = f"""
    <html>
    <body>
        <h2 style="color: #2e6c80;">Reporte de Facturación {flujo}</h2>
        <p>Estimado(a),</p>
        <p>El siguiente correo adjunta el reporte de facturación de <strong>flujo {flujo}</strong> correspondiente al período de <strong>{mes_periodo} del año {año_periodo}</strong>.</p>
        <p>Este correo es automático, favor no responder.</p>
        <br>
        <p>Atentamente,</p>
        <p><strong>Equipo Sinacofi</strong></p>
    </body>
    </html>
    """

    # Adjuntar el cuerpo HTML al mensaje
    msg.attach(MIMEText(html_body, 'html'))

    # Ruta del archivo a adjuntar
    file_name = os.path.basename(file_path)

    # Abrir el archivo en modo binario
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Codificar el archivo en base64
    encoders.encode_base64(part)

    # Agregar encabezados al archivo adjunto
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_name}",
    )

    msg.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_emails, msg.as_string())
            print("Correos enviados exitosamente")
            logger.info("Correos enviados exitosamente")

        os.remove(file_path)
        print(f"Archivo {file_name} eliminado.")
        logger.info(f"Eliminando archivo {file_name}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        logger.error(f"Error al enviar el correo: {e}")
