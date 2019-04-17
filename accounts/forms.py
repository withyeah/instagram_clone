from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email',]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction',]
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):           # Meta class 도 상속 받을 수 있다.
        model = get_user_model()       
        fields = UserCreationForm.Meta.fields