from django.shortcuts import render, redirect
from .models import *
from inventory.models import Company, Supervisor
from .forms import *
from purchase.models import Stock, SupervisorHasCompany, SupervisorHasWarehouse
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

# Create your views here.


def update_wtp_stock(php, curr_qty=0, check1=False):

    wtp = Warehouse_To_Plant.objects.get(id=php.warehouse_to_plant.id)
    stk = Stock.objects.get(warehouse=wtp.warehouse, product=php.product)
    s1 = plant_Stock.objects.all()

    for st in s1:
        if wtp.plant == st.plant and php.product == st.product and stk.warehouse == wtp.warehouse and stk.product == st.product:
            pstock = plant_Stock.objects.get(
                plant=wtp.plant, product=php.product)
            if stk:
                if check1 == True:

                    stk.qty -= curr_qty
                    stk.save()
                    pstock.qty += curr_qty
                    pstock.save()
                    print('sagar was here as a true.')
                    break
                else:
                    stk.qty -= php.qty
                    stk.save()
                    pstock.qty += php.qty
                    pstock.save()

                    print('sagar was here as a false.')
                    break
    else:
        s1, created = plant_Stock.objects.update_or_create(
            plant=wtp.plant, product=php.product, qty=php.qty)
        stk.qty -= s1.qty
        stk.save()


def update_plant_stock(php, curr_qty=0, check=False):
    wtp = DispatchDetail.objects.get(id=php.id)
    plt = Dispatch.objects.get(id=wtp.dispatch.id)
    s1 = plant_Stock.objects.all()

    for st in s1:
        if plt.plant == st.plant and php.product == st.product:
            pstock = plant_Stock.objects.get(
                plant=plt.plant, product=php.product)
            if check == True:
                pstock.qty -= curr_qty
                pstock.save()
                print('sagar was here as a true.')
                break
            else:
                pstock.qty -= php.qty
                pstock.save()
                print('sagar was here as a false.')
                break
    else:
        return HttpResponse('Error while updating plant stock.')

def dispatch_del_update_plant_stock(php):
    wtp = DispatchDetail.objects.get(id=php.id)
    plt = Dispatch.objects.get(id=wtp.dispatch.id)
    s1 = plant_Stock.objects.all()

    for st in s1:
        if plt.plant == st.plant and php.product == st.product:
            pstock = plant_Stock.objects.get(plant=plt.plant, product=php.product)
            pstock.qty += php.qty
            pstock.save()
            print('sagar was here as a false.')
            break
    else:
        return HttpResponse('Error while updating plant stock.')



def dispatch(request):

    sales_form = Dispatch_Form()
    cust = Customer.objects.all()
    dis = Dispatch.objects.all()
    dhp = DispatchDetail.objects.all()

    context = {'salesform': sales_form,
               'cust': cust, 'sales_data': dis, 'shp': dhp}
    if request.POST:
        sales_form = Dispatch_Form(request.POST)
        print("sagar was in collection .")
        if sales_form.is_valid():
            frm = sales_form.save()
            wtp_id = frm.id

            return redirect('dispatch_detail', wtp_id)
        else:
            print("form has error")

    return render(request, 'dispatch/dispatch_home.html', context)


def dispatch_detail(request, id):
    dispatch_detailForm = DispatchDetail_Form()
    did = Dispatch.objects.get(id=id)
    d = DispatchDetail.objects.filter(dispatch=did.id)
    context = {'dispatch_detailForm': dispatch_detailForm, 'did': did, 'd': d}
    if request.POST:
        dispatch_detailForm = DispatchDetail_Form(request.POST)
        if dispatch_detailForm.is_valid():
            prod = dispatch_detailForm.cleaned_data['product']
            qty = dispatch_detailForm.cleaned_data['qty']
            pid = dispatch_detailForm.cleaned_data['dispatch']
            p1 = plant_Stock.objects.get(plant=did.plant,product=prod)
            if qty > p1.qty:
                messages.warning(request,"not enough stock to dispatch")
                return redirect('dispatch_detail', id)

            php, created = DispatchDetail.objects.get_or_create(
                product=prod, dispatch=pid, defaults={"qty": qty})
            if created:
                # purchase_prod = product_form.save()
                update_plant_stock(php)
                print(created)
            else:
                php.qty += qty
                php.save()
                update_plant_stock(php, qty, check=True)
                check = True

        return redirect('dispatch_detail', id)

    return render(request, "dispatch/dispatch_detail.html", context)


