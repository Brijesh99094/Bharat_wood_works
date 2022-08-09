from django.urls import path
from . import views
from .views import Update_Purchase

urlpatterns = [

    path('purchase/', views.product_purchase_detail, name='purchase'),
    path('purchase_return/', views.purchase_return, name='purchase_return'),
    path('Updatepurchase/<int:id>', views.Update_Purchase, name='updatepurchase'),
    path('Updatepurchasereturn/<int:id>',
         views.Update_Purchase_Return, name='updatepurchasereturn'),
    path('Update_purchase_detail/<id>',
         views.Update_product_detail, name='update_product_detail'),
    path('add_product/', views.product_detail, name='pur_product'),
    path('warehouse/', views.warehouse, name='warehouse'),
    path('Updatewarehouse/<id>', views.Update_warehouse, name='update_warehouse'),
    path('stock/', views.stock, name='stock'),
    path('product/', views.product, name='product'),
    path('Deleteproduct/<id>', views.delete_product, name='delete_product'),
    path('Updateproduct/<id>', views.update_product, name='update_product'),
    path('delete/<id>', views.deletepurchase, name='delete_purchase'),
    path('deleteproduct/<id>', views.deleteproduct, name='deleteproduct'),
    path('purchasereturn/<id>', views.purchasereturn, name='purchasereturn'),
    path('purchasereturnproduct/<id>',
         views.purchase_return_product, name='pur_return_product'),
    path('pur_ret_has_prod/<id>', views.pur_ret_has_prod, name='pur_ret_has_prod'),
    path('deletereturnproduct/<id>', views.deletepurchase_return_product,
         name='deletereturnproduct'),
    path('deletepurchasereturn/<id>', views.deletepurchase_return,
         name='delete_purchase_return'),
    path('supplier/', views.supplier_view, name='supplier'),
    path('Update_supplier/<id>', views.update_supplier, name='update_supplier'),
    path('Delete_supplier/<id>', views.supplier_delete, name='deletesupplier'),
    path('UpdateReturnProductDetail/<id>', views.update_return_product_detail,
         name='update_return_product_detail'),
    path('Update_pur_ret_product/<id>/',
         views.update_pur_ret_product, name='update_pur_ret_product'),
    path('transportation/', views.transportation, name='transportation'),
    path('deletetrns/<id>', views.deletetrns, name='deletetrns'),
    path('update_trns/<id>', views.update_trns, name='update_trns'),





]
