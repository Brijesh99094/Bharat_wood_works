from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Max, Count
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def updatestock(product_purchase, curr_qty=0, check=False):
    purchase_ware = Purchase.objects.get(id=product_purchase.purchase.id)
    ware = purchase_ware.warehouse
    s1 = Stock.objects.all()
    for st in s1:
        if ware == st.warehouse and product_purchase.product == st.product:
            stock = Stock.objects.get(
                warehouse=ware, product=product_purchase.product)
            if stock:
                if check == True:
                    stock.qty += curr_qty
                    stock.save()
                    break
                else:
                    stock.qty += product_purchase.qty
                    stock.save()
                    break
    else:
        s1, created = Stock.objects.update_or_create(
            warehouse=ware, product=product_purchase.product, qty=product_purchase.qty)


def purchase_return(request):

    pr = PurchaseReturn.objects.all()
    prhp = Purchase_Return_has_Product.objects.all()
    context = {'prhp': prhp, 'pr': pr}
    return render(request, 'purchase/purchase_return.html', context)


@login_required(login_url='login')
def product_purchase_detail(request):
    #pid = Purchase.objects.latest('id')
    #pid1 = pid.id +1
    pur = Purchase.objects.select_related(
        'warehouse', 'supplier').all().order_by('-purchase_date')
    php = Purchase_has_Product.objects.select_related(
        'purchase', 'product').all()
    shw = SupervisorHasWarehouse()
    if request.user.role == 'Supervisor':
        acc = Supervisor.objects.get(account=request.user)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=acc.id)
        # pur = Purchase.objects.select_related('warehouse', 'supplier').all().order_by('-purchase_date')
        # php = Purchase_has_Product.objects.select_related('purchase', 'product').all()

    form = PurchaseForm()
    context = {'form': form, 'pur': pur, 'php': php, 'shw': shw}
    if request.POST:
        form = PurchaseForm(request.POST)
        if form.is_valid():
            warehouse = form.cleaned_data['warehouse']
            form.save()
            return redirect('pur_product')
        else:
            return HttpResponse('error in form valid')
    return render(request, 'purchase/purchase_item.html', context)


