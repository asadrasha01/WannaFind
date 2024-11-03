from django.core.management.base import BaseCommand
from home.models import Message 
import json

class Command(BaseCommand):
    help = 'Fix messages with JSON-encoded content'

    def handle(self, *args, **kwargs):
        messages = Message.objects.all()
        fixed_count = 0
        
        for message in messages:
            try:
                decoded_content = json.loads(message.content)
                if isinstance(decoded_content, dict) and 'content' in decoded_content:
                    message.content = decoded_content['content']
                    message.save()
                    fixed_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Fixed message ID {message.id}'))
            except json.JSONDecodeError:
                continue
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} messages with JSON-encoded content'))