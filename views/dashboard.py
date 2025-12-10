import flet as ft
from flet import padding, border_radius, border
from layouts import create_main_layout
from components import create_info_card, TABLE_HEADER_BG
from activity_log import get_recent_activities, count_anomalies
from users_data import list_users
from checkin_log import (
    get_active_checkins_count,
    get_checkins_today_count,
    get_user_checkins_count,
)

def dashboard_view(page: ft.Page):
    """Recreates the DASHBOARD.png screen."""
    current_user = (page.session.get("current_user") or "").lower()

    user_role = page.session.get("user_role") or "User"

    # Activity list:
    # - Admin: show all recent activities
    # - User: show only their own
    activities = get_recent_activities(limit=50)
    if user_role == "Admin":
        filtered = activities
    else:
        filtered = [a for a in activities if a.get("username", "").lower() == current_user]

    activity_data = [
        (
            activity.get("event_type", ""),
            activity.get("username", ""),
            activity.get("timestamp", ""),
            activity.get("description", ""),
        )
        for activity in filtered[:5]
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
        bgcolor=TABLE_HEADER_BG,
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

    # Metrics: for admin show real counts; for non-admin show only their check-in count
    if user_role == "Admin":
        total_users = str(len(list_users()))
        active_sessions = str(get_active_checkins_count())
        checkins_today = str(get_checkins_today_count())
        anomalies = str(count_anomalies())
        metrics_row = ft.Row(
            [
                create_info_card("Total Users", total_users),
                create_info_card("Active Sessions", active_sessions),
                create_info_card("Check-ins Today", checkins_today),
            ],
            spacing=20,
            wrap=True,
        )
    else:
        my_checkins = str(get_user_checkins_count(current_user))
        metrics_row = ft.Row(
            [
                create_info_card("My Check-ins", my_checkins),
            ],
            spacing=20,
            wrap=True,
        )

    content = ft.Column(
        [
            ft.Text("Dashboard", size=20, weight=ft.FontWeight.BOLD, color="#000000"),
            metrics_row,
            ft.Container(height=30),
            ft.Text("Recent Activity", size=18, weight=ft.FontWeight.BOLD, color="#000000"),
            activity_table,
            ft.Container(height=20),
        ],
    )

    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/dashboard", user_role)
