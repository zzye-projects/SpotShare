
from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse

from spot_share.models import Address
from django.contrib.auth.models import User, Group
from spot_share.serializers import AddressSerializer


class AddressTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = User.objects.create_superuser(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        cls.staff_user1 = User.objects.create_user(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        cls.staff_user2 = User.objects.create_user(
            username='StaffUser2', 
            password='StaffUser2@123!'
        )
        cls.customer_user = User.objects.create_user(
            username='CustomerUser2', 
            password='CustomerUser2@123!'
        )
        group, created = Group.objects.get_or_create(name='Staff')
        cls.staff_user1.groups.add(group)
        cls.staff_user2.groups.add(group)

        cls.address1 = Address.objects.create(
            street = 'street1',
            street_no = 1, 
            city = 'city1',
            state = 'state1',
            postal_code = 'postal_code1',
            country = 'country1'
        )
        cls.address1.add_user(cls.staff_user1)

        cls.address2 = Address.objects.create(
            street = 'street2',
            street_no = 2, 
            city = 'city2',
            state = 'state2',
            postal_code = 'postal_code2',
            country = 'country2',
        )

        cls.address3_payload = {
            'street': 'street3',
            'street_no': 3, 
            'city': 'city3',
            'state': 'state3',
            'postal_code': 'postal_code3',
            'country': 'country3',
        }
    
    def test_list_addresses(self):
        serializer = AddressSerializer(Address.objects.all(), many=True)
        response = self.client.get(reverse('address-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_details_address(self):
        serializer = AddressSerializer(self.address1)
        response = self.client.get(reverse('address-detail', kwargs={'pk': self.address1.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
    
    def test_post_address(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.post(
            reverse('address-list'), 
            data=self.address3_payload, 
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        address3 = Address.objects.filter(postal_code='postal_code3').first()
        self.assertEqual(address3.street, 'street3')
        self.assertEqual(address3.street_no, 3)
        self.assertEqual(address3.city, 'city3')
        self.assertEqual(address3.state, 'state3')
        self.assertEqual(address3.country, 'country3')

    def test_fail_auth_post_address(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.post(
            reverse('address-list'), 
            data=self.address3_payload, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_add_user_to_address(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.post(
            reverse('add-user-to-address', kwargs={'pk': self.address2.pk}), 
            data={
                'users': [self.staff_user1.pk, self.staff_user2.pk]
            }, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.address2.users.all()), 2)
        self.assertTrue(self.address2.users.filter(pk=self.staff_user1.pk).exists())
        self.assertTrue(self.address2.users.filter(pk=self.staff_user2.pk).exists())

    # def test_fail_add_user_to_address(self):
    #     self.client.login(
    #         username='SuperUser', 
    #         password='SuperUser@123!'
    #     )
    #     response = self.client.post(
    #         reverse('add-user-to-address', kwargs={'pk': self.address2.pk}), 
    #         data={'users': [self.customer_user.pk]}, 
    #         format='json'
    #     )
    #     print(response)


    # def test_post_category(self):
    #     self.client.login(
    #         username='ManagerUser', 
    #         password='ManagerUser@123!'
    #     )
    #     payload = {
    #         'slug': 'category3',
    #         'title': 'Category3'
    #     }

    #     response = self.client.post(
    #         reverse('category-list'), 
    #         data=payload, 
    #         format='json'
    #     )
    #     category = get_object_or_404(Category, title='Category3')
        
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(category.slug, 'category3')
    #     self.assertEqual(category.title, 'Category3')
    #     self.assertEqual(len(Category.objects.all()), 3)

    # def test_filter_category(self):
    #     self.client.login(
    #         username='CustomerUser', 
    #         password='CustomerUser@123!'
    #     )

    #     serializer = CategorySerializer(self.category1)
    #     response = self.client.get(reverse('category-list'), {'title__icontains':'1'})
       
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data['results']), 1)
    #     self.assertEqual(response.data['results'][0], serializer.data)

    # def test_order_category(self):
    #     self.client.login(
    #         username='CustomerUser', 
    #         password='CustomerUser@123!'
    #     )
        
    #     serializer1 = CategorySerializer(self.category1)
    #     serializer2 = CategorySerializer(self.category2)

    #     response = self.client.get(reverse('category-list'), {'ordering':'-slug'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data['results'][0], serializer2.data)
    #     self.assertEqual(response.data['results'][1], serializer1.data)

    # def test_paginate_category(self):
    #     self.client.login(
    #         username='CustomerUser', 
    #         password='CustomerUser@123!'
    #     )

    #     serializer = CategorySerializer(self.category2)
    #     response = self.client.get(reverse('category-list'), {'page_size':'1', 'page': 2})
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data['results']), 1)
    #     self.assertEqual(response.data['results'][0], serializer.data)

    # def test_put_category(self):
    #     self.client.login(
    #         username='ManagerUser', 
    #         password='ManagerUser@123!'
    #     )
    #     payload = {
    #         'slug' : 'category11',
    #         'title' : 'Category11'
    #     }
    #     response = self.client.put(
    #         reverse('category-detail',
    #         kwargs={'pk': self.category1.pk}), 
    #         data=payload, format='json'
    #     )
    #     category = get_object_or_404(Category, pk=self.category1.pk)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(category.title, 'Category11')
    #     self.assertEqual(category.slug, 'category11')
    #     self.assertEqual(len(Category.objects.all()), 2)

    # def test_patch_category(self):
    #     self.client.login(
    #         username='ManagerUser', 
    #         password='ManagerUser@123!'
    #     )
    #     payload = {
    #         'slug' : 'category11',
    #     }
    #     response = self.client.patch(
    #         reverse('category-detail',
    #         kwargs={'pk': self.category1.pk}), 
    #         data=payload, format='json'
    #     )
    #     category = get_object_or_404(Category, pk=self.category1.pk)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(category.title, 'Category1')
    #     self.assertEqual(category.slug, 'category11')
    #     self.assertEqual(len(Category.objects.all()), 2)

    # def test_delete_category(self):
    #     self.client.login(
    #         username='ManagerUser', 
    #         password='ManagerUser@123!'
    #     )
    #     response = self.client.delete(
    #         reverse('category-detail',
    #         kwargs={'pk': self.category1.pk})
    #     )
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(len(Category.objects.all()), 1)
    #     self.assertEqual(len(Category.objects.filter(pk=self.category1.pk)), 0)