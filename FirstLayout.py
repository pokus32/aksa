# -*- coding: utf-8 -*-
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from calendar_ui import DatePicker
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from db import DataBase
from datetime import datetime
from kivy.uix.dropdown import DropDown

db = DataBase()

norm_bg_color = (0.90,0.89,0.82,1)
row1_color_fl = (0.52,1,0.75, 1)
row2_color_fl = (0.82,1,0.75, 1)

class RemoveLabel(Label):
    pass


class MainRowLayout(BoxLayout):
    pass


class TextRowLayoutNew(BoxLayout):
    type_layout = ObjectProperty()


class TextRowLayoutHeader(BoxLayout):
    pass


class TextInputRowLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(TextInputRowLayout, self).__init__(**kwargs)
        self.date_i.text = datetime.now().strftime('%Y-%m-%d')
        self.date_i.self_date = datetime.now()

    def make_norm_date(self, arg=None):
        try:
            date = datetime.strptime(arg.text, '%d.%m.%Y')
        except:
            date = datetime.strptime(arg.text, '%Y-%m-%d')
        self.date_i.text = date.strftime('%Y-%m-%d')
        self.date_i.self_date = date

    def calc(self, arg):
        if self.price_tl.text == '':
            price = 0
        else:
            price = float(self.price_tl.text)
        if self.quantity_i.text == '':
            quantity = 0
        else:
            quantity = float(self.quantity_i.text)
        if self.payed_tl.text == '':
            payed = 0
        else:
            payed = float(self.payed_tl.text)
        total = price * quantity
        self.total_tl.text = str(total)
        balance = total - payed
        self.balance_tl.text = str(balance)

        if self.price_dl.text == '':
            price = 0
        else:
            price = float(self.price_dl.text)
        if self.quantity_i.text == '':
            quantity = 0
        else:
            quantity = float(self.quantity_i.text)
        if self.payed_dl.text == '':
            payed = 0
        else:
            payed = float(self.payed_dl.text)
        total = price * quantity
        self.total_dl.text = str(total)
        balance = total - payed
        self.balance_dl.text = str(balance)

        if self.price_eu.text == '':
            price = 0
        else:
            price = float(self.price_eu.text)
        if self.quantity_i.text == '':
            quantity = 0
        else:
            quantity = float(self.quantity_i.text)
        if self.payed_eu.text == '':
            payed = 0
        else:
            payed = float(self.payed_eu.text)
        total = price * quantity
        self.total_eu.text = str(total)
        balance = total - payed
        self.balance_eu.text = str(balance)


class PopupLayout(BoxLayout):
    delete_mode_button = ObjectProperty()


