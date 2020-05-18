import random
from time import sleep

from django.conf import settings as django_settings
from django.test import override_settings

if (django_settings.LOGIN_ENABLED):
    from speedy.core.base.test import tests_settings
    from speedy.core.base.test.models import SiteTestCase
    from speedy.core.base.test.decorators import only_on_speedy_match
    from speedy.core.accounts.test.user_factories import ActiveUserFactory
    from speedy.core.blocks.models import Block
    from speedy.core.accounts.models import User
    from speedy.match.likes.models import UserLike
    from speedy.match.likes.test.mixins import SpeedyMatchLikesLanguageMixin


    @only_on_speedy_match
    class LikeViewTestCase(SiteTestCase):
        def set_up(self):
            super().set_up()
            self.user_1 = ActiveUserFactory()
            self.user_2 = ActiveUserFactory()
            self.page_url = '/{}/likes/like/'.format(self.user_2.slug)

        def test_user_can_like(self):
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertRedirects(response=r, expected_url=self.user_2.get_absolute_url(), status_code=302, target_status_code=200)
            self.assertEqual(first=UserLike.objects.count(), second=1)
            like = UserLike.objects.first()
            self.assertEqual(first=like.from_user.id, second=self.user_1.id)
            self.assertEqual(first=like.to_user.id, second=self.user_2.id)

        def test_user_cannot_like_self(self):
            self.client.login(username=self.user_2.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertEqual(first=r.status_code, second=403)
            self.assertEqual(first=UserLike.objects.count(), second=0)

        def test_user_cannot_like_other_user_if_blocked(self):
            Block.objects.block(blocker=self.user_1, blocked=self.user_2)
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertEqual(first=r.status_code, second=403)
            self.assertEqual(first=UserLike.objects.count(), second=0)

        def test_user_cannot_like_other_user_if_blocking(self):
            Block.objects.block(blocker=self.user_2, blocked=self.user_1)
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertEqual(first=r.status_code, second=403)
            self.assertEqual(first=UserLike.objects.count(), second=0)

        def test_user_cannot_like_twice(self):
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertRedirects(response=r, expected_url=self.user_2.get_absolute_url(), status_code=302, target_status_code=200)
            self.assertEqual(first=UserLike.objects.count(), second=1)
            like = UserLike.objects.first()
            self.assertEqual(first=like.from_user.id, second=self.user_1.id)
            self.assertEqual(first=like.to_user.id, second=self.user_2.id)
            r = self.client.post(path=self.page_url)
            self.assertEqual(first=r.status_code, second=403)
            self.assertEqual(first=UserLike.objects.count(), second=1)


    @only_on_speedy_match
    class UnlikeViewTestCase(SiteTestCase):
        def set_up(self):
            super().set_up()
            self.user_1 = ActiveUserFactory()
            self.user_2 = ActiveUserFactory()
            self.page_url = '/{}/likes/unlike/'.format(self.user_2.slug)

        def test_user_can_unlike(self):
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_2)
            self.assertEqual(first=UserLike.objects.count(), second=1)
            r = self.client.post(path=self.page_url)
            self.assertRedirects(response=r, expected_url=self.user_2.get_absolute_url(), status_code=302, target_status_code=200)
            self.assertEqual(first=UserLike.objects.count(), second=0)

        def test_user_cannot_unlike_if_doesnt_like(self):
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertEqual(first=r.status_code, second=403)
            self.assertEqual(first=UserLike.objects.count(), second=0)

        def test_user_cannot_unlike_twice(self):
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_2)
            self.assertEqual(first=UserLike.objects.count(), second=1)
            r = self.client.post(path=self.page_url)
            self.assertRedirects(response=r, expected_url=self.user_2.get_absolute_url(), status_code=302, target_status_code=200)
            self.assertEqual(first=UserLike.objects.count(), second=0)
            r = self.client.post(path=self.page_url)
            self.assertEqual(first=r.status_code, second=403)
            self.assertEqual(first=UserLike.objects.count(), second=0)


    class LikeListViewsTestCaseMixin(SpeedyMatchLikesLanguageMixin):
        def set_up(self):
            super().set_up()
            self.user_1 = ActiveUserFactory()
            self.user_2 = ActiveUserFactory()
            self.user_3 = ActiveUserFactory()
            self.user_4 = ActiveUserFactory()
            self.user_5 = ActiveUserFactory()
            self.default_url = '/{}/likes/'.format(self.user_1.slug)
            self.to_url = '/{}/likes/people-i-like/'.format(self.user_1.slug)
            self.from_url = '/{}/likes/people-who-like-me/'.format(self.user_1.slug)
            self.mutual_url = '/{}/likes/mutual/'.format(self.user_1.slug)
            UserLike.objects.add_like(from_user=self.user_1, to_user=ActiveUserFactory(slug="user-99"))
            UserLike.objects.add_like(from_user=self.user_1, to_user=ActiveUserFactory(slug="user-98"))
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_3)
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_2)
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_5)
            UserLike.objects.add_like(from_user=ActiveUserFactory(slug="user-97"), to_user=self.user_1)
            UserLike.objects.add_like(from_user=ActiveUserFactory(slug="user-96"), to_user=self.user_1)
            UserLike.objects.add_like(from_user=self.user_5, to_user=self.user_1)
            UserLike.objects.add_like(from_user=self.user_2, to_user=self.user_1)
            self.to_likes = {
                User.objects.get(slug="user-99"),
                User.objects.get(slug="user-98"),
                self.user_3,
                self.user_2,
                self.user_5,
            }
            self.from_likes = {
                User.objects.get(slug="user-97"),
                User.objects.get(slug="user-96"),
                self.user_2,
                self.user_5,
            }
            self.mutual_likes = {
                self.user_2,
                self.user_5,
            }
            self.client.login(username=self.user_1.slug, password=tests_settings.USER_PASSWORD)
            sleep(0.02)
            self.user_5.profile.update_last_visit()
            sleep(0.01)
            self.user_4.profile.update_last_visit()
            sleep(0.01)
            self.user_2.profile.update_last_visit()
            sleep(0.01)
            self.user_3.profile.update_last_visit()
            self.assertEqual(first=UserLike.objects.count(), second=9)

        def _test_all_like_list_views_contain_strings(self, strings):
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=len(self.to_likes))
            for string in strings:
                self.assertIn(member=string, container=r.content.decode())
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=len(self.from_likes))
            for string in strings:
                self.assertIn(member=string, container=r.content.decode())
            r = self.client.get(path=self.mutual_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=len(self.mutual_likes))
            for string in strings:
                self.assertIn(member=string, container=r.content.decode())

        def test_visitor_has_no_access(self):
            self.client.logout()
            self.assertEqual(first=self.client.get(path=self.to_url).status_code, second=302)
            self.assertEqual(first=self.client.get(path=self.from_url).status_code, second=302)
            self.assertEqual(first=self.client.get(path=self.mutual_url).status_code, second=302)

        def test_default_redirect(self):
            r = self.client.get(path=self.default_url)
            self.assertRedirects(response=r, expected_url=self.to_url, status_code=302, target_status_code=200)

        def test_user_can_see_who_they_like(self):
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=5)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=self.to_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2={self.user_1})
            to_likes = set(self.to_likes)
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_4)
            to_likes.add(self.user_4)
            self.assertEqual(first=UserLike.objects.count(), second=10)
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=6)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=self.to_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=to_likes)
            self.assertEqual(first=r.context['object_list'][0].to_user, second=self.user_3)
            sleep(0.01)
            self.user_4.profile.update_last_visit()
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=6)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=self.to_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=to_likes)
            self.assertEqual(first=r.context['object_list'][0].to_user, second=self.user_4)
            Block.objects.block(blocker=self.user_4, blocked=self.user_1)
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=6)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=self.to_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=to_likes)
            Block.objects.block(blocker=self.user_1, blocked=self.user_4)
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=5)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=to_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=self.to_likes)
            Block.objects.unblock(blocker=self.user_1, blocked=self.user_4)
            r = self.client.get(path=self.to_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=5)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=to_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=self.to_likes)

        def test_user_can_see_who_likes_them(self):
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=4)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=self.from_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2={self.user_1})
            from_likes = set(self.from_likes)
            UserLike.objects.add_like(from_user=self.user_4, to_user=self.user_1)
            from_likes.add(self.user_4)
            self.assertEqual(first=UserLike.objects.count(), second=10)
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=5)
            self.assertNotEqual(first={like.from_user for like in r.context['object_list']}, second=self.from_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=from_likes)
            self.assertEqual(first=r.context['object_list'][0].from_user, second=self.user_2)
            sleep(0.01)
            self.user_4.profile.update_last_visit()
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=5)
            self.assertNotEqual(first={like.from_user for like in r.context['object_list']}, second=self.from_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=from_likes)
            self.assertEqual(first=r.context['object_list'][0].from_user, second=self.user_4)
            Block.objects.block(blocker=self.user_1, blocked=self.user_4)
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=4)
            self.assertNotEqual(first={like.from_user for like in r.context['object_list']}, second=from_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=self.from_likes)
            Block.objects.unblock(blocker=self.user_1, blocked=self.user_4)
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=5)
            self.assertNotEqual(first={like.from_user for like in r.context['object_list']}, second=self.from_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=from_likes)
            Block.objects.block(blocker=self.user_4, blocked=self.user_1)
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=4)
            self.assertNotEqual(first={like.from_user for like in r.context['object_list']}, second=from_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=self.from_likes)
            Block.objects.unblock(blocker=self.user_4, blocked=self.user_1)
            r = self.client.get(path=self.from_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=4)
            self.assertNotEqual(first={like.from_user for like in r.context['object_list']}, second=from_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2=self.from_likes)

        def test_user_can_see_mutual_likes(self):
            r = self.client.get(path=self.mutual_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=2)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=self.mutual_likes)
            self.assertSetEqual(set1={like.from_user for like in r.context['object_list']}, set2={self.user_1})
            mutual_likes = set(self.mutual_likes)
            UserLike.objects.add_like(from_user=self.user_1, to_user=self.user_4)
            UserLike.objects.add_like(from_user=self.user_4, to_user=self.user_1)
            mutual_likes.add(self.user_4)
            self.assertEqual(first=UserLike.objects.count(), second=11)
            r = self.client.get(path=self.mutual_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=3)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=self.mutual_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=mutual_likes)
            self.assertEqual(first=r.context['object_list'][0].to_user, second=self.user_2)
            sleep(0.01)
            self.user_4.profile.update_last_visit()
            r = self.client.get(path=self.mutual_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=3)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=self.mutual_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=mutual_likes)
            self.assertEqual(first=r.context['object_list'][0].to_user, second=self.user_4)
            Block.objects.block(blocker=self.user_4, blocked=self.user_1)
            r = self.client.get(path=self.mutual_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=2)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=mutual_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=self.mutual_likes)
            Block.objects.unblock(blocker=self.user_4, blocked=self.user_1)
            r = self.client.get(path=self.mutual_url)
            self.assertEqual(first=r.status_code, second=200)
            self.assertEqual(first=len(r.context['object_list']), second=2)
            self.assertNotEqual(first={like.to_user for like in r.context['object_list']}, second=mutual_likes)
            self.assertSetEqual(set1={like.to_user for like in r.context['object_list']}, set2=self.mutual_likes)

        def test_like_list_views_titles(self):
            self._test_all_like_list_views_contain_strings(strings=[
                self._list_to_title_dict_by_gender[User.GENDER_OTHER_STRING],
                self._list_from_title_dict_by_gender[User.GENDER_OTHER_STRING],
                self._list_mutual_title,
            ])
            user_99 = User.objects.get(slug="user-99")
            user_97 = User.objects.get(slug="user-97")
            gender_count_dict = {
                User.GENDER_FEMALE_STRING: 0,
                User.GENDER_MALE_STRING: 0,
                User.GENDER_OTHER_STRING: 0,
            }
            for gender in User.GENDER_VALID_VALUES:
                for user in [self.user_3, self.user_2, self.user_5, User.objects.get(slug="user-98"), User.objects.get(slug="user-96")]:
                    user.gender = gender
                    user.save_user_and_profile()
                if (gender == User.GENDER_OTHER):
                    two_genders = [random.choice([User.GENDER_FEMALE, User.GENDER_MALE]), gender]
                else:
                    two_genders = [User.GENDER_FEMALE, User.GENDER_MALE]
                for gender_to_match in [User.GENDER_VALID_VALUES, [gender], two_genders]:
                    self.user_1.speedy_match_profile.gender_to_match = gender_to_match
                    self.user_1.save_user_and_profile()
                    for gender_99 in User.GENDER_VALID_VALUES:
                        for gender_97 in User.GENDER_VALID_VALUES:
                            user_99.gender = gender_99
                            user_97.gender = gender_97
                            user_99.save_user_and_profile()
                            user_97.save_user_and_profile()
                            if ((gender in [User.GENDER_FEMALE, User.GENDER_MALE]) and (gender_to_match == [gender]) and (len({user_99.gender, user_97.gender, self.user_2.gender}) == 1)):
                                gender_string = self.user_2.get_gender()
                                self.assertIn(member=gender_string, container=[User.GENDER_FEMALE_STRING, User.GENDER_MALE_STRING])
                                self.assertEqual(first=gender_string, second=User.GENDERS_DICT.get(gender))
                            else:
                                gender_string = User.GENDER_OTHER_STRING
                                self.assertEqual(first=gender_string, second=User.GENDERS_DICT.get(User.GENDER_OTHER))
                            self._test_all_like_list_views_contain_strings(strings=[
                                self._list_to_title_dict_by_gender[gender_string],
                                self._list_from_title_dict_by_gender[gender_string],
                                self._list_mutual_title,
                            ])
                            gender_count_dict[gender_string] += 1
            expected_gender_count_dict = {
                User.GENDER_FEMALE_STRING: 1,
                User.GENDER_MALE_STRING: 1,
                User.GENDER_OTHER_STRING: 79,
            }
            self.assertDictEqual(d1=gender_count_dict, d2=expected_gender_count_dict)

        def test_like_list_views_titles_with_empty_lists(self):
            User.objects.all().exclude(pk=self.user_1.pk).delete()
            self.user_2 = None
            self.user_3 = None
            self.user_4 = None
            self.user_5 = None
            self.to_likes = set()
            self.from_likes = set()
            self.mutual_likes = set()
            self.assertEqual(first=UserLike.objects.count(), second=0)
            self._test_all_like_list_views_contain_strings(strings=[
                self._list_to_title_dict_by_gender[User.GENDER_OTHER_STRING],
                self._list_from_title_dict_by_gender[User.GENDER_OTHER_STRING],
                self._list_mutual_title,
            ])
            gender_count_dict = {
                User.GENDER_FEMALE_STRING: 0,
                User.GENDER_MALE_STRING: 0,
                User.GENDER_OTHER_STRING: 0,
            }
            for gender in User.GENDER_VALID_VALUES:
                if (gender == User.GENDER_OTHER):
                    two_genders = [random.choice([User.GENDER_FEMALE, User.GENDER_MALE]), gender]
                else:
                    two_genders = [User.GENDER_FEMALE, User.GENDER_MALE]
                for gender_to_match in [User.GENDER_VALID_VALUES, [gender], two_genders]:
                    self.user_1.speedy_match_profile.gender_to_match = gender_to_match
                    self.user_1.save_user_and_profile()
                    if ((gender in [User.GENDER_FEMALE, User.GENDER_MALE]) and (gender_to_match == [gender])):
                        gender_string = User.GENDERS_DICT.get(gender)
                        self.assertIn(member=gender_string, container=[User.GENDER_FEMALE_STRING, User.GENDER_MALE_STRING])
                    else:
                        gender_string = User.GENDER_OTHER_STRING
                        self.assertEqual(first=gender_string, second=User.GENDERS_DICT.get(User.GENDER_OTHER))
                    self._test_all_like_list_views_contain_strings(strings=[
                        self._list_to_title_dict_by_gender[gender_string],
                        self._list_from_title_dict_by_gender[gender_string],
                        self._list_mutual_title,
                    ])
                    gender_count_dict[gender_string] += 1
            expected_gender_count_dict = {
                User.GENDER_FEMALE_STRING: 1,
                User.GENDER_MALE_STRING: 1,
                User.GENDER_OTHER_STRING: 7,
            }
            self.assertDictEqual(d1=gender_count_dict, d2=expected_gender_count_dict)


    @only_on_speedy_match
    class LikeListViewsEnglishTestCase(LikeListViewsTestCaseMixin, SiteTestCase):
        def validate_all_values(self):
            super().validate_all_values()
            self.assertEqual(first=self.language_code, second='en')


    @only_on_speedy_match
    @override_settings(LANGUAGE_CODE='he')
    class LikeListViewsHebrewTestCase(LikeListViewsTestCaseMixin, SiteTestCase):
        def validate_all_values(self):
            super().validate_all_values()
            self.assertEqual(first=self.language_code, second='he')