def del_dispatch(request, id):
    if request.POST:
        dObj = Dispatch.objects.get(id=id)
        dProd = DispatchDetail.objects.filter(dispatch=dObj)
        col = Collection.objects.filter(dispatch=dObj).count()
        if col > 0:
            messages.warning(request,"Delete All Collection Of  This Dispatch")
            return redirect('dispatch')
        else:
            for i in dProd:
                dispatch_del_update_plant_stock(i)
            dObj.delete()
            messages.warning(request,"Dispatch deleted")
            return redirect('dispatch')

def del_coll(request,id):
    if request.POST:
        col = Collection.objects.get(id=id) 
        cold = CollectionDetail.objects.filter(collection=col)
        stk = Stock.objects.filter(warehouse=col.warehouse)
        for s1 in stk:
            for pid in cold:
                if s1.product.id == pid.product.id:
                    s1.qty -= pid.qty
                    s1.save()
        col.delete()
        return redirect('collection',col.dispatch.id)



def update_dispatch(request, id):
    dObj = Dispatch.objects.get(id=id)
    sales_form = Dispatch_Form(instance=dObj)
    cust = Customer.objects.all()
    dis = Dispatch.objects.all()
    dhp = DispatchDetail.objects.filter(dispatch=dObj)
    context = {'salesform': sales_form, 'cust': cust,
               'sales_data': dis, 'shp': dhp, 'dObj': dObj}
    if request.POST:
        sales_form = Dispatch_Form(request.POST, instance=dObj)
        if sales_form.is_valid():
            sales_form.save()
            return redirect('dispatch')
        else:
            return HttpResponse('Form has error')
    return render(request, "dispatch/update_dispatch.html", context)


def update_dispatch_detail(request,id):
    dispatch_detailForm = DispatchDetail_Form()
    did = Dispatch.objects.get(id=id)
    d = DispatchDetail.objects.filter(dispatch=did.id)
    context = {'dispatch_detailForm': dispatch_detailForm, 'did': did, 'd': d}
    if request.POST:
        dispatch_detailForm = DispatchDetail_Form(request.POST)
        if dispatch_detailForm.is_valid():
            prod = dispatch_detailForm.cleaned_data['product']
            qty = dispatch_detailForm.cleaned_data['qty']
            pid = dispatch_detailForm.cleaned_data['dispatch']
            print(prod,qty,pid)
            php, created = DispatchDetail.objects.get_or_create(
                product=prod, dispatch=pid, defaults={"qty": qty})
            if created:
                #purchase_prod = product_form.save()

                print(created)
            else:
                php.qty += qty
                php.save()

                check = True
            return redirect('update_dispatch_detail',id)
        else:
            return HttpResponse('form has error')
    return render(request,"dispatch/update_dispatch_detail.html",context)


def collection_to_warehouse(php, curr_qty=0, check=False):
    col = Collection.objects.get(id=php.collection.id)
    s1 = Stock.objects.all()
    for st in s1:
        if col.warehouse == st.warehouse and php.product == st.product:
            stock = Stock.objects.get(warehouse=col.warehouse, product=php.product)
            if stock:
                if check == True:
                    stock.qty += curr_qty
                    stock.save()
                    break
                else:
                    stock.qty += php.qty
                    stock.save()
                    break
    else:   
        s1, created = Stock.objects.update_or_create(
            warehouse=col.warehouse,product=php.product, qty=php.qty)

def deleteproduct_dispatch(request,id):
    if request.POST:
        dd = DispatchDetail.objects.get(id=id)
        dis = Dispatch.objects.get(id=dd.dispatch.id)
        plt = plant_Stock.objects.get(plant=dis.plant,product=dd.product)
        if plt:
            plt.qty += dd.qty
            plt.save()
        dd.delete()
        return redirect('update_dispatch_detail',dis.id)




