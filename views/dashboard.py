import flet as ft
from flet import padding, border_radius, border
from layouts import create_main_layout
from components import create_info_card
from activity_log import get_recent_activities

def dashboard_view(page: ft.Page):
    """Recreates the DASHBOARD.png screen."""
    activities = get_recent_activities(limit=5)
    activity_data = [
        (activity["event_type"], activity["username"], activity["timestamp"], activity["description"])
        for activity in activities
    ]

    header_row = ft.Container(
        ft.Row(
            [
                ft.Container(ft.Text("Event", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=150),
                ft.Container(ft.Text("User", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=200),
                ft.Container(ft.Text("Time", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=200),
                ft.Container(ft.Text("Details", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), expand=True),
            ],
            spacing=0,
        ),
        padding=padding.symmetric(horizontal=15, vertical=12),
        bgcolor="#007BFF",
        border_radius=border_radius.only(top_left=8, top_right=8),
    )

    activity_table = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.ListView(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(ft.Text(row[0], size=12, color=ft.Colors.BLACK87), width=150),
                                    ft.Container(ft.Text(row[1], size=12, color=ft.Colors.BLACK87), width=200),
                                    ft.Container(ft.Text(row[2], size=12, color=ft.Colors.GREY_700), width=200),
                                    ft.Container(ft.Text(row[3], size=12, color=ft.Colors.BLACK87), expand=True),
                                ],
                                spacing=0,
                            ),
                            padding=padding.symmetric(horizontal=15, vertical=10),
                            bgcolor=ft.Colors.WHITE,
                        )
                        for row in activity_data
                    ],
                    spacing=0,
                    expand=True
                )
            ],
            spacing=0,
        ),
        border=border.all(1, ft.Colors.GREY_300),
        border_radius=border_radius.all(8),
        bgcolor=ft.Colors.WHITE,
        expand=True,
    )

    content = ft.Column(
        [
            ft.Text("Dashboard", size=20, weight=ft.FontWeight.BOLD, color="#007BFF"),
            ft.Row(
                [
                    create_info_card("Total Users", "1"),
                    create_info_card("Active Sessions", "1"),
                    create_info_card("Check-ins Today", "1"),
                    create_info_card("Anomalies Detected", "0"),
                ],
                spacing=20,
            ),
            ft.Container(height=30),
            ft.Text("Recent Activity", size=18, weight=ft.FontWeight.BOLD, color="#007BFF"),
            activity_table,
        ],
        expand=True
    )

    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/dashboard", user_role)
