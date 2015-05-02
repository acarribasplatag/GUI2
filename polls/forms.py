
from django import forms
from polls.models import Category, Poll, Choice, Feedback
import datetime,json

# This is where the data for the form that creates a poll is processed.
class CreatePollForm(forms.Form):
    # This gets the poll_text (title) of the poll, it is a charfield with a max length of 300.
    poll_text = forms.CharField(label='Poll Text', max_length=300, error_messages={'required': 'This field is required.'})
    
    # This gets the category list to give to the form.
    latest_category_list = Category.objects.order_by('category_text')
    list2 = []
    i = 1
    for bar in latest_category_list:
        list2.append((i, bar.category_text))
        i = i+1

    # Set the category that the poll belongs to and the choices of the poll.
    category = forms.ChoiceField(choices=list2, required=True, error_messages={'required': 'This field is required.'})
    choices = forms.CharField(required=True, label= 'Choices (comma-separated)', widget=forms.Textarea, error_messages={'required': 'This field is required.'})

    def __init__(self, *args, **kwargs):
        super(CreatePollForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = self.getCats()

    # Run a validation on the choices.
    def clean_choices(self):
        print 'This method was called!'
        data = self.cleaned_data['choices']
        choices = [x.strip() for x in data.split(',')]
        choices2 = []
        for c in choices:
            print c
            strippedString = c.strip()
            if not strippedString:
                raise forms.ValidationError("Choices cannot be empty")
            c2 = c.lower()
            choices2.append(c2)
            print c2
        print self.has_duplicates(choices2)
        if self.has_duplicates(choices2):
            print 'Nonunique'
            raise forms.ValidationError("All choices must be unique")

        # Always return the cleaned data, whether you have changed it or not.
        return data
    
    # Check if their are any duplicates.
    def has_duplicates(self, values):
    # For each element, check all following elements for a duplicate.
        for i in range(0, len(values)):
            for x in range(i + 1, len(values)):
                if values[i] == values[x]:
                    return True
        return False

    # This method save the poll.
    def save(self, request):
        data = self.cleaned_data
        cat = self.getCategoryWithName(data['category'])
        topic = Poll(poll_text=data['poll_text'], category = cat, user=request.user, pub_date=datetime.datetime.now())
        topic.save()
        d = data['choices']
        # Get the choices by splitting on the ",".
        choices = [x.strip() for x in d.split(',')]

        # Save all the choices of the poll.
        for c in choices:
            choice = Choice(poll=topic, choice_text=c, votes=0, user=request.user, pub_date=datetime.datetime.now())
            choice.save()
        return topic

    # Get a category object given the name of the category.
    def getCategoryWithName(self, name):
        latest_category_list = Category.objects.order_by('category_text')
        i = 0
        for bar in latest_category_list:
            if int(name)-1==i:
                return latest_category_list[i]

    # Get all the categories.
    def getCats(self):
        latest_category_list = Category.objects.order_by('category_text')
        list2 = []
        i = 1
        for bar in latest_category_list:
            list2.append((i, bar.category_text))
            i = i+1
        return list2

# This is for the Contact us form.
class ContactUsForm(forms.ModelForm):
    class Meta:
    	model = Feedback #this form will create a Feedback object
        fields = '__all__' #form requires all fields in Feedback object
