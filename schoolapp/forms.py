from django import forms
from .models import *
from django.forms import inlineformset_factory,modelformset_factory


FeeStructureFormset = inlineformset_factory(
    Invoice, FeeStructure, fields=["fee_type", "feeamount"], extra=1, can_delete=True
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)


class DateInput(forms.DateInput):
    input_type = 'date'
class StudentForm(forms.ModelForm):
    classnameS = forms.ModelChoiceField(queryset=Class.objects.all())
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(),
            'date_of_addmission': DateInput()
        }

class SessionTerm_Form(forms.ModelForm):#
    sessionnameSAT = forms.ModelChoiceField(queryset=CurrentSession.objects.all(),label='Current Session',help_text='Click <a href="/appURL/sessionandterm/">here</a> to add new session')
    termnameSAT = forms.ModelChoiceField(queryset=CurrentTerm.objects.all(),label='Current Term',help_text='Click <a href="/appURL/sessionandterm/">here</a> to add new term')
    class Meta:
        model = SessionAndTerm
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(),
            'date_of_addmission': DateInput()
        }

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        exclude =('receiptFK',)
        widgets = {
            'date_paid': DateInput(),
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = CurrentSession
        fields = '__all__'

class TermForm(forms.ModelForm):
    class Meta:
        model = CurrentTerm
        fields = '__all__'

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

