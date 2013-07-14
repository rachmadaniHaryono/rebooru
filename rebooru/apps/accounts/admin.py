from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from rebooru.apps.accounts.models import Account

class AccountCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    """

    # two passwords for confirmation
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'email')

    def clean_password2(self):
        """
        Makes sure both given passwords match
        """
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Passwords don't match")

        return pass2

    def save(self, commit=True):
        """
        Saves the account with a hashed password
        """

        # get an initialized account but don't save it yet
        account = super(AccountCreationForm, self).save(commit=False)

        # set the hashed password
        account.set_password(self.cleaned_data['password1'])

        # save it
        if commit:
            account.save()

        return account

class AccountChangeForm(forms.ModelForm):
    """
    A form for making changes to existing accounts
    """
    # don't show an editable password field
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        # exclude date_joined since we don't ever wanna change that
        fields = [
                'username', 'password', 'is_active', 'is_staff',
                'is_superuser', 'groups', 'user_permissions', 'bio', 'site'
        ]

    def clean_password(self):
        """
        If the user manages to submit a different password, despite the
        read-only field, throw it away and use the initial value
        """
        return self.initial['password']

class AccountAdmin(UserAdmin):
    """
    An admin class that takes into account our new forms
    """
    # UserAdmin gives a lot of useful stuff, but some stuff relies on the
    # original User model, so we have to override those to work with Accounts
    form = AccountChangeForm
    add_form = AccountCreationForm

    # various properties for the account admin section
    # these must be defined in order to override originals in UserAdmin
    # since those reference the vanilla User model
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    # organize the forms into sets
    fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Profile', {'fields': ('bio', 'site')}),
            ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
            ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2')}
            ),
    )


# register our new, corrected admin
admin.site.register(Account, AccountAdmin)
