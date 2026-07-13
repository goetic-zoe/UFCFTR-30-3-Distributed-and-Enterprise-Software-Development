from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, CartItem

# TC-001: As a producer, I want to create an account so that I can list my products on the marketplace.
class ProducerRegistrationTestCase(TestCase):
    def test_producer_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'bristolvalleyfarm',
            'email': 'jane.smith@bristolvalleyfarm.com',
            'password1': 'securePassword123!',
            'password2': 'securePassword123!',
            'user_type': 'producer'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        user = User.objects.get(username='bristolvalleyfarm')
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.user_type, 'producer')

# TC-002: As a customer, I want to register for an account so that I can browse and purchase local products.
class CustomerRegistrationTestCase(TestCase):
    def test_customer_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'robertjohnson',
            'email': 'robert.johnson@email.com',
            'password1': 'securePassword123!',
            'password2': 'securePassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        user = User.objects.get(username='robertjohnson')
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.user_type, 'customer')

# TC-003: As a producer, I want to list a new product so that customers can find and purchase it.
class ProductListingTestCase(TestCase):
    def setUp(self):
        self.producer = User.objects.create_user(username='bristolvalleyfarm', password='securePassword123!', user_type='producer')
        self.client.login(username='bristolvalleyfarm', password='securePassword123!')

    def test_product_listing(self):
        response = self.client.post(reverse('add_product'), {
            'name': 'Organic Free Range Eggs',
            'description': 'Fresh organic eggs from free-range hens, collected daily',
            'price': 3.50,
            'availability_start': '2026-07-14',
            'availability_end': '2026-08-14',
            'type': 'dairy_eggs',
            'allergens': 'Contains eggs'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to product management
        product = Product.objects.get(name='Organic Free Range Eggs')
        self.assertIsNotNone(product)
        self.assertEqual(product.producer, self.producer)

# TC-004: As a customer, I want to browse products by category so that I can find specific items I need.
class BrowseProductsByCategoryTestCase(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='robertjohnson', password='securePassword123!')
        self.client.login(username='robertjohnson', password='securePassword13!')

        producer = User.objects.create_user(username='bristolvalleyfarm', password='securePassword123!', user_type='producer')
        Product.objects.create(name='Organic Carrots', description='Fresh organic carrots', price=2.00, availability_start='2026-07-14',
                               availability_end='2026-08-14', type='vegetables', producer=producer)
        Product.objects.create(name='Fresh Milk', description='Organic milk from local farm', price=1.50,
                               availability_start='2026-07-14', availability_end='2026-08-14', type='dairy_eggs',
                               producer=producer)

    def test_browse_by_category(self):
        response = self.client.get(reverse('product_list'), {'type': 'vegetables'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, 'Organic Carrots')

# TC-006: As a customer, I want to add products to my shopping cart so that I can purchase multiple items together.
class AddToCartTestCase(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='robertjohnson', password='securePassword123!')
        self.client.login(username='robertjohnson', password='securePassword123!')

        producer = User.objects.create_user(username='bristolvalleyfarm', password='securePassword123!', user_type='producer')
        self.product = Product.objects.create(name='Organic Carrots', description='Fresh organic carrots', price=2.00,
                                              availability_start='2026-07-14', availability_end='2026-08-14',
                                              type='vegetables', producer=producer)

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to cart
        cart_item = CartItem.objects.get(user=self.customer, product=self.product)
        self.assertIsNotNone(cart_item)

# TC-015: As a customer, I want to see allergen warnings clearly displayed so that I can avoid products that may harm me or my family.
class AllergenWarningTestCase(TestCase):
    def setUp(self):
        producer = User.objects.create_user(username='bristolvalleyfarm', password='securePassword123!', user_type='producer')
        self.product_with_allergens = Product.objects.create(name='Cheddar Cheese', description='Delicious cheddar cheese',
                                                             price=5.00, availability_start='2026-07-14',
                                                             availability_end='2026-08-14', type='dairy_eggs',
                                                             producer=producer, allergens='Contains: Milk')

        self.product_without_allergens = Product.objects.create(name='Fresh Apples', description='Fresh organic apples',
                                                                price=3.00, availability_start='2026-07-14',
                                                                availability_end='2026-08-14', type='fruit',
                                                                producer=producer)

    def test_allergen_warning(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        product_with_allergens = products.get(name='Cheddar Cheese')
        product_without_allergens = products.get(name='Fresh Apples')

        self.assertIn(product_with_allergens.allergens, str(response.content))
        self.assertNotIn('Contains:', product_without_allergens.description)