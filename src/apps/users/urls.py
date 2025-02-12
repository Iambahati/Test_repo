from django.urls import path
from .views import (index, signup_view, signin_view,
                    # signout_view, dashboard_view, profile_view, profile_update_view, password_change_view, password_change_done_view, password_reset_view, password_reset_done_view, password_reset_confirm_view, password_reset_complete_view,)
                    
                    )

urlpatterns = [
    path("", index, name="index"),
    path("register/", signup_view, name="register"), # User registration
    path("login/", signin_view, name="login"), # User login  
]