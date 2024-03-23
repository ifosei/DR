from django.urls import path
from .views import *

urlpatterns = [
    path('',base,name='base'),
    path('lvalues',l_values,name='lvalues'),
    path('fp1',fp1,name='fp1'),
    path('fp2',fp2,name='fp2'),
    path('dpf1f2',dpf1f2,name='dpf1f2'),
    path('dpf3',dpf3,name='dpf3'),
    path('dpf4',dpf4,name='dpf4'),
    path('results',results,name='results')

]
