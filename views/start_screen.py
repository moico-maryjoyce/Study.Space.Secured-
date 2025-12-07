import flet as ft
from flet import padding, border_radius
from components import PRIMARY_COLOR, SECONDARY_COLOR
import os


def start_screen(page: ft.Page):
    """
    Study.Space.Secured Start Screen
    Matches the exact design from the wireframe
    - Logo centered
    - "START NOW" button
    - Copyright text
    - Gray background
    """
   
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "assets", "logo.png")
   
    # --- LOGO & TEXT ---
    # Create logo container - centered logo only
    logo_content = ft.Container(
        content=ft.Image(
            src=logo_path,
            width=220,
            height=170,
            fit=ft.ImageFit.CONTAIN,
            error_content=ft.Text("Logo", size=20, weight=ft.FontWeight.BOLD)
        ),
        alignment=ft.alignment.center,
    )

    # --- START BUTTON ---
    # Pill-shaped button with proper emphasis - matching the design
    start_button = ft.Container(
        content=ft.Text(
            "START NOW",
            size=15,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        padding=padding.symmetric(horizontal=50, vertical=14),
        bgcolor=PRIMARY_COLOR,
        border_radius=border_radius.all(25),
        alignment=ft.alignment.center,
        on_click=lambda e: page.go("/login"),
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2),
        ),
    )

    # --- MAIN CARD CONTAINER ---
    # White card with logo and button
    main_card = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=20),  # Top spacing
                logo_content,
                ft.Container(height=35),  # Logo to Button Gap
                start_button,
                ft.Container(height=30),  # Button to Copyright Gap
                ft.Text(
                    "NO COPYRIGHT INFRINGEMENT.",
                    size=10,
                    color="#999999",
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        ),
        padding=padding.all(35),
        width=420,
        height=450,
        bgcolor=ft.Colors.WHITE,
        border_radius=border_radius.all(18),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
        alignment=ft.alignment.center,
    )

    # --- FULL SCREEN LAYOUT ---
    return ft.Container(
        content=ft.Row(
            [main_card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor="#C0C0C0",  # Match the gray background from wireframe
        alignment=ft.alignment.center,
    )
