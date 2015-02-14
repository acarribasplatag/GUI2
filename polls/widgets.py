from django import forms

class OptionsMultiWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
        )
        super(OptionsMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(':::')[0:10]
        return ['', '', '','','','','','','', '']