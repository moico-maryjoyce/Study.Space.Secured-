import flet as ft
import json
from pathlib import Path
from flet import padding, border_radius, border, Icons
from layouts import create_main_layout
from components import create_info_card, create_action_button, PRIMARY_COLOR, TABLE_HEADER_BG

# Path to the shared data file
# We go up one level from 'views/' to root, then into 'data/'
ACTIVITY_DATA_FILE = Path(__file__).parent.parent / "data" / "activity_log.json"

def _load_audit_data():
    """
    Loads and transforms activity logs into the format expected by the Audit Log view.
    """
    if not ACTIVITY_DATA_FILE.exists():
        return []
    
    try:
        with open(ACTIVITY_DATA_FILE, "r", encoding="utf-8") as f:
            raw_logs = json.load(f)
    except Exception:
        return []

    processed_logs = []
    
    for log in raw_logs:
        event_type = log.get("event_type", "Unknown")
        description = log.get("description", "")
        
        # --- Logic to determine Status and Anomaly based on event type ---
        status = "Success"
        anomaly = "No"
        
        # Determine Status
        if "failed" in event_type.lower() or "denied" in description.lower():
            status = "Failed"
        elif "locked" in event_type.lower():
            status = "Locked"
        elif "timeout" in event_type.lower():
            status = "Timeout"
        
        # Determine Anomaly (Flag failed attempts or locks)
        if status in ["Failed", "Locked", "Timeout"]:
            anomaly = "Yes"
        
        # Prettify Event Type for display
        display_event = event_type.replace("_", " ").title()

        processed_logs.append({
            "timestamp": log.get("timestamp", "N/A"),
            "event_type": display_event,
            "user": log.get("username", "Unknown"),
            "ip_address": "127.0.0.1",  # Placeholder: IP is not currently captured in activity_log.json
            "status": status,
            "anomaly": anomaly,
            "raw_description": description # Keep for export or details
        })
        
    return processed_logs

def audit_logs_view(page: ft.Page):
    """Audit Logs View - Shows system events and user activities with clean, simple design."""
    
    # Load real data instead of hardcoded samples
    log_data = _load_audit_data()

    # Dropdowns for filtering
    event_type_dd = ft.Dropdown(
        options=[
            ft.dropdown.Option("All Events"),
            ft.dropdown.Option("Login Success"),
            ft.dropdown.Option("Login Failed"),
            ft.dropdown.Option("User Created"),
            ft.dropdown.Option("Profile Updated"),
            ft.dropdown.Option("User Locked"),
            ft.dropdown.Option("Logout"),
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
        options=[ft.dropdown.Option("All Status"), ft.dropdown.Option("Success"), ft.dropdown.Option("Failed"), ft.dropdown.Option("Locked")],
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
            "Locked": "#E57373",
            "Timeout": "#FFD54F",
        }
        return colors.get(status, "#757575")

    def update_ui(e=None):
        """Update the audit logs table based on filters."""
        # Refresh data on update
        current_data = _load_audit_data()
        
        # Filter logic
        filtered_data = []
        filter_event = event_type_dd.value
        filter_status = status_dd.value
        filter_query = search_field.value.lower() if search_field.value else ""

        for log in current_data:
            # 1. Filter by Event Type
            if filter_event != "All Events" and log["event_type"] != filter_event:
                continue
            
            # 2. Filter by Status
            if filter_status != "All Status" and log["status"] != filter_status:
                continue
                
            # 3. Search Query (Username or Event Type)
            if filter_query:
                if (filter_query not in log["user"].lower() and 
                    filter_query not in log["event_type"].lower()):
                    continue
            
            filtered_data.append(log)

        # Build header
        header_row = ft.Container(
            ft.Row(
                [
                    ft.Container(ft.Text("Timestamp", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE), width=180),
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
        if not filtered_data:
            rows.append(ft.Container(
                content=ft.Text("No logs found matching criteria", italic=True, color=ft.Colors.GREY_500),
                padding=20,
                alignment=ft.alignment.center
            ))
        else:
            for i, log in enumerate(filtered_data):
                is_anomaly = log["anomaly"] == "Yes"
                row_bg = ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_200
                
                rows.append(ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text(log["timestamp"], size=12, color="#333333"), width=180),
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
                            alignment=ft.alignment.center_left,
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
                content=ft.Column([header_row] + rows, spacing=0, expand=True, scroll=ft.ScrollMode.AUTO),
                padding=padding.only(bottom=10),
                bgcolor=ft.Colors.WHITE,
                height=500, # Fixed height for scrolling
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
        """Export current filtered logs to CSV."""
        import csv
        
        # Get current data (re-apply filters logic or just export all)
        # For simplicity, we export ALL data currently
        data_to_export = _load_audit_data()
        
        filename = "audit_logs_export.csv"
        try:
            if not data_to_export:
                raise Exception("No data to export")

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                # Get headers from first key
                writer = csv.DictWriter(f, fieldnames=data_to_export[0].keys())
                writer.writeheader()
                writer.writerows(data_to_export)
                
            page.snack_bar = ft.SnackBar(ft.Text(f"Exported {len(data_to_export)} records to {filename}"), bgcolor=ft.Colors.GREEN_700)
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Export failed: {str(ex)}"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()

    # Calculate stats for the cards
    current_data = _load_audit_data()
    total_events = len(current_data)
    anomalies = sum(1 for log in current_data if log["anomaly"] == "Yes")
    failed_actions = sum(1 for log in current_data if log["status"] == "Failed")

    content = ft.Column([
        ft.Row([ft.Text("Audit Logs", size=20, weight=ft.FontWeight.BOLD, color="#000000")]),
        ft.Row(
            [
                create_info_card("Total Events", str(total_events)),
                create_info_card("Anomalies", str(anomalies), color_start="#E57373", color_end="#F44336"),
                create_info_card("Failed Actions", str(failed_actions), color_start="#FFD54F", color_end="#FFB300"),
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
