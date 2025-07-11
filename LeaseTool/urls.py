"""
URL configuration for LeaseTool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path ,include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('LeaseTool/',include('auth_system.urls')),
    path('LeaseTool/',include('tool.urls')),
    path('LeaseTool/',include('lessee.urls')),
    

]


urlpatterns += [    path('', lambda request: HttpResponse("""
        <html>
        <head><title>Welcome to LeaseTool</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>🔧 LeaseTool</h1>
            <h2>A complete end-to-end solution for lessors to track their tools efficiently.</h2>
            <p>To get started, please <a href='/LeaseTool/signup/'>Signup</a>.</p>
        </body>
        </html>
    """)),]