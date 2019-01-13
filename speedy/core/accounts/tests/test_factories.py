import string
import random
from datetime import date

import factory
import factory.fuzzy

# from unittest import TestCase as PythonTestCase #### TODO

from django.conf import settings as django_settings
from django.test import TestCase as DjangoTestCase #### TODO
from django.contrib.sites.models import Site

from speedy.core.base.test import tests_settings
# from speedy.core.base.test.models import SiteTestCase #### TODO
from speedy.core.base.utils import normalize_username
from speedy.core.accounts.models import User, UserEmailAddress
from speedy.core.accounts.translation import UserTranslationOptions #### TODO
from speedy.core.accounts.forms import LocalizedFirstLastNameMixin #### TODO


if (django_settings.LOGIN_ENABLED):

    # _test_case = PythonTestCase()
    _test_case = DjangoTestCase()
    # _test_case = SiteTestCase()
    # _test_case.set_up()


    class UserConfirmedEmailAddressFactory(factory.DjangoModelFactory):
        email = factory.Faker('email')
        is_confirmed = True

        class Meta:
            model = UserEmailAddress


    # class DefaultUserFactory(factory.DjangoModelFactory, PythonTestCase): # ~~~~ TODO
    # class DefaultUserFactory(factory.DjangoModelFactory, DjangoTestCase): # ~~~~ TODO
    # class DefaultUserFactory(factory.DjangoModelFactory, SiteTestCase):
    # class DefaultUserFactory(PythonTestCase, factory.DjangoModelFactory): # ~~~~ TODO
    # class DefaultUserFactory(DjangoTestCase, factory.DjangoModelFactory): # ~~~~ TODO
    # class DefaultUserFactory(SiteTestCase, factory.DjangoModelFactory):
    class DefaultUserFactory(factory.DjangoModelFactory):
        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
        date_of_birth = factory.fuzzy.FuzzyDate(start_date=date(year=1900, month=1, day=1))
        gender = factory.fuzzy.FuzzyChoice(choices=User.GENDER_VALID_VALUES)
        slug = factory.fuzzy.FuzzyText(chars=string.ascii_lowercase)
        username = factory.LazyAttribute(lambda o: normalize_username(username=o.slug))
        password = factory.fuzzy.FuzzyText(chars=string.ascii_lowercase)
        _password = factory.PostGenerationMethodCall(method_name='set_password', raw_password=tests_settings.USER_PASSWORD)

        class Meta:
            model = User

        @factory.post_generation
        def validate_first_and_last_name_in_all_languages(self, created, extracted, **kwargs):
            _test_case.assertTupleEqual(tuple1=User.LOCALIZABLE_FIELDS, tuple2=('first_name', 'last_name'))
            _test_case.assertEqual(first=self.first_name_en, second=self.first_name)
            _test_case.assertEqual(first=self.first_name_he, second=self.first_name)
            _test_case.assertEqual(first=self.last_name_en, second=self.last_name)
            _test_case.assertEqual(first=self.last_name_he, second=self.last_name)
            field_name_localized_list = list()
            for base_field_name in User.LOCALIZABLE_FIELDS:
                for language_code in django_settings.ALL_LANGUAGE_CODES:
                    field_name_localized = '{}_{}'.format(base_field_name, language_code)
                    _test_case.assertEqual(first=getattr(self, field_name_localized), second=getattr(self, base_field_name), msg="DefaultUserFactory::fields don't match ({field_name_localized}, {base_field_name}), self.pk={self_pk}, self.username={self_username}, self.slug={self_slug}, self.profile.get_name()={self_profile_get_name}".format(
                        field_name_localized=field_name_localized,
                        base_field_name=base_field_name,
                        self_pk=self.pk,
                        self_username=self.username,
                        self_slug=self.slug,
                        self_profile_get_name=self.profile.get_name(),
                    ))
                    field_name_localized_list.append(field_name_localized)
            _test_case.assertListEqual(list1=field_name_localized_list, list2=['first_name_en', 'first_name_he', 'last_name_en', 'last_name_he'])


    class InactiveUserFactory(DefaultUserFactory):
        @factory.post_generation
        def deactivate_speedy_net_profile(self, created, extracted, **kwargs):
            # Deactivate only on speedy.net, speedy.match default is inactive.
            site = Site.objects.get_current()
            if (site.id == django_settings.SPEEDY_NET_SITE_ID):
                self.profile.deactivate()


    class ActiveUserFactory(DefaultUserFactory):
        @factory.post_generation
        def activate_profile(self, created, extracted, **kwargs):
            site = Site.objects.get_current()
            if (site.id == django_settings.SPEEDY_MATCH_SITE_ID):
                # ~~~~ TODO: this code is specific for Speedy Match, should not be in core.
                from speedy.core.uploads.tests.test_factories import UserImageFactory
                from speedy.match.accounts.models import SiteProfile as SpeedyMatchSiteProfile
                self.profile.profile_description = "Hi!"
                self.profile.city = "Tel Aviv."
                self.profile.children = "One boy."
                self.profile.more_children = "Yes."
                self.profile.match_description = "Hi!"
                self.profile.height = random.randint(SpeedyMatchSiteProfile.settings.MIN_HEIGHT_ALLOWED, SpeedyMatchSiteProfile.settings.MAX_HEIGHT_ALLOWED)
                _test_case.assertEqual(first=self.diet, second=User.DIET_UNKNOWN)
                _test_case.assertEqual(first=self.profile.smoking_status, second=SpeedyMatchSiteProfile.SMOKING_STATUS_UNKNOWN)
                _test_case.assertEqual(first=self.profile.marital_status, second=SpeedyMatchSiteProfile.MARITAL_STATUS_UNKNOWN)
                self.diet = random.choice(User.DIET_VALID_VALUES)
                self.profile.smoking_status = random.choice(SpeedyMatchSiteProfile.SMOKING_STATUS_VALID_VALUES)
                self.profile.marital_status = random.choice(SpeedyMatchSiteProfile.MARITAL_STATUS_VALID_VALUES)
                _test_case.assertNotEqual(first=self.diet, second=User.DIET_UNKNOWN)
                _test_case.assertNotEqual(first=self.profile.smoking_status, second=SpeedyMatchSiteProfile.SMOKING_STATUS_UNKNOWN)
                _test_case.assertNotEqual(first=self.profile.marital_status, second=SpeedyMatchSiteProfile.MARITAL_STATUS_UNKNOWN)
                self.profile.gender_to_match = User.GENDER_VALID_VALUES
                self.photo = UserImageFactory(owner=self)
                self.profile.activation_step = 9
                email = UserConfirmedEmailAddressFactory(user=self)
                email.save()
                self.save_user_and_profile()
                step, error_messages = self.profile.validate_profile_and_activate()
                if (len(error_messages) > 0):
                    raise Exception("Error messages not as expected, {}".format(error_messages))
                if (not (step == len(SpeedyMatchSiteProfile.settings.SPEEDY_MATCH_SITE_PROFILE_FORM_FIELDS))):
                    raise Exception("Step not as expected, {}".format(step))
            else:
                self.profile.activate()


    class UserEmailAddressFactory(factory.DjangoModelFactory):
        user = factory.SubFactory(DefaultUserFactory)
        email = factory.Faker('email')

        class Meta:
            model = UserEmailAddress


