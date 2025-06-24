import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import config

def enviar_correo(eventos):
    if not eventos:
        print("[INFO] No hay eventos para enviar por correo.")
        return

    remitente = config.EMAIL_USER
    destinatario = config.EMAIL_RECEIVER
    contraseña = config.EMAIL_PASSWORD

    # Componer el cuerpo del correo
    cuerpo = "\n\n".join([
        f"{e['nombre']} - {e['fecha']} ({e['origen']})\n{e['link']}"
        for e in eventos
    ])

    mensaje = MIMEMultipart()
    mensaje["Subject"] = f"📢 {len(eventos)} nuevos eventos detectados"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.attach(MIMEText(cuerpo, "plain"))

    try:
        if "gmail.com" in remitente.lower():
            print("[INFO] Enviando correo usando Gmail...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(remitente, contraseña)
                server.sendmail(remitente, destinatario, mensaje.as_string())

        elif "outlook.com" in remitente.lower() or "hotmail.com" in remitente.lower() or "office365.com" in remitente.lower():
            print("[INFO] Enviando correo usando Outlook/Office 365...")
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(remitente, contraseña)
                server.sendmail(remitente, destinatario, mensaje.as_string())

        else:
            print("[WARN] Dominio de correo no reconocido, se intenta con configuración de Outlook por defecto...")
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(remitente, contraseña)
                server.sendmail(remitente, destinatario, mensaje.as_string())

        print(f"[INFO] Correo enviado a {destinatario} con {len(eventos)} eventos.")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {str(e)}")

def enviar_telegram(eventos):
    if not eventos:
        print("[INFO] No hay eventos para enviar por Telegram.")
        return

    mensaje = "\n\n".join([
        f"{e['nombre']} - {e['fecha']} ({e['origen']})\n{e['link']}"
        for e in eventos
    ])
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": f"📢 {len(eventos)} nuevos eventos detectados:\n\n{mensaje}"
    }

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"[INFO] Notificación enviada por Telegram con {len(eventos)} eventos.")
        else:
            print(f"[ERROR] Error al enviar por Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el mensaje por Telegram: {str(e)}")