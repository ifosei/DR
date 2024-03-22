from django.urls import path
from .views import *

urlpatterns = [
    path('',base,name='base'),
    path('lvalues',l_values,name='lvalues'),
    path('fp1',fp1,name='fp1'),
    path('fp2',fp2,name='fp2')
]