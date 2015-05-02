from django import forms

# This was originally designed for entering poll choices, wherein choices were added to a list that was then saved.
# This design was deemed to complex to implement within the time frame, so this form of input was removed.
# However, this functionality may eventually return in a future release.
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