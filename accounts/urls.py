from django.urls import path
from .views import login_view, week_selection, işitsel_sozel_module_view,save_audio,week_modules,verbal_memory_module ,complete_module,attention_module,home_view, save_click_time, user_weeks,user_week_modules, user_module_logs, calisma_bellegi_view, complete_module, basit_calisma_view, karmasik_calisma_view, işitsel_bellek_view,işitsel_zemin_view
from . import admin_views, views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'), 
    path('complete-module/', complete_module, name='complete_module'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('week-selection/', week_selection, name='week_selection'),
    path('modules/<int:week>/', week_modules, name='week_modules'),
    path('attention-module/<int:week>/', attention_module, name='attention_module'),
    path('verbal-memory-module/<int:week>/', verbal_memory_module, name='verbal_memory_module'),
    path('save-audio/', save_audio, name='save_audio'),
    path('işitsel-sozel/<int:week>/', işitsel_sozel_module_view, name='işitsel_sozel_module'),
    path('admin/view-click-times/<int:user_id>/<int:week>/', admin_views.admin_view_click_times, name='admin_view_click_times'),
    path('admin/users/<int:user_id>/weeks/', user_weeks, name='user_weeks'),  # İstifadəçinin həftələri
    path('admin/users/<int:user_id>/weeks/<int:week>/modules/', user_week_modules, name='user_week_modules'),  # Həftənin modulları
    path('admin/users/<int:user_id>/weeks/<int:week>/modules/<str:module>/', user_module_logs, name='user_module_logs'),  # Modul loqları
    path('save-click-time/', save_click_time, name='save_click_time'),
    path('calisma-bellegi/<int:week>/', calisma_bellegi_view, name='calisma_bellegi'),
    path('basit-calisma/<int:week>/', basit_calisma_view, name='basit_calisma'),
    path('karmasik-calisma/<int:week>/', karmasik_calisma_view, name='karmasik_calisma'),
    path('işitsel-bellek/<int:week>/', işitsel_bellek_view, name='işitsel_bellek'),
    path('işitsel-zemin/<int:week>/', işitsel_zemin_view, name='işitsel_zemin'),
    #####
    path('admin_esma/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom_admin/user_management/', views.users_list, name='user_management'),
    path('analytics/', lambda request: HttpResponse("Statistika"), name='analytics'),
    #user_list
    path('custom_admin/users/create/', views.create_user, name='create_user'),
    path('custom_admin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('custom_admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    #module_result
    path('module_results/', views.module_results, name='module_results'),
    path('module_results/user/<int:user_id>/weeks/', views.user_weeks, name='user_weeks'),
    path('modules/<int:user_id>/<int:week>/', views.week_modules_admin, name='week_modules_admin'),
    path('module_results/user/<int:user_id>/week/<int:week>/module/<int:module_id>/', views.module_details, name='module_details'),    
    path('module_results/user/<int:user_id>/download_pdf/', views.download_results_pdf, name='download_results_pdf'),   
    path('audio-and-video-change/', views.audio_and_video_change, name='audio_and_video_change'),
    path('save-click-data/', views.save_click_data, name='save_click_data'),
    path('save-audio-karmaşik/', views.save_audio_karmasik, name='save_audio_karmasik'),
    path('save-audio-basit/', views.save_basit_audio, name='save_basit_audio'),
    path('save-audio-zemin/', views.save_audio_zemin, name='save_audio_zemin'),
    path('save-audio-bellek/', views.save_audio_isitsel_bellek, name='save_audio_bellek'),
    path('save-audio-verbal/', views.save_verbal_audio, name='save_verbal_audio'),
    path('search_users/', views.search_users, name='search_users'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
