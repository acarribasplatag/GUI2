from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from registration.models import UserProfile

class PollPortalUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField()
    lastname = forms.CharField()
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(PollPortalUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.firstname
        user.last_name = self.lastname
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            
        prof = UserProfile(user=user)
        prof.save()
        
        return prof
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        return avatar

class UserProfilePicUploadForm(forms.Form):
    avatar = forms.FileField()

    
class UserProfileEditForm(forms.Form):
    avatar = forms.FileField(label="Select New Profile Picture")
    aboutMe = forms.CharField(widget=forms.Textarea, label="About Me")
    interests = forms.CharField(widget=forms.Textarea, label="Interests")
    
    class Meta:
         fields = ['avatar', 'aboutMe', 'interests']
    
