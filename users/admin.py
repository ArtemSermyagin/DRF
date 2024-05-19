from django.contrib import admin
from users.models import (
    User,
    Payment,
    Subscription
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'date',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
