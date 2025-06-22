from django.urls import path
from a_users.views import *

urlpatterns = [
    #path('', profile_view, name="profile"),
    path('', welcome_page, name="profile"),
    path('edit/', profile_edit_view, name="profile-edit"),
    path('onboarding/', profile_edit_view, name="profile-onboarding"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('emailverify/', profile_emailverify, name="profile-emailverify"),
    path('delete/', profile_delete_view, name="profile-delete"),
    path('users/', user_list_view, name="user-list"),
    path('batches/', batch_list_view, name="batch-list"),
    path('batches/<int:batch>/', batch_user_list_view, name="batch-user-list"),
    path('departments/', dept_list_view, name="dept-list"),
    path('departments/<str:department>/', dept_list_batch_view, name="dept-list-batch"),
    path('departments/<str:department>/<int:batch>/', dept_batch_user_list_view, name="dept-batch-user-list"),
]