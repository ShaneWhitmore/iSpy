import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from gpiozero import LED, Button
from signal import pause
from picamera import PiCamera
import datetime

button = Button(22)
camera = PiCamera()

camera.start_preview()
frame = 1


def send_mail(eFrom, to, subject, text, attachment):
    smtpServer = 'sandbox server from mailgun'
    smtpUser = ' my user name here'
    smtpPassword = 'my password here '
    port = 587

    fp = open(attachment, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msg = MIMEMultipart()
    msg.attach(MIMEText(text))
    msgImage['Content-Disposition'] = 'attachment; filename="image.jpg"'
    msg.attach(msgImage)
    msg['Subject'] = subject

    s = smtplib.SMTP(smtpServer, port)
    s.login(smtpUser, smtpPassword)
    s.sendmail(eFrom, to, msg.as_string())
    s.quit()


while True:
    button.wait_for_press()
    fileLoc = f'/home/pi/project1/images/frame{frame}.jpg'
    currentTime = datetime.datetime.now().strftime("%H:%M:%S")

    camera.capture(fileLoc)
    print(f'frame {frame} taken at {currentTime}')
    frame += 1

    text = f'Hi,\n the attached image was taken today at {currentTime}'
    send_mail('raspberry pi mailgun email', 'my email address here', 'Door    Event', text, fileLoc)


