from django.urls import path,include
from Admin import views
app_name="webadmin"

urlpatterns = [
    path('HomePage/',views.home_page,name='homepage'),

    path('AddHouse/',views.add_house,name='add_house'),
    path('AddHouseList/',views.add_houselist,name='add_houselist'),

    path('update_house/<int:did>',views.update_house,name='update_house'),
    path('delete_house/<int:did>',views.delete_house,name='delete_house'),



    path('Category/',views.category,name='Category'),
    
    path('CategoryList/',views.categorylist,name='categorylist'),

    path('update_category/<int:did>',views.update_category,name='update_category'),
    path('delete_category/<int:did>',views.delete_category,name='delete_category'),
    
    path('Report/',views.report,name='report'),
    path('ajaxreport/',views.ajaxreport,name="ajaxreport"),

    path('OwnersList/',views.ownerslist,name='ownerslist'),
    path('send_mail/<int:booking_id>/', views.send_booking_mail, name='send_mail'),

    path('logout/',views.logout,name='logout'),
    





    
   
]
