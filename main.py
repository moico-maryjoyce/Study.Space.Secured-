import flet as ft

# Import reusable components and layouts
from layouts import create_main_layout
from components import * # Imports constants and reusable widgets

# Import all screen views
from start_screen import start_screen
from login_screens import login_screen
from views.dashboard_view import dashboard_view
from views.checkinout_view import check_in_out_view
from views.profile_views import profile_view
from views.users_view import users_view
from views.auditlogs_view import audit_logs_view
from views.settings_view import settings_view
from users_data import get_user, ensure_default_admin_user


def main(page: ft.Page):
    page.title = "Study.Space.Secured! UI"
    page.window_width = 1200
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.Theme(font_family="Arial")

    # Seed a default admin account if none exists yet
    ensure_default_admin_user()

    # Store current user and role in session
    page.session.set("current_user", "")
    page.session.set("user_role", "User")  # Default to User role

    def route_change(route):
        page.views.clear()

        # Get current user role
        current_user = page.session.get("current_user")
        user_role = page.session.get("user_role") or "User"

        # The initial landing page
        if page.route == "/":
            page.views.append(start_screen(page))
        # Login and Sign-up
        elif page.route == "/login":
            page.views.append(login_screen(page, is_login=True))
        elif page.route == "/signup":
            page.views.append(login_screen(page, is_login=False))
        # Internal App Screens
        elif page.route == "/dashboard":
            page.views.append(dashboard_view(page))
        elif page.route == "/checkinout":
            page.views.append(check_in_out_view(page))
        elif page.route == "/profile":
            # Default to User Profile
            page.views.append(profile_view(page, is_admin_view=False))
        elif page.route == "/profile/admin":
            # Admin Profile view - admin only
            if user_role == "Admin":
                page.views.append(profile_view(page, is_admin_view=True))
            else:
                page.go("/dashboard")
                return
        elif page.route == "/users":
            # Users management - admin only
            if user_role == "Admin":
                page.views.append(users_view(page))
            else:
                page.go("/dashboard")
                return
        elif page.route == "/auditlogs":
            # Audit logs - admin only
            if user_role == "Admin":
                page.views.append(audit_logs_view(page))
            else:
                page.go("/dashboard")
                return
        elif page.route == "/settings":
            page.views.append(settings_view(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)

