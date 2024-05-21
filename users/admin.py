from django.contrib import admin

from users.models import Payment, User

admin.site.register(User)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "lesson", "payment_amount", "payment_method",)
