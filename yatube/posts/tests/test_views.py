from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import PAGINATOR_CONST
from ..models import Post, Group, User

INDEX = reverse('posts:index')
SLUG = 'Testgroup'
GROUP = reverse('posts:group', kwargs={'slug': SLUG})
SLUG2 = 'Testgroup2'
GROUP2 = reverse('posts:group', kwargs={'slug': SLUG2})
USERNAME = 'User'
PROFILE = reverse('posts:profile', kwargs={'username': USERNAME})


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=USERNAME)
        cls.group = Group.objects.create(
            title='testt',
            slug=SLUG,
            description='testd',
        )
        cls.group_2 = Group.objects.create(
            title="testt2",
            slug=SLUG2,
            description="testd2",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group,
        )
        self.REVERSE_POST = reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        )

    def post_checking(self, post):
        self.assertEqual(post.pk, self.post.pk)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)

    def test_group_page_show_correct_context(self):
        response_group = self.authorized_client.get(GROUP)
        group_test = response_group.context.get('group')
        self.assertEqual(group_test, self.group)

    def test_show_correct_context(self):
        urls_names = [
            GROUP,
            INDEX,
            PROFILE,
        ]
        for value in urls_names:
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                self.assertEqual(Post.objects.count(), 1)
                self.assertEqual(self.post,
                                 response.context.get('page_obj')[0])

    def test_post_detail_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        post = response.context['post']
        self.post_checking(post)

    def test_post_not_in_group2(self):
        response_group = self.authorized_client.get(GROUP2)
        self.assertNotIn(self.post, response_group.context.get('page_obj'))

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(PROFILE)
        self.assertEqual(self.user, response.context.get('author'))


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='user')
        posts = [Post(author=cls.user,
                      text=str(i))
                 for i in range(PAGINATOR_CONST)]
        Post.objects.bulk_create(posts)

    def test_page_count_records(self):
        response = self.client.get(INDEX)
        self.assertEqual(
            len(response.context.get('page_obj').object_list), PAGINATOR_CONST
        )
