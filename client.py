# import hashlib
# import random
# import json
import binascii
import json
import traceback
import uuid
import numpy as np
import datetime
import Crypto
import Crypto.Random
from Crypto.Random import get_random_bytes
# from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
# import werkzeug
import requests
import os
import pandas as pd
import qrcode
# from pyzbar.pyzbar import decode

class Client:

    def __init__(self,server_ip,password=None):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(2048, random)
        self._public_key = self._private_key.publickey()
        self.contacts_name_key={}
        self.contacts_pkey_key = {}
        self.contacts=pd.DataFrame(columns=['name','public_key'])
        #self.groups = {}
        self.server_ip=server_ip
        self.request_session=requests.Session()
        self._public_key_send=binascii.b2a_hex(self._public_key.exportKey()).decode('ascii')
        self.chat_history=pd.DataFrame(columns=['sender_contact_id','receiver_contact_id','message','time','contact_id','content_address']) # contact:messages
        self.aes_key= get_random_bytes(16)
        self.aes_cipher = AES.new(self.aes_key, AES.MODE_EAX)
        self.nonce = self.aes_cipher.nonce
        self.download_files_path='secure_messenger_download'
        if not os.path.isdir(self.download_files_path):
            os.makedirs(self.download_files_path)



        self.password=password
        if password is not None:
            if os.path.isfile('private_key.pem') and os.path.isfile('aes_key.pem') and os.path.isfile('nonce.pem'):

                self.login_local(self.password)
                try:
                    self.load_contacts()
                    self.load_chat_history()
                except Exception as e:
                    ''
            else:
                self.dump_password_encrypted_private_key(password)

    def dump_password_encrypted_private_key(self,password):
        with open('private_key.pem','wb') as f:
            dumped=self._private_key.export_key(passphrase=password)
            f.write(dumped)
        with open('aes_key.pem','wb') as f:

            encryptor = PKCS1_OAEP.new(self._public_key)
            encrypted = encryptor.encrypt(self.aes_key)
            f.write(encrypted)

        with open('nonce.pem','wb') as f:

            encryptor = PKCS1_OAEP.new(self._public_key)
            encrypted = encryptor.encrypt(self.nonce)
            f.write(encrypted)

    def sign_up(self,):
        if self.server_ip is  None:
            return
        # send public key to server
        url=self.server_ip+'/login'
        payload = { 'time': str(datetime.datetime.now().timestamp()), 'public_key': self._public_key_send}


        resp=self.request_session.post(url, json=payload)

    def login_local(self,password):
        with open('private_key.pem', 'rb') as f:
            key_enc=f.read()
            self._private_key = RSA.importKey(key_enc,passphrase=password)
            self._public_key = self._private_key.publickey()
            self._public_key_send = binascii.b2a_hex(self._public_key.exportKey()).decode('ascii')
        with open('aes_key.pem','rb') as f:
            data=f.read()
            decrypter = PKCS1_OAEP.new(self._private_key)

            decrypted_dict = decrypter.decrypt(data)


            self.aes_key = decrypted_dict

        with open('nonce.pem', 'rb') as f:
            data = f.read()
            decrypter = PKCS1_OAEP.new(self._private_key)

            decrypted_dict = decrypter.decrypt(data)


            self.nonce = decrypted_dict

    def dump_contacts(self):
        # encryptor = PKCS1_OAEP.new(self._public_key)
        cipher = AES.new(self.aes_key, AES.MODE_EAX, self.nonce)
        ciphertext = cipher.encrypt(self.contacts.to_json(orient='records').encode())
        # to_write=encryptor.encrypt(self.contacts.to_json(orient='records').encode())
        with open('contacts.p', 'wb') as f:
            f.write(ciphertext)

    def load_contacts(self):
        # decrypter = PKCS1_OAEP.new(self._private_key)
        cipher = AES.new(self.aes_key, AES.MODE_EAX, self.nonce)
        if os.path.isfile('contacts.p'):
            with open('contacts.p', 'rb') as f:
                # decrypted=decrypter.decrypt(f.read())
                data = cipher.decrypt(f.read())
                self.contacts=pd.read_json(data.decode(),orient='records')

    def send_message(self,contact_id,msg=None,file=None,extension=None,file_path=None):
        if self.server_ip is  None:
            print('no server')
            return
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce

        if file is not None:
            ciphertext_file = cipher.encrypt(file)
            cipher = AES.new(key, AES.MODE_EAX, nonce)
        else:
            ciphertext_file=b''

        if msg is not None:
            ciphertext_msg = cipher.encrypt(msg.encode('ascii'))
        else:
            ciphertext_msg=''.encode('ascii')





        receiver_public_key=RSA.importKey(binascii.a2b_hex(self.contacts.iloc[contact_id]['public_key']))
        receiver_public_key_send = self.contacts.iloc[contact_id]['public_key']
        encryptor = PKCS1_OAEP.new(receiver_public_key)
        encrypted_nonce=binascii.b2a_hex(encryptor.encrypt(nonce)).decode('ascii')
        encrypted_aes_key = binascii.b2a_hex(encryptor.encrypt(key)).decode('ascii')
        encrypted_file = binascii.b2a_hex(ciphertext_file).decode('ascii')
        encrypted_message = binascii.b2a_hex(ciphertext_msg).decode('ascii')
        dtime=str(datetime.datetime.now().timestamp())
        #send request
        url=self.server_ip+'/textmessage'
        payload={'message':encrypted_message,'encrypted_file':encrypted_file,'time':dtime,'receiver_public_key':receiver_public_key_send,'sender_public_key':self._public_key_send,'encrypted_nonce':encrypted_nonce,'encrypted_aes_key':encrypted_aes_key,'extension':extension}
        print('payload',payload)
        resp=self.request_session.post(url,json=payload)
        if resp.json()['status']=='success':

            self.update_chat_history('me',contact_id,msg,dtime,file_path)

    def add_contact(self,public_key,name):

        contact=pd.Series({'public_key':public_key,'name':name})
        self.contacts=self.contacts.append(contact,ignore_index=True)

    def update(self):
        if self.server_ip is  None:
            return
        url = self.server_ip + '/update'

        payload = {'public_key': self._public_key_send}

        resp=self.request_session.post(url, json=payload)
        decrypter=PKCS1_OAEP.new(self._private_key)


        resp_j=resp.json()

        message_list=resp_j['messages']
        print('msg',message_list)


        final=[]
        for message_pack in message_list:
            message_enc=message_pack['message']
            message_time = message_pack['time']
            message_seder_public_key = message_pack['sender_public_key']
            message_enc_file=message_pack['encrypted_file']
            message_extension = message_pack['extension']
            message_encrypted_aes_key = message_pack['encrypted_aes_key']
            message_encrypted_nonce = message_pack['encrypted_nonce']
            key=decrypter.decrypt(binascii.a2b_hex(message_encrypted_aes_key.encode('ascii')))
            nonce = decrypter.decrypt(binascii.a2b_hex(message_encrypted_nonce.encode('ascii')))
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            if message_seder_public_key in  self.contacts['public_key'].values:
                message_seder_contact_id=self.contacts[self.contacts['public_key']==message_seder_public_key].index[0]
            else:
                self.add_contact(message_seder_public_key,'unknown')
                message_seder_contact_id = self.contacts[self.contacts['public_key'] == message_seder_public_key].index[0]
            message_text=cipher.decrypt(binascii.a2b_hex(message_enc.encode('ascii'))).decode('ascii')
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            file=cipher.decrypt(binascii.a2b_hex(message_enc_file))
            if file !=b'':

                file_name=uuid.uuid4().hex
                file_path=os.path.join(self.download_files_path,file_name+'.'+message_extension)

                with open(file_path,'wb') as f:
                    f.write(file)
            else:
                file_path=None

            self.update_chat_history(message_seder_contact_id,'me',message_text,message_time,file_path)

        return

    def generate_qr_code_public_key(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=7,
            border=1,
        )
        qr.add_data(self._public_key_send)
        qr.make()
        img = qr.make_image()
        return img

    def read_qr_code(self,img):
        np_img=np.array(img,np.uint8)
        decoded=decode(np_img)
        decoded=decoded[0].data

        return decoded

    def update_chat_history(self,sender_contact_id,receiver_contact_id,message,message_time,file_add):
        '''

        :param sender_contact_id:  id or me
        :param receiver_contact_id: id or me
        :param message:
        :param message_time:
        :return:
        '''
        if sender_contact_id=='me':
            contact_id=receiver_contact_id
        elif receiver_contact_id=='me':
            contact_id = sender_contact_id


        message_s=pd.Series({'sender_contact_id':sender_contact_id,
                             'receiver_contact_id':receiver_contact_id,
                             'message':message,
                             'time':message_time,
                             'contact_id':contact_id,
                             'content_address':file_add})
        self.chat_history=self.chat_history.append(message_s,ignore_index=True)

    def dump_chat_history(self):
        '''

        :param sender_contact_id:  id or me
        :param receiver_contact_id: id or me
        :param message:
        :param message_time:
        :return:
        '''

        cipher = AES.new(self.aes_key, AES.MODE_EAX, self.nonce)
        ciphertext = cipher.encrypt(self.chat_history.to_json(orient='records').encode())
        # to_write=encryptor.encrypt(self.contacts.to_json(orient='records').encode())
        with open('history.p', 'wb') as f:
            f.write(ciphertext)

    def load_chat_history(self):
        # decrypter = PKCS1_OAEP.new(self._private_key)
        cipher = AES.new(self.aes_key, AES.MODE_EAX, self.nonce)
        if os.path.isfile('history.p'):
            with open('history.p', 'rb') as f:
                # decrypted=decrypter.decrypt(f.read())
                data = cipher.decrypt(f.read())
                self.chat_history=pd.read_json(data.decode(),orient='records')






