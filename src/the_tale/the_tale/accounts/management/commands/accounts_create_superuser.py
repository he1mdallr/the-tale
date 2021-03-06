# coding: utf-8

from django.core.management.base import BaseCommand

from the_tale.accounts import logic
from the_tale.accounts import models

class Command(BaseCommand):

    help = 'create super user'

    def handle(self, *args, **options):
        if models.Account.objects.exists():
            print('some users have created already, superuser MUST be created first')
            exit(0)

        NICK = 'superuser'
        EMAIL = 'superuser@example.com'
        PASSWORD = '111111'

        result, account_id, bundle_id = logic.register_user(NICK, email=EMAIL, password=PASSWORD, referer=None, referral_of_id=None, action_id=None, is_bot=False)

        models.Account.objects.filter(id=account_id).update(is_superuser=True, is_staff=True)

        print('nick:', NICK)
        print('email:', EMAIL)
        print('password:', PASSWORD)
        print('login to site.url/admin and change password!')
