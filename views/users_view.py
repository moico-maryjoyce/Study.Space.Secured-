import flet as ft
from flet import padding, border_radius, border, Icons
from layouts import create_main_layout
from components import ADMIN_ROLE_COLOR, USER_ROLE_COLOR, SUCCESS_COLOR, PRIMARY_COLOR, create_action_button, TABLE_HEADER_BG
from users_data import search_users, delete_user, toggle_lock, get_user
from activity_log import get_recent_activities

def users_view(page: ft.Page):
    """User management screen with functional actions (delete, lock/unlock, search/filter, view logs)."""

    # Get current user from session to prevent self-deletion
    current_user = page.session.get("current_user")

    # Controls for filtering/search
    role_dd = ft.Dropdown(
        options=[ft.dropdown.Option("All Roles"), ft.dropdown.Option("Admin"), ft.dropdown.Option("User")],
        value="All Roles",
        width=200,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333",
        on_change=lambda e: update_ui()
    )
    status_dd = ft.Dropdown(
        options=[ft.dropdown.Option("All Status"), ft.dropdown.Option("Active"), ft.dropdown.Option("Inactive")],
        value="All Status",
        width=200,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333",
        on_change=lambda e: update_ui()
    )
    search_field = ft.TextField(
        hint_text="Username or email",
        width=300,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333",
        on_change=lambda e: update_ui()
    )

    # Container placeholders (give it height so internal ListView can scroll)
    list_container = ft.Container(expand=True, height=500)

    def show_snack(message: str, success: bool = True):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=(ft.Colors.GREEN_700 if success else ft.Colors.RED_700))
        page.snack_bar.open = True
        page.update()

    def do_toggle_lock(username: str):
        # We use 'system' if current_user is None
        actor = current_user if current_user else "system"
        success = toggle_lock(username, actor=actor)
        
        if success:
            show_snack(f"Toggled lock status for {username}")
            # Refresh the UI to update the lock icon
            update_ui()
        else:
            show_snack(f"Failed to toggle lock for {username}", success=False)

    def update_ui(e=None):
        role = role_dd.value
        status = status_dd.value
        q = search_field.value
        
        # Fetch fresh data
        users = search_users(role=role, status=status, query=q)

        # Build header
        header_row = ft.Container(
            ft.Row(
                [
                    ft.Container(ft.Text("Username", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=120),
                    ft.Container(ft.Text("Name", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=160),
                    ft.Container(ft.Text("Email", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), expand=True),
                    ft.Container(ft.Text("Role", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=80),
                    ft.Container(ft.Text("Status", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=80),
                    ft.Container(ft.Text("2FA", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=50),
                    ft.Container(ft.Text("Last Login", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=150),
                    ft.Container(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=140),
                ],
                spacing=0,
            ),
            padding=padding.symmetric(horizontal=15, vertical=12),
            bgcolor=TABLE_HEADER_BG,
            border_radius=border_radius.only(top_left=8, top_right=8),
        )

        rows = []
        # Handle case where no users found
        if not users:
            rows.append(ft.Container(
                content=ft.Text("No users found.", italic=True),
                padding=20,
                alignment=ft.alignment.center
            ))
        
        for i, u in enumerate(users):
            role_color = ADMIN_ROLE_COLOR if u.get("role") == "Admin" else USER_ROLE_COLOR
            locked = u.get("locked", False)
            username_val = u.get("username")
            
            # Safe Last Login Handling
            last_login = u.get("last_login")
            if not last_login:
                last_login = "Never"
            
            # Action Buttons Logic
            actions = []
            # Check if this row is the current logged-in user (case-insensitive)
            if current_user and username_val.lower() == current_user.lower():
                actions.append(ft.Text("Current User", size=11, italic=True, color=ft.Colors.GREY_600))
            else:
                # LOCK BUTTON
                lock_icon = Icons.LOCK_OUTLINE if not locked else Icons.LOCK_OPEN
                lock_tooltip = "Lock User" if not locked else "Unlock User"
                lock_color = ft.Colors.GREY_600 if not locked else ft.Colors.GREEN_600
                
                lock_btn = ft.IconButton(
                    lock_icon, 
                    icon_color=lock_color, 
                    tooltip=lock_tooltip, 
                    icon_size=18, 
                    on_click=lambda e, u=username_val: do_toggle_lock(u)
                )
                
                actions.append(lock_btn)

            # Alternating row background for readability
            row_bg = ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_200
            
            # Status Indicator (Shows 'Locked' in red if locked, otherwise normal status)
            display_status = "Locked" if locked else u.get("status", "Active")
            status_color = ft.Colors.RED if locked else SUCCESS_COLOR

            rows.append(ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(u.get("username"), size=12, color="#000000", weight=ft.FontWeight.BOLD), width=120),
                    ft.Container(ft.Text(u.get("name"), size=12, color="#333333"), width=160),
                    ft.Container(ft.Text(u.get("email"), size=12, color="#555555"), expand=True),
                    ft.Container(ft.Text(u.get("role"), color=role_color, size=12), width=80),
                    ft.Container(ft.Text(display_status, color=status_color, size=12), width=80),
                    ft.Container(ft.Text("Yes" if u.get("twofa") else "No", size=12, color="#27AE60" if u.get("twofa") else "#E74C3C", weight=ft.FontWeight.BOLD), width=50),
                    ft.Container(ft.Text(last_login, size=12, color="#888888"), width=150),
                    ft.Container(ft.Row(actions, spacing=0), width=140),
                ], spacing=0),
                padding=padding.symmetric(horizontal=15, vertical=10),
                bgcolor=row_bg,
            ))

        list_container.content = ft.Card(
            content=ft.Container(
                content=ft.ListView(
                    controls=[header_row] + rows,
                    spacing=0,
                    expand=True,
                ),
                padding=padding.only(bottom=10),
                bgcolor=ft.Colors.WHITE,
                expand=True,
            ),
            elevation=1,
            expand=True,
            height=500,
        )
        page.update()

    # Wire filter changes handled inline above

    # Controls row
    search_fields = ft.Row([
        ft.Column([ft.Text("Role", weight=ft.FontWeight.BOLD, size=14, color="#000000"), role_dd]),
        ft.Column([ft.Text("Status", weight=ft.FontWeight.BOLD, size=14, color="#000000"), status_dd]),
        ft.Column([ft.Text("Search", weight=ft.FontWeight.BOLD, size=14, color="#000000"), search_field], expand=True),
        create_action_button("Refresh", Icons.REFRESH, on_click=lambda e: update_ui(), color=PRIMARY_COLOR)
    ], spacing=20, alignment=ft.MainAxisAlignment.START)

    content = ft.Column(
        [
            ft.Row([ft.Text("User Management", size=20, weight=ft.FontWeight.BOLD, color="#000000")]),
            search_fields,
            ft.Container(height=12),
            list_container,
            ft.Container(height=20),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Initial population
    update_ui()
    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/users", user_role)
