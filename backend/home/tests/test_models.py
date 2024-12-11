from django.test import TestCase
from django.contrib.auth.models import User
from home.models import ItemRequest, Deal, Feedback

class ItemRequestModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Create a test item request
        self.item = ItemRequest.objects.create(
            user=self.user,
            title='Test Item',
            description='A description for test item.',
            condition='new',
            category='electronics'
        )
    
    def test_item_creation(self):
        # Test that an ItemRequest is created correctly.
        self.assertEqual(self.item.title, 'Test Item')
        self.assertEqual(self.item.description, 'A description for test item.')
        self.assertEqual(self.item.condition, 'new')
        self.assertEqual(self.item.category, 'electronics')
        self.assertTrue(self.item.active)
        self.assertEqual(str(self.item), 'Test Item')
    
    def test_item_str_method(self):
        # Test the __str__ method of ItemRequest.
        self.assertEqual(str(self.item), 'Test Item')


class DealModelTest(TestCase):
    def setUp(self):
        # Create users
        self.seller = User.objects.create_user(username='seller', password='password123')
        self.buyer = User.objects.create_user(username='buyer', password='password123')
        # Create an item
        self.item = ItemRequest.objects.create(
            user=self.seller,
            title='Deal Item',
            description='Item for deal.',
            condition='used',
            category='furniture'
        )
        # Create a deal
        self.deal = Deal.objects.create(
            item=self.item,
            buyer=self.buyer,
            seller=self.seller
        )
    
    def test_deal_creation(self):
        #Test that a Deal is created correctly.
        self.assertEqual(self.deal.item, self.item)
        self.assertEqual(self.deal.buyer, self.buyer)
        self.assertEqual(self.deal.seller, self.seller)
        self.assertEqual(str(self.deal), f"Deal on {self.item.title} between {self.buyer.username} and {self.seller.username}")


class FeedbackModelTest(TestCase):
    def setUp(self):
        # Create users
        self.reviewer = User.objects.create_user(username='reviewer', password='password123')
        self.reviewee = User.objects.create_user(username='reviewee', password='password123')
        # Create feedback
        self.feedback = Feedback.objects.create(
            reviewer=self.reviewer,
            reviewee=self.reviewee,
            comment='Great seller!',
            rating=5
        )
    
    def test_feedback_creation(self):
        #Test that a Feedback is created correctly.
        self.assertEqual(self.feedback.reviewer, self.reviewer)
        self.assertEqual(self.feedback.reviewee, self.reviewee)
        self.assertEqual(self.feedback.comment, 'Great seller!')
        self.assertEqual(self.feedback.rating, 5)
        expected_str = f"Feedback from {self.reviewer.username} to {self.reviewee.username}"
        self.assertEqual(str(self.feedback), expected_str)