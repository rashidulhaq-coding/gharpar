from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm


class PwdChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",
        widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3','placeholder':'Password','id':'form-oldpass'}),
    )
    new_password1 = forms.CharField(label="New Password",
        widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3','placeholder':'Password','id':'form-newpass'}),
    )
    new_password2 = forms.CharField(label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3','placeholder':'Password','id':'form-new-pass2'}),
    )


class UserEditForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = False
        self.fields['email'].required = False

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password",
        widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3','placeholder':'Password','id':'form-newpass'}),
    )
    new_password2 = forms.CharField(label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3','placeholder':'Password','id':'form-new-pass2'}),
    )

class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254,widget= forms.TextInput(
        attrs={'class':'form-control mb-3', 'placeholder':'Email','id':'form-email'}
   ))

    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email = email)
        if not test:
            raise forms.ValidationError("Unfortunatley we can not find that email address.")
        return email

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email',widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'}))

    # email = forms.EmailField(max_length=50, help_text='Required', error_messages={'required': 'Sorry, You will need an email'}, widget=forms.TextInput(
    #     attrs={'autofocus': True, 'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-email','name':'email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password','class':'form-control','placeholder':'Password','id':'login-pwd','name':'password'}),
    )


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'autofocus': True,'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))
    email = forms.EmailField(max_length=50,help_text='Required',error_messages={'required':'Sorry, You will need an email'},widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-email','name': 'email'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password','class':'form-control','placeholder':'Password','id':'login-pwd'}),
    )
    password2 = forms.CharField(label='Repeat Password',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password','class':'form-control','placeholder':'Password','id':'login-pwd'}),
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','password2')
    
    def clear_password2(self):
        cd= self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match.")
        return cd['password2']
    
    def clear_email(self):
        email = self.cleaned_data['email']
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("please user another Email, this is already taken.")
        return email
    
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs.update(
    #         {'class':'form-control mb-3','placeholder': 'E-mail','name':'email'}
    #     )
    #     self.fields['password'].widget.attrs.update(
    #         {'class':'form-control mb-3','placeholder': 'Password'}
    #     )
    #     self.fields['password2'].widget.attrs.update(
    #         {'class':'form-control mb-3','placeholder': 'Password'}
    #     )