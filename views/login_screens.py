import flet as ft
from flet import padding, ControlState, border_radius, border
from components import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BG_WHITE
from auth import check_credentials, add_user
from activity_log import log_activity
from users_data import get_user, add_user_record


def login_screen(page: ft.Page, is_login=True):
    """Login and Sign-up screen with simple JSON-backed persistence."""

    # Input fields with proper styling
    username_field = ft.TextField(
        label="Username",
        width=320,
        height=42,
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color="#F5F5F5",
        border_color="#E0E0E0",
        label_style=ft.TextStyle(color=TEXT_COLOR, size=13),
        text_style=ft.TextStyle(color="#000000", size=13),
        hint_style=ft.TextStyle(color=TEXT_COLOR, size=13),
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=320,
        height=42,
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color="#F5F5F5",
        border_color="#E0E0E0",
        label_style=ft.TextStyle(color=TEXT_COLOR, size=13),
        text_style=ft.TextStyle(color="#000000", size=13),
        hint_style=ft.TextStyle(color=TEXT_COLOR, size=13),
    )
    email_field = ft.TextField(
        label="E-mail",
        width=320,
        height=42,
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color="#F5F5F5",
        border_color="#E0E0E0",
        label_style=ft.TextStyle(color=TEXT_COLOR, size=13),
        text_style=ft.TextStyle(color="#000000", size=13),
        hint_style=ft.TextStyle(color=TEXT_COLOR, size=13),
    )

    def show_snack(message: str, success: bool = True):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=(ft.Colors.GREEN_700 if success else ft.Colors.RED_700))
        page.snack_bar.open = True
        page.update()

    def on_login(e):
        username = username_field.value.strip()
        password = password_field.value
        if not username or not password:
            show_snack("Please enter username and password", success=False)
            return
        
        try:
            # Check credentials (returns tuple: success, message, remaining_lockout_time)
            success, message, remaining_lockout = check_credentials(username, password)
        except Exception as ex:
            show_snack(f"Login error: {ex}", success=False)
            return
        
        if success:
            show_snack(message, success=True)
            # Get user role from users_data - normalize username to lowercase
            username_lower = username.lower()
            user_data = get_user(username_lower)
            user_role = user_data.get("role", "User") if user_data else "User"
            # Store in session
            page.session.set("current_user", username_lower)
            page.session.set("user_role", user_role)
            log_activity("login_success", username, f"User {username} logged in successfully")
            page.go("/dashboard")
        else:
            show_snack(message, success=False)
            # Log failed attempt with remaining lockout info if applicable
            if remaining_lockout > 0:
                log_activity("login_failed", username_field.value.strip(), f"Account locked - {remaining_lockout} minutes remaining")
            else:
                log_activity("login_failed", username_field.value.strip(), message)

    def on_signup(e):
        username = username_field.value.strip()
        password = password_field.value
        email = email_field.value.strip()

        if not username or not password or not email:
            show_snack("Please fill in username, email and password", success=False)
            return

        try:
            created = add_user(username, password, email)
        except Exception as ex:
            show_snack(f"Sign up failed: {ex}", success=False)
            return

        if created:
            try:
                # Add user metadata (default role is User) and attempt DB write
                add_user_record(username, name=username, email=email)
                show_snack("Account created. You may now log in.")
                log_activity("user_created", username, f"New user {username} created with default role")
                page.go("/login")
            except Exception as ex:
                show_snack(f"User created but metadata save failed: {ex}", success=False)
        else:
            show_snack("Username already exists", success=False)

    def logo_header():
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "assets", "logo.png")
        
        return ft.Container(
            content=ft.Image(
                src=logo_path,
                width=180,
                height=140,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Logo", size=20, weight=ft.FontWeight.BOLD)
            ),
            alignment=ft.alignment.center,
            margin=padding.only(bottom=20),
        )

    # Build controls depending on mode
    controls = [
        logo_header(),
        username_field,
        password_field,
    ]

    if not is_login:
        controls.insert(3, email_field)

    controls.extend([
        ft.Container(height=25),
        ft.ElevatedButton(
            "Log in" if is_login else "Create Account",
            bgcolor=PRIMARY_COLOR,
            color=ft.Colors.WHITE,
            width=300,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
            ),
            on_click=(on_login if is_login else on_signup),
        ),
        ft.Container(height=15),
    ])

    if is_login:
        controls.extend([
            ft.Text("Don't have account?", size=13, color=TEXT_COLOR),
            ft.TextButton(
                "Sign up here",
                on_click=lambda e: page.go("/signup"),
                style=ft.ButtonStyle(
                    color={ControlState.DEFAULT: PRIMARY_COLOR},
                    text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_600),
                ),
            ),
        ])
    else:
        controls.extend([
            ft.Text("Already have an account?", size=13, color=TEXT_COLOR),
            ft.TextButton(
                "Log in",
                on_click=lambda e: page.go("/login"),
                style=ft.ButtonStyle(
                    color={ControlState.DEFAULT: PRIMARY_COLOR},
                    text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_600),
                ),
            ),
        ])

    form_card = ft.Container(
        content=ft.Container(
            content=ft.Column(
                controls,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=40,
            width=400,
        ),
        bgcolor=BG_WHITE,
        border_radius=border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [form_card],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        bgcolor="#F8F6F2",
    )
