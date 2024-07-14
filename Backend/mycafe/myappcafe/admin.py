from django.contrib import admin
from .models import Producto, Ingrediente, Receta, Venta, Mesa, Reserva, CustomUser, Boleta, ContactMessage

# Registra tus modelos aquí
admin.site.register(Producto)
admin.site.register(Ingrediente)
admin.site.register(Receta)
admin.site.register(Venta)
admin.site.register(Mesa)
admin.site.register(Reserva)
admin.site.register(CustomUser)
admin.site.register(Boleta)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'email', 'message', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'email', 'message', 'user__username')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # if editing an existing object
            return self.readonly_fields + ('user', 'name', 'email', 'message', 'created_at')
        return self.readonly_fields