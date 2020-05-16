from django.urls import path, include
from .views.home import Home
from .views.base import (
    ListingView, CreateView, UpdateView, DeleteView, DetailView,
    InlineCreateView, InlineDeleteView, InlineUpdateView)
from .views.brewery import (BreweryCreateView, BreweryUpdateView,
                            BreweryDetailView)
from .views.person import PersonCreateView, PersonUpdateView, PersonDetailView
from .views.style import StyleDetailView
from .views.search import Search


urlpatterns = [

    path('auth/', include('django.contrib.auth.urls')),

    path('i18n/', include('django.conf.urls.i18n')),

    path('', Home.as_view(), name="home"),

    path('search', Search.as_view(), name="search"),

    # Non generic views
    #
    path('brewery/add/',
         BreweryCreateView.as_view(),
         name="create_brewery"),

    path('brewery/<int:pk>/edit',
         BreweryUpdateView.as_view(),
         name="edit_brewery"),

    path('brewery/<int:pk>',
         BreweryDetailView.as_view(),
         name="view_brewery"),

    path('person/<int:pk>',
         PersonDetailView.as_view(),
         name="view_person"),

    path('person/add/',
         PersonCreateView.as_view(),
         name="create_person"),

    path('person/<int:pk>/edit',
         PersonUpdateView.as_view(),
         name="edit_person"),

    path('style/<int:pk>',
         StyleDetailView.as_view(),
         name="view_style"),

    # Generic delete view
    #
    path('<str:model>/<int:pk>/delete',
         DeleteView.as_view(),
         name="delete"),

    # Generic listing
    #
    path('<str:model>/list',
         ListingView.as_view(),
         name="list"),

    # Generic detail view
    #
    path('<str:model>/<int:pk>',
         DetailView.as_view(),
         name="view"),

    # Generic add view
    #
    path('<str:model>/add/',
         CreateView.as_view(),
         name="create"),

    # Generic edit view
    #
    path('<str:model>/<int:pk>/edit',
         UpdateView.as_view(),
         name="edit"),

    # Generic inline add
    #
    path('<str:parent_model>/<int:parent_pk>/add_<str:model>',
         InlineCreateView.as_view(),
         name="inline_create"),

    # Generic inline edit
    #
    path('<str:parent_model>/<int:parent_pk>/edit_<str:model>/<int:pk>',
         InlineUpdateView.as_view(),
         name="inline_edit"),

    # Generic inline delete
    #
    path('<str:parent_model>/<int:parent_pk>/rm_<str:model>/<int:pk>',
         InlineDeleteView.as_view(),
         name="inline_delete"),
]
