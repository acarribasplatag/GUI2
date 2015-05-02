from django.forms import fields
from widgets import OptionsMultiWidget

class VotingChoicesField(fields.MultiValueField):
    widget = OptionsMultiWidget
 
def __init__(self, *args, **kwargs):
    list_fields = [fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31),
                   fields.CharField(max_length=31)]
    super(VotingChoicesField, self).__init__(list_fields, *args, **kwargs) 