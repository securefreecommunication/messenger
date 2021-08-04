# Messenger
Simple and Secure Messenger 

This respitory includes a client and server codes for a simple yet secure messenger.
Today many seured messenger app exists with numerous great services but the intention of this project lies in having your own secure messenger when those services are out of reach and the available messenger are not secure because of oragnizations or governments intentions. This is how people can retain their privacy in restricted systems.

## Philosophie
You will be able to host your own messenger system and share it with your cirlce of trust. It is a secure way of communication with no links to your identity only ones who know your public code can communicate with you and your identity remains in your circle of trust. In the more complete version servers should be able to communicate with their own trusted peers for sending public group information on a bigger level. Since no data will be kept on the servers not even sncrypted messages there will no means of leaking the data or recovery. Every thing is kept encrypted and password protected on your machine. Most important data is your private key which will be saved on your machine in messnger local folder in private_key.pem and is password protected, every other information will be decrypted only by this key. keep it safe and if you want to delete everything delete this file permanently. The following describe several design guidelines of this project.

- Messages should be end to end encrypted.
- No data will remain on the servers only public keys.
- No phone numbers are needed.
- In the future servers will be able to merge and send public group informations

## Description
There are two parties of the system . Server and Client just like every other chatting service out there. current implementation is very simple just giving you the tools of communication and written in few nights. The whole project is written on Python using Kivy as user interface and flask in backend.

Client : will send encrypted messages to server. sending encrypted files are also supported while there is no limits on file size you could blow up your server ram since no databases exist on the server to retain the data in current implementation.
Current implementation does not have open socket with the server so updates and recieved messages are get by an client call for update to the server. all data existing on your machine is encrypted with your private key and private key is also password protected.

Server: Every information is kept on ram. each time server receives a message it holds the messages indexed by public key and delivers the messages when ever they are successfully delivere to recipient, after successful delivery the messages are dumped from the server ram and only exist on sender and recipient mahcines.


