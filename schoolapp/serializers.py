from rest_framework import serializers
from .models import *



class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class MemberOfStaffSerializers(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class CreateResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = CreateResult
        fields = '__all__'

class CurrentSessionSerializers(serializers.ModelSerializer):
    class Meta:
        model = CurrentSession
        fields = '__all__'

class CurrentTermSerializers(serializers.ModelSerializer):
    class Meta:
        model = CurrentTerm
        fields = '__all__'

class ClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ReceiptSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


class FeeStructureSerializers(serializers.ModelSerializer):
   class Meta:
        model = FeeStructure
        fields = '__all__'



