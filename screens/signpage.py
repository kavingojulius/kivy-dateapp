from kivy.uix.screenmanager  import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.app import App

import sqlite3


def create_user_table():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert user details into the SQLite database
def insert_user_details(username, password, email):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                   (username, password, email))
    conn.commit()
    conn.close()

def passwords_match(password, cpassword):
    return password == cpassword


class SignPage(Screen):

   def data_show(self):
      create_user_table()
      username = self.ids.username.text
      password = self.ids.password.text
      cpassword = self.ids.cpassword.text
      email = self.ids.email.text

      
      if email == "" or username == "" or password == "" or cpassword == "":
         check_string = 'Missing details !!!'
         self.show_error_dialog(check_string)
      elif not passwords_match(password, cpassword):
         check_string = 'Passwords do not match.'
         self.show_error_dialog(check_string)
      else:
         check_string = "[b]Email : [/b]" + email + "\n[b]Password :  [/b]" + password + "\n[b]Username :  [/b]" + username

         edit = MDFlatButton(text='Edit',on_release=self.close_dialog)
         okay = MDFlatButton(text='Okay',on_release=self.redirect_to_user_details)       

         self.dialog = MDDialog(title='Confirm Details',text=check_string,buttons=[edit,okay])                                                                                                                          
         self.dialog.open()
      
   def show_error_dialog(self, message):
      self.error_dialog = MDDialog(title='Error', text=message, buttons=[MDFlatButton(text='Dismiss', on_release=self.close_error_dialog)])
      self.error_dialog.open()
   def close_error_dialog(self, instance):
      self.error_dialog.dismiss()

   def redirect_to_user_details(self, instance):
      username = self.ids.username.text
      password = self.ids.password.text
      cpassword = self.ids.cpassword.text
      email = self.ids.email.text

      if not passwords_match(password, cpassword):
         # Passwords don't match, show an error message or toast here
         check_string = 'Passwords do not match.'
         self.show_error_dialog(check_string)
      else:
         # Passwords match, proceed to store user details
         email = self.ids.email.text
         insert_user_details(username, password, email)
         app = App.get_running_app()
         app.root.current = 'loginpage'
         self.close_dialog(None)
      # if password == cpassword or email != "" or username != "" or password != "" or cpassword != "":
               
      #    # Passwords match, proceed to store user details
      #    email = self.ids.email.text
      #    insert_user_details(username, password, email)
      #    app = App.get_running_app()
      #    app.root.current = 'userdetailspage'
      #    self.close_dialog(None)

      # else: 
      #    self.dialog.dismiss()

   def close_dialog(self, obj):
      self.dialog.dismiss()

   
   # pass
    