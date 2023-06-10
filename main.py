from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.snackbar import BaseSnackbar
import random
from kivy.config import Config
from kivymd.color_definitions import colors
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader

# CustomSnackbar
class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")
    md_bg_color = 255 , 0 , 12
# Beginning to define the size of the application
Window.size = (dp(400), dp(600))
# application body
class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.primary_hue = "800"
        self.title = "Mental Concept"
        kv = Builder.load_file("kivy.kv")
        return kv
    # Start Screen
    def on_start(self):
        Clock.schedule_once(lambda dt: self.change_screen_splash(), 6)
    def change_screen_splash(self):
        app = App.get_running_app()
        app.root.current = "Secondwindow"
        sound = SoundLoader.load('sound/startscreen.mp3')
        if sound:
            sound.play()
    def home_screen(self):
        app = App.get_running_app()
        app.root.current = "Secondwindow"
    #Start counting
    def start_counting(self):
        if self.counter_tow >= 2 and self.counter_one >= 0.5:
            sound = SoundLoader.load('sound/startcount.wav')
            if sound:
                sound.play()
            app = App.get_running_app()
            app.root.current = "start_count"
            self.root.ids.number_label.text = "0"
            Clock.schedule_once(lambda dt: self.count_numbers(), 1)
        else:
            Clock.schedule_once(lambda dt: self.show_warning())
    # Settings Counting
    def count_numbers(self):
        self.numbers = []
        self.sum2 = 0
        self.sum3 = 1
        for i in range(self.counter_tow + 1):
            self.sum3 += 1
            self.num = random.randint(-10, 10)
            self.numbers.append(self.num)
            Clock.schedule_once(lambda dt, num=self.num: self.update_number(num), self.counter_one * i)
            if i >= self.counter_tow :
                Clock.schedule_once(lambda dt: self.change_screen(), self.counter_one * (i+1))
        for num in self.numbers:
            self.sum2 += num
            self.number_o = str(self.numbers).replace(",", " + ").replace("[", "").replace("]", " = ")
            print(self.sum2)
    #update Number $ Checksum
    def check_sum(self, dt, sum):
        self.root.ids.number_label.text = f"{sum}"
    def update_number(self, num,):
        self.root.ids.number_label.text = f"{num}"
    # Answer Writing
    def change_screen(self):
        app = App.get_running_app()
        app.root.current = "user_input"
        self.root.ids.result.text = ""
        self.numbers.clear()
    # =====================================================================
    #                               application buttons
    # =====================================================================
    # Button 1
    counter_one = NumericProperty(0)
    def increment_counter_one(self):
        self.counter_one += 0.5
        self.update_counter_label_one()
    def decrement_counter_one(self):
        if self.counter_one >=1:
            self.counter_one -= 0.5
        else:
            exit
        self.update_counter_label_one()
    def update_counter_label_one(self):
        self.root.ids.counter_label_one.text = str(self.counter_one)

    # Button 2
    counter_tow = NumericProperty(0)
    def increment_counter_tow(self):
        self.counter_tow += 1
        self.update_counter_label_tow()
    def decrement_counter_tow(self):
        if self.counter_tow >=1:
            self.counter_tow -= 1
        else:
            exit
        self.update_counter_label_tow()
    def update_counter_label_tow(self):
        self.root.ids.counter_label_tow.text = str(self.counter_tow)

    #Button 3
    counter_three = NumericProperty(0)
    def increment_counter_three(self):
        self.counter_three += 1
        self.update_counter_label_three()
    def decrement_counter_three(self):
        if self.counter_three >=1:
            self.counter_three -= 1
        else:
            exit
        self.update_counter_label_three()
    def update_counter_label_three(self):
        self.root.ids.counter_label_three.text = str(self.counter_three)

    # Score
    score = NumericProperty(0)

    # progressbar
    progressbar = NumericProperty(0)

# Check answer
    def result_number(self):
        self.number = int(self.root.ids.result.text)
        self.o_number = int(self.sum2)

        if self.number == self.o_number:
            if self.counter_tow >= 5:
                self.progressbar += 4
                self.score += 4
                self.root.ids.score_lable.text = f"{self.score}"
                self.root.ids.progressbar.value = self.progressbar
                self.root.ids.slogan.text = "Keep going"
            else:
                self.progressbar += 2
                self.score += 2
                self.root.ids.score_lable.text = f"{self.score}"
                self.root.ids.progressbar.value = self.progressbar
                self.root.ids.slogan.text = "Keep going"
            if self.progressbar and self.score >= 100 :
                sound = SoundLoader.load('sound/extrabonus.wav')
                if sound:
                    sound.play()
                app = App.get_running_app()
                app.root.current = "score_window"
                self.root.ids.progressbar.value = 1
                self.root.ids.score_lable.text = f"{self.score}"
                self.root.ids.lable_score.text = f"Score is {self.score}"
            else:
                sound = SoundLoader.load('sound/success.mp3')
                if sound:
                    sound.play()
                app = App.get_running_app()
                app.root.current = "happy_window"
        else:
            sound = SoundLoader.load('sound/los.wav')
            if sound:
                sound.play()
            app = App.get_running_app()
            app.root.current = "sad"
            self.root.ids.correct_answer.text = f"The correct answer is [{self.o_number}] !"
            self.root.ids.correct_answer_information.text = f"result = [{self.o_number}]"
            self.root.ids.correct_answer_label.text = f"{(self.number_o)}"
# Warning Message
    def show_warning(self):
        snackbar = CustomSnackbar(
            text="Please Enter Flash Timeing & Number Of Digits!",
            font_size=13,
            icon="information",
            snackbar_x="10dp",
            snackbar_y="8dp",
            radius = [25, 25, 10, 5],
            shadow_color="#F45050",
            shadow_softness= 0,
        )
        snackbar.size_hint_x = (
            Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width
        snackbar.open()

App().run()