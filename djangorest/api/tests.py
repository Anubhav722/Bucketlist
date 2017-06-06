# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bucketlist

from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

# Create your tests here.
class ModelTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(username="nerd")
		self.name = "Write world class code"
		self.bucketlist = Bucketlist(name=self.name, owner=user)

	def test_model_can_create_a_bucketlist(self):
		old_count = Bucketlist.objects.count()
		self.bucketlist.save()
		new_count = Bucketlist.objects.count()
		self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(username="nerd")

		self.Client = APIClient()
		self.bucketlist_data = {'name': 'Go to Ibiza', 'owner': user.id}

		self.response = self.client.post(
				reverse('create'),
				self.bucketlist_data,
				format='json')

	def test_api_can_create_a_bucketlist(self):
		self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

	def test_authorization_is_enforced(self):
		new_client = APIClient()
		res = new_client.get('/bucketlist/', kwargs={'pk':3}, format="json")
		self.assertEqual(res.status_code, status_code.HTTP_401_UNAUTHORIZED)

	def test_api_can_get_a_bucketlist(self):
		bucketlist = Bucketlist.objects.get(id=1)
		response = self.client.get(
				'/bucketlist/',
				kwargs ={'pk':bucketlist.id}, format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, bucketlist)

	def test_api_can_update_bucketlist(self):
		bucketlist = Bucketlist.objects.get()
		change_bucketlist = {'name': 'Something new'}
		res = self.client.put(
				reverse('details', kwargs={'pk': bucketlist.id}),
				change_bucketlist, format='json'
			)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		# change_bucketlist = {'name': 'Something new'}
		# res = self.client.put(
		# 		reverse('details', kwargs={'pk': bucketlist.id}),
		# 		change_bucketlist, format='json'
		# 	)
		# self.assertEqual(res.status_code, status_code.HTTP_200_OK)

	def test_api_can_delete_bucketlist(self):
		bucketlist = Bucketlist.objects.get()
		response = self.client.delete(
				reverse('details', kwargs={'pk': bucketlist.id}),
				format='json',
				follow=True)

		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)