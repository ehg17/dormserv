from django.contrib import admin
from cal.models import Entry, Item, Order

class EntryAdmin(admin.ModelAdmin):
	list_display = ('start_time', 'date','deliveries_avail', 'demand_counter', 'is_active', 'week_num', 'week_day',)

class ItemAdmin(admin.ModelAdmin):
	list_display = ('item_name', 'item_price', 'item_category')

class OrderInline(admin.StackedInline):
    model = Order

class OrderAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'time', 'total_price')

admin.site.register(Entry, EntryAdmin)

admin.site.register(Item, ItemAdmin)

admin.site.register(Order, OrderAdmin)
