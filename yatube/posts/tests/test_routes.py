from django.test import TestCase
from django.urls import reverse


SLUG = 'testgroup'
USERNAME = 'TestAuthor'
POST_ID = 1


class ReverseTests(TestCase):
    urls_names = [
    [
                '/',
                reverse('posts:index')
            ],
            [
                '/create/',
                reverse('posts:create')
            ],
            [
                f'/group/{SLUG}/',
                reverse('posts:group', args=[SLUG])
            ],
            [
                f'/profile/{USERNAME}/',
                reverse('posts:profile', args=[USERNAME])
            ],
            [
                f'/posts/{POST_ID}/',
                reverse('posts:post_detail', args=[POST_ID])
            ],
            [
                f'/posts/{POST_ID}/edit/',
                reverse('posts:post_edit',
                        args=[POST_ID])
            ]
    ]

    def test_url_uses_correct_reverse(self):
        for direct_url, reversed_url in self.urls_names:
            self.assertEqual(direct_url, reversed_url)
