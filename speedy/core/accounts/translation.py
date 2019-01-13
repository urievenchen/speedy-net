from modeltranslation.translator import register, TranslationOptions

from speedy.core.accounts.models import User


@register(User)
class UserTranslationOptions(TranslationOptions):
    # fields = ('first_name', 'last_name') # ~~~~ TODO: remove this line!
    fields = User.LOCALIZABLE_FIELDS


