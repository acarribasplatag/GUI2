
from django import forms
from polls.models import Category, Poll, Choice
import datetime,json

class CreatePollForm(forms.Form):
    poll_text = forms.CharField(label='Poll Text', max_length=300, error_messages={'required': 'This field is required.'})
    latest_category_list = Category.objects.order_by('category_text')
    list2 = []
    i = 1
    for bar in latest_category_list:
        list2.append((i, bar.category_text))
        i = i+1
    category = forms.ChoiceField(choices=list2, required=True, error_messages={'required': 'This field is required.'})
    choices = forms.CharField(label= 'Choices: (comma-separated)', widget=forms.Textarea, error_messages={'required': 'This field is required.'})

    def __init__(self, *args, **kwargs):
        super(CreatePollForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = self.getCats()

    def save(self, request):
        data = self.cleaned_data
        cat = self.getCategoryWithName(data['category'])
        topic = Poll(poll_text=data['poll_text'], category = cat, user=request.user, pub_date=datetime.datetime.now())
        topic.save()
        d = data['choices']
        choices = [x.strip() for x in d.split(',')]

        for c in choices:
            choice = Choice(poll=topic, choice_text=c, votes=0, user=request.user, pub_date=datetime.datetime.now())
            choice.save()
        return topic

    def getCategoryWithName(self, name):
        latest_category_list = Category.objects.order_by('category_text')
        i = 0
        for bar in latest_category_list:
            if int(name)-1==i:
                return latest_category_list[i]
            i = i+1

    def getCats(self):
        latest_category_list = Category.objects.order_by('category_text')
        list2 = []
        i = 1
        for bar in latest_category_list:
            list2.append((i, bar.category_text))
            i = i+1
        return list2


class ContactUsForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    comment = forms.CharField(required=True)

    class Meta:
        fields = ('email', 'name', 'comment')

    def save(self, data):
         baseUrl = 'https://api.github.com/repos/bdonald25/GUI2/issues';
# 
#         newIssue = {
#             'title': "New Issue",
#             'body':  data['comment'] + "\n Posted by:" + data['name'] + " " + data['name'],
#             'token': "6fa39168b56ad905f38a3c2fb7a4bf36496e193a"
#         }
# 
#         headers = {'content-type': 'application/json'}
# 
#         r = requests.post(baseUrl, data=json.dumps(newIssue), headers=headers)
#         print r
# 
#         return r