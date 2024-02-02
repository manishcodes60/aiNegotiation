from django import forms
from crispy_forms.helper import FormHelper

class UploadTranscriptForm(forms.Form):
    upload_transcript_text = forms.CharField(
        label='Paste Negotiation Statement Text Here', 
        max_length=100)

    # def __init__(self, *args, **kwargs):
    #     super(UploadTranscriptForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-2'
    #     self.helper.field_class = 'col-lg-8'
        # self.helper.add_input(Submit('submit', 'Submit'))
