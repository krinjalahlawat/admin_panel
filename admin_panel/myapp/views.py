from django.shortcuts import render, redirect,HttpResponseRedirect,get_object_or_404,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapp.forms import EmployeeForm  
from myapp.models import Employee  
 

  
def addnew(request):  
    if request.method == "GET":  
        form = EmployeeForm(request.GET)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
 
def index(request): 
    employees = Employee.objects.all()   
    entries_per_page = 5
    paginator = Paginator(employees, entries_per_page)

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)
    
    return render(request,"show.html",{'employees':employees})  
 
def edit(request, id):  
    obj=get_object_or_404(Employee,id=id)
    employee = Employee.objects.get(id=id)  
    if request.method=="POST":
        n=request.POST.get("name")
        p=request.POST.get("email")
        e=request.POST.get("contact")
        print(n,p,e)
        obj.name=n
        obj.email=p
        obj.contact=e
        obj.save()
        return HttpResponseRedirect("/")
    return render(request,'edit.html', {'employee':employee})  
 
def update(request, id):  
    obj=get_object_or_404(Employee,id=id)
    if request.method=="POST":
        n=request.POST.get("name")
        p=request.POST.get("email")
        e=request.POST.get("contact")
        print(type(p))
        return render(request,'edit.html', {'obj':obj})  
    return render(request, 'edit.html', {'obj': obj})  
     
def delete(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/")  
def cancel_allrecord(request):
    alldata=Employee.objects.all()
    if request.method=="POST":
        sid=request.POST.getlist('selected_enteries')
        print(sid)
        Employee.objects.filter(id__in=sid).delete()
        return HttpResponseRedirect("/")
def search(request):
    allobj=Employee.objects.all()
    if "qry" in request.GET:
        q=request.GET["qry"]
        if Employee.objects.filter(name__icontains=q):
            Searchdata=Employee.objects.filter(name__icontains=q)
            return render(request,'search.html',{'Searchdata':Searchdata})
        elif Employee.objects.filter(contact__icontains=q):  
            Searchdata=Employee.objects.filter(contact__icontains=q)
            return render(request,'search.html',{'Searchdata':Searchdata})
        elif Employee.objects.filter(email__icontains=q):  
            Searchdata=Employee.objects.filter(email__icontains=q)
            return render(request,'search.html',{'Searchdata':Searchdata}) 
        elif Employee.objects.filter(id=q):  
            Searchdata=Employee.objects.filter(id=q)
            return render(request,'search.html',{'Searchdata':Searchdata}) 
        return HttpResponse("<h1>No result found</h1>") 