# -*- coding: utf-8 -*-

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import json

from db import DataBase

db = DataBase()

norm_bg_color = (0.90,0.89,0.82,1)
row1_color_fl = (0.52,1,0.75, 1)
row2_color_fl = (0.82,1,0.75, 1)


class RemoveLabel(Label):
    pass


class ProdDataInput(GridLayout):
	save_button = ObjectProperty()
	name_input = ObjectProperty()


class ProdRowLayout(BoxLayout):
    pass


class ProdLayout(BoxLayout):
	scroll_layout = ObjectProperty()
	input_area = ObjectProperty()
	data_input = ObjectProperty()

	def __init__(self,**kwargs):
		super(ProdLayout, self).__init__(**kwargs)
		Clock.schedule_once(self.btn_bind, 0.5)


	def btn_bind(self, arg=None):
		self.data_input.save_button.bind(on_release=self.update_prod)
		self.data_input.new_button.bind(on_release=self.new_prod)

	def on_open_tab(self, arg=None):
		Clock.schedule_once(self.make_table, 0.5)

	def make_table(self, arg=None):
		self.inside_layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
		self.inside_layout.bind(minimum_height=self.inside_layout.setter('height'))
		self.scroll_layout.clear_widgets()
		self.scroll_layout.add_widget(self.inside_layout)
		self.data_input.del_button.data_layout = self.inside_layout
		self.data_input.del_button.bind(on_press = self.remove_rows)
		jj = 1
		rows = db.get_all_prods()
		for row in rows:
			if jj == 1:
				norm_bg_color = row1_color_fl
				jj = 2
			else:
				norm_bg_color = row2_color_fl
				jj = 1
			tmp_obj = ProdRowLayout()
			tmp_obj.bind(on_touch_down=self.select_row)
			tmp_obj.name_lbl.data = row
			tmp_obj.name_lbl.bind(on_release=self.fill_form)
			tmp_obj.norm_bg_color = norm_bg_color
			tmp_obj.prod_id = str(row[0])
			tmp_obj.prod_name = str(row[1])
			self.inside_layout.add_widget(tmp_obj)
			self.data_input.save_button.prod_id = 0

	def fill_form(self, arg):
		self.data_input.name_input.text = arg.data[1]
		self.data_input.save_button.prod_id = arg.data[0]


	def update_prod(self, arg=None):
		name = self.data_input.name_input.text
		prod_id = arg.prod_id
		if prod_id:
			db.update_prod(name=name, prod_id=prod_id)
		elif name != '':
			db.insert_new_prod(name)
		self.clear_form()
		self.make_table()

	def new_prod(self, arg):
		arg.prod_id = 0
		self.clear_form()

	def clear_form(self):
		self.data_input.name_input.text = ''
		self.data_input.new_button.prod_id = 0

	def select_row(self, arg=None, touch=None):
		if not (arg.collide_point(*touch.pos) and touch.is_double_tap):
			return
		if arg.is_selected == 1:
			arg.is_selected = 0
			arg.name_layout.remove_widget(arg.name_layout.children[0])
		elif arg.is_selected == 0:
			arg.is_selected = 1
			arg.name_layout.add_widget(RemoveLabel())
	
	def remove_rows(self, arg=None):
		rows_list = []
		for ii in arg.data_layout.children:
			if ii.is_selected:
				rows_list.append(ii.id_lbl.text)
				# arg.data_layout.remove_widget(ii)
		db.remove_prod(rows_list)
		self.make_table()