from django.core.management.base import BaseCommand
from newapp.logic import process_qr_and_leaves

class Command(BaseCommand):
    help = "Process QR expiry and leave automation"

    def handle(self, *args, **kwargs):
        process_qr_and_leaves()
        self.stdout.write("Background processing done")
