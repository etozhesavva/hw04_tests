from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

INDEX = reverse('posts:index')
NEW_POST = reverse('posts:create')
AUTHOR = reverse('about:author')
TECH = reverse('about:tech')
USERNAME = 'TestAuthor'
USERNAME2 = 'TestAuthor2'
AUTH_LOGIN = reverse('login')
SLUG = 'testgroup'
GROUP_URL = reverse('posts:group', kwargs={'slug': SLUG})
PROFILE_URL = reverse('posts:profile', kwargs={'username': USERNAME})

class UrlsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=USERNAME)
        cls.group = Group.objects.create(
            title='Test',
            slug=SLUG,
            description='Test'
        )
        cls.post = Post.objects.create(
            text='Test',
            author=cls.user,
            group=cls.group
        )
        cls.POST_URL = reverse(
            'posts:post_detail',
            args=[cls.post.id])
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit',
            args=[cls.post.id])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user2 = User.objects.create(username=USERNAME2)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)

    def test_urls_status_code(self):
        urls_names = [
            [self.POST_EDIT_URL, self.authorized_client2, 302],
            [INDEX, self.guest_client, 200],
            [NEW_POST, self.guest_client, 302],
            [GROUP_URL, self.guest_client, 200],
            [self.POST_URL, self.guest_client, 200],
            [PROFILE_URL, self.guest_client, 200],
            [AUTHOR, self.guest_client, 200],
            [TECH, self.guest_client, 200],
            [self.POST_EDIT_URL, self.guest_client, 302],
            [self.POST_EDIT_URL, self.authorized_client, 200],
            [NEW_POST, self.authorized_client, 200],
        ]
        for url, client, status in urls_names:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, status)

    def test_urls_uses_correct_template(self):
        template_urls_names = [
            ['posts/index.html', INDEX],
            ['posts/create_post.html', NEW_POST],
            ['posts/group_list.html', GROUP_URL],
            ['posts/post_detail.html', self.POST_URL],
            ['posts/profile.html', PROFILE_URL],
            ['about/author.html', AUTHOR],
            ['about/tech.html', TECH],
            ['posts/create_post.html', self.POST_EDIT_URL]
        ]
        for template, url in template_urls_names:
            with self.subTest(url=url):
                self.assertTemplateUsed(self.authorized_client.get(url),
                                        template)

    def test_redirect_urls_correct(self):
        urls = [
            [NEW_POST, self.guest_client, f'{AUTH_LOGIN}?next={NEW_POST}'],
            [self.POST_EDIT_URL, self.guest_client,
             f'{AUTH_LOGIN}?next={self.POST_EDIT_URL}'],
            [self.POST_EDIT_URL, self.authorized_client2, self.POST_URL],
        ]
        for url, client, redirect in urls:
            with self.subTest(url=url):
                self.assertRedirects(client.get(url, follow=True), redirect)
