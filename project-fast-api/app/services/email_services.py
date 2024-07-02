import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = ''
sender_password = ''

def send_email(recipient_email, subject, body):
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password) 
        
        server.send_message(msg)
        server.quit()
        
        print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
