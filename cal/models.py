from django.db import models
from users.models import User, UserProfile
from django.contrib import admin
import datetime
from django.utils import timezone
from datetime import date, time, timedelta
from django.template import RequestContext


class Entry(models.Model):
	start_time = models.TimeField(auto_now=False)
	date = models.DateField(auto_now=False)
	deliveries_avail = models.IntegerField(default=2)
	demand_counter = models.IntegerField(default=0)

	def fifteen_over(self):
		d_ref = self.date.strftime("%Y:%m:%d")
		d_ref_spl = d_ref.split(":")
		t_ref = self.start_time.strftime("%I:%M")
		t_ref_spl = t_ref.split(":")
		dt = datetime.datetime(int(d_ref_spl[0]), int(d_ref_spl[1]), int(d_ref_spl[2]), int(t_ref_spl[0]), int(t_ref_spl[1]), 00)
		time_of_concern = dt + datetime.timedelta(minutes=15)
		t = time_of_concern.strftime("%I:%M")
		if t[0] == "0":
			return t[1:] + " am"
		return t + " am"

	def view_date(self):
		return self.date.strftime("%m/%d")

	def is_active(self):
		if self.deliveries_avail > 0:
			return True
		return False

	def week_day(self):
		iso = self.date.isocalendar()
		return iso[2]

	def display_time(self):
		t = self.start_time.strftime("%I:%M")
		if t[0] == "0":
			return t[1:] + " am"
		return t + " am"

	def week_num(self):
		iso = self.date.isocalendar()
		return iso[1]

	def __unicode__(self):
		return str(self.start_time) + " " + str(self.date)

	def increase_demand_counter(self):
		self.demand_counter = self.demand_counter + 1

	def decrease_deliveries_avail(self):
		self.deliveries_avail = self.deliveries_avail - 1

	
	#each order mapped to a certain array of food items

class Item(models.Model):
	EGGS = 'EGG'
	COFFEE = 'COF'
	FRUITS = 'FRU'
	OATS = 'OAT'
	YOGURT = 'YOG'
	BAKERY = 'BAK'
	ITEM_CATEGORIES = (
		(EGGS, 'EGG'),
		(COFFEE, 'COF'),
		(FRUITS, 'FRU'),
		(OATS, 'OAT'),
		(YOGURT, 'YOG'),
		(BAKERY, 'BAK'),
		)
	item_name = models.CharField(max_length = 80)
	item_price = models.FloatField(max_length = 5)
	item_description = models.TextField(max_length=200)
	item_category = models.CharField(max_length=3, choices=ITEM_CATEGORIES)
	wanted = models.BooleanField()

	def price_format_usd(self):
		str_price_raw = str(self.item_price)
		price_list = str_price_raw.split(".")
		dollars = price_list[0]
		cents = price_list[1]
		if len(cents) == 1:
			cents = cents + "0"
		return dollars + "." + cents


	def __unicode__(self):
		return self.item_name


class Order(models.Model):
	user = models.ForeignKey(UserProfile)
	time = models.TimeField(auto_now=True)
	date = models.DateField(auto_now=True)
	total_price = models.FloatField(max_length=30, default=0.0)

	def __unicode__(self):
		return self.id