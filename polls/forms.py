
from django import forms
from polls.fields import VotingChoicesField
from polls.models import Category, Question
import datetime

class CreateTopicForm(forms.Form):
    topic_text = forms.CharField(label='Topic Text', max_length=300)
    choices = VotingChoicesField
    latest_category_list = Category.objects.order_by('-pub_date')
    list = []
    # commented this out (error was latest_category_list has no atribute 'index'
#     for bar in latest_category_list:
        #list.append((latest_category_list.index(bar), bar['category_text']))
    category = forms.ChoiceField(choices=list)
    
    def __init__(self, *args, **kwargs):
        super(CreateTopicForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = self.getCats()
        
    def save(self, request):
        data = self.cleaned_data
        cat = self.getCategoryWithName(data['category'])
        topic = Question(data['topic_text'], cat, request.user, datetime.datetime.now())
        topic.save()
        
    def getCategoryWithName(self, name):
        latest_category_list = Category.objects.order_by('-pub_date')
        for bar in latest_category_list:
            if name==bar['category_text']:
                return latest_category_list[latest_category_list.index(bar)]
            
    def getCats(self):
        latest_category_list = Category.objects.order_by('-pub_date')
        list = []
        for bar in latest_category_list:
            list.append((latest_category_list.index(bar), bar['category_text']))
        return list
            
    
        


    
