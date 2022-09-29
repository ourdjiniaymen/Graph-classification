from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda request: redirect('kernels/', permanent=True)),
    path('datasets/',views.getDatasets),
    path('kernels/',views.getKernels),
    path('logs/',views.getResults),
    path('add_evaluation/',views.addEvaluation),
]
