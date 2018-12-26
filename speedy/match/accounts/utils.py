from django.conf import settings as django_settings

from speedy.match.accounts import validators


def get_steps_range():
    return range(1, len(django_settings.SPEEDY_MATCH_SITE_PROFILE_FORM_FIELDS))


def get_step_form_fields(step):
    return list(django_settings.SPEEDY_MATCH_SITE_PROFILE_FORM_FIELDS[step])


def get_step_fields_to_validate(step):
    fields = get_step_form_fields(step=step)
    if (('min_age_match' in fields) or ('max_age_match' in fields)):
        fields.append('min_max_age_to_match')
    return fields


def validate_field(field_name, user):
    if (field_name in ['photo']):
        validators.validate_photo(photo=user.photo)
    elif (field_name in ['profile_description']):
        validators.validate_profile_description(profile_description=user.speedy_match_profile.profile_description)
    elif (field_name in ['city']):
        validators.validate_city(city=user.speedy_match_profile.city)
    elif (field_name in ['children']):
        validators.validate_children(children=user.speedy_match_profile.children)
    elif (field_name in ['more_children']):
        validators.validate_more_children(more_children=user.speedy_match_profile.more_children)
    elif (field_name in ['match_description']):
        validators.validate_match_description(match_description=user.speedy_match_profile.match_description)
    elif (field_name in ['height']):
        validators.validate_height(height=user.speedy_match_profile.height)
    elif (field_name in ['diet']):
        validators.validate_diet(diet=user.diet)
    elif (field_name in ['smoking_status']):
        validators.validate_smoking_status(smoking_status=user.speedy_match_profile.smoking_status)
    elif (field_name in ['marital_status']):
        validators.validate_marital_status(marital_status=user.speedy_match_profile.marital_status)
    elif (field_name in ['gender_to_match']):
        validators.validate_gender_to_match(gender_to_match=user.speedy_match_profile.gender_to_match)
    elif (field_name in ['min_age_match']):
        validators.validate_min_age_match(min_age_match=user.speedy_match_profile.min_age_match)
    elif (field_name in ['max_age_match']):
        validators.validate_max_age_match(max_age_match=user.speedy_match_profile.max_age_match)
    elif (field_name in ['min_max_age_to_match']):
        validators.validate_min_max_age_to_match(min_age_match=user.speedy_match_profile.min_age_match, max_age_match=user.speedy_match_profile.max_age_match)
    elif (field_name in ['diet_match']):
        validators.validate_diet_match(diet_match=user.speedy_match_profile.diet_match)
    elif (field_name in ['smoking_status_match']):
        validators.validate_smoking_status_match(smoking_status_match=user.speedy_match_profile.smoking_status_match)
    elif (field_name in ['marital_status_match']):
        validators.validate_marital_status_match(marital_status_match=user.speedy_match_profile.marital_status_match)


