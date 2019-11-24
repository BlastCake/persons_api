from django.urls import path
from .views import PersonCreateView, PersonsIdsListView, PersonDetailView, CompareVectorsView



urlpatterns = [

    path('person/create/', PersonCreateView.as_view()),
    path('person/detail/<str:id>/', PersonDetailView.as_view()),
    path('persons/compare/usr_1=<str:id1>&usr_2=<str:id2>/', CompareVectorsView.as_view()),
    path('persons/', PersonsIdsListView.as_view()),

]
