from http import HTTPStatus

from authapp.models import CustomUser

from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail as django_mail

from mainapp.models import News
from mainapp import tasks as mainapp_tasks


class TestMainPage(TestCase):
    def test_page_index_open(self):
        path = reverse("mainapp:main")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        path = reverse("mainapp:contacts")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):

    def setUp(self) -> None:
        for i in range(10):
            News.objects.create(
                title=f'News{i}',
                preamble=f'Pre{i}',
                body=f'Body{i}'
            )

        CustomUser.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'django', 'password': 'geekbrains'}
        )

    def test_open_page(self):
        path = reverse("mainapp:news")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self):
        news_obj = News.objects.first()

        path = reverse("mainapp:news_detail", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonim(self):
        path = reverse("mainapp:news_create")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_item_by_admin(self):

        news_count = News.objects.all().count()

        path = reverse("mainapp:news_create")
        self.client_with_auth.post(
            path,
            data={
                'title': 'Test news',
                'preamble': 'Test preamble',
                'body': 'Test body',
            }
        )
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(News.objects.all().count(), news_count + 1)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()

        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)


class TestTaskMailSend(TestCase):
    fixtures = ("authapp/fixtures/0001_user_admin.json",)

    def test_mail_send(self):
        message_text = "test_message_text"
        user_obj = CustomUser.objects.first()
        mainapp_tasks.send_feedback_mail(
            {"user_id": user_obj.id, "message": message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)



