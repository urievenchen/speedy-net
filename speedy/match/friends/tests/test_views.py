import unittest
from django.conf import settings as django_settings

from speedy.core.base.test.models import SiteTestCase
from speedy.core.base.test.decorators import only_on_speedy_match

if (django_settings.LOGIN_ENABLED):
    from speedy.core.friends.tests.test_views import UserFriendListViewTestCaseMixin


    @only_on_speedy_match
    class UserFriendListViewTestCase(UserFriendListViewTestCaseMixin, SiteTestCase):
        @unittest.skip
        def test_visitor_can_open_the_page(self):
            raise NotImplementedError()

        def test_visitor_cannot_open_the_page(self):
            self.client.logout()
            r = self.client.get(path=self.first_user_friends_list_url)
            self.assertEqual(first=r.status_code, second=404)