class FirstLayout(BoxLayout):
    scroll_layout = ObjectProperty()
    edit_mode = 0

    def __init__(self,**kwargs):
        super(FirstLayout, self).__init__(**kwargs)
        Clock.schedule_once(self.make_table, 1)

    def on_open_tab(self, arg=None):
        Clock.schedule_once(self.make_table, 0.5)

    def make_table(self, arg=None):
        self.inside_layout = GridLayout(cols=1, padding = 1, spacing=1, size_hint_y=None)
        self.inside_layout.bind(minimum_height=self.inside_layout.setter('height'),
            minimum_width=self.inside_layout.setter('width'))
        self.scroll_layout.clear_widgets()
        self.scroll_layout.add_widget(self.inside_layout)
        jj = 1
        rows = db.get_all()
        for row in rows:
            if jj == 1:
                norm_bg_color = row1_color_fl
                jj = 2
            else:
                norm_bg_color = row2_color_fl
                jj = 1
            box = MainRowLayout()
            # box.height = 41
            # box.balance_layout.remove_widget(box.label_layout)
            box.id_lbl.bind(on_release=self.open_popup)
            box.name_lbl.bind(on_release=self.open_popup)
            self.inside_layout.add_widget(box)
            box.norm_bg_color = norm_bg_color
            box.ids.id_lbl.text = str(row[0])
            box.ids.id_lbl.client_id = row[0]
            box.ids.name_lbl.client_id = row[0]
            box.ids.name_lbl.text = str(row[1])
            box.ids.balance_tl.text = '{:,.2f}₺'.format(row[2]) if row[2] else "" #'0.0₺'
            box.ids.balance_dl.text = '{:,.2f}$'.format(row[3]) if row[3] else "" #'0.0$'
            box.ids.balance_eu.text = '{:,.2f}€'.format(row[4]) if row[4] else "" #'0.0€'

    def insert_new_client(self, arg=None):
        db.insert_new_client(arg.name_lbl.text)
        self.make_table()

    def open_popup(self, arg=None, edit_mode=None):
        main_layout = PopupLayout()
        jj = 1
        rows = db.get_by_client_id(arg.client_id)
        client = ''
        header = TextRowLayoutHeader()
        main_layout.top_layout.add_widget(header)
        input_row = TextInputRowLayout()
        main_layout.bind(on_touch_down=self.close_dropdown)
        input_row.type_i.bind(on_touch_down=self.open_dropdown_prod)
        input_row.type_i.bind(text=self.close_dropdown)
        main_layout.close_button.link = input_row
        main_layout.top_layout.add_widget(input_row)
        blns_tl = 0
        blns_dl = 0
        blns_eu = 0
        for row in rows[::-1]:
            if row[15] == 0 and row[16] == 0 and row[17] == 0:
                continue
            # print(row[1])
            if row[1]:
                if jj == 1:
                    norm_bg_color = row1_color_fl
                    jj = 2
                else:
                    norm_bg_color = row2_color_fl
                    jj = 1
                box = TextRowLayoutNew()
                box.bind(on_touch_down=self.select_row)
                box.norm_bg_color = norm_bg_color
                box.ids.id_lbl.text = str(row[1])
                box.ids.date_lbl.text = str(row[3])
                box.ids.type_lbl.text = str(row[4])
                box.ids.quantity_lbl.text = str(row[5])

                box.price_tl.text = '{:,.2f}'.format(row[6])
                box.price_dl.text = '{:,.2f}'.format(row[7])
                box.price_eu.text = '{:,.2f}'.format(row[8])

                box.total_tl.text = '{:,.2f}'.format(row[9])
                box.total_dl.text = '{:,.2f}'.format(row[10])
                box.total_eu.text = '{:,.2f}'.format(row[11])

                box.payed_tl.text = '{:,.2f}'.format(row[12])
                box.payed_dl.text = '{:,.2f}'.format(row[13])
                box.payed_eu.text = '{:,.2f}'.format(row[14])

                box.balance_tl.text = '{:,.2f}'.format(row[15])
                box.balance_dl.text = '{:,.2f}'.format(row[16])
                box.balance_eu.text = '{:,.2f}'.format(row[17])

                box.client_id = row[1]
                blns_tl = '\n{:,.2f}₺'.format(row[15]) if row[15] else ""  # '0.0₺'
                blns_dl = '\n{:,.2f}$'.format(row[16]) if row[16] else ""  # '0.0$'
                blns_eu = '\n{:,.2f}€'.format(row[17]) if row[17] else ""  # '0.0€'

                main_layout.data_layout.add_widget(box)
        input_row.client_id = arg.client_id
        client = arg.client_name
        try:
            ttl = client + blns_tl + blns_dl + blns_eu
        except:
            ttl = client
        self.popup = Popup(title = ttl,
                      content = main_layout, 
                      size_hint =(None, None), size =(Window.width, Window.height),
                      title_color = [1,0,0,1], title_size = "17dp")
        main_layout.close_button.bind(on_release = self.close_popup)
        main_layout.escape_button.bind(on_press = self.escape_popup)
        main_layout.delete_mode_button.bind(on_press = self.remove_rows)
        main_layout.delete_mode_button.data_layout = main_layout.data_layout
        self.popup.open()

    def close_popup(self, arg=None):
        data = []
        data.append(arg.link.client_id)
        data.append('"' + arg.link.ids.date_i.text + '"')
        data.append('"' + arg.link.ids.type_i.text + '"')
        data.append(arg.link.ids.quantity_i.text)

        data.append('0.0' if arg.link.ids.price_tl.text == '' else arg.link.ids.price_tl.text)
        data.append('0.0' if arg.link.ids.price_dl.text == '' else arg.link.ids.price_dl.text)
        data.append('0.0' if arg.link.ids.price_eu.text == '' else arg.link.ids.price_eu.text)

        data.append(arg.link.ids.total_tl.text)
        data.append(arg.link.ids.total_dl.text)
        data.append(arg.link.ids.total_eu.text)

        data.append('0.0' if arg.link.ids.payed_tl.text == '' else arg.link.ids.payed_tl.text)
        data.append('0.0' if arg.link.ids.payed_dl.text == '' else arg.link.ids.payed_dl.text)
        data.append('0.0' if arg.link.ids.payed_eu.text == '' else arg.link.ids.payed_eu.text)

        data.append(arg.link.ids.balance_tl.text)
        data.append(arg.link.ids.balance_dl.text)
        data.append(arg.link.ids.balance_eu.text)
        if arg.link.ids.balance_tl.text != '0' or\
            arg.link.ids.balance_dl.text != '0' or\
            arg.link.ids.balance_eu.text != '0' and\
            arg.link.ids.date_i.text and\
            arg.link.ids.type_i.text != '':
            db.insert_data(data)
        self.escape_popup()

    def close_dropdown(self, arg=None, arg2=None):
        if hasattr(self, 'dropdown_prod'):
            self.dropdown_prod.dismiss()

    def escape_popup(self, arg=None, arg2=None):
        self.close_dropdown()
        self.popup.dismiss()
        self.make_table()

    def select_row(self, arg=None, touch=None):
        if not (arg.collide_point(*touch.pos) and touch.is_double_tap):
            return
        if arg.is_selected == 1:
            arg.is_selected = 0
            arg.type_layout.remove_widget(arg.type_layout.children[0])
        elif arg.is_selected == 0:
            arg.is_selected = 1
            arg.type_layout.add_widget(RemoveLabel())

    def remove_rows(self, arg=None):
        rows_list = []
        for ii in arg.data_layout.children:
            if ii.is_selected:
                rows_list.append(ii.id_lbl.text)
        db.remove_rows(rows_list)
        self.escape_popup()

    def open_dropdown_prod(self, arg=None, touch=None):
        self.close_dropdown()
        if not arg.collide_point(*touch.pos):
            return
        self.dropdown_prod = dropdown_prod = DropDown()
        dropdown_prod.auto_dismiss = False

        def on_sel(one, button):
            arg.text = button.text
            one.dismiss()

        prods = db.get_all_prods()
        for item in prods:
            btn = Button(text = str(item[1]),
                size_hint_y = None, height = 35,  
                background_color=(0.45, 0.24, 0.12, 1))
            btn.company_data = item
            btn.bind(on_release = lambda btn: dropdown_prod.select(btn))
            dropdown_prod.add_widget(btn)
        dropdown_prod.bind(on_select = on_sel)
        dropdown_prod.open(arg)