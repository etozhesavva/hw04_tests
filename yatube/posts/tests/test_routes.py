from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post, User

SLUG = 'testgroup'
USERNAME = 'TestAuthor'
POST_ID = 1


class ReverseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username=USERNAME)
        self.group = Group.objects.create(slug=SLUG)
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group,
        )
        self.urls_names = [
            [
                '/',
                reverse('posts:index')
            ],
            [
                '/create/',
                reverse('posts:create')
            ],
            [
                f'/group/{self.group.slug}/',
                reverse('posts:group', args=[self.group.slug])
            ],
            [
                f'/profile/{self.user.username}/',
                reverse('posts:profile', args=[self.user.username])
            ],
            [
                f'/posts/{self.post.id}/',
                reverse('posts:post_detail', args=[self.post.id])
            ],
            [
                f'/posts/{self.post.id}/edit/',
                reverse('posts:post_edit',
                        args=[self.post.id])
            ]
        ]

    def test_url_uses_correct_reverse(self):
        for direct_url, reversed_url in self.urls_names:
            self.assertEqual(direct_url, reversed_url)
