import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from memories.models import Memory
from users.models import HindsightUser

class MemoriesViewTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('user1','user1@test.com', 'user1_pw')
        h_user1 = HindsightUser(user = user1)
        h_user1.save()
        user1.save()

        user2 = User.objects.create_user('user2','user2@test.com', 'user2_pw')
        h_user2 = HindsightUser(user = user2)
        h_user2.save()
        user2.save()

        memory1 = Memory(image = 'memories/test1.jpg', owner = h_user1,latitude = 0, longitude = 0)
        memory1.save()
                
        memory2 = Memory(image = 'memories/test2.jpg', owner = h_user2,latitude = 0.0003, longitude = 0.0004)

        memory2.save()
                
        memory3 = Memory(image = 'memories/test3.jpg', owner = h_user1,latitude = 5, longitude = 12)
        memory3.save()

    def test_near_view(self):
        self.client.login(username='user1', password='user1_pw')
        response = self.client.get(reverse('memories:view_near'), {'longitude':0,'latitude':0})
        memories = json.loads(response.content)['memories']
        self.assertEqual(memories[0]['image'], 'memories/test1.jpg')
        self.assertTrue(memories[0]['owned_by_user'])
        self.assertEqual(memories[0]['latitude'],0)
        self.assertEqual(memories[0]['longitude'],0)
        self.assertTrue(memories[0].has_key('created'))
        self.assertEqual(memories[1]['image'], 'memories/test2.jpg')
        self.assertFalse(memories[1]['owned_by_user'])
        self.assertEqual(memories[1]['latitude'],0.0003)
        self.assertEqual(memories[1]['longitude'],0.0004)
        self.assertTrue(memories[1].has_key('created'))
        

    def test_not_owned_specific_view(self):
        self.client.login(username='user1', password='user1_pw')
        response = self.client.get(reverse('memories:view_specific', args=(Memory.objects.all()[1].pk,)), {'longitude':0, 'latitude':0})
        memory = json.loads(response.content)['memory']
        self.assertEqual(memory['image'], 'memories/test2.jpg')
        self.assertFalse(memory['owned_by_user'])
        self.assertEqual(memory['latitude'],0.0003)
        self.assertEqual(memory['longitude'],0.0004)
        self.assertTrue(memory.has_key('created'))

    def test_owned_specific_view(self):
        self.client.login(username='user2', password='user2_pw')
        response = self.client.get(reverse('memories:view_specific', args=(Memory.objects.all()[1].pk,)), {'longitude':0, 'latitude':0})
        memory = json.loads(response.content)['memory']
        self.assertEqual(memory['image'], 'memories/test2.jpg')
        self.assertTrue(memory['owned_by_user'])
        self.assertEqual(memory['latitude'],0.0003)
        self.assertEqual(memory['longitude'],0.0004)
        self.assertTrue(memory.has_key('created'))

    def test_owned_view(self):
        self.client.login(username='user1', password='user1_pw')
        response = self.client.get(reverse('memories:view_owned'), {'longitude':0,'latitude':0})
        memories = json.loads(response.content)['memories']
        self.assertEqual(memories[0]['image'],'memories/test1.jpg')
        self.assertEqual(memories[0]['latitude'],0)
        self.assertEqual(memories[0]['longitude'],0)
        self.assertTrue(memories[0].has_key('created'))
        self.assertEqual(memories[1]['image'], 'memories/test3.jpg')
        self.assertEqual(memories[1]['latitude'],5)
        self.assertEqual(memories[1]['longitude'],12)
        self.assertTrue(memories[1].has_key('created'))

    def test_add_view(self):    
        self.client.login(username='user1', password='user1_pw')
        with open('test4.jpg') as fp:
            response = self.client.post(reverse('memories:add'), {'memory':fp, 'latitude': 0.05, 'longitude': 0.12,})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Memory.objects.all()[3].image.name, 'memories/test4.jpg')

    def test_unsuccessful_add_view(self):
        with open('test4.jpg') as fp:
            response = self.client.post(reverse('memories:add'), {'memory':fp, 'latitude': 0.05, 'longitude': 0.12,})
            self.assertEqual(response.status_code, 403)

    def test_successful_edit_view(self):
        self.client.login(username='user1', password='user1_pw')
        response = self.client.post(reverse('memories:edit', args=(Memory.objects.all()[0].pk,)), {'caption':"HERE IS CAPTION HELLO"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Memory.objects.all()[0].caption, "HERE IS CAPTION HELLO")
 
    def test_unsuccessful_edit_view(self):
        self.client.login(username='user2', password='user2_pw')
        response = self.client.post(reverse('memories:edit', args=(Memory.objects.all()[0].pk,)), {'caption':"HERE IS CAPTION HELLO"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Memory.objects.all()[1].caption, None)  
        
    def test_successful_delete_view(self):
        self.client.login(username='user1', password='user1_pw')
        count = len(Memory.objects.all())
        response = self.client.post(reverse('memories:delete', args=(Memory.objects.all()[0].pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Memory.objects.all()), count - 1)

    def test_unsuccessful_delete_view(self):
        self.client.login(username='user1', password='user1_pw')
        count = len(Memory.objects.all())
        response = self.client.post(reverse('memories:delete', args=(Memory.objects.all()[1].pk,)))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Memory.objects.all()), count)

