from django.shortcuts import render,redirect
from .models import *
from rest_framework import viewsets
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .resources import StudentResource
from tablib import Dataset
from .forms import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator
from .forms import FeeStructureFormset
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


# Create your views here.
def SchoolApps(request):
    return render(request,"schoolapp/index.html")

def UploadStudent(request):
    return render(request,"schoolapp/studentuploadcsv.html")


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def StudentRecord(request):
    ctx = {}
    query = request.GET.get("q")
    if query:
        first_name = Student.objects.filter(first_name__icontains=query)
        sur_name = Student.objects.filter(sur_name__icontains=query)
        other_name = Student.objects.filter(other_name__icontains=query)
        gender = Student.objects.filter(gender__icontains=query)
        classnameS = Student.objects.filter(classnameS__classname__contains=query)
        registeration_number = Student.objects.filter(registeration_number__icontains=query)
        status = Student.objects.filter(status__icontains=query)
        mobile_no = Student.objects.filter(mobile_no__icontains=query)
        address = Student.objects.filter(address__icontains=query)
        others = Student.objects.filter(others__icontains=query)
        allStudent = first_name.union(sur_name, other_name, gender, classnameS, registeration_number, status,
                                          mobile_no, address, others)
        page = request.GET.get('page', 1)

        paginator = Paginator(allStudent, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        allStudent = Student.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(allStudent, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    ctx["allStudent"] = users
    if is_ajax(request=request):
        html = render_to_string(template_name="schoolapp/ajax_student_record.html", context={"allStudent": allStudent})
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request,"schoolapp/student.html",ctx)

def StaffRecord(request):
    ctx = {}
    query = request.GET.get("q")
    if query:
        first_name = Staff.objects.filter(first_name__icontains=query)
        sur_name = Staff.objects.filter(sur_name__icontains=query)
        other_name = Staff.objects.filter(other_name__icontains=query)
        gender = Staff.objects.filter(gender__icontains=query)
        status = Staff.objects.filter(status__icontains=query)
        mobile_no = Staff.objects.filter(mobile_no__icontains=query)
        address = Staff.objects.filter(address__icontains=query)
        others = Staff.objects.filter(others__icontains=query)
        allStaff = first_name.union(sur_name, other_name, gender, status,
                                      mobile_no, address, others)
        page = request.GET.get('page', 1)

        paginator = Paginator(allStaff, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        allStaff = Staff.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(allStaff, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    ctx["allStaff"] = users
    if is_ajax(request=request):
        html = render_to_string(template_name="schoolapp/ajax_staff_record.html", context={"allStaff": allStaff})
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request,"schoolapp/staff.html",ctx)

def InvoiceRecord(request):
    all_inv = Invoice.objects.all().annotate(fee=Sum('invoiceFS__feeamount'),rec=Sum('receiptR__amount'))
    return render(request,"schoolapp/invoice.html",{'invoice': all_inv})


#Student Section
def GetStudentsRecord(request,id):
    queryset = Student.objects.get(id=id)
    getinvoice = Invoice.objects.filter(studentnameI__first_name=queryset.first_name).annotate(fee=Sum('invoiceFS__feeamount'),rec=Sum('receiptR__amount'))
    return render(request,'schoolapp/getstudentsrecord.html',{'student': queryset,'invoice': getinvoice})

def CreateStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('studentrecord')
    else:
        form = StudentForm()
    return render(request, 'schoolapp/createstudent.html',{'forms':form})

def Session_Term(request):
    if request.method == 'POST':
        form = SessionTerm_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sessionandterm')
    else:
        form = SessionTerm_Form()
    return render(request, 'schoolapp/sessionandterm.html',{'forms':form})

def UpdateStudent(request, id):
    student = Student.objects.get(id=id)
    studentedit = StudentForm(request.POST or None, instance= student)
    if request.method == 'POST':
        if studentedit.is_valid():
            studentedit.save()
            return redirect('studentrecord')
        else:
            return redirect('studentrecord')
    return render(request,"schoolapp/studentform.html",{"updatestudent":studentedit,"student":student})

def DeleteStudentForm(request,id):
    delelestu = Student.objects.get(id=id)
    delelestu.delete()
    return redirect('studentrecord')


#Staff Section
def GetStaffRecord(request,id):
    queryset = Staff.objects.get(id=id)
    return render(request,"schoolapp/getstaffrecord.html",{'staff': queryset})


def CreateStaff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffrecord')
    else:
        form = StaffForm()
    return render(request, 'schoolapp/createstaff.html',{'forms':form})

def UpdateStaff(request, id):
    staff = Staff.objects.get(id=id)
    staffedit = StaffForm(request.POST or None, instance= staff)
    if request.method == 'POST':
        if staffedit.is_valid():
            staffedit.save()
            return redirect('staffrecord')
        else:
            return redirect('staffrecord')
    return render(request,"schoolapp/updatestaff.html",{"updatestaff":staffedit,"staff":staff})

def DeleteStaff(request,id):
    delelestu = Staff.objects.get(id=id)
    delelestu.delete()
    return redirect('staffrecord')



def GetInvoiceRecord(request,id):
    queryset = Invoice.objects.get(id=id)
    allreceipt = []
    allfee = []
    balance = 0
    getreceipt = Receipt.objects.filter(receiptFK__studentnameI=queryset.studentnameI)
    getfee = FeeStructure.objects.filter(feeFK__studentnameI=queryset.studentnameI)
    sum = 0
    for get in getreceipt:
        sum = sum + get.amount
        balance = queryset.balance_from_prev_term - sum
    allreceipt.append(sum)
    allreceipt.append(balance)
    fees = 0
    total_payable = 0
    for fee in getfee:
        fees = fees + fee.feeamount
    total_payable = fees + queryset.balance_from_prev_term
    allfee.append(fees)
    allfee.append(total_payable)
    return render(request,"schoolapp/getinvoicerecord.html",{'invoice': queryset,'alls':allreceipt,'gets':getreceipt,'allfee':allfee,'getfee':getfee})



def DeleteInvoice(request,id):
    delelestu = Invoice.objects.get(id=id)
    delelestu.delete()
    return redirect('invoicerecord')






def ViewResult(request):
    result = CreateResult.objects.all().annotate(total=Sum('studentresult__test_score'),totals=Sum('studentresult__exem_score'))
    return render(request,"schoolapp/viewresult.html",{'result':result})


def CreateSession(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewsession')
    else:
        form = SessionForm()
        current_session = CurrentSession.objects.all()
    return render(request, 'schoolapp/viewsession.html',{'forms':form,"current_session":current_session})

def UpdateSession(request, id):
    update_session = CurrentSession.objects.get(id=id)
    edit_session = SessionForm(request.POST or None, instance= update_session)
    if request.method == 'POST':
        if edit_session.is_valid():
            edit_session.save()
            return redirect('viewsession')
        else:
            return redirect('updatesession')
    return render(request,"schoolapp/updatesession.html",{"edit_session":edit_session,"update_session":update_session})

def DeleteSession(request,id):
    dell = CurrentSession.objects.get(id=id)
    dell.delete()
    return redirect('viewsession')


def CreateTerm(request):
    if request.method == 'POST':
        term = TermForm(request.POST)
        if term.is_valid():
            term.save()
            return redirect('viewterm')
    else:
        term = TermForm()
        current_term = CurrentTerm.objects.all()
    return render(request, 'schoolapp/viewterm.html',{'term':term,"current_term":current_term})

def UpdateTerm(request, id):
    update_term = CurrentTerm.objects.get(id=id)
    edit_term = TermForm(request.POST or None, instance= update_term)
    if request.method == 'POST':
        if edit_term.is_valid():
            edit_term.save()
            return redirect('viewterm')
        else:
            return redirect('updateterm')
    return render(request,"schoolapp/updateterm.html",{"edit_term":edit_term,"update_term":update_term})

def DeleteTerm(request,id):
    dell = CurrentTerm.objects.get(id=id)
    dell.delete()
    return redirect('viewterm')


def CreateSubject(request):
    if request.method == 'POST':
        subject = SubjectForm(request.POST)
        if subject.is_valid():
            subject.save()
            return redirect('viewsubject')
    else:
        subject = SubjectForm()
        sub = Subject.objects.all()
    return render(request, 'schoolapp/viewsubject.html',{'subject':subject,"sub":sub})

def UpdateSubject(request, id):
    update_sub = Subject.objects.get(id=id)
    edit_sub = SubjectForm(request.POST or None, instance= update_sub)
    if request.method == 'POST':
        if edit_sub.is_valid():
            edit_sub.save()
            return redirect('viewsubject')
        else:
            return redirect('viewsubject')
    return render(request,"schoolapp/updatesubject.html",{"edit_sub":edit_sub,"update_sub":update_sub})

def DeleteSubject(request,id):
    dell = Subject.objects.get(id=id)
    dell.delete()
    return redirect('viewsubject')


def CreateClass(request):
    if request.method == 'POST':
        classs = ClassForm(request.POST)
        if classs.is_valid():
            classs.save()
            return redirect('viewclass')
    else:
        classs = ClassForm()
        cls = Class.objects.all()
    return render(request, 'schoolapp/viewclass.html',{'classs':classs,"cls":cls})

def UpdateClass(request, id):
    update_class = Class.objects.get(id=id)
    edit_class = ClassForm(request.POST or None, instance= update_class)
    if request.method == 'POST':
        if edit_class.is_valid():
            edit_class.save()
            return redirect('viewclass')
        else:
            return redirect('viewclass')
    return render(request,"schoolapp/updateclass.html",{"edit_class":edit_class,"update_class":update_class})

def DeleteClass(request,id):
    dell = Class.objects.get(id=id)
    dell.delete()
    return redirect('viewclass')

def Delete_Confirm(request,id):
    rec = Student.objects.get(id=id)
    return render(request,"schoolapp/confirm_delete.html",{'rec':rec})

def Delete_Confirm_Staff(request,id):
    staff = Staff.objects.get(id=id)
    return render(request,"schoolapp/confirm_delete_staff.html",{'staff':staff})

def Delete_Confirm_Invoice(request,id):
    invoice = Invoice.objects.get(id=id)
    return render(request,"schoolapp/confirm_delete_invoice.html",{'invoice':invoice})

def upload_csv(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = StudentResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']
        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'), format='json')
            result = employee_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            employee_resource.import_data(dataset, dry_run=False)
    return render(request, 'schoolapp/studentuploadcsv.html')


def AddReceipt(request,id):
    if request.method == 'POST':
        receipt = ReceiptForm(request.POST)
        if receipt.is_valid():
            res = receipt.save(commit=False)
            res.receiptFK_id= id
            res.save()

            return redirect('invoicerecord')
    else:
        receipt = ReceiptForm()
        invoice = Invoice.objects.get(id=id)
        allreceipt = []
        allfee = []
        balance = 0
        getreceipt = Receipt.objects.filter(receiptFK__studentnameI=invoice.studentnameI)
        getfee = FeeStructure.objects.filter(feeFK__studentnameI=invoice.studentnameI)
        sum = 0
        for get in getreceipt:
            sum = sum + get.amount
            balance = invoice.balance_from_prev_term - sum
        allreceipt.append(sum)
        allreceipt.append(balance)
        fees = 0
        total_payable = 0
        for fee in getfee:
            fees = fees + fee.feeamount
        total_payable = fees + invoice.balance_from_prev_term
        allfee.append(fees)
        allfee.append(total_payable)
    context = {}
    context['invoice'] = invoice
    context['alls'] = allreceipt
    context['gets'] = getreceipt
    context['allfee'] = allfee
    context['getfee'] = getfee
    context['receipt_form'] = receipt
    return render(request, "schoolapp/addreceipt.html",context)


class InvoiceCreateView(CreateView):
    model = Invoice
    fields = "__all__"
    success_url = "/appURL/invoicerecord/"

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = FeeStructureFormset(
                self.request.POST, prefix="feestructure_set"
            )
        else:
            context["items"] = FeeStructureFormset(prefix="feestructure_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceUpdateView(UpdateView):
    model = Invoice
    fields = '__all__'
    success_url = "/appURL/invoicerecord/"

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = FeeStructureFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["items"] = FeeStructureFormset(instance=self.object)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        itemsformset = context["items"]
        if form.is_valid() and itemsformset.is_valid():
            form.save()
            itemsformset.save()
        return super().form_valid(form)