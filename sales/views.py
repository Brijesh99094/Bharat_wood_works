from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from io import BytesIO
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.views import View
from django.contrib.auth.decorators import login_required



###############################################################
############################ PDF  #############################
###############################################################



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, id, *args, **kwargs):
        salesObj = Sales.objects.get(id=id)
        sales_prodObj = Sales_has_product.objects.filter(sales=salesObj.id)
        total = 0
        for sp in sales_prodObj:
            total += (sp.price * sp.qty)

        context = {'sales_data': salesObj,
                   'shp': sales_prodObj, 'total': total }
        pdf = render_to_pdf('sales/pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

###############################################################
############################ end of PDF  ######################
###############################################################


def updatestock_sales(product_sales, curr_qty=0, check=False):
    sales_ware = Sales.objects.get(id=product_sales.sales.id)
    ware = sales_ware.warehouse
    s1 = Stock.objects.all()
    for st in s1:
        if ware == st.warehouse and product_sales.product == st.product:
            stock = Stock.objects.get(
                warehouse=ware, product=product_sales.product)
            if stock:
                if check == True:
                    stock.qty -= curr_qty
                    stock.save()
                    break
                else:
                    stock.qty -= product_sales.qty
                    stock.save()
                    break
    else:
        s1, created = Stock.objects.update_or_create(
            warehouse=ware, product=product_sales.product, qty=product_sales.qty)


@login_required(login_url='login')
def sales_master(request):
    sales_data = Sales.objects.select_related('warehouse', 'sales_user').all()
    shp = Sales_has_product.objects.select_related('sales', 'product').all()
    salesform = SalesForm()
    shw = SupervisorHasWarehouse()
    if request.user.role == 'Supervisor':
        acc = Supervisor.objects.get(account=request.user)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=acc.id)
    context = {'salesform': salesform,
               'sales_data': sales_data, 'shp': shp, 'shw': shw}
    if request.POST:
        salesform = SalesForm(request.POST)
        if salesform.is_valid():
            salesform.save()
            return redirect('sales_product')
        else:
            return HttpResponse('error in form valid')
    return render(request, 'sales/sales.html', context)


