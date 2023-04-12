from django.contrib import admin
from django.http import HttpResponseRedirect

# from django.conf.urls import url

from .models import User, Item, Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user_id"]
    change_list_template = "admin/model_change_list.html"

    # def get_urls(self):
    #     urls = super(ModelAdmin, self).get_urls()
    #     custom_urls = [
    #         url('^import/$', self.process_import, name='process_import'), ]
    #     return custom_urls + urls
    #
    # def process_import_btmp(self, request):
    #     import_custom = ImportCustom()
    #     count = import_custom.import_data()
    #     self.message_user(request, f"создано {count} новых записей")
    #     return HttpResponseRedirect("../")


@admin.register(Item)
class UserAdmin(admin.ModelAdmin):
    list_display = ("item_id", "category", "subcategory", "photo_id", "description")
    list_editable = ("category", "subcategory", "photo_id", "description")
    # list_display_links = "item_id"


@admin.register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user_id", "item_id", "count")
    list_editable = ("user_id", "item_id", "count")
    # list_display_links = "order_id"
