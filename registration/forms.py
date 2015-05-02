from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from registration.models import UserProfile

#Create a user. Extends Djangos UserCreationForm.
class PollPortalUserCreationForm(UserCreationForm):
    # Require the following to be filled in along with what django requires (username, password1, password2)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    # Save the new user to the database.
    def save(self, commit=True):
        user = super(PollPortalUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        #create user profile
        prof = UserProfile(user=user)
        prof.save()

        return prof
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        return avatar

# Upload a prifile pic.
class UserProfilePicUploadForm(forms.Form):
    avatar = forms.FileField()

# Edit a user.
class UserProfileEditForm(forms.Form):
    # These are not required because you do not need to update all of them at once. 
    # You can just upload a profile pic, or just change the about me section of the user page.
    avatar = forms.FileField(label="Select New Profile Picture", required=False)
    aboutMe = forms.CharField(widget=forms.Textarea, label="About Me", required=False)
    interests = forms.CharField(widget=forms.Textarea, label="Interests", required=False)

    class Meta:
         fields = ['avatar', 'aboutMe', 'interests']
