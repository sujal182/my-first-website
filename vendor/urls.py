from django.urls import path , include
from .views import *

urlpatterns = [
    path('ven_reg/',registration_ven,name='ven_reg'),
    path('ven_login/',ven_login,name='ven_login'),
    path('add_pro/',add_pro,name='add_pro'),
    path('ven_index/',ven_index,name='ven_index'),
    path('update_pro/<int:id>',update_pro,name='update_pro'),

]