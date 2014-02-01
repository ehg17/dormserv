from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from cal.models import Entry, Item, Order
from users.models import UserProfile
from forms import ItemForm
from django.utils import timezone
import datetime
from datetime import date, time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from twilio.rest import TwilioRestClient
import stripe
from random import randint

# Create your views here.

@login_required
def display_calendar(request):
	context = RequestContext(request)
	current_week = datetime.datetime.now().isocalendar()[1]+1
	workables = []

	for delivery in Entry.objects.all():
		if delivery.week_num() == current_week:
			workables.append(delivery)

	mon = []
	tue = []
	wed = []
	thurs = []
	fri = []
	sat = []
	sun = []
	m_date = ""
	t_date = ""
	w_date = ""
	th_date = ""
	f_date = ""
	s_date = ""
	su_date = ""

	current_user = request.user
	print current_user
	for delivery in workables:

		if delivery.week_day() == 1:
			mon.append(delivery)
			k = delivery.date.strftime("%m/%d")
			m_date = k
		if delivery.week_day() == 2:
			tue.append(delivery)
			k = delivery.date.strftime("%m/%d")
			t_date = k
		if delivery.week_day() == 3:
			wed.append(delivery)
			k = delivery.date.strftime("%m/%d")
			w_date = k
		if delivery.week_day() == 4:
			thurs.append(delivery)
			k = delivery.date.strftime("%m/%d")
			th_date = k		
		if delivery.week_day() == 5:
			fri.append(delivery)
			k = delivery.date.strftime("%m/%d")
			f_date = k		
		if delivery.week_day() == 6:
			sat.append(delivery)
			k = delivery.date.strftime("%m/%d")
			s_date = k		
		if delivery.week_day() == 7:
			sun.append(delivery)
			k = delivery.date.strftime("%m/%d")
			su_date = k	
	date_tuple = (m_date, t_date, w_date, th_date, f_date, s_date, su_date)
	return render_to_response(
            'calendar.html',
            {'mon': mon, 'tue': tue, 'wed': wed, 'thurs' : thurs, 'fri': fri, 'sat': sat, 'sun': sun, 'current_user':current_user, 'date_tuple':date_tuple},
            context)


@login_required
def detail(request, entry_id):
	context = RequestContext(request)
	entry = get_object_or_404(Entry, pk=entry_id)
	current_entry = Entry.objects.get(id=entry_id)
	current_user = request.user
	if request.method == 'POST': 
  		items=request.POST.getlist('item_list')
  		purchase_price = 0.0
  		items_to_verify = []
 		this_user = UserProfile.objects.get(id=1)
  		#create the order instance
  		for i in items:
  			k = Item.objects.get(id=i)
  			items_to_verify.append(k)
  			purchase_price = purchase_price + k.item_price
  			

  		ptp = str(purchase_price*100+250)[:-2]
  		price_to_pass = ptp[:-2]+"."+ptp[-2:]
  		stripe_format_str_price = ptp[:-2]+ptp[-2:]

  		order = Order(user=this_user, total_price=purchase_price)
  		order.save()
  		print str(order.total_price)
		return render_to_response('confirm.html', {'price_to_pass': price_to_pass, 'items_to_verify':items_to_verify, 'current_user':current_user, 'this_user':this_user, 'current_entry':current_entry, 'order': order, 'stripe_format_str_price':stripe_format_str_price}, context)

	eggs = []
	coffee = []
	oats = []
	bakery = []
	fruit = []
	yogurt = []

	item_list = []
	for item in Item.objects.all():
		item_list.append(item)
		if item.item_category == "EGG":
			eggs.append(item)
		if item.item_category == "COF":
			coffee.append(item)
		if item.item_category == "FRU":
			fruit.append(item)
		if item.item_category == "BAK":
			bakery.append(item)
		if item.item_category == "OAT":
			oats.append(item)
		if item.item_category == "YOG":
			yogurt.append(item)

	if current_entry.deliveries_avail == 0:
		return HttpResponse("No more deliveries avail at this time!")

	return render_to_response(
		'menu.html', 
		{'item_list':item_list, 'current_user':current_user, 'current_entry':current_entry, 'eggs':eggs, 'coffee':coffee, 'oats':oats, 'bakery':bakery, 'fruit':fruit, 'yogurt':yogurt,}, 
		context)

@login_required
def profile(request):
	context = RequestContext(request)
	current_user = request.user
	return render_to_response('profile.html', {'current_user':current_user,}, context)

@login_required
def validate_purchase(request, entry_id):
	context = RequestContext(request)
	current_entry = Entry.objects.get(id=entry_id)
	current_user = request.user
	if current_entry.deliveries_avail == 0:
		return HttpResponse("No more deliveries avail at this time!")
	'''
	# Set your secret key: remember to change this to your live secret key in production
	# See your keys here https://manage.stripe.com/account
	stripe.api_key = "sk_test_4qn67c9y4axf9qYUKtg8JSa9"

	# Get the credit card details submitted by the form
	token = request.POST.get('stripeToken')

	# Create the charge on Stripe's servers - this will charge the user's card
	try:
	  charge = stripe.Charge.create(
	      amount=1000, # amount in cents, again
	      currency="usd",
	      card=token,
	      description="payinguser@example.com"
	  )
	except stripe.CardError, e:
	  # The card has been declined
	  pass
	'''
	#print current_entry.deliveries_avail
	current_entry.decrease_deliveries_avail()
	current_entry.save()
	#print current_entry.deliveries_avail
	this_user = UserProfile.objects.get(id=(current_user.id-1))
	account_sid = "ACd2d6a002416aad11df6d7b3d529506b2"
	auth_token = "616085bee1e2c14db70339a86bfa9dda"
	client = TwilioRestClient(account_sid, auth_token)
	message = client.sms.messages.create(body=this_user.user.first_name + ", thanks for your order to be delivered at " + current_entry.display_time() + " from Dormserv!", to= this_user.phone, from_="+19146185355") # Replace with your Twilio number
	#print message.sid

	list_of_greetings = ["It's that easy.", "All done.", "Thanks for your order.", "Isn't this the best?", "That's breakfast done right.", "Isn't this the best thing since the C-1 Express?"]
	greeting_to_return = ""
	r = randint(0,len(list_of_greetings)-1)
	for n in range(len(list_of_greetings)):
		if r == n:
			greeting_to_return = list_of_greetings[n]

	return render_to_response(
		'thanks.html', 
		{'greeting_to_return':greeting_to_return, 'current_user':current_user}, 
		context)
