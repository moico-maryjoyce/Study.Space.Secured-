import flet as ft
from flet import padding, border_radius, border, Icons
from layouts import create_main_layout
from components import create_info_card, create_action_button, PRIMARY_COLOR, TABLE_HEADER_BG


def audit_logs_view(page: ft.Page):
    """Audit Logs View - Shows system events and user activities with clean, simple design."""
    
    # Sample audit log data
    log_data = [
        {"timestamp": "2025-12-06 21:45:12", "event_type": "Password Changed", "user": "Moico", "ip_address": "172.16.5.33", "status": "Success", "anomaly": "No"},
        {"timestamp": "2025-12-06 21:40:05", "event_type": "OTP Verification", "user": "Quite", "ip_address": "103.21.244.88", "status": "Success", "anomaly": "No"},
        {"timestamp": "2025-12-06 21:35:18", "event_type": "Login Success", "user": "Oronan", "ip_address": "192.168.1.45", "status": "Success", "anomaly": "No"},
        {"timestamp": "2025-12-06 21:30:42", "event_type": "Failed Login Attempt", "user": "Oronan", "ip_address": "192.168.1.45", "status": "Failed", "anomaly": "Yes"},
        {"timestamp": "2025-12-06 21:25:33", "event_type": "Profile Updated", "user": "Admin", "ip_address": "192.168.1.100", "status": "Success", "anomaly": "No"},
        {"timestamp": "2025-12-06 21:20:15", "event_type": "Access Granted", "user": "Sarah_J", "ip_address": "10.0.0.50", "status": "Success", "anomaly": "No"},
        {"timestamp": "2025-12-06 21:15:08", "event_type": "Session Timeout", "user": "Mike_T", "ip_address": "172.16.0.25", "status": "Timeout", "anomaly": "No"},
        {"timestamp": "2025-12-06 21:10:22", "event_type": "Failed 2FA", "user": "John_D", "ip_address": "203.15.30.45", "status": "Failed", "anomaly": "Yes"},
        {"timestamp": "2025-12-06 21:05:11", "event_type": "Permission Denied", "user": "Test_User", "ip_address": "192.168.0.99", "status": "Failed", "anomaly": "Yes"},
        {"timestamp": "2025-12-06 21:00:55", "event_type": "Password Reset", "user": "Admin", "ip_address": "192.168.1.100", "status": "Success", "anomaly": "No"},
    ]

    # Dropdowns for filtering
    event_type_dd = ft.Dropdown(
        options=[
            ft.dropdown.Option("All Events"),
            ft.dropdown.Option("Password Changed"),
            ft.dropdown.Option("OTP Verification"),
            ft.dropdown.Option("Login Success"),
            ft.dropdown.Option("Failed Login Attempt"),
            ft.dropdown.Option("Profile Updated"),
            ft.dropdown.Option("Access Granted"),
            ft.dropdown.Option("Session Timeout"),
            ft.dropdown.Option("Failed 2FA"),
            ft.dropdown.Option("Permission Denied"),
            ft.dropdown.Option("Password Reset"),
        ],
        value="All Events",
        width=200,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333"
    )
    status_dd = ft.Dropdown(
        options=[ft.dropdown.Option("All Status"), ft.dropdown.Option("Success"), ft.dropdown.Option("Failed"), ft.dropdown.Option("Timeout")],
        value="All Status",
        width=200,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333"
    )
    search_field = ft.TextField(
        hint_text="Username or event",
        width=300,
        bgcolor=ft.Colors.WHITE,
        border="1px solid #CCCCCC",
        border_radius=4,
        text_size=13,
        color="#333333"
    )

    # Container for the table
    list_container = ft.Container()

    def get_status_color(status: str) -> str:
        """Get color for status badge."""
        colors = {
            "Success": "#81C784",
            "Failed": "#E57373",
            "Timeout": "#FFD54F",
        }
        return colors.get(status, "#757575")

    def update_ui(e=None):
        """Update the audit logs table."""
        # Build header
        header_row = ft.Container(
            ft.Row(
                [
                    ft.Container(ft.Text("Timestamp", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=160),
                    ft.Container(ft.Text("Event Type", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=150),
                    ft.Container(ft.Text("User", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=110),
                    ft.Container(ft.Text("IP Address", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=140),
                    ft.Container(ft.Text("Status", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=100),
                    ft.Container(ft.Text("Anomaly", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=90),
                ],
                spacing=0,
            ),
            padding=padding.symmetric(horizontal=15, vertical=12),
            bgcolor=TABLE_HEADER_BG,
            border_radius=border_radius.only(top_left=8, top_right=8),
        )

        # Build rows
        rows = []
        for i, log in enumerate(log_data):
            is_anomaly = log["anomaly"] == "Yes"
            row_bg = ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_200
            
            rows.append(ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(log["timestamp"], size=12, color="#333333"), width=160),
                    ft.Container(ft.Text(log["event_type"], size=12, color="#333333"), width=150),
                    ft.Container(ft.Text(log["user"], size=12, color="#000000", weight=ft.FontWeight.BOLD), width=110),
                    ft.Container(ft.Text(log["ip_address"], size=12, color="#555555"), width=140),
                    ft.Container(
                        content=ft.Container(
                            content=ft.Text(log["status"], size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            padding=padding.symmetric(horizontal=12, vertical=5),
                            bgcolor=get_status_color(log["status"]),
                            border_radius=border_radius.all(4),
                        ),
                        width=100,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        ft.Text(log["anomaly"], size=12, color=ft.Colors.RED if is_anomaly else ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                        width=90,
                    ),
                ], spacing=0),
                padding=padding.symmetric(horizontal=15, vertical=10),
                bgcolor=row_bg,
            ))

        list_container.content = ft.Card(
            content=ft.Container(
                content=ft.Column([header_row] + rows, spacing=0, expand=True),
                padding=padding.only(bottom=10),
                bgcolor=ft.Colors.WHITE
            ),
            elevation=1,
            expand=True
        )
        page.update()

    # Wire filter changes
    event_type_dd.on_change = update_ui
    status_dd.on_change = update_ui
    search_field.on_change = update_ui

    # Controls row
    search_fields = ft.Row([
        ft.Column([ft.Text("Event Type", weight=ft.FontWeight.BOLD, size=14, color="#000000"), event_type_dd]),
        ft.Column([ft.Text("Status", weight=ft.FontWeight.BOLD, size=14, color="#000000"), status_dd]),
        ft.Column([ft.Text("Search", weight=ft.FontWeight.BOLD, size=14, color="#000000"), search_field], expand=True),
    ], spacing=20, alignment=ft.MainAxisAlignment.START)

    def export_logs(e):
        """Export audit logs to CSV."""
        import csv
        import os
        filename = "audit_logs_export.csv"
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=log_data[0].keys())
                writer.writeheader()
                writer.writerows(log_data)
            page.snack_bar = ft.SnackBar(ft.Text(f"Exported to {filename}"), bgcolor=ft.Colors.GREEN_700)
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Export failed: {str(ex)}"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()

    content = ft.Column([
        ft.Row([ft.Text("Audit Logs", size=20, weight=ft.FontWeight.BOLD, color="#000000")]),
        ft.Row(
            [
                create_info_card("Total Events", str(len(log_data))),
                create_info_card("Anomalies", str(sum(1 for log in log_data if log["anomaly"] == "Yes"))),
                create_info_card("Failed Actions", str(sum(1 for log in log_data if log["status"] == "Failed"))),
            ],
            spacing=20,
            wrap=True,
        ),
        ft.Container(height=20),
        ft.Row([
            search_fields,
            ft.Row([
                create_action_button("Refresh", Icons.REFRESH, on_click=lambda e: update_ui(), color=PRIMARY_COLOR),
                create_action_button("Export", Icons.DOWNLOAD, on_click=export_logs, color=PRIMARY_COLOR),
            ], spacing=10),
        ], spacing=20, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Container(height=12),
        list_container,
        ft.Container(height=20),
    ])

    # Initial population
    update_ui()
    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/auditlogs", user_role)
