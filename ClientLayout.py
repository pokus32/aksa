# -*- coding: utf-8 -*-

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
import json

from db import DataBase

db = DataBase()

norm_bg_color = (0.90,0.89,0.82,1)
row1_color_fl = (0.52,1,0.75, 1)
row2_color_fl = (0.82,1,0.75, 1)


class ClientInputLayout(GridLayout):
    ok_button = ObjectProperty()
    client_name = ObjectProperty()
    contact1 = ObjectProperty()
    contact2 = ObjectProperty()
    contact3 = ObjectProperty()
    contact4 = ObjectProperty()
    contact5 = ObjectProperty()


class DataInput(GridLayout):
	save_button = ObjectProperty()
	name_input = ObjectProperty()
	province_input = ObjectProperty()
	district_input = ObjectProperty()
	locality_input = ObjectProperty()
	street_input = ObjectProperty()
	substreet_input = ObjectProperty()
	number_input = ObjectProperty()


class ClientRowLayout(BoxLayout):
    pass


class ClientLayout(BoxLayout):
	scroll_layout = ObjectProperty()
	input_area = ObjectProperty()
	data_input = ObjectProperty()

	def __init__(self,**kwargs):
		super(ClientLayout, self).__init__(**kwargs)
		# self.data_input.save_button.bind(on_release=self.insert_new_client)
		Clock.schedule_once(self.btn_bind, 0.5)

	def btn_bind(self, arg=None):
		self.data_input.save_button.bind(on_release=self.update_client)
		self.data_input.new_button.bind(on_release=self.new_client)

	def on_open_tab(self, arg=None):
		Clock.schedule_once(self.make_table, 0.5)

	def make_table(self, arg=None):
		self.inside_layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
		self.inside_layout.bind(minimum_height=self.inside_layout.setter('height'))##,
			# minimum_width=self.inside_layout.setter('width'))
		self.scroll_layout.clear_widgets()
		self.scroll_layout.add_widget(self.inside_layout)
		jj = 1
		rows = db.get_all_clients()
		for row in rows:
			# print(row)
			if jj == 1:
				norm_bg_color = row1_color_fl
				jj = 2
			else:
				norm_bg_color = row2_color_fl
				jj = 1
			tmp_obj = ClientRowLayout()
			tmp_obj.name_lbl.data = row
			tmp_obj.name_lbl.bind(on_release=self.fill_form)
			tmp_obj.norm_bg_color = norm_bg_color
			tmp_obj.client_id = str(row[0])
			tmp_obj.client_name = str(row[1])
			self.inside_layout.add_widget(tmp_obj)

	def fill_form(self, arg):
		adress = json.loads(arg.data[8])
		self.data_input.name_input.text = arg.data[1]
		self.data_input.save_button.client_id = arg.data[0]

		contact1 = json.loads(arg.data[2])
		self.data_input.client_name_input.text = contact1.get('client_name', '')
		self.data_input.client_surname_input.text = contact1.get('client_surname', '')
		self.data_input.client_phone_input.text = contact1.get('client_phone', '')

		self.data_input.province_input.text = adress.get('province', '')
		self.data_input.district_input.text = adress.get('district', '')
		self.data_input.locality_input.text = adress.get('locality', '')
		self.data_input.street_input.text = adress.get('street', '')
		self.data_input.substreet_input.text = adress.get('substreet', '')
		self.data_input.number_input.text = adress.get('number', '')


	def update_client(self, arg=None):
		name = self.data_input.name_input.text
		contact1 = {}
		contact1.update({'client_name': self.data_input.client_name_input.text})
		contact1.update({'client_surname': self.data_input.client_surname_input.text})
		contact1.update({'client_phone': self.data_input.client_phone_input.text})
		data = {}
		data.update({'province': self.data_input.province_input.text})
		data.update({'district': self.data_input.district_input.text})
		data.update({'locality': self.data_input.locality_input.text})
		data.update({'street': self.data_input.street_input.text})
		data.update({'substreet': self.data_input.substreet_input.text})
		data.update({'number': self.data_input.number_input.text})
		adress = json.dumps(data)
		contact1 = json.dumps(contact1)
		client_id = arg.client_id
		if client_id:
			db.update_client(name=name, client_id=client_id, adress=adress, contact1=contact1)
		elif name != '':
			db.insert_new_client(name, adress=adress, contact1=contact1)
		self.clear_form()
		self.make_table()

	def new_client(self, arg):
		self.data_input.save_button.client_id = 0
		self.clear_form()

	def clear_form(self):
		self.data_input.name_input.text = ''
		self.data_input.save_button.client_id = 0

		self.data_input.client_name_input.text = ''
		self.data_input.client_surname_input.text = ''
		self.data_input.client_phone_input.text = ''

		self.data_input.province_input.text = ''
		self.data_input.district_input.text = ''
		self.data_input.locality_input.text = ''
		self.data_input.street_input.text = ''
		self.data_input.substreet_input.text = ''
		self.data_input.number_input.text = ''