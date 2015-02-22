
from django import forms
from polls.models import Category, Question, Choice
import datetime

class CreateTopicForm(forms.Form):
    topic_text = forms.CharField(label='Topic Text', max_length=300, error_messages={'required': 'This field is required.'})
    latest_category_list = Category.objects.order_by('category_text')
    list2 = []
    i = 1
    for bar in latest_category_list:
        list2.append((i, bar.category_text))
        i = i+1
    category = forms.ChoiceField(choices=list2, required=True, error_messages={'required': 'This field is required.'})
    choices = forms.CharField(label= 'Choices: (comma-separated)', widget=forms.Textarea, error_messages={'required': 'This field is required.'})
    
    def __init__(self, *args, **kwargs):
        super(CreateTopicForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = self.getCats()
        
    def save(self, request):
        data = self.cleaned_data
        cat = self.getCategoryWithName(data['category'])
        topic = Question(question_text=data['topic_text'], category = cat, user=request.user, pub_date=datetime.datetime.now())
        topic.save()
        d = data['choices']
        choices = [x.strip() for x in d.split(',')]
        
        for c in choices:
            choice = Choice(question=topic, choice_text=c, votes=0, user=request.user, pub_date=datetime.datetime.now())
            choice.save()
        
    def getCategoryWithName(self, name):
        latest_category_list = Category.objects.order_by('-pub_date')
        i = 0
        for bar in latest_category_list:
            if int(name)==i:
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
    
        


    
