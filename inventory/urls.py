from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('add1/', views.add1, name='add1'),
    path('add2/<int:key>', views.add2, name='add2'),
    path('register/', views.register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('addExisting/<int:key>', views.addExisting, name='addExisting'),
    path('allocate/<int:key>', views.allocate, name='allocate'),
    path('delete/<int:key>',views.delete,name='delete'),
    path('edit/<int:key>',views.edit,name='edit'),
    path('createroom/',views.createroom,name='createroom'),
    path('createfloor/',views.createfloor,name='createfloor'),
    path('createSubitems/<int:key>',views.createSubItem,name='createSubItem'),
    path('createCategory/',views.createCategory,name='createCategory'),
    path('logoutPrompt/',views.logoutPrompt,name='logoutPrompt'),
    path('advancedSearch/',views.advancedSearch,name='advancedSearch'),
    path('downloadCSV/<int:key>',views.downloadCSV,name='downloadCSV'),
    path('chooseCategory/',views.chooseCategory,name='chooseCategory'),
    path('settings/',views.settings,name='settings'),
    path('deletefloor/',views.deletefloor,name='deletefloor'),
    path('showRooms/',views.showRooms,name='showRooms'),
    path('editRoom/<int:key>',views.editRoom,name='editRoom'),
    path('deleteRoom/',views.deleteRoom,name='deleteRoom'),
    path('editCategoryNow/<int:key>',views.editCategoryView,name='editCategoryView'),
    path('showCategories/',views.showCategories,name='showCategories'),
    path('deleteCategory/',views.deleteCategorie,name='deleteCategory'),
    path('editFloor/',views.editFloor,name='editFloor'),
    path('editAccount/',views.editAccount,name='editAccount'),
    path('home/',views.homeView,name='home'),
    path('editSubItem/<int:key>',views.editSubItem,name='editSubItem'),
    path('addExistingSubItem/<int:key>',views.addExistingSubItem,name='addExistingSubItem'),
    path('deleteSubItem/<int:key>',views.deleteSubItem,name='deleteSubItem'),
    path('details/<int:key>', views.details, name='details'),
]


