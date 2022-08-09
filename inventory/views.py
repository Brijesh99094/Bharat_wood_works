from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Q
from .models import *
from sales.models import *
from dispatch.models import *
from datetime import date
from django.contrib import messages
from django.views.generic import View
from dispatch.models import *
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
import datetime


# EMAIL
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading


def home(request):
    return render(request, 'inventory/BWW.html')


@login_required(login_url='login')
@admin_only
def Admin_dashboard(request):
    c1 = Customer.objects.all()
    context = {
        'c1':c1
    }
    return render(request, 'inventory/tab-Admin-dashboard.html',context)


@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def users(request):
    users = Account.objects.filter(is_active=True).order_by('-date_joined')
    today = date.today()
    recent_users = []
    for user in users:
        if user.date_joined.strftime('%Y-%m-%d') == today.strftime('%Y-%m-%d'):
            recent_users.append(user)

    context = {'users': users, 'today': today, "recent_users": recent_users}
    if request.POST:
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = form.data.get('role')
            group = Group.objects.get(name=user_group)
            user.groups.add(group)
            if user_group == 'Customer':
                messages.success(request, 'New User Added ' + user.username)
                return redirect('CustomerDetail')
            if user_group == 'Dealer':
                messages.success(request, 'New User Added ' + user.username)
                return redirect('DealerDetail')
            if user_group == 'Supervisor':
                messages.success(request, 'New User Added ' + user.username)
                return redirect('SupervisorDetail')
            if user_group == 'Company':
                messages.success(request, 'New User Added ' + user.username)
                return redirect('CompanyDetail')
        else:
            context['registration_form'] = form
    else:
        form = Registration()
        # registration----->ends
        context['registration_form'] = form
    return render(request, 'inventory/tab-Admin-users.html', context)


@login_required(login_url='login')
def Customer_Detail(request):
    acc = Account.objects.latest('id')
    form = CustomerDetailForm()
    if request.POST:
        form = CustomerDetailForm(request.POST)
        print(form.data)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            messages.error(request, 'User not create!!!!')
    context = {'form': form, 'acc': acc}
    return render(request, 'inventory/customer_details.html', context)


@login_required(login_url='login')
def Dealer_Detail(request):
    acc = Account.objects.latest('id')
    form = DealerDetailForm()
    if request.POST:
        form = DealerDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            messages.error(request, 'User not create!!!!')
    context = {'form': form, 'acc': acc}
    return render(request, 'inventory/Dealer_info.html', context)


@login_required(login_url='login')
def Company_Detail(request):
    acc = Account.objects.latest('id')
    form = CompanyDetailForm()
    if request.POST:
        form = CompanyDetailForm(request.POST)
        if form.is_valid():
            c = form.save()
            com = Company.objects.latest('id')
            print(com)
            return redirect('plant', com.id)
        else:
            messages.error(request, 'User not create!!!!')
    context = {'form': form, 'acc': acc}
    return render(request, 'inventory/Company_info.html', context)


@login_required(login_url='login')
def Supervisor_Detail(request):
    acc = Account.objects.latest('id')
    form = SupervisorDetailForm()
    if request.POST:
        form = SupervisorDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment', acc.id)
        else:
            messages.error(request, 'User not create!!!!')
    context = {'form': form, 'acc': acc}
    return render(request, 'inventory/Supervisor_info.html', context)


@login_required(login_url='login')
def assign(request, id):
    shw = SupervisorHasWarehouseForm()
    shc = SupervisorHasCompanyForm()
    sup = Supervisor.objects.get(account=id)
    objshw = SupervisorHasWarehouse.objects.filter(supervisor=sup)
    objshc = SupervisorHasCompany.objects.filter(supervisor=sup)
    context = {'shw': shw, 'shc': shc, 'sup': sup,
               'objshw': objshw, 'objshc': objshc}
    if request.POST.get('ware'):
        shw = SupervisorHasWarehouseForm(request.POST)
        if shw.is_valid():
            data = shw.cleaned_data['warehouse']
            obj1 = SupervisorHasWarehouse.objects.filter(
                supervisor=sup, warehouse=data)
            if obj1:
                messages.warning(request, 'This warehouse is already Assigned')
                pass
            else:
                shw.save()
                messages.success(request, 'added')
                return redirect('assignment', id)
        else:
            messages.error(request, 'failed')
    if request.POST.get('comp'):
        shc = SupervisorHasCompanyForm(request.POST)
        if shc.is_valid():
            data = shc.cleaned_data['company']
            obj1 = SupervisorHasCompany.objects.filter(
                supervisor=sup, company=data)
            if obj1:
                messages.warning(request, 'This Company is already Assigned')
                pass
            else:
                shc.save()
                messages.success(request, 'added')
                return redirect('assignment', id)
        else:
            messages.error(request, 'failed')
    return render(request, 'inventory/supervisor_to.html', context)


