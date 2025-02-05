from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from pfm import views
from django.contrib.auth import views as vi
urlpatterns=[
 
    path('', views.accueil, name='index'),
    path('login', views.logIn, name='login'),
    path('home',views.home,name="home"),
    path('logout',views.logOut,name="logout"),    
    
    
    path('register',views.register,name='register'),
    path('registerEmploye',views.registerEmploye,name='registerEmploye'),
    path('registervechule',views.registervoiture,name='registervechule'),


    path('show',views.show,name="show"),
    path('showemploye',views.showemploye,name="showemploye"),

    
    path('edit/<int:id>', views.edit),
    path('editemploye/<int:id>', views.editEmploye),


    path('update/<int:id>/', views.update,name='user_update'),
    path('updateEmploye/<int:id>/', views.updateEmploye,name='employe_update'),

    
    path('lievechule/<int:id>/', views.affectation,name='lievechule'),

    path('confirm-delete/<int:id>/', views.confirm_delete, name='confirm_delete'),

    path('destroy/<int:id>/',views.destroy, name='destroy'),
    path('deleteEmploye/<int:id>/',views.destroyEmploye, name='employe_delete'),
    path('deletevechule/<int:id>/',views.destroyvechule, name='deletevechule'),

    path('view/<int:id>',views.view, name='view'),  
    path('viewemploye/<int:id>',views.viewemploye, name='viewemploye'),  
    path('lieviewvechule/<int:id>',views.viewvechule, name='lieviewvechule'),  

    
    path('modifiemotdepasse',views.changepassword,name='modifiemotdepasse'),

    path('dashbord',views.showdashboard,name="dashboard"),
    path('managerequest',views.managerequest,name="managerequest"),
    path('vechulefleet',views.vehicles_for_client,name="vechulefleet"),
    path('viewClient/<int:id>',views.remplacement, name='viewClient'),  
    path('historiqueclient',views.historique,name="historiqueclient"),
    
    path('historique_request',views.historique_request,name="historique_request"),

    path('dashboardemploye',views.dashboardemploye,name="dashboardemploye"),
    path('clientvechule',views.clientvechule,name="clientvechule"),
    path('avaiblevechule',views.avaiblevechule,name="avaiblevechule"),
    path('viewrequest',views.requestview,name="viewrequest"),
    path('remplacemnt_view/<int:id>',views.remplacemnt_view,name="remplacemnt_view"),
    path('remplacemnt_view/remplacevechule/<int:id>/<int:rempl_id>',views.remplacevechule,name="remplacevechule"),



    path('reset_password',vi.PasswordResetView.as_view(template_name="pfm/test/password_reset.html"),name='rest_password'),
    path('rest_password_send',vi.PasswordResetDoneView.as_view(template_name="pfm/test/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>',vi.PasswordResetConfirmView.as_view(template_name="pfm/test/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete',vi.PasswordResetCompleteView.as_view(template_name="pfm/test/password_reset_done.html"),name="password_reset_complete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