@login_required(login_url='login')
def product_detail(request):
    product_form = PurchaseProductForm()

    purchase_id = Purchase.objects.latest('id')

    items = Purchase_has_Product.objects.filter(purchase=purchase_id)
    context = {'product_form': product_form,
               'items': items, 'purchase_id': purchase_id}
    if request.POST:
        product_form = PurchaseProductForm(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            pid = product_form.cleaned_data['purchase']
            price = product_form.cleaned_data['price']

            php, created = Purchase_has_Product.objects.get_or_create(
                product=prod, purchase=pid, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()

                updatestock(php)
                print(created)
            else:
                php.qty += qty
                php.save()

                check = True
                updatestock(php, qty, check)
        return redirect('pur_product')
    return render(request, 'purchase/add_item.html', context)


@login_required(login_url='login')
def deletepurchase(request, id):
    context = {}
    if request.POST:
        pur = Purchase.objects.get(id=id)
        pur_ret = PurchaseReturn.objects.filter(purchase=pur).count()
        if pur_ret > 0:
            messages.warning(
                request, 'You can not delete this. First delete all Returns of this purchase')
            return redirect('purchase')
        else:
            prod = Purchase_has_Product.objects.filter(purchase=pur)
            stock = Stock.objects.filter(warehouse=pur.warehouse)

        #stock1 = Stock.objects.filter(warehouse=pur.warehouse).values_list('product',flat=True)
        #prod1 =  Purchase_has_Product.objects.filter(purchase= pur).values_list('product',flat=True)
        #intersected_data = prod1.intersection(stock1)
        #################  intersaction ##############
            for s1 in stock:
                for pid in prod:
                    if s1.product.id == pid.product.id:
                        s1.qty -= pid.qty
                        s1.save()
            pur.delete()
            return redirect('purchase')
    return redirect('purchase')


@login_required(login_url='login')
def deleteproduct(request, id):
    if request.POST:
        php = Purchase_has_Product.objects.get(id=id)
        ware = Purchase.objects.get(id=php.purchase.id)
        stock = Stock.objects.get(
            warehouse=ware.warehouse, product=php.product)
        stock.qty -= php.qty
        stock.save()
        php.delete()
        return redirect('pur_product')


########################################################################################################
def updatestock2(product_purchase, curr_qty=0, check=False):
    purchase_ware = PurchaseReturn.objects.get(
        id=product_purchase.purchase_return.id)
    ware = purchase_ware.warehouse
    s1 = Stock.objects.all()
    for st in s1:
        if ware == st.warehouse and product_purchase.product == st.product:
            stock = Stock.objects.get(
                warehouse=ware, product=product_purchase.product)
            if stock:
                if check == True:
                    stock.qty -= curr_qty
                    stock.save()
                    break
                else:
                    stock.qty -= product_purchase.qty
                    stock.save()
                    break
    else:
        s1, created = Stock.objects.update_or_create(
            warehouse=ware, product=product_purchase.product, qty=product_purchase.qty)


@login_required(login_url='login')
def purchasereturn(request, id):
    purchaseObj = Purchase.objects.get(id=id)
    pr = PurchaseReturn.objects.filter(purchase=purchaseObj)
    prhp = Purchase_Return_has_Product.objects.all()

    truck_own = Transportation.objects.all()
    context = {'pid': purchaseObj, 't1': truck_own, 'prhp': prhp, 'pr': pr}
    if request.POST:
        pr_date = request.POST.get('purchase_return_date')

        pr_warehouse = request.POST.get('warehouse')

        ware = Warehouse.objects.get(warehouse_name=pr_warehouse)
        pr_supplier = request.POST.get('supplier')
        supp = Supplier.objects.get(supplier_name=pr_supplier)
        pr_truck_owner = request.POST.get('truck_owner')
        truckown = Transportation.objects.get(co_name=pr_truck_owner)
        pr_truck_no = request.POST.get('truck_no')
        pr_weight = request.POST.get('weight')
        #purchase_return = PurchaseReturn.objects.create(purchase_return_date=pr_date)
        # purchase_return.save()
        pr_obj = PurchaseReturn.objects.create(purchase_return_date=pr_date, purchase=purchaseObj,
                                               warehouse=ware, supplier=supp, truck_owner=truckown, truck_no=pr_truck_no, weight=pr_weight)
        pr_obj.save()
        prc = True
        pr_id = pr_obj.id
        print(pr_id)
        return redirect('pur_return_product', pr_id)
    return render(request, 'purchase/purchasereturn.html', context)


def checkqty(prod, pr):
    total_qty = 0
    purchase_ret = PurchaseReturn.objects.filter(purchase=pr.purchase)
    for i in purchase_ret:
        try:
            prhp = Purchase_Return_has_Product.objects.get(
                purchase_return=i, product=prod)
            total_qty += prhp.qty
        except Exception as e:
            print(e)

    return total_qty


@login_required(login_url='login')
def purchase_return_product(request, id):
    pur1 = PurchaseReturn.objects.latest('id')
    items = Purchase_has_Product.objects.filter(purchase=pur1.purchase)
    purchase = pur1.purchase
    pr_obj = PurchaseReturn.objects.filter(purchase=pur1.purchase)
    total_qty = []
    d = {}
    for i in items:
        total_qty.append(checkqty(i.product, pur1))
    d = dict(zip(items, total_qty))
    context = {'items': items, 'pur1': pur1,
               'purchase': purchase, 'd': d.items()}
    return render(request, 'purchase/add_item2.html', context)

    # for i in prhp:
    #     print(i.product,i.qty)


@login_required(login_url='login')
def pur_ret_has_prod(request, id):
    pr = PurchaseReturn.objects.latest('id')
    prod = Purchase_has_Product.objects.get(id=id)
    product_form = PurchaseReturnProductForm(instance=prod)
    context = {'product_form': product_form, 'pr': pr}
    if request.POST:
        product_form = PurchaseReturnProductForm(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            price = product_form.cleaned_data['price']
            total_qty = checkqty(prod, pr)
            product_prch = Purchase_has_Product.objects.get(
                purchase=pr.purchase, product=prod)
            if (total_qty+qty) > product_prch.qty:
                messages.warning(
                    request, 'Quantity should not be grater then purchase')
                return redirect('pur_return_product', id)
            prhp, created = Purchase_Return_has_Product.objects.get_or_create(
                product=prod, purchase_return=pr, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()
                #print('i am in created')
                updatestock2(prhp)
                print(created)
            else:
                prhp.qty += qty
                prhp.save()
                print('i am in php')
                check = True
                updatestock2(prhp, qty, check)
            return redirect('pur_return_product', id)
        else:
            print('hello')
    return render(request, 'purchase/purchase_return_product.html', context)


@login_required(login_url='login')
def deletepurchase_return(request, id):
    context = {}
    if request.POST:
        pur = PurchaseReturn.objects.get(id=id)
        prod = Purchase_Return_has_Product.objects.filter(
            purchase_return=pur).order_by('product')
        stock = Stock.objects.filter(
            warehouse=pur.warehouse).order_by('product')
        s_lst, p_lst = [], []
        for s1 in stock:
            for pid in prod:
                if s1.product.id == pid.product.id:
                    s1.qty += pid.qty
                    s1.save()
        pur.delete()
        return redirect('purchasereturn', pur.purchase)


@login_required(login_url='login')
def deletepurchase_return_product(request, id):
    if request.POST:
        phrp = Purchase_Return_has_Product.objects.get(id=id)
        ware = PurchaseReturn.objects.get(id=phrp.purchase_return.id)
        stock = Stock.objects.get(
            warehouse=ware.warehouse, product=phrp.product)
        stock.qty += phrp.qty
        stock.save()
        phrp.delete()
        return redirect('updatepurchasereturn', phrp.purchase_return.id)


@login_required(login_url='login')
def supplier_view(request):
    supp_form = SupplierForm()
    supplier_data = Supplier.objects.all()
    context = {'supplier': supp_form, 'supplier_data': supplier_data}
    if request.POST:
        supp_form = SupplierForm(request.POST)
        if supp_form.is_valid():
            messages.success(request, 'New supplier added')
            supp_form.save()
            return redirect('supplier')
    return render(request, 'purchase/supplier.html', context)


def update_supplier(request, id):
    supplier_data = Supplier.objects.get(id=id)
    supp_form = SupplierForm(instance=supplier_data)
    if request.POST:
        supp_form = SupplierForm(request.POST, instance=supplier_data)
        if supp_form.is_valid():
            supp_form.save()
            return redirect('supplier')


@login_required(login_url='login')
def supplier_delete(request, id):
    if request.POST:
        sup = Supplier.objects.get(id=id)
        messages.success(request, 'Supplier Removed')
        sup.is_active = False
        sup.save()
        return redirect('supplier')


@login_required(login_url='login')
def stock(request):
    stockform = StockForm()
    if request.user.role == 'Supervisor':
        s = Stock.objects.all()
        acc = Supervisor.objects.get(account=request.user)
        shw = SupervisorHasWarehouse.objects.filter(supervisor=acc.id)
        context = {'s': s, 'shw': shw, 'stockform': stockform}

    elif request.user.role == 'admin':
        shw = SupervisorHasWarehouse()
        s = Stock.objects.all()
        context = {'s': s, 'shw': shw, 'stockform': stockform}
    else:
        print("nothing")

    if request.POST:
        stockform = StockForm(request.POST)
        if stockform.is_valid():
            ware = stockform.cleaned_data['warehouse']
            prod = stockform.cleaned_data['product']
            qty = stockform.cleaned_data['qty']
            stock = Stock.objects.filter(warehouse=ware, product=prod).count()
            if stock == 1:
                stock = Stock.objects.get(
                    warehouse=ware, product=prod)
                if stock:
                    stock.qty += qty
                    stock.save()
            else:
                s1, created = Stock.objects.update_or_create(
                    warehouse=ware, product=prod, qty=qty)

            messages.success(request, 'Stock Added')
            return redirect('stock')
        else:
            messages.success(request, 'Please Select Something!!')
    return render(request, 'purchase/stock.html', context)


@login_required(login_url='login')
def product(request):
    context = {}
    prod_data = Product.objects.all().order_by('-id')
    productform = ProductForm()
    if request.POST:
        productform = ProductForm(request.POST)
        if productform.is_valid():
            prod = productform.cleaned_data['product_name']
            unit = productform.cleaned_data['unit']
            size = productform.cleaned_data['size']
            holes = productform.cleaned_data['holes']
            hole_size = productform.cleaned_data['hole_size']

            prod_data, created = Product.objects.get_or_create(
                product_name=prod,
                unit=unit,
                size=size,
                holes=holes,
                hole_size=hole_size,
            )
            if created:
                messages.success(request, "Product added")
            else:
                messages.warning(request, "Product already exist")

            return redirect('product')
    context = {'productform': productform, 'prod_data': prod_data}
    return render(request, 'purchase/add_product.html', context)


@login_required(login_url='login')
def delete_product(request, id):
    if request.POST:
        prod = Product.objects.get(id=id)
        prod.delete()
        messages.success(request, 'Product Removed')
        return redirect('product')


@login_required(login_url='login')
def update_product(request, id):
    product = Product.objects.get(id=id)
    up_form = ProductForm(instance=product)
    if request.POST:
        up_form = ProductForm(request.POST, instance=product)
        if up_form.is_valid():
            up_form.save()
            return redirect('product')
    return redirect('product')


@login_required(login_url='login')
def warehouse(request):
    context = {}
    warehouse_data = Warehouse.objects.all().order_by('-id')
    warehouseform = WarehouseForm()
    if request.POST:
        warehouseform = WarehouseForm(request.POST)
        if warehouseform.is_valid():
            try:
                w = Warehouse.objects.get(
                    warehouse_name=warehouseform.cleaned_data['warehouse_name'], area=warehouseform.cleaned_data['area'])
                messages.warning(request, "warehouse already exist!!!")
            except:
                print('Does not exist')
                warehouseform.save()

                return redirect('warehouse')
    context = {'warehouseform': warehouseform,
               'warehouse_data': warehouse_data}
    return render(request, 'purchase/warehouse.html', context)


def Update_warehouse(request, id):
    ware = Warehouse.objects.get(id=id)
    warehouseform = WarehouseForm(instance=ware)
    if request.POST:
        warehouseform = WarehouseForm(request.POST, instance=ware)
        if warehouseform.is_valid():
            warehouseform.save()
            return redirect('warehouse')


@login_required(login_url='login')
def Update_Purchase(request, id):
    pd = Purchase.objects.get(id=id)
    prod_data = Purchase_has_Product.objects.filter(purchase=pd)
    w1_data = pd.warehouse
    form = PurchaseForm(instance=pd)
    if request.POST:
        frm = PurchaseForm(request.POST, instance=pd)
        if frm.is_valid():

            frm.save()
            return redirect("purchase")
    context = {
        'pd': pd,
        'form': form,
        'product_data': prod_data
    }
    return render(request, 'purchase/update_purchase.html', context)


@login_required(login_url='login')
# Updatepurchasereturn ---url 'updatepurchasereturn'
def Update_Purchase_Return(request, id):
    pd = PurchaseReturn.objects.get(id=id)
    prod_data = Purchase_Return_has_Product.objects.filter(purchase_return=pd)
    w1_data = pd.warehouse
    form = PurchaseReturnForm(instance=pd)
    if request.POST:
        frm = PurchaseReturnForm(request.POST, instance=pd)
        if frm.is_valid():
            date = frm.cleaned_data['purchase_return_date']
            frm.save()
            return redirect("purchasereturn", pd.purchase)
    context = {
        'pd': pd,
        'form': form,
        'product_data': prod_data
    }
    return render(request, 'purchase/update_purchase_return.html', context)


pr1 = PurchaseReturn()
print(type(pr1))

###############################################################


@login_required(login_url='login')
def update_return_product_detail(request, id):
    pur1 = PurchaseReturn.objects.get(id=id)
    global pr1
    pr1 = pur1
    items = Purchase_has_Product.objects.filter(purchase=pur1.purchase)
    purchase = pur1.purchase
    pr_obj = PurchaseReturn.objects.filter(purchase=pur1.purchase)
    total_qty = []
    d = {}
    for i in items:
        total_qty.append(checkqty(i.product, pur1))
    d = dict(zip(items, total_qty))
    context = {'items': items, 'pur1': pur1,
               'purchase': purchase, 'd': d.items()}
    return render(request, 'purchase/update_add_item2.html', context)


@login_required(login_url='login')
def update_pur_ret_product(request, id):
    pr = globals()['pr1']
    print(pr)
    prod = Purchase_has_Product.objects.get(id=id)
    product_form = PurchaseReturnProductForm(instance=prod)
    context = {'product_form': product_form, 'pr': pr}
    if request.POST:
        product_form = PurchaseReturnProductForm(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            price = product_form.cleaned_data['price']
            total_qty = checkqty(prod, pr)
            product_prch = Purchase_has_Product.objects.get(
                purchase=pr.purchase, product=prod)
            if (total_qty+qty) > product_prch.qty:
                messages.warning(request, 'something goes wrong')
                return redirect('update_return_product_detail', pr.id)
            prhp, created = Purchase_Return_has_Product.objects.get_or_create(
                product=prod, purchase_return=pr, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()
                #print('i am in created')
                updatestock2(prhp)
                print(created)
            else:
                prhp.qty += qty
                prhp.save()
                print('i am in php')
                check = True
                updatestock2(prhp, qty, check)
            return redirect('update_return_product_detail', pr.id)
        else:
            print('hello')
    return render(request, 'purchase/update_pur_ret_has_prod.html', context)


@login_required(login_url='login')
def Update_product_detail(request, id):
    product_form = PurchaseProductForm()
    purchase_id = Purchase.objects.get(id=id)
    items = Purchase_has_Product.objects.filter(purchase=purchase_id)
    context = {'product_form': product_form,
               'items': items, 'purchase_id': purchase_id}
    if request.POST:
        product_form = PurchaseProductForm(request.POST)
        if product_form.is_valid():
            prod = product_form.cleaned_data['product']
            qty = product_form.cleaned_data['qty']
            pid = product_form.cleaned_data['purchase']
            price = product_form.cleaned_data['price']

            php, created = Purchase_has_Product.objects.get_or_create(
                product=prod, purchase=pid, defaults={"qty": qty, "price": price})
            if created:
                #purchase_prod = product_form.save()

                updatestock(php)
                print(created)
            else:
                php.qty += qty
                php.save()

                check = True
                updatestock(php, qty, check)
            return redirect('update_product_detail', id)
        else:
            return HttpResponse("hellow there ")

    return render(request, 'purchase/add_item.html', context)


def transportation(request):
    trns_form = TransportationForm()
    trns_data = Transportation.objects.all()
    area = Area.objects.all()

    context = {'trns_form': trns_form, 'area': area, 'trns_data': trns_data}
    if request.POST:
        trns_form = TransportationForm(request.POST)
        if trns_form.is_valid():
            messages.success(request, 'New data added')
            trns_form.save()
            return redirect('transportation')
    return render(request, 'purchase/transportation.html', context)


@login_required(login_url='login')
def deletetrns(request, id):
    if request.POST:
        sup = Transportation.objects.get(id=id)
        messages.success(request, 'Removed')
        sup.is_active = False
        sup.save()
        return redirect('transportation')


def update_trns(request, id):
    trns_data = Transportation.objects.get(id=id)
    trns_form = TransportationForm(instance=trns_data)
    if request.POST:
        trns_data = TransportationForm(request.POST, instance=trns_data)
        if trns_data.is_valid():
            trns_data.save()
            return redirect('transportation')
        else:
            print("form has error")
