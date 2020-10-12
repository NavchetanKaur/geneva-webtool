"""geneva_webtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from geneva_app import views, views_g, views_gs

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Web services interface for GENEVA')

urlpatterns = [
	path('', views.geneva_home, name='geneva_home'),
    path('single_gene', views.single_gene, name='single_gene'),
    path('gene_set', views.gene_set, name='gene_set'),
	path('gene_table', views.gene_table, name='gene_table'),
    path('gene_set_table', views.gene_set_table, name='gene_set_table'),
    path('gse_description', views.gse_elab, name='gse_description'),
    path('gsig_gse_description', views.gene_sig_gse_elab, name='gene_sig_gse_elab'),
    path('license', views.license, name='license'),
    path('help', views.help, name='help'),
    path('admin/', admin.site.urls),
    path('gene_query/', views_g.GeneApiView.as_view(), name='gene_query'),
    path('gene_set_query/', views_gs.GeneSetApiView.as_view(), name='gene_set_query'),
    path('services', schema_view, name="geneva_services"),
]
