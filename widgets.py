# -*- coding: utf-8 -*-
from kivy.factory import Factory
from kivy.clock import Clock

class LongpressLabel(Factory.ButtonBehavior, Factory.Label):
    __events__ = ('on_long_press', )

    long_press_time = Factory.NumericProperty(1)
    
    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')
        
    def on_long_press(self, *largs):
        pass

class ClicablAnchorLayout(Factory.ButtonBehavior, Factory.DragBehavior, Factory.AnchorLayout):
    __events__ = ('on_long_press', )

    long_press_time = Factory.NumericProperty(1)
    
    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')
        
    def on_long_press(self, *largs):
        pass