def collection(request,id):
    saless_form = Collection_Form()
    cust = Customer.objects.all()
    dis_id = Dispatch.objects.get(id=id)
    collection = Collection.objects.filter(dispatch=dis_id)
    chp = CollectionDetail.objects.all()
    context = {'salessform': saless_form, 'cust': cust,
               'sales_dataa': collection, 'shpp': chp,'dis':dis_id}
    if request.POST:
        print("sagar was in collection .")
        saless_form = Collection_Form(request.POST)
        if saless_form.is_valid():
            frm = saless_form.save()
            wtpp_id = frm.id
            return redirect('collection_detail', wtpp_id)
        else:
            print("form has error")
    return render(request, 'dispatch/collection.html', context)


def checkqty(prod, pr):
    total_qty = 0
    purchase_ret = Collection.objects.filter(dispatch=pr.dispatch)
    for i in purchase_ret:
        try:
            prhp = CollectionDetail.objects.get(
                collection=i, product=prod)
            total_qty += prhp.qty
        except Exception as e:
            print(e)

    return total_qty



def collection_detail(request, id):
    cl = Collection.objects.get(id=id)
    pur1 = Collection.objects.latest('id')
    items = DispatchDetail.objects.filter(dispatch=pur1.dispatch)
    purchase = pur1.dispatch
    pr_obj = Collection.objects.filter(dispatch=pur1.dispatch)
    total_qty = []
    d = {}
    for i in items:
        total_qty.append(checkqty(i.product, pur1))
    d = dict(zip(items, total_qty))
    context = {'items': items, 'pur1': pur1,
               'purchase': purchase, 'd': d.items()}
    return render(request, 'dispatch/collection_detail.html', context)


def col_has_product(request,id):
    pr = Collection.objects.latest('id')
    prod = DispatchDetail.objects.get(id=id)
    dispatch_detailForm = CollectionDetail_Form(instance=prod)
    #d = CollectionDetail.objects.filter(collection=did.id)
    context = {'dispatch_detailForm': dispatch_detailForm, 'pr': pr,}
    if request.POST:
        dispatch_detailForm = CollectionDetail_Form(request.POST)
        if dispatch_detailForm.is_valid():
            prod = dispatch_detailForm.cleaned_data['product']
            qty = dispatch_detailForm.cleaned_data['qty']
            pid = dispatch_detailForm.cleaned_data['collection']
            total_qty = checkqty(prod, pr)
            product_prch = DispatchDetail.objects.get(
                dispatch=pr.dispatch, product=prod)
            if (total_qty+qty) > product_prch.qty:
                messages.warning(request, 'Quantity should not be grater then Dispatch')
                return redirect('col_has_product', id)
            php, created = CollectionDetail.objects.get_or_create(
                product=prod, collection=pid, defaults={"qty": qty})
            if created:
                # purchase_prod = product_form.save()
                collection_to_warehouse(php)
                print(created)
            else:
                php.qty += qty
                php.save()
                check = True
                collection_to_warehouse(php,qty,check)
        return redirect('collection_detail', pr.id)

    return render(request, "dispatch/col_has_product.html", context)


def update_collection(request,id):
    col = Collection.objects.get(id=id)
    saless_form = Collection_Form(instance=col)
    cust = Customer.objects.all()
    collection = Collection.objects.all()
    chp = CollectionDetail.objects.all()
    context = {'salessform': saless_form, 'cust': cust,'sales_data': collection, 'shp': chp,'col':col}
    if request.POST:
        print("sagar was in collection .")
        saless_form = Collection_Form(request.POST,instance=col)
        print(saless_form)
        if saless_form.is_valid():
            saless_form.save()
            return redirect('collection',col.dispatch.id)
        else:
            print("form has error")
    return render(request, 'dispatch/update_collection.html', context)

def update_collection_detail(request,id):
    pur1 = Collection.objects.get(id=id)
    items = DispatchDetail.objects.filter(dispatch=pur1.dispatch)
    purchase = pur1.dispatch
    pr_obj = Collection.objects.filter(dispatch=pur1.dispatch)
    total_qty = []
    d = {}
    for i in items:
        total_qty.append(checkqty(i.product, pur1))
    d = dict(zip(items, total_qty))
    context = {'items': items, 'pur1': pur1,
               'purchase': purchase, 'd': d.items()}
    return render(request, 'dispatch/update_collection_detail.html', context)


