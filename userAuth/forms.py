
# Create your models here.
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from userAuth.templates.models import UserType


class UserCreation(UserCreationForm):
    '''
    helper = FormHelper()
    helper.form_id = 'blog_post_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'
    '''

    first_name = forms.CharField(max_length=32, help_text='First name')
    last_name = forms.CharField(max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64,
                             help_text='Enter a valid email address')
    type = forms.ChoiceField(choices=(
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ))

    class Meta:
        model = UserType
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'type')
