from django.test import TestCase
from django.contrib.auth.models import User
from home.serializers import ItemRequestSerializer

class ItemRequestSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='serializeruser', password='password123')
        self.valid_data = {
            'user': self.user.id,
            'title': 'Serializer Test Item',
            'description': 'Description for serializer test.',
            'condition': 'used',
            'category': 'books'
        }
        self.invalid_data = {
            'user': self.user.id,
            'title': '',  # Title is required
            'description': 'Description with empty title.',
            'condition': 'invalid_condition',  # Invalid choice
            'category': 'books'
        }
    
    def test_valid_serializer(self):
        #Test serializer with valid data.
        serializer = ItemRequestSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        item = serializer.save()
        self.assertEqual(item.title, 'Serializer Test Item')
    
    def test_invalid_serializer(self):
        #Test serializer with invalid data.
        serializer = ItemRequestSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('condition', serializer.errors)
