import flet as ft
from flet import padding, border_radius, border, Icons
from layouts import create_main_layout
from components import ADMIN_ROLE_COLOR, USER_ROLE_COLOR, SUCCESS_COLOR, PRIMARY_COLOR, create_action_button, TABLE_HEADER_BG
from users_data import search_users, delete_user, toggle_lock, list_users
from activity_log import get_recent_activities


def users_view(page: ft.Page):
    """User management screen with functional actions (delete, lock/unlock, search/filter, view logs)."""

    current_user = "admin"

    # Controls for filtering/search
    role_dd = ft.Dropdown(
        options=[ft.dropdown.Option("All Roles"), ft.dropdown.Option("Admin"), ft.dropdown.Option("User")],
        value="All Roles",
        width=200,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333"
    )
    status_dd = ft.Dropdown(
        options=[ft.dropdown.Option("All Status"), ft.dropdown.Option("Active"), ft.dropdown.Option("Inactive")],
        value="All Status",
        width=200,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333"
    )
    search_field = ft.TextField(
        hint_text="Username or email",
        width=300,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333"
    )

    # Container placeholders
    list_container = ft.Container()

    def show_snack(message: str, success: bool = True):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=(ft.Colors.GREEN_700 if success else ft.Colors.RED_700))
        page.snack_bar.open = True
        page.update()

    def view_logs(username: str):
        activities = get_recent_activities(50)
        user_activities = [a for a in activities if a.get("username", "").lower() == username.lower()]
        items = []
        for a in user_activities:
            timestamp_text = ft.Text(a['timestamp'], size=11, color="#000000", weight=ft.FontWeight.BOLD)
            event_text = ft.Text(a['event_type'], size=11, color="#E74C3C", weight=ft.FontWeight.BOLD)
            desc_text = ft.Text(a['description'], size=11, color="#333333")
            log_row = ft.Container(
                content=ft.Column([
                    ft.Row([timestamp_text, ft.Text(" | "), event_text], spacing=5),
                    ft.Text(desc_text.value, size=11, color="#666666", italic=True)
                ], spacing=3),
                padding=10,
                bgcolor="#F8F9FA",
                border_radius=4,
                border="1px solid #E0E0E0"
            )
            items.append(log_row)
        
        if not items:
            items = [ft.Text("No recent logs for this user", size=12, color="#999999", italic=True)]
        
        dlg = ft.AlertDialog(
            title=ft.Text(f"Logs for {username}", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
            content=ft.Container(
                content=ft.Column(items, scroll=ft.ScrollMode.AUTO, spacing=8),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=4,
                width=500,
                height=400
            ),
            actions=[ft.TextButton("Close", on_click=lambda e: page.dialog.close())]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def confirm_delete(username: str):
        def do_delete(e):
            success = delete_user(username, actor=current_user)
            page.dialog.open = False
            if success:
                show_snack(f"Deleted user {username}")
            else:
                show_snack(f"Failed to delete {username}", success=False)
            update_ui()

        dlg = ft.AlertDialog(title=ft.Text("Confirm delete"), content=ft.Text(f"Delete user {username}? This is irreversible."), actions=[ft.TextButton("Cancel", on_click=lambda e: page.dialog.close()), ft.TextButton("Delete", on_click=do_delete)])
        page.dialog = dlg
        dlg.open = True
        page.update()

    def do_toggle_lock(username: str):
        success = toggle_lock(username, actor=current_user)
        if success:
            show_snack(f"Toggled lock for {username}")
        else:
            show_snack(f"Failed to toggle lock for {username}", success=False)
        update_ui()

    def update_ui(e=None):
        role = role_dd.value
        status = status_dd.value
        q = search_field.value
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
        for i, u in enumerate(users):
            role_color = ADMIN_ROLE_COLOR if u.get("role") == "Admin" else USER_ROLE_COLOR
            locked = u.get("locked", False)
            username_val = u.get("username")
            actions = []
            if username_val.lower() == current_user.lower():
                actions.append(ft.Text("Current User"))
            else:
                actions.append(ft.IconButton(Icons.DELETE_FOREVER, icon_color=ft.Colors.RED_600, tooltip="Delete User", icon_size=18, on_click=lambda e, u=username_val: confirm_delete(u)))
                actions.append(ft.IconButton(Icons.LOCK_OUTLINE if not locked else Icons.LOCK_OPEN, icon_color=ft.Colors.GREY_600, tooltip=("Lock User" if not locked else "Unlock User"), icon_size=18, on_click=lambda e, u=username_val: do_toggle_lock(u)))

            # alternating row background for readability
            row_bg = ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_200

            rows.append(ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(u.get("username"), size=12, color="#000000", weight=ft.FontWeight.BOLD), width=120),
                    ft.Container(ft.Text(u.get("name"), size=12, color="#333333"), width=160),
                    ft.Container(ft.Text(u.get("email"), size=12, color="#555555"), expand=True),
                    ft.Container(ft.Text(u.get("role"), color=role_color, size=12), width=80),
                    ft.Container(ft.Text(u.get("status"), color=SUCCESS_COLOR, size=12), width=80),
                    ft.Container(ft.Text("Yes" if u.get("twofa") else "No", size=12, color="#27AE60" if u.get("twofa") else "#E74C3C", weight=ft.FontWeight.BOLD), width=50),
                    ft.Container(ft.Text(u.get("last_login", ""), size=12, color="#888888"), width=150),
                    ft.Container(ft.Row(actions, spacing=6), width=140),
                ], spacing=0),
                padding=padding.symmetric(horizontal=15, vertical=10),
                bgcolor=row_bg,
            ))

        list_container.content = ft.Card(content=ft.Container(content=ft.Column([header_row] + rows, spacing=0, expand=True), padding=padding.only(bottom=10), bgcolor=ft.Colors.WHITE), elevation=1, expand=True)
        page.update()

    # Wire filter changes
    role_dd.on_change = update_ui
    status_dd.on_change = update_ui
    search_field.on_change = update_ui

    # Controls row
    search_fields = ft.Row([
        ft.Column([ft.Text("Role", weight=ft.FontWeight.BOLD, size=14, color="#000000"), role_dd]),
        ft.Column([ft.Text("Status", weight=ft.FontWeight.BOLD, size=14, color="#000000"), status_dd]),
        ft.Column([ft.Text("Search", weight=ft.FontWeight.BOLD, size=14, color="#000000"), search_field], expand=True),
        create_action_button("Refresh", Icons.REFRESH, on_click=lambda e: update_ui(), color=PRIMARY_COLOR)
    ], spacing=20, alignment=ft.MainAxisAlignment.START)

    content = ft.Column([
        ft.Row([ft.Text("User Management", size=20, weight=ft.FontWeight.BOLD, color="#000000")]),
        search_fields,
        ft.Container(height=12),
        list_container,
        ft.Container(height=20),
    ])

    # Initial population
    update_ui()
    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/users", user_role)
