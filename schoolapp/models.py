from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class CurrentSession(models.Model):
    sessionname = models.CharField(max_length=400)
    def __str__(self):
        return self.sessionname

class CurrentTerm(models.Model):
    termname = models.CharField(max_length=400)
    def __str__(self):
        return self.termname

class SessionAndTerm(models.Model):
    sessionnameSAT = models.ForeignKey(CurrentSession, on_delete=models.CASCADE, related_name="sessionSAT")
    termnameSAT = models.ForeignKey(CurrentTerm, on_delete=models.CASCADE, related_name="termSAT")
    def __str__(self):
        return self.sessionname + self.termname

class Subject(models.Model):
    subjectname = models.CharField(max_length=400)
    def __str__(self):
        return self.subjectname

class Class(models.Model):
    classname = models.CharField(max_length=400)
    def __str__(self):
        return self.classname

class Student(models.Model):
    statuschoice = [
        ('Active','Active'),
        ('Inactive','Inactive'),
    ]
    genders = [
        ('Male','Male'),
        ('Female','Female'),
    ]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100,choices=statuschoice,default='Active')
    registeration_number = models.CharField(max_length=1200,unique=True)
    first_name = models.CharField(max_length=500)
    sur_name = models.CharField(max_length=500)
    other_name = models.CharField(max_length=500, blank=True,null=True)
    gender = models.CharField(max_length=300,choices=genders,default='Male')
    date_of_birth = models.DateField()
    classnameS = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="classS")
    date_of_addmission = models.DateField()
    mobile_no = models.IntegerField(null=True, blank=True,unique=True)
    address = models.TextField(null=True, blank=True)
    others = models.TextField(null=True, blank=True)
    passport = models.ImageField(upload_to='home/images',null=True, blank=True)

    def __str__(self):
        return self.first_name

class Staff(models.Model):
    statuschoice = [
        ('Active','Active'),
        ('Inactive','Inactive'),
    ]
    genders = [
        ('Male','Male'),
        ('Female','Female'),
    ]
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    status = models.CharField(max_length=100,choices=statuschoice,default='Active')
    first_name = models.CharField(max_length=500)
    sur_name = models.CharField(max_length=500)
    other_name = models.CharField(max_length=500, blank=True,null=True)
    gender = models.CharField(max_length=300,choices=genders,default='Male')
    date_of_birth = models.DateField()
    date_of_addmission = models.DateField()
    mobile_no = models.IntegerField(validators=[mobile_num_regex],unique=True)
    address = models.TextField(null=True, blank=True)
    others = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.first_name

class Invoice(models.Model):
    statuschoice = [
        ('Active','Active'),
        ('Inactive','Inactive'),
    ]
    studentnameI = models.ForeignKey(Student,on_delete=models.CASCADE, related_name="studentI")
    sessionnameI = models.ForeignKey(CurrentSession,on_delete=models.CASCADE, related_name="sessionI")
    termnameI = models.ForeignKey(CurrentTerm,on_delete=models.CASCADE, related_name="termI")
    classnameI = models.ForeignKey(Class,on_delete=models.CASCADE, related_name="classI")
    balance_from_prev_term = models.IntegerField()
    status = models.CharField(max_length=100,choices=statuschoice,default='Active')

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()
        return payable - paid

    def amount_payable(self):
        items = FeeStructure.objects.filter(feeFK=self)
        total = 0
        for item in items:
            total += item.feeamount
        return total

    def total_amount_payable(self):
        return self.balance_from_prev_term + self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(receiptFK=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount
        return amount

class FeeStructure(models.Model):
    fee_type = models.CharField(max_length=400)
    feeamount = models.IntegerField()
    feeFK = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoiceFS")
    def __str__(self):
        return self.fee_type

class Receipt(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=2000,blank=True,null=True)
    date_paid = models.CharField(max_length=800, blank=True, null=True)
    receiptFK = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="receiptR")

class CreateResult(models.Model):
    studentnameCR = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="stuCR")
    sessionnameCR = models.ForeignKey(CurrentSession, on_delete=models.CASCADE, related_name="sessionCR")
    termnameCR = models.ForeignKey(CurrentTerm, on_delete=models.CASCADE, related_name="termCR")

class StudentSubject(models.Model):
    subjectCR = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="studentsubject")
    test_score = models.IntegerField(null=True, blank=True)
    exem_score = models.IntegerField(null=True, blank=True)
    resultFK = models.ForeignKey(CreateResult, on_delete=models.CASCADE, related_name="studentresult")

