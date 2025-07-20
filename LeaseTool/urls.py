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


from django.http import HttpResponse
from django.urls import path

urlpatterns += [
    path('', lambda request: HttpResponse("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Welcome to LeaseTool</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    background-color: #f0f4f8;
                    color: #333;
                }
                .container {
                    padding: 100px 20px;
                }
                h1 {
                    font-size: 48px;
                    color: #2c3e50;
                }
                h2 {
                    font-size: 24px;
                    color: #34495e;
                    margin-bottom: 40px;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                    font-weight: 500;
                }
                a:hover {
                    text-decoration: underline;
                }
                .footer {
                    margin-top: 60px;
                    font-size: 14px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔧 LeaseTool</h1>
                <h2>A complete end-to-end solution for lessors to track their tools efficiently.</h2>
                
                <p>To get started, please <a href='/LeaseTool/signup/'>Signup</a>.</p>

                <div style="margin-top: 40px;"></div>

                <p>Or, you can <a href='https://github.com/Darshan93027/LeaseTool.git' target="_blank">check out the GitHub repo</a>.</p>
                
                <div style="margin-top: 40px;"></div>

                <p>Contact me at <a href='mailto:contactdarshan07@email.com'>contactdarshan07@email.com</a></p>

                <div class="footer">
                    Developed by Darshan Sharma
                </div>
            </div>
        </body>
        </html>
    """)),
]
