# Used also by Speedy Net.

MIN_HEIGHT_ALLOWED = 1 # In cm.
MAX_HEIGHT_ALLOWED = 450 # In cm.

SPEEDY_MATCH_SITE_PROFILE_FORM_FIELDS = [
    [],  # There's no step 0
    [],  # Step 1 = registration form
    ['photo'],
    ['profile_description', 'city', 'height'],
    ['children', 'more_children'],
    ['diet', 'smoking_status'],
    ['marital_status'],
    ['gender_to_match', 'match_description', 'min_age_match', 'max_age_match'],
    ['diet_match', 'smoking_status_match'],
    ['marital_status_match']
]
