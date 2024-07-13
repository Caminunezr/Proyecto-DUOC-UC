from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Elimina datos huérfanos de la base de datos'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Eliminar registros huérfanos en la tabla de mensajes de contacto
            cursor.execute("""
                DELETE FROM myappcafe_contactmessage
                WHERE user_id IS NOT NULL AND user_id NOT IN (SELECT id FROM auth_user)
            """)
            self.stdout.write(self.style.SUCCESS('Successfully deleted orphaned contact messages.'))

            # Eliminar registros huérfanos en la tabla de ventas
            cursor.execute("""
                DELETE FROM myappcafe_venta
                WHERE usuario_id IS NOT NULL AND usuario_id NOT IN (SELECT id FROM auth_user)
            """)
            self.stdout.write(self.style.SUCCESS('Successfully deleted orphaned sales records.'))

            # Eliminar registros huérfanos en la tabla de reservas
            cursor.execute("""
                DELETE FROM myappcafe_reserva
                WHERE usuario_id IS NOT NULL AND usuario_id NOT IN (SELECT id FROM auth_user)
            """)
            self.stdout.write(self.style.SUCCESS('Successfully deleted orphaned reservations.'))

            # Eliminar registros huérfanos en la tabla de boletas
            cursor.execute("""
                DELETE FROM myappcafe_boleta
                WHERE usuario_id IS NOT NULL AND usuario_id NOT IN (SELECT id FROM auth_user)
            """)
            self.stdout.write(self.style.SUCCESS('Successfully deleted orphaned invoices.'))