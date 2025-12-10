import flet as ft
from flet import padding, border_radius, border, Icons

# Color Palette
PRIMARY_COLOR = "#A895C9"
SECONDARY_COLOR = "#C9C0DB"
ACCENT_COLOR = "#FFF7D6"
TEXT_COLOR = "#333333"
LIGHT_TEXT = "#666666"
BG_WHITE = "#FFFFFF"
BG_LIGHT = "#F0F4F7"
BG_TINT = "#F7F4FB"
BORDER_COLOR = "#D3D3D3"
SUCCESS_COLOR = "#81C784"
WARNING_COLOR = "#FFD54F"
DANGER_COLOR = "#E57373"
TABLE_HEADER_BG = "#9B7CB5"
TABLE_BORDER_COLOR = "#D3D3D3"
ADMIN_ROLE_COLOR = "#E57373"
USER_ROLE_COLOR = "#81C784"

# Spacing
SPACING_SM = 8
SPACING_MD = 12
SPACING_LG = 16
SPACING_XL = 24

# --- REUSABLE COMPONENTS ---

def create_text_field(label: str, password=False, hint_text="", width=None, required=False):
    """Creates a standardized text field with improved styling."""
    label_text = f"{label} {'*' if required else ''}"
    return ft.Column(
        spacing=6,
        controls=[
            ft.Text(label_text, weight=ft.FontWeight.W_600, size=13, color=TEXT_COLOR),
            ft.Container(
                content=ft.TextField(
                    value="",
                    hint_text=hint_text,
                    border=ft.InputBorder.OUTLINE,
                    text_style=ft.TextStyle(size=13, color=TEXT_COLOR),
                    hint_style=ft.TextStyle(size=13, color=LIGHT_TEXT),
                    content_padding=padding.symmetric(horizontal=14, vertical=12),
                    password=password,
                    can_reveal_password=password,
                    cursor_color=PRIMARY_COLOR,
                ),
                height=42,
                border_radius=border_radius.all(8),
                bgcolor=BG_WHITE,
                width=width,
                border=border.all(1, BORDER_COLOR),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=2,
                    color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                    offset=ft.Offset(0, 1),
                ),
            )
        ],
        width=width,
    )

def create_button(text: str, on_click=None, is_primary=True, width=None, height=45, icon=None):
    """Creates a standard button with improved styling."""
    btn_content = ft.Text(
        text,
        size=14,
        weight=ft.FontWeight.W_600,
        color=ft.Colors.WHITE if is_primary else PRIMARY_COLOR,
    )
    
    shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=4,
        color=ft.Colors.with_opacity(0.15, PRIMARY_COLOR) if is_primary else ft.Colors.with_opacity(0, ft.Colors.BLACK),
        offset=ft.Offset(0, 2),
    ) if is_primary else None
    
    return ft.Container(
        content=btn_content,
        padding=padding.symmetric(horizontal=20, vertical=10),
        alignment=ft.alignment.center,
        bgcolor=PRIMARY_COLOR if is_primary else BG_LIGHT,
        border_radius=border_radius.all(8),
        on_click=on_click,
        ink=True,
        width=width,
        height=height,
        border=border.all(1.5, PRIMARY_COLOR) if not is_primary else None,
        shadow=shadow,
    )

def create_admin_button(text: str, is_primary=True, on_click=None, icon=None):
    """Creates the standard profile buttons."""
    return create_button(text, on_click, is_primary, width=200, height=45)

def create_info_card(title: str, value: str, icon=None, color_start=None, color_end=None):
    """Card for Dashboard metrics with enhanced styling."""
    if not color_start:
        color_start = PRIMARY_COLOR
    if not color_end:
        color_end = SECONDARY_COLOR
        
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(title, size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                ft.Text(value, size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            spacing=8
        ),
        width=220,
        padding=padding.all(24),
        border_radius=border_radius.all(12),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[color_start, color_end],
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
    )

def create_dropdown(label: str, options: list, value: str = None, width=None, required=False, on_change=None):
    """Creates a standardized dropdown field with improved styling."""
    label_text = f"{label} {'*' if required else ''}"
    return ft.Column(
        spacing=6,
        controls=[
            ft.Text(label_text, weight=ft.FontWeight.W_600, size=13, color=TEXT_COLOR),
            ft.Container(
                content=ft.Dropdown(
                    options=[ft.dropdown.Option(opt) for opt in options],
                    value=value or options[0] if options else None,
                    border=ft.InputBorder.OUTLINE,
                    on_change=on_change,
                    text_size=13,
                    bgcolor=BG_WHITE,
                ),
                height=42,
                border_radius=border_radius.all(8),
                width=width,
                border=border.all(1, BORDER_COLOR),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=2,
                    color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                    offset=ft.Offset(0, 1),
                ),
            )
        ],
        width=width,
    )

def create_table_row(cells: list, is_header=False, widths=None):
    """Creates a table row with enhanced styling."""
    row_controls = []
    for i, cell in enumerate(cells):
        cell_width = widths[i] if widths and i < len(widths) else None
        row_controls.append(
            ft.Container(
                content=ft.Text(
                    cell,
                    weight=ft.FontWeight.W_600 if is_header else ft.FontWeight.NORMAL,
                    size=12,
                    color=ft.Colors.WHITE if is_header else TEXT_COLOR,
                ),
                width=cell_width,
                padding=padding.symmetric(horizontal=12, vertical=12),
            )
        )
    
    return ft.Container(
        content=ft.Row(row_controls, spacing=0),
        bgcolor=TABLE_HEADER_BG if is_header else BG_WHITE,
        border=border.only(bottom=border.BorderSide(1, TABLE_BORDER_COLOR)),
        border_radius=border_radius.only(
            top_left=8 if is_header else 0,
            top_right=8 if is_header else 0
        ),
    )

def create_section_title(title: str, subtitle: str = None):
    """Creates a section title with improved hierarchy."""
    return ft.Column(
        [
            ft.Text(title, size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Container(height=2, width=40, bgcolor=SECONDARY_COLOR),
        ],
        spacing=8,
    )

def create_badge(text: str, color: str = PRIMARY_COLOR, text_color: str = ft.Colors.WHITE):
    """Creates a badge/tag with improved styling."""
    return ft.Container(
        content=ft.Text(text, size=11, weight=ft.FontWeight.W_600, color=text_color),
        padding=padding.symmetric(horizontal=12, vertical=6),
        bgcolor=color,
        border_radius=border_radius.all(20),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=3,
            color=ft.Colors.with_opacity(0.1, color),
            offset=ft.Offset(0, 1),
        ),
    )

def create_divider(height: int = 1, color: str = BORDER_COLOR):
    """Creates a divider line."""
    return ft.Container(height=height, bgcolor=color)

def create_action_button(label: str, icon: str = None, on_click=None, color: str = PRIMARY_COLOR):
    """Creates a styled action button with icon and text."""
    return ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(icon, size=18, color=ft.Colors.WHITE) if icon else None,
                ft.Text(label, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            spacing=8,
        ),
        bgcolor=color,
        style=ft.ButtonStyle(
            padding=padding.symmetric(horizontal=16, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
        on_click=on_click,
    )
