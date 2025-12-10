import sys
from pathlib import Path

# Ensure project root on sys.path so local imports resolve when executed directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import flet as ft
from flet import padding, border_radius, Icons
from layouts import create_main_layout
from components import PRIMARY_COLOR, SUCCESS_COLOR, TEXT_COLOR, LIGHT_TEXT, BG_WHITE, BG_LIGHT, BORDER_COLOR, TABLE_HEADER_BG

def settings_view(page: ft.Page):
    """Clean Security Settings view matching app design."""

    # Theme toggle state stored in session
    dark_mode = bool(page.session.get("dark_mode")) if page.session.contains_key("dark_mode") else False
    theme_switch = ft.Ref[ft.Switch]()

    def handle_theme_toggle(e):
        val = theme_switch.current.value if theme_switch.current else False
        page.session.set("dark_mode", val)
        page.theme_mode = ft.ThemeMode.DARK if val else ft.ThemeMode.LIGHT
        page.update()
    
    # Apply theme on load
    page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT

    # Dark mode card
    dark_mode_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(Icons.DARK_MODE, color=PRIMARY_COLOR, size=20),
                ft.Text("Dark Mode", weight=ft.FontWeight.BOLD, size=14, color=TEXT_COLOR),
            ], spacing=10),
            ft.Container(height=12),
            ft.Row(
                [
                    ft.Text("Toggle dark theme", size=12, color=LIGHT_TEXT),
                    ft.Switch(ref=theme_switch, value=dark_mode, on_change=handle_theme_toggle)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
        ], spacing=0),
        padding=padding.all(16),
        bgcolor=BG_WHITE,
        border_radius=border_radius.all(8),
        border=ft.border.all(1, BORDER_COLOR),
    )

    content = ft.Column([
        # Header
        ft.Row([
            ft.Text("Security Settings", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ]),
        ft.Container(height=20),
        
        # Theme Section
        ft.Text("Appearance", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(height=12),
        dark_mode_card,
        
    ], spacing=0, scroll=ft.ScrollMode.AUTO)
    
    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/settings", user_role)