@login_required(login_url='login')
def delete_assigned_warehouse(request, id):
    if request.POST:
        acc = SupervisorHasWarehouse.objects.get(id=id)
        sup = Supervisor.objects.get(id=acc.supervisor.id)
        acc.delete()

        return redirect('update_assignment', sup.id)


@login_required(login_url='login')
def delete_assigned_company(request, id):
    if request.POST:
        acc = SupervisorHasCompany.objects.get(id=id)
        sup = Supervisor.objects.get(id=acc.supervisor.id)
        acc.delete()
        return redirect('update_assignment', sup.id)


@login_required(login_url='login')
def Update_assign(request, id):
    shw = SupervisorHasWarehouseForm()
    shc = SupervisorHasCompanyForm()
    sup = Supervisor.objects.get(id=id)
    objshw = SupervisorHasWarehouse.objects.filter(supervisor=sup)
    objshc = SupervisorHasCompany.objects.filter(supervisor=sup)
    context = {'shw': shw, 'shc': shc, 'sup': sup,
               'objshw': objshw, 'objshc': objshc}
    if request.POST.get('ware'):
        shw = SupervisorHasWarehouseForm(request.POST)
        if shw.is_valid():
            data = shw.cleaned_data['warehouse']
            obj1 = SupervisorHasWarehouse.objects.filter(
                supervisor=sup, warehouse=data)
            if obj1:
                messages.warning(request, 'This warehouse is already Assigned')
                pass
            else:
                shw.save()
                messages.success(request, 'added')
                return redirect('update_assignment', id)
        else:
            messages.error(request, 'failed')
    if request.POST.get('comp'):
        shc = SupervisorHasCompanyForm(request.POST)
        if shc.is_valid():
            data = shc.cleaned_data['company']
            obj1 = SupervisorHasCompany.objects.filter(
                supervisor=sup, company=data)
            if obj1:
                messages.warning(request, 'This Company is already Assigned')
                pass
            else:
                shc.save()
                messages.success(request, 'added')
                return redirect('assignment', id)
        else:
            messages.error(request, 'failed')
    return render(request, 'inventory/update_supervisor_to.html', context)


@login_required(login_url='login')
def profile(request, id):
    shw = None
    shc = None
    form = None
    plant = Plant()
    email = Account.objects.get(email=id)
    if email.role == 'Customer':
        b = Customer.objects.get(account=email.id)
        form = CustomerDetailForm(instance=b)
        if request.POST:
            form = CustomerDetailForm(request.POST, instance=b)
            if form.is_valid():
                username = form.cleaned_data['customer_name']
                email.username = username
                email.save()
                form.save()
                return redirect('users')
            else:
                print("form has error")

    elif email.role == 'Dealer':
        b = Dealer.objects.get(account=email.id)
        form = DealerDetailForm(instance=b)
        if request.POST:
            form = DealerDetailForm(request.POST, instance=b)
            if form.is_valid():
                username = form.cleaned_data['dealer_name']
                email.username = username
                email.save()
                form.save()
                return redirect('users')
            else:
                print("form has error")
    elif email.role == 'Supervisor':
        b = Supervisor.objects.get(account=email.id)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=b)
        shc = SupervisorHasCompany.objects.filter(supervisor=b)
        form = SupervisorDetailForm(instance=b)
        if request.POST:
            form = SupervisorDetailForm(request.POST, instance=b)
            if form.is_valid():
                username = form.cleaned_data['supervisor_name']
                email.username = username
                email.save()
                form.save()
                return redirect('users')
            else:
                print("form has error")
    elif email.role == 'Company':
        b = Company.objects.get(account=email.id)
        form = CompanyDetailForm(instance=b)
        plant = Plant.objects.filter(company=b)
        if request.POST:
            form = CompanyDetailForm(request.POST, instance=b)
            if form.is_valid():
                username = form.cleaned_data['company_name']
                email.username = username
                email.save()
                form.save()
                return redirect('users')
            else:
                print("form has error")
    else:
        b = 'happy birthday'
    context = {'b': b, 'email': email, 'shw': shw,
               'shc': shc, 'form': form, 'plant': plant}

    return render(request, 'inventory/profie.html', context)


