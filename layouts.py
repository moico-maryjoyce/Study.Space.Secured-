import flet as ft
from flet import border, padding, Icons
from components import PRIMARY_COLOR, BG_LIGHT, BG_WHITE, SECONDARY_COLOR, TEXT_COLOR, BORDER_COLOR

# --- LAYOUT CONSTANTS ---
BG_COLOR = "#F8F6F2"
HEADER_BG_COLOR = BG_WHITE
HEADER_HEIGHT = 80
NAV_ITEM_HEIGHT = 50

def create_main_layout(page: ft.Page, content: ft.Control, current_route: str):
    """
    Creates the common header/navigation layout for all internal screens.
    Includes navigation tabs with active indicators and settings button.
    """
    def navigate(e):
        page.go(e.control.data)

    def nav_item(text: str, route: str):
        is_selected = current_route.startswith(route)
        return ft.Container(
            content=ft.Text(
                text,
                size=15,
                weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_500,
                color=PRIMARY_COLOR if is_selected else TEXT_COLOR,
            ),
            padding=padding.symmetric(horizontal=18, vertical=16),
            bgcolor=HEADER_BG_COLOR,
            border=border.only(
                bottom=border.BorderSide(4, PRIMARY_COLOR) if is_selected else border.BorderSide(0)
            ),
            on_click=navigate,
            data=route,
            ink=True,
            tooltip=text,
        )

    # Header with navigation
    header = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        nav_item("Dashboard", "/dashboard"),
                        nav_item("Check In/Out", "/checkinout"),
                        nav_item("My Profile", "/profile"),
                        nav_item("Users", "/users"),
                        nav_item("Audit Logs", "/auditlogs"),
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=Icons.SETTINGS,
                            icon_size=20,
                            tooltip="Settings",
                            on_click=lambda e: page.go("/settings"),
                            icon_color=SECONDARY_COLOR,
                        ),
                    ],
                    spacing=5,
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=padding.symmetric(horizontal=20, vertical=10),
        bgcolor=HEADER_BG_COLOR,
        border=border.only(bottom=border.BorderSide(1, BORDER_COLOR)),
        height=HEADER_HEIGHT,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=2,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(0, 1),
        ),
    )

    # Main container
    return ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(
                    content=content,
                    padding=padding.all(28),
                    expand=True,
                    bgcolor=BG_COLOR,
                )
            ],
            spacing=0,
            expand=True,
        ),
        bgcolor=BG_COLOR,
        expand=True,
    )

def create_card(title: str, content: ft.Control, padding_val=24, subtitle: str = None):
    """
    Creates a standard card container with title, subtitle, and content.
    """
    header_content = [
        ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
    ]
    if subtitle:
        header_content.append(ft.Text(subtitle, size=13, color="#888888"))
    
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Column(header_content, spacing=5),
                ft.Container(height=1, bgcolor="#E0E0E0"),
                ft.Container(
                    content=content,
                    padding=padding.all(padding_val),
                    expand=True,
                )
            ],
            spacing=0,
            expand=True,
        ),
        padding=padding.all(20),
        bgcolor=BG_WHITE,
        border_radius=ft.border_radius.all(10),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.BLACK08,
            offset=ft.Offset(0, 2),
        ),
    )

def create_stat_row(stats: list):
    """
    Creates a row of stat cards for dashboard.
    stats: list of dicts with keys: title, value, icon (optional), color (optional)
    """
    from components import create_info_card
    
    stat_cards = []
    for stat in stats:
        stat_cards.append(
            create_info_card(
                stat.get("title"),
                stat.get("value"),
                icon=stat.get("icon"),
                color_start=stat.get("color_start"),
                color_end=stat.get("color_end"),
            )
        )
    
    return ft.Row(
        stat_cards,
        spacing=20,
        wrap=True,
        alignment=ft.MainAxisAlignment.START,
    )

def create_section_divider(height: int = 30):
    """Creates a vertical spacing divider."""
    return ft.Container(height=height)