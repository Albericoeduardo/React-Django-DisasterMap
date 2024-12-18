from django.test import TestCase
from ..models import Category, Event

class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(id="wildfires", name="Wildfires")
        self.event = Event.objects.create(
            id="EONET_111",
            title="Wildfire in TestCase 111",
            description="",
            date="2024-12-13T10:03:00Z",
            location="[-10.332798, -48.305152]",
            country="Brazil",
            link="",
            category=self.category
        )

    def test_category_str(self):
        self.assertEqual(str(self.category.name), "Wildfires")

    def test_event_str(self):
        self.assertEqual(str(self.event.title), "Wildfire in TestCase 111")

    def test_event_category_relationship(self):
        self.assertEqual(self.event.category, self.category)
        self.assertIn(self.event, self.category.events.all())