@login_required(login_url='login')
def delete_user(request, id):
    if request.POST:
        acc = Account.objects.get(id=id)
        acc.is_active = False
        acc.save()
        return redirect('users')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Dealer'])
def Dealer_dashboard(request):
    return render(request, 'inventory/Dealer_dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Supervisor'])
def Supervisor_dashboard(request):
    return render(request, 'inventory/Supervisor_dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Company'])
def Company_dashboard(request):
    context = {}
    user = request.user
    print(user)
    c = Company.objects.get(account=user)
    context = {'com': c}
    return render(request, 'inventory/Company_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def Customer_dashboard(request):
    return render(request, 'inventory/Customer_dashboard.html')


@unauthenticated_user
def login_view(request):
    context = {}

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                messages.success(request, ' Welcome '+user.email)
                return redirect('Admin_dashboard')
            else:
                messages.error(request, ' Enter valid Email/Password ')
                form = UserAuthenticationForm()
                context['login_form'] = form
    return render(request, 'inventory/Login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


###################################EMAIL_STARTS#####################################

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class RequestResetEmailView(View):
    #decorators = [login_required]

    # @method_decorator(decorators)
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('Admin_dashboard')
        else:
            return render(request, 'registration/password_reset_form.html')

    def post(self, request):
        email = request.POST['email']

        user = Account.objects.filter(email=email)
        if user.exists():

            current_site = get_current_site(request)
            email_subject = 'Reset your password',
            message = render_to_string('registration/password_reset_email.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0])
                                       }
                                       )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],


            )

            EmailThread(email_message).start()

        else:
            messages.error(request, 'Email does not exist')
            return redirect('password_reset')

        messages.success(request, 'Email has been sent for reset password')
        return render(request, 'registration/password_reset_form.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = Account.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password reset link is expired please request for new1')
                return render(request, 'registration/password_reset_form.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'something goes wrong')
            return render(request, 'registration/password_reset_form.html')
        return render(request, 'registration/password_reset_confirm.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if len(password1) < 6:
            messages.error(request, 'Password must have 6 charecter ')
            context['has_error'] = True
        if password1 != password2:
            messages.error(request, 'Password not matched ')
            context['has_error'] = True

        if context['has_error'] == True:
            return render(request, 'registration/password_reset_confirm.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = Account.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()

            messages.success(
                request, 'your password has been reset successfully now you can login')
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'something goes wrong')
            return render(request, 'registration/password_reset_confirm.html', context)

        return render(request, 'registration/password_reset_confirm.html', context)

###################################EMAIL_ENDS#####################################

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else: 
        return print("hello")



def report(request):
    cst = Customer.objects.all()
    dealer = Dealer.objects.all()
    plt = Plant.objects.all()
    supp = Supplier.objects.all()
    ware = Warehouse.objects.all()
    t_owner = Transportation.objects.all()
    prod = Product.objects.all()
    date={}
    context={}
    if request.POST:

        ware1 = request.POST.get('warehouse')
        prod1 = request.POST.get('product')
        supplier = request.POST.get('supplier')
        customer = request.POST.get('customer')
        dealer = request.POST.get('dealer')
        truck_owner = request.POST.get('truck_owner')
        d1 = request.POST.get('date_from')
        d2 = request.POST.get('date_to')
        plt1  = request.POST.get('plant')
        frmname = request.POST.get('role')
        
        if frmname == "stock":
            query = "SELECT * FROM purchase_stock WHERE"
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if prod1:
                query += ' product_id='+prod1+' AND'
            if ware1 == "" and prod1 == "":
                query = "select * from purchase_stock    "
            query = query[:-4] + ';'
            s1 = Stock.objects.raw(query)
            print(s1)
            context={'s1':s1,'frmname':frmname}

        if frmname == "plant_stock":
            query = "SELECT * FROM dispatch_plant_stock WHERE"
            if plt1:
                query += ' plant_id='+plt1+' AND'
            if prod1:
                query += ' product_id='+prod1+' AND'
            if plt1 == "" and prod1 == "":
                query = "select * from dispatch_plant_stock    "
            query = query[:-4] + ';'
            s1 = plant_Stock.objects.raw(query)
            context={'s1':s1,'frmname':frmname}
        
        
        if frmname == "warehouse_to_plant":
            query = "SELECT * FROM dispatch_warehouse_to_plant WHERE"
            if plt1:
                query += ' plant_id='+plt1+' AND'
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select warehouse_to_plant_id from dispatch_warehouse_to_plant_detail where product_id='+prod1+') AND'
            if plt1 == "" and prod1 == "" and  ware1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM dispatch_warehouse_to_plant    "
            query = query[:-4] + ';'
            s1 = Warehouse_To_Plant.objects.raw(query)
            print(s1)
            s2 = Warehouse_To_Plant_Detail.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
        

        if frmname == "purchase":
            query = "SELECT * FROM purchase_purchase WHERE"
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if supplier:
                query += ' supplier_id='+supplier+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select purchase_id from purchase_purchase_has_product where product_id='+prod1+') AND'
            if prod1 == "" and  supplier=="" and ware1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM purchase_purchase    "
            query = query[:-4] + ';'
            s1 = Purchase.objects.raw(query)
            print(s1)
            s2 = Purchase_has_Product.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
            
        if frmname == "purchase_return":
            query = "SELECT * FROM purchase_purchasereturn WHERE"
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if supplier:
                query += ' supplier_id='+supplier+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select purchase_id from purchase_purchase_return_has_product where product_id='+prod1+') AND'
            if prod1 == "" and  supplier=="" and ware1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM purchase_purchasereturn    "
            query = query[:-4] + ';'
            s1 = PurchaseReturn.objects.raw(query)
            print(s1)
            s2 = Purchase_Return_has_Product.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
        

        if frmname == "sale":
            query = "SELECT * FROM sales_sales WHERE"
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if customer:
                query += ' customer_id='+customer+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select sales_id from sales_sales_has_product where product_id='+prod1+') AND'
            if prod1 == "" and  customer=="" and ware1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM sales_sales    "
            query = query[:-4] + ';'
            s1 = Sales.objects.raw(query)
            print(s1)
            s2 = Sales_has_product.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
        

        if frmname == "dispatch":
            query = "SELECT * FROM dispatch_dispatch WHERE"
            if plt1:
                query += ' warehouse_id='+ware1+' AND'
            if customer:
                query += ' customer_id='+customer+' AND'
            if dealer:
                query += ' dealer_id='+dealer+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select sales_id from dispatch_dispatchdetail where product_id='+prod1+') AND'
            if prod1 == "" and dealer=="" and customer=="" and plt1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM dispatch_dispatch    "
            query = query[:-4] + ';'
            s1 = Dispatch.objects.raw(query)
            print(s1)
            s2 = DispatchDetail.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
           
        
        if frmname == "collection":
            query = "SELECT * FROM dispatch_collection WHERE"
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if customer:
                query += ' customer_id='+customer+' AND'
            if dealer:
                query += ' dealer_id='+dealer+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select sales_id from dispatch_collectiondetail where product_id='+prod1+') AND'
            if prod1 == "" and dealer=="" and  customer=="" and ware1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM dispatch_collection    "
            query = query[:-4] + ';'
            s1 = Collection.objects.raw(query)
            print(s1)
            s2 = CollectionDetail.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
           
        
        if frmname == "sales_return":
            query = "SELECT * FROM sales_salesreturn WHERE"
            if ware1:
                query += ' warehouse_id='+ware1+' AND'
            if customer:
                query += ' customer_id='+customer+' AND'
            if truck_owner:
                query += ' truck_owner_id='+truck_owner+' AND'
            if d1 and d2:
                query += ' date between "'+d1+'" AND "'+d2+'" AND'
            if prod1:
                query += ' id in (select sales_id from sales_salesreturn_has_product where product_id='+prod1+') AND'
            if prod1 == "" and  customer=="" and ware1 == "" and truck_owner=="" and d1=="" and d2=="":
                query = "SELECT * FROM sales_salesreturn    "
            query = query[:-4] + ';'
            s1 = Sales.objects.raw(query)
            print(s1)
            s2 = Sales_has_product.objects.all()
            context={'s1':s1,'s2':s2,'frmname':frmname}
            pr
  
        date = {'d':datetime.date.today()}
        context.update(date)
        pdf = render_to_pdf('inventory/pdf_report_temp1.html',context) 
        return HttpResponse(pdf,content_type='application/pdf')

    context={'cst':cst,'dealer':dealer,'plt':plt,'supp':supp,'ware':ware,'owner':t_owner,'prod':prod}
    return render(request,"inventory/tab-Admin-reports.html",context)