def update_col_has_product(request,id):
    pr = Collection.objects.latest('id')
    prod = DispatchDetail.objects.get(id=id)
    dispatch_detailForm = CollectionDetail_Form(instance=prod)
    #d = CollectionDetail.objects.filter(collection=did.id)
    context = {'dispatch_detailForm': dispatch_detailForm, 'pr': pr,}
    if request.POST:
        dispatch_detailForm = CollectionDetail_Form(request.POST)
        if dispatch_detailForm.is_valid():
            prod = dispatch_detailForm.cleaned_data['product']
            qty = dispatch_detailForm.cleaned_data['qty']
            pid = dispatch_detailForm.cleaned_data['collection']
            total_qty = checkqty(prod, pr)
            product_prch = DispatchDetail.objects.get(
                dispatch=pr.dispatch, product=prod)
            if (total_qty+qty) > product_prch.qty:
                messages.warning(request, 'Quantity should not be grater then Dispatch')
                return redirect('update_col_has_product', id)
            php, created = CollectionDetail.objects.get_or_create(
                product=prod, collection=pid, defaults={"qty": qty})
            if created:
                # purchase_prod = product_form.save()
                collection_to_warehouse(php)
                print(created)
            else:
                php.qty += qty
                php.save()
                check = True
                collection_to_warehouse(php,qty,check)
        return redirect('update_collection_detail', pr.id)

    return render(request, "dispatch/col_has_product.html", context)

def plant(request, id):
    shw = PlantForm()
    print(id)
    com = Company.objects.get(id=id)
    objshw = Plant.objects.filter(company=com)
    context = {'shw': shw, 'objshw': objshw, 'com': com}
    if request.POST:
        shw = PlantForm(request.POST)
        if shw.is_valid():
            data = shw.cleaned_data['plant_name']
            area = shw.cleaned_data['area']
            company = shw.cleaned_data['company']
            obj1 = Plant.objects.create(
                plant_name=data, area=area, company=company)
            obj1.save()
        else:
            print("form has error")
    return render(request, 'dispatch/plant.html', context)


def delete_assigned_plant(request, id):
    if request.POST:
        acc = Plant.objects.get(id=id)
        com = Company.objects.get(id=acc.company.id)
        acc.delete()
        return redirect('update_plant', com.id)


def update_plant(request, id):
    shw = PlantForm()
    com = Company.objects.get(id=id)
    objshw = Plant.objects.filter(company=com)
    context = {'shw': shw, 'objshw': objshw, 'com': com}
    if request.POST:
        shw = PlantForm(request.POST)
        if shw.is_valid():
            data = shw.cleaned_data['plant_name']
            area = shw.cleaned_data['area']
            company = shw.cleaned_data['company']
            obj1 = Plant.objects.create(
                plant_name=data, area=area, company=company)
            obj1.save()
        else:
            print("form has error")

    return render(request, 'dispatch/update_plant.html', context)


def warehouse_to_plant(request):
    wtp = Warehouse_To_Plant_Form()
    wtps = Warehouse_To_Plant.objects.all()
    wtpd = Warehouse_To_Plant_Detail.objects.all()
    shw = SupervisorHasWarehouse()
    shc = SupervisorHasCompany()
    prod = Product.objects.filter(product_name='pvc')
    plt = Plant()
    if request.user.role == 'Supervisor':
        acc = Supervisor.objects.get(account=request.user)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=acc.id)
        shc = SupervisorHasCompany.objects.filter(supervisor=acc.id)
        plt = Plant.objects.all()

    context = {'wtps': wtps, 'wtp': wtp, 'wtpd': wtpd,
               'shw': shw, 'shc': shc, 'plt': plt, 'prod': prod}
    if request.POST:
        wtp = Warehouse_To_Plant_Form(request.POST)
        if wtp.is_valid():

            frm = wtp.save()
            wtp_id = frm.id
            return redirect('warehouse_to_plant_product_detail', wtp_id)
        else:
            print("form has error")
    return render(request, 'dispatch/warehouse_to_plant.html', context)


