from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp
import sqlite3

class UserDetailsPage(Screen):
    username = ""
    email = ""

    def on_pre_enter(self):
        self.load_user_details()

    def load_user_details(self):

        app = MDApp.get_running_app()
        user_id = app.user_id

        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, email FROM users WHERE id = ?', (user_id,))  # Assuming the user ID is 1 for simplicity
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            self.username, self.email = user_data
            # self.update_user_details()
        else:
            self.username = "No User Found"
            self.email = "No Email Found"

        # print("Username:", self.username)
        # print("Email:", self.email)

        self.update_user_details()

    def update_user_details(self):        
        user_details_layout = self.ids.user_details_layout
        user_details_layout.clear_widgets()

        # Create the MDLabel widgets for username and email
        username_label = MDLabel(text=f"Username : [size=20][b]{self.username}[/b][/size]", markup=True)
        email_label = MDLabel(text=f"Email : [size=20]{self.email}[/size]", markup=True)

        # print("Username label:", username_label)
        # print("Email label:", email_label)

        # Add the labels to the layout
        user_details_layout.add_widget(username_label)
        user_details_layout.add_widget(email_label)

    def logout(self):
        app = MDApp.get_running_app()
        app.user_id = None  # Reset the user_id attribute
        app.root.current = 'homepage'












