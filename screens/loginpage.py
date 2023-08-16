from kivy.uix.screenmanager  import Screen
from screens.userdetailspage import UserDetailsPage
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
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

# Function to check if the email and password match a user in the database
def authenticate_user(email, password):
   conn = sqlite3.connect('user_database.db')
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
   user_data = cursor.fetchone()
   conn.close()
   return user_data

class LoginPage(Screen):

   def on_login_button_click(self):
      email = self.ids.email.text
      password = self.ids.password.text

      user_data = authenticate_user(email, password)

      if user_data:
         app = MDApp.get_running_app()
         app.user, app.email, app.username = user_data[0], user_data[3], user_data[1]
         # app.root.current = 'userdetailspage'
         app.on_login_success(user_data[0])
      else:
         check_string = 'Invalid credentials. Please try again.'
         self.show_error_dialog(check_string)

   def show_error_dialog(self, message):
      self.error_dialog = MDDialog(title='Error', text=message, buttons=[MDFlatButton(text='Dismiss', on_release=self.close_error_dialog)])
      self.error_dialog.open()

   def close_error_dialog(self, instance):
      self.error_dialog.dismiss()

   # def show_password(self,value):
   #    if value:
   #       self.root.ids.password.password = True
   #    else:
   #       self.root.ids.password.password = False

   def login_success(self, user_id):
      app = MDApp.get_running_app()
      app.on_login_success(user_id)

   

      