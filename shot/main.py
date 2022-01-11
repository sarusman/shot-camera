import cv2, os
import numpy as np
import requests, smtplib, datetime, time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


cv2.namedWindow("CAMERA INPUT")
vc = cv2.VideoCapture(0)

old_frame=np.array([0, 0, 0])

v=0
os.system('clear')

def sms(message, numéro):
	report = {"value1": numéro, "value2":message}
	requests.post("https://maker.ifttt.com/trigger/trigger_ifttte/with/key/CléSecrete", data=report)
	return True

def mail( dmail, nom):
	img_data = open(os.getcwd()+"/images/"+nom, 'rb').read()
	message = MIMEMultipart()
	message['Subject'] = 'INTRUSION'
	message['From'] = 'mobilitchi@gmail.com'
	message['To'] = dmail
	conex=smtplib.SMTP('smtp.gmail.com:587')
	message.attach(MIMEText(nom.split(".")[0]))
	fp = open("images/"+nom, 'rb')
	message.attach(MIMEImage(fp.read()))
	fp.close()
	conex.ehlo()
	conex.starttls()
	conex.ehlo()
	conex.login('mobilitchi@gmail.com', '*')
	conex.sendmail('mobilitchi@gmail.com', dmail ,message.as_string())
	conex.quit()
	return True




number_liste=[] # Ajouter ici les numéros à qui envoyé l'alerte : exp : "**********"

while True:
	rval, frame = vc.read()
	cv2.imshow("CAMERA", frame)
	key = cv2.waitKey(20)
	if key == 27:
		break
	t = np.sum(old_frame - frame)
	if t>500000000:
		name=str(datetime.datetime.now())+'.png'
		cv2.imwrite("images/"+name,frame)
		mail( "VOTRE ADRESSE MAIL --> MAIL RECEPTEUR", name)
		for number in number_liste:
			try: # car lien à redéfinir ...
				sms("VOIR MAIL", number)
			except:
				pass
	old_frame=frame






