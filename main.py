# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel

from FirstLayout import FirstLayout
from ClientLayout import ClientLayout
from ProdLayout import ProdLayout
from widgets import *


class Start(TabbedPanel):
    def __init__(self, **kwargs):
        super(Start, self).__init__(**kwargs)
        Clock.schedule_once(self.on_tab_width, 0.1)


class startApp(App):
    def build(self):
        return Start()


def main():
    startApp().run()


if __name__ == '__main__':
    main()
