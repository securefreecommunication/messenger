import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import logging
import datetime
import collections
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import werkzeug
from flask import Flask#, request,make_response
from flask_restful import Resource, Api,reqparse, fields, marshal

app=Flask(__name__)
api=Api(app)
# auth = HTTPTokenAuth()

### setting up authentication
tokens = {
    "secret-token-1": 'hooman',
    "secret-token-2": True
}
# @auth.verify_token
# def verify_token(token):
#
#     if token in tokens:
#
#         return tokens[token]
#



class Message:
    time=None
    content=None

class Server:
    def __init__(self,ip,port):
        self.users= pd.DataFrame(columns=['public_key'])# id and public keys
        self.id_message={}# user_id:[Message]
        self.ip=ip
        self.port=port

    def send_messages(self,user_id):
        return_message=[]
        if user_id in self.id_message:
            for message in self.id_message[user_id]:
                return_message.append(message)
                self.id_message[user_id].remove(message)


            if  self.id_message[user_id]==[]:
                self.id_message.pop(user_id)

        return return_message

    def match_user(self,public_key):

        if public_key not in self.users['public_key'].values:
            self.users=self.users.append(pd.Series({'public_key':public_key}),ignore_index=True)

        return self.users[self.users['public_key']==public_key].index[0]

    def receive_text_message(self,message,receiver_public_key,sender_public_key,time,encrypted_file,extension,encrypted_nonce,encrypted_aes_key):
        user_id=self.match_user(receiver_public_key)
        if user_id not in self.id_message.keys():
            self.id_message[user_id]=[]
            self.id_message[user_id].append({'message':message,'time':time,'sender_public_key':sender_public_key,'encrypted_file':encrypted_file,'extension':extension,'encrypted_nonce':encrypted_nonce,'encrypted_aes_key':encrypted_aes_key})

        else:
            self.id_message[user_id].append({'message':message,'time':time,'sender_public_key':sender_public_key,'encrypted_file':encrypted_file,'extension':extension,'encrypted_nonce':encrypted_nonce,'encrypted_aes_key':encrypted_aes_key})



server=Server('0.0.0.0',5000)

class Default(Resource):
    def __init__(self):
        # self.reqparser=reqparse.RequestParser()
        # self.reqparser.add_argument('hashtag', type=str, required=True,
        #                            help='No hashtag provided',
        #                            location='json')
        # self.reqparser.add_argument('n', type=str, required=False,
        #                             help='No n provided',
        #                             location='json')
        super(Default,self).__init__()


    # @auth.login_required
    def get(self):


        return {"title":"Secure Messenger","version":"0.0.0","date_time":str(datetime.datetime.now())}

class LogIn(Resource):
    def __init__(self):

        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('time', type=str, required=True,
                                    help='No time provided',
                                    location='json')
        self.reqparser.add_argument('public_key', type=str, required=True,
                                    help='No public key provided',
                                    location='json')

        super(LogIn, self).__init__()
    def post(self):
        '''
        public_key
        message
        :return:
        '''


        try:
            args = self.reqparser.parse_args()
            public_key = args['public_key']
            time = args['time']
            server.match_user(public_key)

            return {'status':'success'}
        except Exception as e:
            return {'status':'fail','error':e}

class UpdateUser(Resource):
    def __init__(self):

        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('public_key', type=str, required=True,
                                    help='No public key provided',
                                    location='json')

        super(UpdateUser, self).__init__()
    def post(self):

        try:
            args = self.reqparser.parse_args()
            public_key = args['public_key']
            user_id=server.match_user(public_key)

            messages=server.send_messages(user_id)

            return {'status':'success','messages':messages}
        except Exception as e:
            return {'status':'fail','error':e}

class ReceiveTextMessage(Resource):
    def  __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('message', type=str, required=False,
                                    help='No message provided',
                                    location='json')
        self.reqparser.add_argument('time', type=str, required=True,
                                    help='No time provided',
                                    location='json')
        self.reqparser.add_argument('receiver_public_key', type=str, required=True,
                                    help='No receiver public key provided',
                                    location='json')
        self.reqparser.add_argument('sender_public_key', type=str, required=True,
                                    help='No sender public key provided',
                                    location='json')
        self.reqparser.add_argument('encrypted_file', type=str, required=False,
                                    help='No sender public key provided',
                                    location='json')
        self.reqparser.add_argument('extension', type=str, required=False,
                                    help='No sender public key provided',
                                    location='json')
        self.reqparser.add_argument('encrypted_aes_key', type=str, required=False,
                                    help='No sender public key provided',
                                    location='json')
        self.reqparser.add_argument('encrypted_nonce', type=str, required=False,
                                    help='No sender public key provided',
                                    location='json')
        #encrypted_file
        super(ReceiveTextMessage, self).__init__()
    def post(self):
        '''
        public_key
        message
        :return:
        '''

        try:
            args=self.reqparser.parse_args()
            receiver_public_key=args['receiver_public_key']
            sender_public_key = args['sender_public_key']
            time = args['time']
            message = args['message']
            encrypted_file = args['encrypted_file']
            extension = args['extension']
            encrypted_aes_key = args['encrypted_aes_key']
            encrypted_nonce = args['encrypted_nonce']
            server.receive_text_message(message,receiver_public_key,sender_public_key,time,encrypted_file,extension,encrypted_nonce,encrypted_aes_key)
            return {'status':'success'}
        except Exception as e:
            return {'status': 'fail','error':e}



api.add_resource(Default, '/', endpoint = 'default')
api.add_resource(ReceiveTextMessage, '/textmessage', endpoint = 'textmessage')
api.add_resource(UpdateUser, '/update', endpoint = 'update')
api.add_resource(LogIn, '/login', endpoint = 'login')


if __name__ == '__main__':
    app.run(debug=None,host='0.0.0.0')