from django.urls import path
from . import views

app_name = 'lineup'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('host/', views.host, name='host'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/create-session/', views.admin_create_session, name='admin_create_session'),
    path('admin-panel/delete-session/', views.admin_delete_session, name='admin_delete_session'),
    path('admin-panel/toggle-staff/', views.admin_toggle_staff, name='admin_toggle_staff'),
    path('admin-panel/delete-user/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/clear-completed/', views.admin_clear_completed, name='admin_clear_completed'),
    path('api/raise-hand/', views.raise_hand, name='raise_hand'),
    path('api/leave/', views.leave_queue, name='leave_queue'),
    path('api/next/', views.next_participant, name='next_participant'),
    path('api/clear/', views.clear_queue, name='clear_queue'),
    path('api/queue/', views.get_queue, name='get_queue'),
    path('api/full-state/', views.full_state, name='full_state'),
    path('api/admin-state/', views.admin_state, name='admin_state'),
    path('api/remove/', views.remove_participant, name='remove_participant'),
    path('api/registrations/', views.get_registrations, name='get_registrations'),
    path('api/registrations/create/', views.create_registrations, name='create_registrations'),
    path('api/registrations/edit/', views.edit_registration, name='edit_registration'),
    path('api/registrations/delete/', views.delete_registration, name='delete_registration'),
    path('api/registrations/register/', views.register_for_event, name='register_for_event'),
    path('api/registrations/unregister/', views.unregister_from_event, name='unregister_from_event'),
    path('api/registrations/<int:reg_id>/entries/', views.get_registration_entries, name='get_registration_entries'),
]