def warehouse_to_plant_product_detail(request, id):
    context = {}
    product_form = Warehouse_To_Plant_Detail_Form()
    wtp_id = Warehouse_To_Plant.objects.get(id=id)
    prod = Stock.objects.filter(warehouse=wtp_id.warehouse)
    items = Warehouse_To_Plant_Detail.objects.filter(warehouse_to_plant=wtp_id)
    context = {'product_form': product_form,
               'items': items, 'wtp_id': wtp_id, 'prod': prod}
    if request.POST:
        product_form = Warehouse_To_Plant_Detail_Form(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            pid = product_form.cleaned_data['warehouse_to_plant']
            stk = Stock.objects.get(warehouse=wtp_id.warehouse, product=prod)
            if stk.qty < qty:
                messages.warning(request, 'હવે ટ્રાન્સફર કરવા માટે સ્ટોક નથી.')
                return redirect('warehouse_to_plant_product_detail', id)
            wtp = Warehouse_To_Plant.objects.get(id=pid.id)
            php, created = Warehouse_To_Plant_Detail.objects.get_or_create(
                product=prod, warehouse_to_plant=pid, defaults={"qty": qty})

            if created:
                # purchase_prod = product_form.save()
                update_wtp_stock(php)
            else:
                php.qty += qty
                php.save()
                check1 = True
                update_wtp_stock(php,qty, check1)
        return redirect('warehouse_to_plant_product_detail', id)
    return render(request, 'dispatch/warehouse_to_plant_detail.html', context)


def update_warehouse_to_plant_product_detail(request, id):
    context = {}
    product_form = Warehouse_To_Plant_Detail_Form()
    wtp_id = Warehouse_To_Plant.objects.get(id=id)
    prod = Stock.objects.filter(warehouse=wtp_id.warehouse)
    items = Warehouse_To_Plant_Detail.objects.filter(warehouse_to_plant=wtp_id)
    context = {'product_form': product_form,
               'items': items, 'wtp_id': wtp_id, 'prod': prod}
    if request.POST:
        product_form = Warehouse_To_Plant_Detail_Form(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            pid = product_form.cleaned_data['warehouse_to_plant']
            stk = Stock.objects.get(warehouse=wtp_id.warehouse, product=prod)
            if stk.qty < qty:
                messages.warning(
                    request, 'હવે ટ્રાન્સફર કરવા માટે સ્ટોક નથી . ')
                return redirect('update_warehouse_to_plant_product_detail', id)
            wtp = Warehouse_To_Plant.objects.get(id=pid.id)
            php, created = Warehouse_To_Plant_Detail.objects.get_or_create(
                product=prod, warehouse_to_plant=pid, defaults={"qty": qty})

            if created:
                # purchase_prod = product_form.save()

                update_wtp_stock(php)
            else:
                php.qty += qty
                php.save()
                check = True
                update_wtp_stock(php, qty, check)
        return redirect('update_warehouse_to_plant_product_detail', id)
    return render(request, 'dispatch/update_warehouse_to_plant_detail.html', context)


def Update_warehouse_to_plant(request, id):
    wtps = Warehouse_To_Plant.objects.get(id=id)
    wtp = Warehouse_To_Plant_Form(instance=wtps)
    wtpd = Warehouse_To_Plant_Detail.objects.filter(warehouse_to_plant=id)
    shw = SupervisorHasWarehouse()
    if request.user.role == 'Supervisor':
        acc = Supervisor.objects.get(account=request.user)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=acc.id)
    context = {'wtps': wtps, 'wtp': wtp, 'wtpd': wtpd, 'shw': shw}
    if request.POST:
        wtp = Warehouse_To_Plant_Form(request.POST, instance=wtps)
        if wtp.is_valid():
            frm = wtp.save()
            wtp_id = frm.id
            return redirect('warehouse_to_plant')
        else:
            print("form has error")
    return render(request, 'dispatch/update_warehouse_to_plant.html', context)


def Delete_wtp(request, id):
    if request.POST:
        pur = Warehouse_To_Plant.objects.get(id=id)
        prod = Warehouse_To_Plant_Detail.objects.filter(warehouse_to_plant=pur)
        stock = Stock.objects.filter(warehouse=pur.warehouse)
        plantStock = plant_Stock.objects.filter(plant=pur.plant)

        # stock1 = Stock.objects.filter(warehouse=pur.warehouse).values_list('product',flat=True)
        # prod1 =  Purchase_has_Product.objects.filter(purchase= pur).values_list('product',flat=True)
        # intersected_data = prod1.intersection(stock1)
        #################  intersaction ##############
        s_lst, p_lst = [], []
        for s1 in stock:
            for pid in prod:
                if s1.product.id == pid.product.id:
                    s1.qty += pid.qty
                    s1.save()
        for s1 in plantStock:
            for pid in prod:
                if s1.product.id == pid.product.id:
                    s1.qty -= pid.qty
                    s1.save()
        pur.delete()

        return redirect('warehouse_to_plant')
    return redirect('warehouse_to_plant')


def deleteproduct_wtp(request, id):

    if request.POST:
        php = Warehouse_To_Plant_Detail.objects.get(id=id)
        ware = Warehouse_To_Plant.objects.get(id=php.warehouse_to_plant.id)
        stock = Stock.objects.get(
            warehouse=ware.warehouse, product=php.product)
        stock.qty += php.qty
        stock.save()
        plantStock = plant_Stock.objects.get(
            plant=ware.plant, product=php.product
        )
        plantStock.qty -= php.qty
        plantStock.save()

        php.delete()
        messages.error(request, "Product deleted.")
        return redirect('update_warehouse_to_plant_product_detail', ware.id)


def deleteproduct_wtp2(request, id):

    if request.POST:
        php = Warehouse_To_Plant_Detail.objects.get(id=id)
        ware = Warehouse_To_Plant.objects.get(id=php.warehouse_to_plant.id)
        stock = Stock.objects.get(
            warehouse=ware.warehouse, product=php.product)
        stock.qty += php.qty
        stock.save()
        plantStock = plant_Stock.objects.get(
            plant=ware.plant, product=php.product
        )
        plantStock.qty -= php.qty
        plantStock.save()

        php.delete()
        messages.error(request, "Product deleted.")
        return redirect('warehouse_to_plant_product_detail', ware.id)


def plantstock(request):
    stockform = plant_StockForm()
    if request.user.role == 'Supervisor':
        s = plant_Stock.objects.all()
        acc = Supervisor.objects.get(account=request.user)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=acc.id)
        context = {'s': s, 'shw': shw, 'stockform': stockform}

    elif request.user.role == 'admin':
        shw = SupervisorHasWarehouse()
        s = plant_Stock.objects.all()
        context = {'s': s, 'shw': shw, 'stockform': stockform}
    else:
        return HttpResponse("nothing")

    if request.POST:
        stockform = plant_StockForm(request.POST)
        if stockform.is_valid():
            ware = stockform.cleaned_data['plant']
            prod = stockform.cleaned_data['product']
            qty = stockform.cleaned_data['qty']
            stock = plant_Stock.objects.filter(
                plant=ware, product=prod).count()
            if stock == 1:
                stock = plant_Stock.objects.get(
                    plant=ware, product=prod)
                if stock:
                    stock.qty += qty
                    stock.save()
            else:
                s1, created = plant_Stock.objects.update_or_create(
                    plant=ware, product=prod, qty=qty)

            messages.success(request, 'Stock Added')
            return redirect('plantstock')
        else:
            messages.success(request, 'Please Select Something!!')
    return render(request, 'dispatch/plant_stock.html', context)




def checkqty_list(prod, pr):
    total_qty = 0
    purchase_ret = Collection.objects.filter(dispatch=pr)
    for i in purchase_ret:
            try:
                prhp = CollectionDetail.objects.get(
                    collection=i, product=prod)
                total_qty += prhp.qty
            except Exception as e:
                print("")

    return total_qty


def dis_list(request,id):
    cst = Customer.objects.get(id=id)
    d1 = Dispatch.objects.filter(customer=cst)
    dd = DispatchDetail.objects.all()
    total_qty = []
    prod_lst = []
    d = {}
    for dispatch in d1:
        for dis_detail in dd:
            if dispatch == dis_detail.dispatch:
                prod_lst.append(dis_detail)
                total_qty.append(checkqty_list(dis_detail.product,dispatch ))
   
    d = dict(zip(prod_lst,total_qty))
        
    context={
        'cst':cst,
        'd1':d1,
        'items':dd,
        'd':d.items()
    }
    return render(request,'dispatch/summary_detail.html',context)
    