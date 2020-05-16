from __future__ import print_function
import pickle
import os.path
import smtplib
import base64
import mimetypes
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)    
    message["to"] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}
    
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None    

def getService():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    serviceApi = build('gmail', 'v1', credentials=creds)
    return serviceApi
    
if __name__ == '__main__':
    service = getService()
    remetente = "<jeffersonf781@gmail.com>"
    destinatário = "<jeffersonf781@gmail.com>"
    assunto = "testeAPI"
    texto_mensagem = "teste realizado com sucesso"
    mensagem = create_message(remetente, destinatário, assunto, texto_mensagem)
    send_message(service, "me", mensagem)
