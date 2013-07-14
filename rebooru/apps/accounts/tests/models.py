from django.test import TestCase
from django.forms import ValidationError

from rebooru.apps.accounts.models import Account
from rebooru.apps.accounts.admin import AccountCreationForm, AccountChangeForm

class AccountTest(TestCase):
    fixtures = ['account_testdata.json']

    def test_create_account(self):
        """Tests account creation"""
        # test a proper, basic creation
        acc = Account.objects.create_user('testuser', 'mypass')

        # login checks, should pretty much always work but with custom stuff who knows
        self.assertEquals(acc.get_username(), 'testuser')
        self.assertTrue(acc.check_password('mypass'))

        # test defaults
        self.assertEquals(acc.bio, '')
        self.assertEquals(acc.site, '')
        self.assertEquals(acc.email, '')
        self.assertFalse(acc.is_superuser)
        self.assertFalse(acc.is_staff)
        self.assertTrue(acc.is_active)

        # test compatibility functions
        self.assertEquals(acc.get_full_name(), 'testuser')
        self.assertEquals(acc.get_short_name(), 'testuser')

    def test_create_superuser(self):
        """Tests creating a superuser"""
        superacc = Account.objects.create_superuser('superb', 'pass2')
        self.assertTrue(superacc.is_superuser)

    def test_create_invalid_account(self):
        """Tests creating a user without the required fields"""
        self.assertRaises(ValueError, Account.objects.create_user, '', '')
        self.assertRaises(ValueError, Account.objects.create_user, 'myuser', '')
        self.assertRaises(ValueError, Account.objects.create_user, '', 'mypass')

    def test_create_form(self):
        """Tests the user creation form"""
        # unbound
        form = AccountCreationForm()
        self.assertTrue(isinstance(form.instance, Account))
        
        # bound
        form = AccountCreationForm({'username': 'testacc'})
        self.assertTrue(isinstance(form.instance, Account))

        # save with valid data
        form = AccountCreationForm({'username': 'testacc', 'password1': 'mypass', 'password2': 'mypass'})
        self.assertTrue(form.is_valid())
        acc = form.save()
        self.assertEquals(acc.get_username(), 'testacc')
        self.assertTrue(acc.check_password('mypass'))

        # make sure we can't create a username twice
        form = AccountCreationForm({'username': 'testacc', 'password1': 'mypass', 'password2': 'mypass'})
        self.assertFalse(form.is_valid())
        self.assertTrue('username' in form.errors)

        # save with unmatching passwords
        form = AccountCreationForm({'username': 'testacc2', 'password1': 'mypass', 'password2': 'yourpass'})
        self.assertFalse(form.is_valid())
        self.assertTrue('password1' in form.errors or 'password2' in form.errors)

    def test_change_form(self):
        """Tests the user change form"""
        # all we really did here was the password check
        # the password for the account in the fixture should be 'mypass'
        # so let's check that first
        acc = Account.objects.get(pk=1)
        self.assertTrue(acc.check_password('mypass'))

        # now let's throw it in the form
        form = AccountChangeForm({
            'username': acc.get_username(),
            'password': 'haha oh no im clever',
            'is_active': acc.is_active,
            'is_staff': acc.is_staff,
            'is_superuser': acc.is_superuser,
            'bio': acc.bio,
            'site': acc.site,
            }, instance=acc
        )
        saved_acc = form.save()

        # it should still be the same
        self.assertTrue(saved_acc.check_password('mypass'))
