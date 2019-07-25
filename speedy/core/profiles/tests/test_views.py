from datetime import date

from django.conf import settings as django_settings
from django.test import override_settings
from django.test.client import RequestFactory
from django.views import generic
from friendship.models import Friend

if (django_settings.LOGIN_ENABLED):
    from speedy.core.base.test import tests_settings
    from speedy.core.base.test.models import SiteTestCase
    from speedy.core.base.test.decorators import only_on_sites_with_login
    from speedy.core.accounts.models import UserAccessField, User
    from speedy.core.accounts.tests.test_views import RedirectMeMixin
    from speedy.core.profiles.views import UserMixin

    from speedy.core.accounts.test.user_factories import ActiveUserFactory


    class UserMixinTestView(UserMixin, generic.View):
        def get(self, request, *args, **kwargs):
            return self


    class UserMixinTextCaseMixin(object):
        def set_up(self):
            super().set_up()
            self.factory = RequestFactory()
            self.user = ActiveUserFactory(slug='look-at-me', username='lookatme')
            self.other_user = ActiveUserFactory()

        def test_find_user_by_exact_slug(self):
            view = UserMixinTestView.as_view()(self.factory.get('/look-at-me/some-page/'), slug='look-at-me')
            self.assertEqual(first=view.get_user().id, second=self.user.id)


    @only_on_sites_with_login
    class LoggedInUserTestCase(RedirectMeMixin, SiteTestCase):
        def set_up(self):
            super().set_up()
            self.factory = RequestFactory()
            self.user = ActiveUserFactory(slug='look-at-me', username='lookatme')
            self.other_user = ActiveUserFactory()

        def test_redirect_to_login_me(self):
            self.assert_me_url_redirects_to_login_url()

        def test_redirect_to_login_me_add_trailing_slash(self):
            r = self.client.get(path='/me')
            self.assertRedirects(response=r, expected_url='/me/', status_code=301, target_status_code=302)
            self.assert_me_url_redirects_to_login_url()

        # ~~~~ TODO: login and test /me/ and user profiles while logged in.


    class UserDetailViewTestCaseMixin(object):
        def set_up(self):
            super().set_up()
            self.user = ActiveUserFactory(first_name_en="Corrin", last_name_en="Gideon", slug="corrin-gideon", date_of_birth=date(year=1992, month=9, day=12), gender=User.GENDER_FEMALE)
            self.user.first_name_he = "קורין"
            self.user.last_name_he = "גדעון"
            self.user.save()
            self.user_profile_url = '/{}/'.format(self.user.slug)
            self.other_user = ActiveUserFactory()

        def test_user_profile_not_logged_in(self):
            r = self.client.get(path=self.user_profile_url)
            if (django_settings.SITE_ID == django_settings.SPEEDY_NET_SITE_ID):
                self.assertIn(member=self.full_name, container=r.content.decode())
                self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
                self.assertNotIn(member=self.birth_date, container=r.content.decode())
                self.assertNotIn(member=self.birth_year, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_year, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_date, container=r.content.decode())
            elif (django_settings.SITE_ID == django_settings.SPEEDY_MATCH_SITE_ID):
                expected_url = '/login/?next={}'.format(self.user_profile_url)
                self.assertRedirects(response=r, expected_url=expected_url, status_code=302, target_status_code=200)
            else:
                raise NotImplementedError()

        def test_user_own_profile_logged_in(self):
            self.client.login(username=self.user.slug, password=tests_settings.USER_PASSWORD)
            r = self.client.get(path=self.user_profile_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertIn(member=self.first_name, container=r.content.decode())
            if (django_settings.SITE_ID == django_settings.SPEEDY_NET_SITE_ID):
                self.assertIn(member=self.full_name, container=r.content.decode())
            elif (django_settings.SITE_ID == django_settings.SPEEDY_MATCH_SITE_ID):
                self.assertNotIn(member=self.full_name, container=r.content.decode())
            else:
                raise NotImplementedError()
            self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
            self.assertIn(member=self.birth_date, container=r.content.decode())
            self.assertNotIn(member=self.birth_year, container=r.content.decode())
            self.assertIn(member=self.user_birth_year, container=r.content.decode())
            self.assertIn(member=self.user_birth_date, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_year, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_date, container=r.content.decode())

        def test_user_profile_month_day_format_from_friend(self):
            # First, check if only the day and month are visible.
            self.user.access_dob_day_month = UserAccessField.ACCESS_FRIENDS
            self.user.save()
            Friend.objects.add_friend(from_user=self.user, to_user=self.other_user).accept()
            self.assertTrue(expr=Friend.objects.are_friends(user1=self.user, user2=self.other_user))
            self.client.login(username=self.other_user.slug, password=tests_settings.USER_PASSWORD)
            r = self.client.get(path=self.user_profile_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertIn(member=self.first_name, container=r.content.decode())
            if (django_settings.SITE_ID == django_settings.SPEEDY_NET_SITE_ID):
                self.assertIn(member=self.full_name, container=r.content.decode())
            elif (django_settings.SITE_ID == django_settings.SPEEDY_MATCH_SITE_ID):
                self.assertNotIn(member=self.full_name, container=r.content.decode())
            else:
                raise NotImplementedError()
            self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
            self.assertIn(member=self.birth_date, container=r.content.decode())
            self.assertNotIn(member=self.birth_year, container=r.content.decode())
            self.assertIn(member=self.user_birth_month_day, container=r.content.decode())
            self.assertNotIn(member=self.user_birth_year, container=r.content.decode())
            self.assertNotIn(member=self.user_birth_date, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_month_day, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_year, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_date, container=r.content.decode())
            # Then, check if all the birth date is visible.
            self.user.access_dob_year = UserAccessField.ACCESS_FRIENDS
            self.user.save()
            r = self.client.get(path=self.user_profile_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
            self.assertIn(member=self.birth_date, container=r.content.decode())
            self.assertNotIn(member=self.birth_year, container=r.content.decode())
            self.assertIn(member=self.user_birth_month_day, container=r.content.decode())
            self.assertIn(member=self.user_birth_year, container=r.content.decode())
            self.assertIn(member=self.user_birth_date, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_month_day, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_year, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_date, container=r.content.decode())
            # Then, check if only the year is visible.
            self.user.access_dob_day_month = UserAccessField.ACCESS_ME
            self.user.save()
            r = self.client.get(path=self.user_profile_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
            self.assertNotIn(member=self.birth_date, container=r.content.decode())
            self.assertIn(member=self.birth_year, container=r.content.decode())
            self.assertNotIn(member=self.user_birth_month_day, container=r.content.decode())
            self.assertIn(member=self.user_birth_year, container=r.content.decode())
            self.assertNotIn(member=self.user_birth_date, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_month_day, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_year, container=r.content.decode())
            self.assertNotIn(member=self.not_user_birth_date, container=r.content.decode())
            # Then logout and check that nothing from the date of birth is visible on Speedy Net.
            # On Speedy Match, the profile is not visible to visitors at all.
            self.client.logout()
            r = self.client.get(path=self.user_profile_url)
            if (django_settings.SITE_ID == django_settings.SPEEDY_NET_SITE_ID):
                self.assertEqual(first=r.status_code, second=200)
                self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
                self.assertNotIn(member=self.birth_date, container=r.content.decode())
                self.assertNotIn(member=self.birth_year, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_month_day, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_year, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_date, container=r.content.decode())
                self.assertNotIn(member=self.not_user_birth_month_day, container=r.content.decode())
                self.assertNotIn(member=self.not_user_birth_year, container=r.content.decode())
                self.assertNotIn(member=self.not_user_birth_date, container=r.content.decode())
                # And then, check if only the day and month are visible again.
                self.user.access_dob_day_month = UserAccessField.ACCESS_ANYONE
                self.user.save()
                r = self.client.get(path=self.user_profile_url)
                self.assertEqual(first=r.status_code, second=200)
                self.assertIn(member="<title>{}</title>".format(self.expected_title[self.site.id]), container=r.content.decode())
                self.assertIn(member=self.birth_date, container=r.content.decode())
                self.assertNotIn(member=self.birth_year, container=r.content.decode())
                self.assertIn(member=self.user_birth_month_day, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_year, container=r.content.decode())
                self.assertNotIn(member=self.user_birth_date, container=r.content.decode())
                self.assertNotIn(member=self.not_user_birth_month_day, container=r.content.decode())
                self.assertNotIn(member=self.not_user_birth_year, container=r.content.decode())
                self.assertNotIn(member=self.not_user_birth_date, container=r.content.decode())
            elif (django_settings.SITE_ID == django_settings.SPEEDY_MATCH_SITE_ID):
                self.assertRedirects(response=r, expected_url='/login/?next={}'.format(self.user_profile_url), status_code=302, target_status_code=200)
            else:
                raise NotImplementedError()


    @only_on_sites_with_login
    class UserDetailViewEnglishTestCase(UserDetailViewTestCaseMixin, SiteTestCase):
        def set_up(self):
            super().set_up()
            self.birth_date = "Birth Date"
            self.birth_year = "Birth Year"
            self.first_name = "Corrin"
            self.last_name = "Gideon"
            self.full_name = "Corrin Gideon"
            self.user_birth_date = "12 September 1992"
            self.user_birth_month_day = "12 September"
            self.user_birth_year = "1992"
            self.not_user_birth_date = "12 September 1990"
            self.not_user_birth_month_day = "21 September"
            self.not_user_birth_year = "1990"
            self.expected_title = {
                django_settings.SPEEDY_NET_SITE_ID: "Corrin Gideon / Speedy Net [alpha]",
                django_settings.SPEEDY_MATCH_SITE_ID: "Corrin / Speedy Match [alpha]",
            }

        def validate_all_values(self):
            super().validate_all_values()
            self.assertEqual(first=self.language_code, second='en')


    @only_on_sites_with_login
    @override_settings(LANGUAGE_CODE='he')
    class UserDetailViewHebrewTestCase(UserDetailViewTestCaseMixin, SiteTestCase):
        def set_up(self):
            super().set_up()
            self.birth_date = "תאריך לידה"
            self.birth_year = "שנת לידה"
            self.first_name = "קורין"
            self.last_name = "גדעון"
            self.full_name = "קורין גדעון"
            self.user_birth_date = "12 ספטמבר 1992"
            # self.user_birth_date = "12 בספטמבר 1992" # ~~~~ TODO: this is the correct string!
            self.user_birth_month_day = "12 ספטמבר"
            # self.user_birth_month_day = "12 בספטמבר" # ~~~~ TODO: this is the correct string!
            self.user_birth_year = "1992"
            self.not_user_birth_date = "12 ספטמבר 1990"
            # self.not_user_birth_date = "12 בספטמבר 1990" # ~~~~ TODO: this is the correct string!
            self.not_user_birth_month_day = "21 ספטמבר"
            # self.user_birth_month_day = "21 בספטמבר" # ~~~~ TODO: this is the correct string!
            self.not_user_birth_year = "1990"
            self.expected_title = {
                django_settings.SPEEDY_NET_SITE_ID: "קורין גדעון / ספידי נט [אלפא]",
                django_settings.SPEEDY_MATCH_SITE_ID: "קורין / ספידי מץ&#39; [אלפא]",
            }

        def validate_all_values(self):
            super().validate_all_values()
            self.assertEqual(first=self.language_code, second='he')