@login_required(login_url='login')
def sales_product(request):
    sales_id = Sales.objects.latest('id')
    items = Sales_has_product.objects.filter(sales=sales_id)
    products = Stock.objects.filter(warehouse=sales_id.warehouse)

    sales_form = SalesProductForm()
    context = {'sales_form': sales_form, 'items': items,
               'sales_id': sales_id, 'products': products}
    if request.POST:
        sales_form = SalesProductForm(request.POST)
        print(sales_form)
        if sales_form.is_valid():
            prod = sales_form.cleaned_data['product']
            qty = sales_form.cleaned_data['qty']
            pid = sales_form.cleaned_data['sales']
            price = sales_form.cleaned_data['price']
            print(price)
            s1 = Stock.objects.get(warehouse=sales_id.warehouse, product=prod)
            if qty > s1.qty:
                messages.warning(request, 'Insufficient stocks')
                return redirect('sales_product')

            shp, created = Sales_has_product.objects.get_or_create(
                product=prod, sales=sales_id, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()
                print('i am in created')
                updatestock_sales(shp)
                print(created)
            else:
                shp.qty += qty
                shp.save()
                print('i am in php')
                check = True
                updatestock_sales(shp, qty, check)
        else:
            return HttpResponse('error in form')
        return redirect('sales_product')
    return render(request, 'sales/sales_product.html', context)



@login_required(login_url='login')
def delete_sales(request, id):
    context = {}
    if request.POST:
        sales = Sales.objects.get(id=id)
        sales_ret = SalesReturn.objects.filter(sales=sales).count()
        if sales_ret > 0:
            messages.warning(request, 'something goes wrong')
            return redirect('sales')
        else:
            prod = Sales_has_product.objects.filter(
                sales=sales).order_by('product')
            stock = Stock.objects.filter(
                warehouse=sales.warehouse).order_by('product')
            s_lst, p_lst = [], []
            for s1 in stock:
                for pid in prod:
                    if s1.product.id == pid.product.id:
                        s1.qty += pid.qty
                        s1.save()
            sales.delete()

            return redirect('sales')
    return render(request, 'sales/delete_sales.html', context)



@login_required(login_url='login')
def delete_sales_product(request, id):
    if request.POST:
        shp = Sales_has_product.objects.get(id=id)
        ware = Sales.objects.get(id=shp.sales.id)
        stock = Stock.objects.get(
            warehouse=ware.warehouse, product=shp.product)
        stock.qty += shp.qty
        stock.save()
        shp.delete()
        return redirect('sales_product')
    return render(request, 'sales/delete_sales_product.html')


@login_required(login_url='login')
def update_sales(request, id):
    pd = Sales.objects.get(id=id)
    prod_data = Sales_has_product.objects.filter(sales=pd)
    w1_data = pd.warehouse
    form = SalesForm(instance=pd)
    if request.POST:
        frm = SalesForm(request.POST, instance=pd)
        if frm.is_valid():
            frm.save()
            return redirect("sales")
    context = {
        'pd': pd,
        'form': form,
        'product_data': prod_data
    }
    return render(request, 'sales/sales_update.html', context)



@login_required(login_url='login')
def Update_product_detail(request, id):
    sales_id = Sales.objects.get(id=id)
    items = Sales_has_product.objects.filter(sales=sales_id)
    products = Stock.objects.filter(warehouse=sales_id.warehouse)
    sales_form = SalesProductForm()
    context = {'sales_form': sales_form, 'items': items,
               'sales_id': sales_id, 'products': products}
    if request.POST:
        sales_form = SalesProductForm(request.POST)
        if sales_form.is_valid():
            prod = sales_form.cleaned_data['product']
            qty = sales_form.cleaned_data['qty']
            pid = sales_form.cleaned_data['sales']
            price = sales_form.cleaned_data['price']
            print(price)
            s1 = Stock.objects.get(warehouse=sales_id.warehouse, product=prod)
            if qty > s1.qty:
                messages.warning(request, 'Insufficient stocks')
                return redirect('update_sales_product', sales_id.id)

            shp, created = Sales_has_product.objects.get_or_create(
                product=prod, sales=sales_id, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()
                print('i am in created')
                updatestock_sales(shp)
                print(created)
            else:
                shp.qty += qty
                shp.save()
                print('i am in php')
                check = True
                updatestock_sales(shp, qty, check)
        else:
            return HttpResponse('error in form')
        return redirect('update_sales_product', sales_id.id)
    return render(request, 'sales/update_sales_product.html', context)


############################################################################################

@login_required(login_url='login')
def saless_return(request):
    sr = SalesReturn.objects.all()
    srhp = SalesReturn_has_product.objects.all()
    context = {'srhp': srhp, 'sr': sr}
    return render(request, 'sales/saless_return.html', context)


def updatestock_sales_return(product_sales_return, curr_qty=0, check=False):
    sales_return_ware = SalesReturn.objects.get(
        id=product_sales_return.sales_return.id)
    ware = sales_return_ware.warehouse
    s1 = Stock.objects.all()
    for st in s1:
        if ware == st.warehouse and product_sales_return.product == st.product:
            stock = Stock.objects.get(
                warehouse=ware, product=product_sales_return.product)
            if stock:
                if check == True:
                    stock.qty += curr_qty
                    stock.save()
                    break
                else:
                    stock.qty += product_sales_return.qty
                    stock.save()
                    break
    else:
        s1, created = Stock.objects.update_or_create(
            warehouse=ware, product=product_sales_return.product, qty=product_sales_return.qty)


@login_required(login_url='login')
def salesreturn(request, id):
    salesObj = Sales.objects.get(id=id)
    sr = SalesReturn.objects.filter(sales=salesObj)
    srhp = SalesReturn_has_product.objects.all()

    truck_own = Transportation.objects.all()
    context = {'sid': salesObj, 't1': truck_own, 'srhp': srhp, 'sr': sr}
    if request.POST:
        sr_date = request.POST.get('sales_return_date')
        sr_warehouse = request.POST.get('warehouse')
        ware = Warehouse.objects.get(warehouse_name=sr_warehouse)
        sr_user = request.POST.get('sales_user')
        print(sr_user)
        sales_user = Account.objects.get(email=sr_user)
        sr_truck_owner = request.POST.get('truck_owner')
        truckown = Transportation.objects.get(co_name=sr_truck_owner)
        sr_truck_no = request.POST.get('truck_no')
        sr_weight = request.POST.get('weight')
        #purchase_return = PurchaseReturn.objects.create(purchase_return_date=pr_date)
        # purchase_return.save()
        sr_obj = SalesReturn.objects.create(sales_return_date=sr_date, sales=salesObj, warehouse=ware,
                                            sales_user=sales_user, truck_owner=truckown, truck_no=sr_truck_no, weight=sr_weight)
        sr_obj.save()
        prc = True
        sr_id = sr_obj.id
        print(sr_id)
        return redirect('sales_return_product', sr_id)
    return render(request, 'sales/salesreturn.html', context)
    # salesreturnform = SalesReturnForm()
    # sales_return_data = SalesReturn.objects.select_related(
    #     'warehouse', 'sales_user').all()
    # srhp = SalesReturn_has_product.objects.select_related(
    #     'sales_return', 'product').all()
    # context = {'salesreturnform': salesreturnform,
    #            'sales_return_data': sales_return_data, 'srhp': srhp}
    # if request.POST:
    #     salesreturnform = SalesReturnForm(request.POST)
    #     if salesreturnform.is_valid():
    #         salesreturnform.save()
    #         return redirect('sales_return_product')
    #     else:
    #         return HttpResponse('error in form valid')

    # return render(request, 'sales/salesreturn.html', context)


def checkqty(prod, pr):
    total_qty = 0
    sales_ret = SalesReturn.objects.filter(sales=pr)
    for i in sales_ret:
        try:
            srhp = SalesReturn_has_product.objects.get(
                sales_return=i, product=prod)
            total_qty += srhp.qty
        except Exception as e:
            print(e)

    return total_qty

@login_required(login_url='login')
def sales_return_product(request, id):
    pur1 = SalesReturn.objects.latest('id')
    items = Sales_has_product.objects.filter(sales=pur1.sales)
    purchase = pur1
    sr_obj = SalesReturn.objects.filter(sales=pur1.sales)
    total_qty = []
    d = {}
    for i in items:
        total_qty.append(checkqty(i.product, pur1.sales))
    d = dict(zip(items, total_qty))
    context = {'items': items, 'pur1': pur1,
               'purchase': purchase, 'd': d.items()}
    return render(request, 'sales/sales_return_product.html', context)


@login_required(login_url='login')
def sales_ret_has_prod(request, id):
    pr = SalesReturn.objects.latest('id')
    prod = Sales_has_product.objects.get(id=id)
    product_form = SalesReturnProductForm(instance=prod)
    context = {'product_form': product_form, 'pr': pr}
    if request.POST:
        product_form = SalesReturnProductForm(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            price = product_form.cleaned_data['price']
            total_qty = checkqty(prod, pr.sales)
            product_prch = Sales_has_product.objects.get(
                sales=pr.sales, product=prod)
            if (total_qty+qty) > product_prch.qty:
                messages.warning(request, 'Insufficient stocks')
                return redirect('sales_return_product', pr.id)
            prhp, created = SalesReturn_has_product.objects.get_or_create(
                product=prod, sales_return=pr, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()
                #print('i am in created')
                updatestock_sales_return(prhp)
                print(created)
            else:
                prhp.qty += qty
                prhp.save()
                print('i am in php')
                check = True
                updatestock_sales_return(prhp, qty, check)
            return redirect('sales_return_product', pr.id)
        else:
            print('hello')
    return render(request, 'sales/sales_return_has_product.html', context)


# def sales_return_product(request,id):
#     sales_return_product_form = SalesReturnProductForm()
#     sales_return_id = SalesReturn.objects.get(id = id)
#     items = SalesReturn_has_product.objects.filter(
#         sales_return=sales_return_id)
#     context = {'sales_return_product_form': SalesReturnProductForm,
#                'items': items, 'sales_return_id': sales_return_id}
#     if request.POST:
#         sales_return_product_form = SalesReturnProductForm(request.POST)
#         if sales_return_product_form.is_valid():
#             prod = sales_return_product_form.cleaned_data['product']
#             qty = sales_return_product_form.cleaned_data['qty']
#             pid = sales_return_product_form.cleaned_data['sales_return']

#             shp, created = SalesReturn_has_product.objects.get_or_create(
#                 product=prod, sales_return=sales_return_id, defaults={"qty": qty})
#             if created:
#                 #purchase_prod = product_form.save()
#                 print('i am in created')
#                 updatestock_sales_return(shp)
#                 print(created)
#             else:
#                 shp.qty += qty
#                 shp.save()
#                 print('i am in php')
#                 check = True
#                 updatestock_sales_return(shp, qty, check)
#         return redirect('sales_return_product',id)
#     return render(request, 'sales/sales_return_product.html', context)


@login_required(login_url='login')
def delete_salesreturn(request, id):
    context = {}
    if request.POST:
        sales_return = SalesReturn.objects.get(id=id)

        prod = SalesReturn_has_product.objects.filter(
            sales_return=sales_return)
        stock = Stock.objects.filter(warehouse=sales_return.warehouse)
        s_lst, p_lst = [], []
        for s1 in stock:
            for pid in prod:
                if s1.product.id == pid.product.id:
                    s1.qty -= pid.qty
                    s1.save()
        sales_return.delete()
        return redirect('sales_return', sales_return.sales)

@login_required(login_url='login')
def delete_salesreturn_product(request, id):
    if request.POST:
        srhp = SalesReturn_has_product.objects.get(id=id)
        ware = SalesReturn.objects.get(id=srhp.sales_return.id)
        stock = Stock.objects.get(
            warehouse=ware.warehouse, product=srhp.product)
        stock.qty -= srhp.qty
        stock.save()
        srhp.delete()
        return redirect('update_sales_return', srhp.sales_return)
    return render(request, 'sales/delete_salesreturn_product.html')

@login_required(login_url='login')
def Update_Sales_Return(request, id):
    pd = SalesReturn.objects.get(id=id)
    prod_data = SalesReturn_has_product.objects.filter(sales_return=pd)
    w1_data = pd.warehouse
    form = SalesReturnForm(instance=pd)
    if request.POST:
        frm = SalesReturnForm(request.POST, instance=pd)
        if frm.is_valid():
            frm.save()
            return redirect("sales_return", pd.sales)
    context = {
        'pd': pd,
        'form': form,
        'product_data': prod_data
    }
    return render(request, 'sales/update_sales_return.html', context)

@login_required(login_url='login')
def update_sales_return_product(request, id):
    pur1 = SalesReturn.objects.get(id=id)
    global pr1
    pr1 = pur1
    items = Sales_has_product.objects.filter(sales=pur1.sales)
    purchase = pur1
    sr_obj = SalesReturn.objects.filter(sales=pur1.sales)
    total_qty = []
    d = {}
    for i in items:
        total_qty.append(checkqty(i.product, pur1.sales))
    d = dict(zip(items, total_qty))
    context = {'items': items, 'pur1': pur1,
               'purchase': purchase, 'd': d.items()}
    return render(request, 'sales/update_sales_return_product.html', context)

@login_required(login_url='login')
def update_sales_ret_has_prod(request, id):
    pr = globals()['pr1']
    prod = Sales_has_product.objects.get(id=id)
    product_form = SalesReturnProductForm(instance=prod)
    context = {'product_form': product_form, 'pr': pr}
    if request.POST:
        product_form = SalesReturnProductForm(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            price = product_form.cleaned_data['price']
            total_qty = checkqty(prod, pr.sales)
            product_prch = Sales_has_product.objects.get(
                sales=pr.sales, product=prod)
            if (total_qty+qty) > product_prch.qty:
                messages.warning(request, 'Insufficient stocks')
                return redirect('update_sales_return_product', pr.id)
            prhp, created = SalesReturn_has_product.objects.get_or_create(
                product=prod, sales_return=pr, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()
                #print('i am in created')
                updatestock_sales_return(prhp)
                print(created)
            else:
                prhp.qty += qty
                prhp.save()
                print('i am in php')
                check = True
                updatestock_sales_return(prhp, qty, check)
            return redirect('update_sales_return_product', pr.id)
        else:
            print('hello')
    return render(request, 'sales/update_sales_ret_has_prod.html', context)
