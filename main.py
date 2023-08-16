from kivymd.app import MDApp
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager  import ScreenManager,Screen, FadeTransition
from kivy.utils import get_color_from_hex

from screens.homepage import HomePage
from screens.welcomepage import WelcomePage
from screens.signpage import SignPage
from screens.loginpage import LoginPage
from screens.userdetailspage import UserDetailsPage
from screens.details import DetailsPage
from screens.components import Info

Window.size = (267,480)

class Date(MDApp):
    user_id = None


    def build(self):                
        self.theme_cls.primary_palette = "Teal"
        #self.theme_cls.theme_style = "Dark"        
        Builder.load_file('screens/welcomepage.kv')
        Builder.load_file('screens/homepage.kv')
        Builder.load_file('screens/signpage.kv')
        Builder.load_file('screens/loginpage.kv')
        Builder.load_file('screens/userdetailspage.kv')
        Builder.load_file('screens/details.kv')
        Builder.load_file('screens/components.kv')

        sm = ScreenManager()        
        sm.add_widget(DetailsPage(name='detailspage'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(SignPage(name='signpage'))
        # sm.add_widget(Info(name='info'))
        sm.add_widget(UserDetailsPage(name='userdetailspage'))                                        
        sm.add_widget(LoginPage(name='loginpage'))
        sm.add_widget(WelcomePage(name='welcomepage'))
        
    
        return sm
    
    def on_login_success(self, user_id):
        self.user_id = user_id  # Store the user ID in the user_id attribute
        self.root.current = 'userdetailspage'
         
Date().run()
























