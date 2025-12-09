import flet as ft
from flet import padding, border_radius, Icons
from layouts import create_main_layout
from components import SUCCESS_COLOR

def settings_view(page: ft.Page):
    """Recreates the Settings.png screen with improved readability and colors."""

    is_otp_enabled = ft.Ref[ft.Switch]()

    security_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Security Settings", size=24, weight=ft.FontWeight.BOLD, color="#007BFF"),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            # Left Column: Two-Factor Authentication
                            ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(Icons.LOCK_OUTLINED, color="#007BFF", size=24),
                                        ft.Text("Two-Factor Authentication (OTP)", weight=ft.FontWeight.BOLD, size=16, color="#333333"),
                                    ], spacing=10),
                                    ft.Row(
                                        [
                                            ft.Text("Enable OTP Verification", size=14, color="#555555"),
                                            ft.Switch(ref=is_otp_enabled, value=False)
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text("• OTP Length: 6 digits", size=13, color="#333333"),
                                                ft.Text("• OTP Expiry: 5 minutes", size=13, color="#333333"),
                                                ft.Text("• OTP delivery: Email / SMS", size=13, color="#333333"),
                                            ]
                                        ),
                                        padding=padding.all(10),
                                        bgcolor="#F0F4F8",
                                        border_radius=border_radius.all(5),
                                        width=250,
                                        margin=ft.margin.only(left=20)
                                    ),
                                ],
                                expand=True
                            ),
                            ft.VerticalDivider(width=1, color="#E0E0E0"),
                            # Right Column: Login Alerts
                            ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color="#E74C3C", size=24),
                                        ft.Text("Login Alerts & Security Notifications", weight=ft.FontWeight.BOLD, size=16, color="#333333"),
                                    ], spacing=10),
                                    ft.Text("Suspicious Login Detection", size=14, color="#555555"),
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Icon(Icons.CHECK, color=SUCCESS_COLOR, size=20),
                                            ft.Text("Enabled", weight=ft.FontWeight.BOLD, color=SUCCESS_COLOR, size=13),
                                            ft.Text("by system", size=12, color="#888888"),
                                        ], spacing=5),
                                        padding=padding.symmetric(horizontal=10, vertical=8),
                                        bgcolor="#E8F5E9",
                                        border_radius=border_radius.all(5),
                                    ),
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Icon(Icons.INFO_OUTLINE, color="#27AE60", size=18),
                                            ft.Text("We monitor unusual login behavior such as:", size=13, color="#27AE60"),
                                        ], spacing=5),
                                        margin=ft.margin.only(top=10)
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text("• New locations", size=13, color="#555555"),
                                                ft.Text("• Unusual login times", size=13, color="#555555"),
                                                ft.Text("• Repeated attempts", size=13, color="#555555"),
                                            ]
                                        ),
                                        margin=ft.margin.only(left=20)
                                    )
                                ],
                                expand=True
                            ),
                        ],
                        spacing=30
                    ),
                    ft.Container(height=30),
                    # Auto Logout
                    ft.Text("Auto Logout", size=18, weight=ft.FontWeight.BOLD, color="#007BFF"),
                    ft.Container(
                        content=ft.Text(
                            "You will be logged out after **15 minutes** of inactivity.",
                            size=13,
                            color="#333333",
                            selectable=True
                        ),
                        padding=padding.all(10),
                        bgcolor="#F0F4F8",
                        border_radius=border_radius.all(5),
                        width=400,
                        margin=ft.margin.only(left=20, top=5)
                    ),
                ],
                expand=True
            ),
            padding=30,
            bgcolor=ft.Colors.WHITE,
        ),
        elevation=2,
        expand=True
    )

    content = ft.Column(
        [
            security_card,
            ft.Container(height=20),
        ],
    )
    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/settings", user_role)
