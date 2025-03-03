from django.test import TestCase
from django.urls import reverse
from .models import ItemModel, CategoryModel


class StoreViewsTestCase(TestCase):
    fixtures = ['fixtures/items.json',
                'fixtures/item_tags.json',
                'fixtures/categories.json']

    def test_view(self):
        response = self.client.get(reverse('store:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_catalog(self):
        response = self.client.get(reverse('store:catalog'))
        self.assertTemplateUsed(response, 'catalog.html')
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        category = CategoryModel.objects.get(slug='clothes')
        items = ItemModel.objects.all()
        response = self.client.get(reverse('store:categories_by', kwargs={'cat_slug': 'clothes'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cat_by.html')
        self.assertEqual(
            list(response.context['object_list']),
            list(items.filter(category=category))[:8]
        )
