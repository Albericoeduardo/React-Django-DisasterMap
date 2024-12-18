from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from api.models import Event, Category
from api.serializers import EventSerializer, CategorySerializer

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(id='wildfires', name='Wildfires')
        self.category2 = Category.objects.create(id='severeStorms', name='Severe Storms')
        self.event = Event.objects.create(
            id='EONET_111',
            title='Wildfire in TestCase 111',
            description='',
            date='2024-12-13T10:03:00Z',
            location="[-10.332798, -48.305152]",
            country="Brazil",
            link="",
            category=self.category
        )
        self.event2 = Event.objects.create(
            id='EONET_112',
            title='Wildfire in TestCase 112',
            description='',
            date='2024-12-14T11:03:00Z',
            location="[-11.332798, -49.305152]",
            country="Brazil",
            link="",
            category=self.category
        )
        self.event3 = Event.objects.create(
            id='EONET_113',
            title='Severe Storms in TestCase 113',
            description='',
            date='2024-12-15T12:03:00Z',
            location="[-12.332798, -50.305152]",
            country="Uruguay",
            link="",
            category=self.category2
        )

    def test_get_events(self):
        response = self.client.get(reverse('get_events'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_categories(self):
        response = self.client.get(reverse('get_categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_events_by_id(self):
        response = self.client.get(reverse('get_events_by_id', kwargs={'event_id': 'EONET_111'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event = Event.objects.filter(id='EONET_111')
        serializer = EventSerializer(event, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_events_by_country(self):
        response = self.client.get(reverse('get_events') + '?country=Brazil')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = Event.objects.filter(country='Brazil')
        serializedEvents = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializedEvents.data)

    def test_filter_events_by_category(self):
        response = self.client.get(reverse('get_events') + '?category=wildfires')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = Event.objects.filter(category='wildfires')
        serializedEvents = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializedEvents.data)

    def test_filter_events_by_start_date(self):
        response = self.client.get(reverse('get_events') + '?start_date=2024-12-14')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events= Event.objects.filter(date__gte='2024-12-14')
        serializedEvents = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializedEvents.data)

    def test_filter_events_by_date_period(self):
        response = self.client.get(reverse('get_events') + '?start_date=2024-12-13&end_date=2024-12-14')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = Event.objects.filter(date__gte='2024-12-13', date__lte='2024-12-14')
        serializedEvents= EventSerializer(events, many=True)
        self.assertEqual(response.data, serializedEvents.data)


# python manage.py test api.tests.test_views