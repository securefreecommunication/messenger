from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem,TwoLineListItem,OneLineAvatarListItem,ContainerSupport,OneLineAvatarIconListItem,BaseListItem,IconLeftWidget,IconRightWidget
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCardSwipe,MDCard
from kivy.core.clipboard import Clipboard
from kivy.app import Builder
from client import Client
from kivy.clock import Clock
import pandas as pd
from kivy.properties import StringProperty
import os
import subprocess
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
KV = '''
<IconPathButton>:

<FileUploadBox>:
    pos_hint:{'x': .08, 'y': 0.08}
    size_hint:(.65,0.08)
    
    MDCard:
        id:root.idp
        orientation:"horizontal"
        pos_hint:{'x': 0, 'y': 0}
        size_hint:(1,1)
        md_bg_color: app.theme_cls.primary_light
        radius: [20]
        
        MDLabel:
            id:file_path
            text:root.file_path
            pos_hint:{"x":0.2,"y":0}
            size_hint:(0.6,1)
            
        MDIconButton:
            id:cancel_button
            icon: "cancel"
            pos_hint:{"right":0.9,"y":0}
            size_hin:(0.3,1)
        
        
    
    
<MessageTextCard>:
    orientation: "vertical"
    size_hint: .5, None
    height: box_top.height + box_bottom.height+20
    md_bg_color: app.theme_cls.primary_light
    padding: "10dp"
    radius: [10]
   
    
    
    
    MDLabel:
        id: box_top
        font_style:"H6"
       
        text: root.sender_text
        theme_text_color: "Secondary"
        adaptive_height: True
        size:(10,10)
        # pos_hint:{'x': 0, 'top': 1}
    
    MDSeparator:
        height: "1dp"
    MDLabel:
        id: box_bottom
        font_style:"Body2"
        text: root.message_text
        theme_text_color: "Secondary"
        adaptive_height: True
       
    
<MessageFileCard>:
    pos_hint:{'right':1}
    orientation: "vertical"
    size_hint: .5, None
    height: box_top.height + box_bottom.height+icon_file.height+20
    md_bg_color: app.theme_cls.primary_light
    padding: "10dp"
    radius: [10]
    
    MDLabel:
        id: box_top
        font_style:"H6"
       
        text: root.sender_text
        theme_text_color: "Secondary"
        adaptive_height: True
        size:(10,10)
        # pos_hint:{'x': 0, 'top': 1}
    
    MDSeparator:
        height: "1dp"
    MDLabel:
        id: box_bottom
        font_style:"Body2"
        text: root.message_text
        theme_text_color: "Secondary"
        adaptive_height: True
    MDSeparator:
        height: "1dp"
    IconPathButton:
        id:icon_file
        pos_hint: {"center_x": .5, "center_y": .5}
        icon: "file"
        adaptive_height: True
        file_path:root.file_path
        
MDScreen:
    RelativeLayout:
        pos_hint:{'x': 0, 'top': 1}
        size_hint: (1,.1)
        # md_bg_color:app.theme_cls.primary_dark
        # Widget:
        #     canvas:
        #         Color:
        #             rgba: app.theme_cls.primary_light
        #         Rectangle:
        #             pos: self.pos
        #             size: self.size
        Widget:
            pos_hint:{'center_x': 0.5, 'y': 0}
            size_hint: (.8,.01)
            size_hint_max_y:1
            size_hint_min_y:1
            canvas:
                Color:
                    rgba: app.theme_cls.primary_dark
            
                Rectangle:
                    pos: self.pos
                    size: self.size
                    
        FitImage:
            id: icon_img
            size_hint:(0.05,0.8)
            # width: dp(5)
            pos_hint: {"center_y": 0.5,"x":0}
            # allow_stretch : True
            
            
        
        MDTextFieldRound:
            id: server_ip_entry
            hint_text: "Server IP"
            icon_left: 'server'
            mode: "rectangle"
            size_hint: (.28,.6)
            pos_hint:{'x': .15, 'center_y': .5}
            line_color_normal:app.theme_cls.primary_light
            current_hint_text_color:app.theme_cls.primary_light
            current_hint_text_color:app.theme_cls.primary_light
                    
        MDTextFieldRound:
            id: password
            password: True
            password_mask: "●"
            icon_left: 'key-variant'
            hint_text: "Password"
            mode: "rectangle"
            size_hint: (.25,.6)
            pos_hint:{'x': 0.48, 'center_y': .5}
            line_color_normal:app.theme_cls.primary_light
            current_hint_text_color:app.theme_cls.primary_light
            current_hint_text_color:app.theme_cls.primary_light
        
        MDRoundFlatButton:
            id: connect_butt
            size_hint: (.2,.6)
            pos_hint:{'right': 0.98, 'center_y': .5}
            text: "Connect"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_dark
            line_color: app.theme_cls.primary_dark
            
                    
    
           
        

    RelativeLayout:
        id:layout_1
        pos_hint:{'x': 0, 'top': .9}
        size_hint: (1,.9)
        
        
        
        RelativeLayout:
            id:contact_layout
            size_hint: (0.3,1)
            pos_hint:{'x': 0, 'top': 1}
            # Widget:
            #     canvas:
            #         Color:
            #             rgba: app.theme_cls.primary_light
            #         Rectangle:
            #             pos: self.pos
            #             size: self.size 
                        
            Widget:
                pos_hint:{'right': 1, 'center_y': 0.5}
                size_hint: (.01,.8)
                size_hint_max_x:1
                size_hint_min_x:1
                canvas:
                    Color:
                        rgba: app.theme_cls.primary_dark
                
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    
            RelativeLayout: 
                pos_hint:{'x': 0, 'top': 1}
                size_hint: (1,.7)
                # Widget:
                #     canvas:
                #         Color:
                #             rgba: app.theme_cls.primary_light
                #         Rectangle:
                #             pos: self.pos
                #             size: self.size 
                
                ScrollView:
                    MDList:
                        id: contact_list
                    
            RelativeLayout:
                id:contact_butts
                pos_hint:{'x': 0, 'y': 0}
                size_hint: (1,.3)
                       
                
                
                MDTextFieldRound:
                    id: contact_code
                    hint_text: "Enter Public Code"
                    mode: "rectangle"
                    pos_hint:{'center_x': .5, 'top': 1}
                    size_hint: (.7,.25)
                MDTextFieldRound:
                    id: contact_name         
                    hint_text: "Enter Contact Name"
                    mode: "rectangle"
                    pos_hint:{'center_x': .5, 'top': .75}
                    size_hint: (.7,.25)
                MDRoundFlatButton:
                    id: add_contact_butt
                    size_hint: (.45,.25)
                    pos_hint:{'center_x': .25, 'top': .5}
                    text: "Add Contact"
                    theme_text_color: "Custom"
                    #text_color: 1, 0, 0, 1
                    #line_color: 0, 0, 1, 1
                MDRoundFlatButton:
                    id: edit_contact_butt
                    size_hint: (.45,.25)
                    pos_hint:{'center_x': .75, 'top': .5}
                    text: "Edit Contact"
                    theme_text_color: "Custom"
                    #text_color: 1, 0, 0, 1
                    #line_color: 0, 0, 1, 1
                
                MDRoundFlatButton:
                    id: copy_my_key_butt
                    size_hint: (.85,.25)
                    pos_hint:{'center_x': .5, 'y': 0}
                    text: "Copy my Public Key"
                    theme_text_color: "Custom"
                    
            
        RelativeLayout:
            id:chat_layout
            pos_hint:{'x': 0.3, 'top': 1}
            size_hint: (.7,1)
           
            RelativeLayout:
                pos_hint:{'x': 0, 'top': 1}
                size_hint: (1,.7)
                
                
                
                # ScrollView:
                #     MDList:
                #         id: chat_history_list
                
                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
                    # size:self.size
                    MDBoxLayout:
                        id:chat_history_list
                        size_hint_y: None
                        orientation:'vertical'
                        spacing:'50dp'
                        
            RelativeLayout:
                id:chat_bottom_layout
                pos_hint:{'x': 0, 'y': 0}
                size_hint: (1,.1)
                # orientation:"horizontal"
               
                MDTextFieldRound:
                    id: message_entry         
                    multiline: True
                    hint_text: "Type your message"
                    mode: "rectangle"
                    size_hint: (.65,.8)
                    pos_hint:{'x': .08, 'y': 0}
                    
                
                
                MDRoundFlatButton:
                    id:send_message_butt
                    size_hint: (.2,.8)
                    pos_hint:{'right': .99, 'y': 0}
                   
                    text: "Send"
                    theme_text_color: "Custom"
                    # text_color: 1, 0, 0, 1
                    # line_color: 0, 0, 1, 1
            
                
            
    
'''
class MessageTextCard(MDCard):
    '''Card with `swipe-to-delete` behavior.'''

    sender_text = StringProperty()
    message_text=StringProperty()
