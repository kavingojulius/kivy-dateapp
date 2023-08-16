from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.slider import MDSlider
from kivy.uix.popup import Popup
# from kivymd.uix import BaseInputDialog
from kivymd.uix.boxlayout import MDBoxLayout
# from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineAvatarListItem ,OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFlatButton
from screens.components import Info
from kivy.properties import StringProperty
import sqlite3
from kivymd.uix.snackbar import Snackbar



class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()
    def set_icon_gender(self, instance_check):
        instance_check.active = True
        check_gender_list = instance_check.get_widgets(instance_check.group)
        
        for check in check_gender_list:
            if check != instance_check:
                check.active = False

        selected_gender = self.text  # Get the text value of the clicked checkbox

        if instance_check.active:
            DetailsPage.selected_genders.append(selected_gender)
        else:
            DetailsPage.selected_genders.remove(selected_gender)

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        
        for check in check_list:
            if check != instance_check:
                check.active = False

        selected_item = self.text  # Get the text value of the clicked checkbox

        if instance_check.active:
            DetailsPage.selected_items.append(selected_item)
        else:
            DetailsPage.selected_items.remove(selected_item)
    
class DetailsPage(Screen):   
    selected_items = []
    selected_genders = []
    content = None
    # def select_item(self, item_text):
    #     # Update the dropdown button text when an item is selected
    #     self.ids.dropdown_button.text = item_text    
    
    def show_gender_popup(self):        
        input_dialog = MDDialog(title='Gender',
                        # text='hello',
                        type="confirmation",                    
                        items=[
                            Item(text="Male", source="assets/image.png",font_style='Caption',),
                            Item(text="Female", source="assets/image.png",font_style='Caption',),                                
                            ],
                        buttons=[
                            MDFlatButton(
                                text="CANCEL",
                                on_release=lambda *args: input_dialog.dismiss(),
                                # theme_text_color="Custom",
                                # text_color=self.theme_cls.primary_color,
                            ),
                            MDFlatButton(
                                text="OK",
                                on_release=lambda *args: self.process_selected_gender(input_dialog),
                                # theme_text_color="Custom",
                                # text_color=self.theme_cls.primary_color,
                            )],
                        )
        input_dialog.open()
    def process_selected_gender(self, instance_dialog, *args):
        for item in self.selected_genders:
            print(f"Selected item: {item}")

        # Clear the selected_items list after processing
        self.selected_items.clear()

        instance_dialog.dismiss()

    def show_confirmation_dialog(self):
        # if not self.dialog:
        dialog = MDDialog(
                title="R/ship Status",
                type="confirmation",
                items=[
                    ItemConfirm(text="Single"),
                    ItemConfirm(text="Married"),
                    ItemConfirm(text="Dating"),
                    ItemConfirm(text="Divorced"),                    
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda *args: dialog.dismiss(),                       
                    ),
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: self.process_selected_items(dialog),                        
                    ),
                ],
            )
        dialog.open() 

    def process_selected_items(self, dialog_instance, *args):
        for item in self.selected_items:
            print(f"Selected item: {item}")
        # Clear the selected_items list after processing
        self.selected_items.clear()

        dialog_instance.dismiss()

    def show_hobbies_dialog(self):
        self.content = HobbiesContent()
        dialog = MDDialog(
                title="Hobbies & Interests",
                type="custom",
                content_cls=self.content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: dialog.dismiss(),
                        ),
                    MDFlatButton(
                        text="OK",
                        # on_release=lambda x: self.print_text(content,dialog),
                        on_release=lambda x: self.ok_button_pressed(dialog),
                            
                        ),
                ],
            )
        dialog.open()
    def ok_button_pressed(self, dialog):       
        hobbies_text = self.content.ids.hobbies_input.text
        interests_text = self.content.ids.interests_input.text

        if not hobbies_text or not interests_text:            
            # print("current values ")
            # print(hobbies_text," and ",interests_text)
            print("Please provide both hobbies and interests.")
            return
        try:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()

            create_table_query = '''
                CREATE TABLE IF NOT EXISTS user_hobbies_interests (
                    id INTEGER PRIMARY KEY,
                    hobbies TEXT,
                    interests TEXT
                )
            '''
            cursor.execute(create_table_query)

            insert_query = "INSERT INTO user_hobbies_interests (hobbies, interests) VALUES (?, ?)"
            cursor.execute(insert_query, (hobbies_text, interests_text))

            conn.commit()

            cursor.close()
            conn.close()

            # print("Data successfully stored in the database.")
            # Close the dialog after storing data
            dialog.dismiss()

            Snackbar(text="Data successfully stored",
                      duration=1,size_hint_x=.8,pos_hint={"center_y":0.2,"center_x":0.5},snackbar_x="1dp",
                        snackbar_y="1dp").open()

        except Exception as e:
            print("An error occurred:", e)
            # Handle error here

    # Rest of your code
    def print_text(self, content, dialog):
        hobbies_text = content.ids.hobbies_input.text
        interests_text = content.ids.interests_input.text

        print("Hobbies:", hobbies_text)
        print("Interests:", interests_text)

        content.ids.hobbies_input.text = ""
        content.ids.interests_input.text = ""


    def AgeSelectionPopup(self):
        popup = AgeSelectionPopup()
        popup.open()
        
class HobbiesContent(MDBoxLayout):
    pass

class AgeSelectionPopup(Popup):
    # def __init__(self,app, **kwargs):
    #     super().__init__(**kwargs)
    #     self.title = 'Select Age'
    #     self.size_hint = (.8, None)
    #     self.size = (300, 200)
        
    #     # self.content = MDFlatButton(text='OK')
    #     self.app = app
    #     self.age_slider = MDSlider(min=1, max=100, 
    #                                 on_value=self.update_selected_age,
    #                                 active=True,color='white',hint_bg_color='white', 
    #                                 track_color_inactive= "red",                                                                            
    #                                 )
    #     self.ok_button = MDFlatButton(
    #         text='OK',
    #         on_release=self.dismiss
    #     )
    #     self.content = self.age_slider  # You can also use a layout here to add multiple widgets
    #     self.content.add_widget(self.ok_button)

    def print_selected_age(self):
        selected_age = int(self.ids.age_slider.value)
        print(f"Selected Age: {selected_age}")

    # def update_selected_age(self, instance, value):
    #     selected_age = value
    #     # self.app.update_age_label(selected_age)
    #     print(f"Selected Age: {selected_age}")


    # def on_option_selected(self, option):
    #     self.ids.relationship_label.text = f"Relationship: {option}"






    









































































# def showpopup(self):        
#         input_dialog = MDDialog(title='Gender',
#                         # text='hello',
#                         type="simple",                    
#                         items=[
#                             Item(text="Male", source="assets/image.png",font_style='Caption',),
#                             Item(text="Female", source="assets/image.png",font_style='Caption',),                                
#                             ],
#                         buttons=[
#                             MDFlatButton(
#                                 text="CANCEL",
#                                 on_release=lambda *args: input_dialog.dismiss(),
#                                 # theme_text_color="Custom",
#                                 # text_color=self.theme_cls.primary_color,
#                             ),
#                             MDFlatButton(
#                                 text="OK",
#                                 on_release=lambda *args: self.process_selected_items(input_dialog),
#                                 # theme_text_color="Custom",
#                                 # text_color=self.theme_cls.primary_color,
#                             )],
#                         )
#         input_dialog.open()