class MessageFileCard(MDCard):
    '''Card with `swipe-to-delete` behavior.'''

    sender_text = StringProperty()
    message_text=StringProperty()
    file_path = StringProperty()
class IconPathButton(MDIconButton):
    '''Card with `swipe-to-delete` behavior.'''

    file_path = StringProperty()

class FileUploadBox(RelativeLayout):
    file_path = StringProperty()
    idp = StringProperty()


class MainPage(MDApp):



    def build(self):
        self.theme_cls.theme_style = "Light"  # "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"  # "500"
        self.client = Client(None)
        self.screen = Builder.load_string(KV)
        self.screen.ids.icon_img.source='..\\lock.png'
        self.screen.ids.connect_butt.bind(on_press=self.connect)
        self.screen.ids.add_contact_butt.bind(on_press=self.add_contact)
        self.screen.ids.edit_contact_butt.bind(on_press=self.edit_contact)
        self.screen.ids.send_message_butt.bind(on_press=self.send_message)
        self.screen.ids.copy_my_key_butt.bind(on_press=self.copy_my_public_key_to_clipboard)
        Window.bind(on_dropfile=self._on_file_drop)
        Clock.schedule_interval(self.update_user_state_regular, 10)

        # self.tap_target_view = MDTapTargetView(
        #     widget=self.screen.ids.server_ip_entry,
        #     title_text="This is an add button",
        #     description_text="This is a description of the button",
        #     widget_position="left_top",
        # )

        self.selected_chat_index=None
        self.waiting_file_path=None
        return self.screen

        # return screen

    def on_start(self):
        self.fill_contacts()
        # self.tap_target_start()

    def on_stop(self):
        password = self.root.ids.password.text
        self.client.dump_contacts()
        self.client.dump_password_encrypted_private_key(password)
        self.client.dump_chat_history()

    def tap_target_start(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()

    def fill_contacts(self):
        self.root.ids.contact_list.clear_widgets()
        for i,contact in self.client.contacts.iterrows():

            self.root.ids.contact_list.add_widget(

                OneLineListItem(text=contact['name'],on_release=self.chat_history_load) )

    def chat_history_load(self, onelinelistitem):
        self.client.update()
        self.cancel_upload('')
        index=len(self.root.ids.contact_list.children) - 1-self.root.ids.contact_list.children.index(onelinelistitem)
        self.selected_chat_index = index
        selected_contact = self.client.contacts.iloc[index]
        contact_history=self.client.chat_history[self.client.chat_history['contact_id']==index]
        self.root.ids.chat_history_list.clear_widgets()
        for i, message in contact_history.iterrows():
            sender=message['sender_contact_id']
            if sender=='me':
                sender='me'
            else:
                sender=selected_contact['name']

            if pd.isna(message['content_address']) or message['content_address'] is None:
                message_card = MessageTextCard(sender_text=sender,
                                               message_text=message['message'])

                if sender=='me':
                    message_card.pos_hint='{"x":0}'
                else:
                    message_card.pos_hint = '{"right":1}'


            else:

                message_card = MessageFileCard(sender_text=sender,
                                               message_text=message['message'], file_path=message['content_address'])
                message_card.ids.icon_file.bind(on_press=self.open_path)

            if sender == 'me':
                message_card.pos_hint = {"x": 0}
            else:

                message_card.pos_hint = {"right": 1}

            self.root.ids.chat_history_list.add_widget(message_card)
            self.screen.ids.chat_history_list.height += message_card.height




    def chat_history_refresh(self):
        self.client.update()
        index = self.selected_chat_index
        if index is not None:


            selected_contact = self.client.contacts.iloc[index]
            contact_history = self.client.chat_history[self.client.chat_history['contact_id'] == index]
            self.root.ids.chat_history_list.clear_widgets()
            for i, message in contact_history.iterrows():
                sender = message['sender_contact_id']
                if sender == 'me':
                    sender = 'me'
                else:
                    sender = selected_contact['name']

                if pd.isna(message['content_address']) or message['content_address'] is None:
                    message_card = MessageTextCard(sender_text=sender,
                                                   message_text=message['message'])



                else:
                    message_card = MessageFileCard(sender_text=sender,
                                                   message_text=message['message'],
                                                   file_path=message['content_address'])

                if sender == 'me':
                    message_card.pos_hint = {"x": 0}
                else:

                    message_card.pos_hint = {"right": 1}

                self.root.ids.chat_history_list.add_widget(message_card)
                self.screen.ids.chat_history_list.height += message_card.height

    def connect(self, instance):
            ip = self.root.ids.server_ip_entry.text
            password = self.root.ids.password.text
            self.client = Client(ip, password)
            self.fill_contacts()

    def add_contact(self,instance):
        contact_key=self.root.ids.contact_code.text
        name = str(self.root.ids.contact_name.text)
        if contact_key!='' and name!='':

            self.client.add_contact(contact_key, name)
            self.fill_contacts()

        pass

    def edit_contact(self,instance):
        index = self.selected_chat_index
        name = str(self.root.ids.contact_name.text)
        self.client.contacts.at[index,'name']=name


        self.fill_contacts()

        pass

    def save(self):
        ip = self.root.ids.server_ip_entry.text
        password = self.root.ids.password.text
        self.client.dump_password_encrypted_private_key(password)
        self.client.dump_contacts()

    def update_user_state_regular(self,dt):
        self.client.update()
        self.chat_history_refresh()
        self.fill_contacts()

    def update_user_state(self):
        self.client.update()
        self.chat_history_refresh()
        self.fill_contacts()

    def copy_my_public_key_to_clipboard(self,instance):

        Clipboard.copy(self.client._public_key_send)

    def copy_contact_public_key_to_clipboard(self,onelinelistitem,instance):
        index = len(self.root.ids.contact_list.children) - 1 - self.root.ids.contact_list.children.index(
            onelinelistitem)
        self.selected_chat_index = index
        selected_contact = self.client.contacts.iloc[self.selected_chat_index]

        Clipboard.copy(selected_contact['public_key'])

    def send_message(self,onelinelistitem):
        if self.selected_chat_index is None:
            print('no chat selected')
        else:
            print('sending message')
            selected_contact = self.client.contacts.iloc[self.selected_chat_index]
            message= self.root.ids.message_entry.text
            self.root.ids.message_entry.text=''
            if self.waiting_file_path is not None:
                with open(self.waiting_file_path,'rb') as f:
                    only_name=os.path.split(self.waiting_file_path)[1]
                    dot_pos=only_name.find('.')
                    ext=only_name[dot_pos:]
                    self.client.send_message(self.selected_chat_index,message,f.read(),ext,self.waiting_file_path)
                self.cancel_upload('')
            else:
                self.client.send_message(self.selected_chat_index, message)

            self.chat_history_refresh()

    def open_path(self,instance):
        path = instance.file_path
        path = os.path.realpath(path)
        subprocess.Popen(r'explorer /select,"{{path}}"'.replace('{{path}}',path))

    def _on_file_drop(self, window, file_path):

        self.waiting_file_path=file_path.decode('ascii')
        self.show_file_upload_box()
        return

    def show_file_upload_box(self):
        self.file_upload_box=FileUploadBox(file_path=self.waiting_file_path,idp='upload_box')
        self.file_upload_box.ids.cancel_button.bind(on_press=self.cancel_upload)
        self.screen.ids.chat_layout.add_widget(self.file_upload_box)

    def cancel_upload(self,instance):
        self.waiting_file_path=None
        self.screen.ids.chat_layout.remove_widget(self.file_upload_box)






MainPage().run()