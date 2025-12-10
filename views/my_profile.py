import sys
from pathlib import Path

# Ensure project root is on sys.path so imports like `layouts` resolve even when this
# module is executed in isolation.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import flet as ft
from flet import padding, border_radius, Icons, ControlState
from layouts import create_main_layout
from components import (create_text_field, create_admin_button, PRIMARY_COLOR, 
                        SECONDARY_COLOR, TEXT_COLOR, BG_LIGHT, BG_WHITE, 
                        BORDER_COLOR, LIGHT_TEXT, create_button)
from activity_log import log_activity
from users_data import get_user, _load_users, _save_users
from auth import check_credentials, _hash_password

def profile_view(page: ft.Page, is_admin_view=False):
    """
    Improved MY PROFILE view for both User and Admin.
    Displays actual user data and allows profile updates.
    """
    
    # Require an authenticated user to load profile data
    current_user = (page.session.get("current_user") or "").strip().lower()
    user_role = page.session.get("user_role") or "User"
    if not current_user:
        page.snack_bar = ft.SnackBar(ft.Text("Please log in to view your profile"), bgcolor=ft.Colors.RED_700)
        page.snack_bar.open = True
        page.update()
        page.go("/login")
        return

    user_data = get_user(current_user) or {}
    user_name = user_data.get("name", current_user)
    user_email = user_data.get("email", "")
    
    # Create editable fields - Compact padding, prefilled with current user data
    username_field = ft.TextField(
        value=current_user,
        label="Username",
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color=BG_WHITE,
        border_color=BORDER_COLOR,
        content_padding=padding.symmetric(horizontal=12, vertical=8),
        text_style=ft.TextStyle(size=12, color=TEXT_COLOR),
    )
    
    name_field = ft.TextField(
        value=user_name,
        label="Full Name",
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color=BG_WHITE,
        border_color=BORDER_COLOR,
        content_padding=padding.symmetric(horizontal=12, vertical=8),
        text_style=ft.TextStyle(size=12, color=TEXT_COLOR),
    )
    
    email_field = ft.TextField(
        value=user_email,
        label="Email Address",
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color=BG_WHITE,
        border_color=BORDER_COLOR,
        content_padding=padding.symmetric(horizontal=12, vertical=8),
        text_style=ft.TextStyle(size=12, color=TEXT_COLOR),
    )
    
    current_password_field = ft.TextField(
        label="Current Password",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color=BG_WHITE,
        border_color=BORDER_COLOR,
        content_padding=padding.symmetric(horizontal=12, vertical=8),
        text_style=ft.TextStyle(size=12, color=TEXT_COLOR),
    )
    
    new_password_field = ft.TextField(
        label="New Password",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color=BG_WHITE,
        border_color=BORDER_COLOR,
        content_padding=padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(size=13, color=TEXT_COLOR),
    )
    
    confirm_password_field = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        filled=True,
        fill_color=BG_WHITE,
        border_color=BORDER_COLOR,
        content_padding=padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(size=13, color=TEXT_COLOR),
    )
    
    # Small labels that we update after saves
    display_username = ft.Text(current_user, size=10, color=TEXT_COLOR)
    display_role = ft.Text(user_role, size=9, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600)

    def on_update_profile(e):
        # Validate inputs
        new_username = username_field.value.strip().lower()
        new_name = name_field.value.strip()
        new_email = email_field.value.strip()
        current_password = current_password_field.value
        new_password = new_password_field.value
        confirm_password = confirm_password_field.value
        if not new_username:
            page.snack_bar = ft.SnackBar(ft.Text("Username cannot be empty"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
        
        # Check if current password is required (if changing password or username)
        if (new_password or new_username != current_user.lower()) and not current_password:
            page.snack_bar = ft.SnackBar(ft.Text("Current password required for security changes"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
        
        # Verify current password if needed
        if current_password:
            success, msg, _ = check_credentials(current_user, current_password)
            if not success:
                page.snack_bar = ft.SnackBar(ft.Text("Current password is incorrect"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()
                return
        
        # Validate password change if provided
        if new_password:
            if new_password != confirm_password:
                page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()
                return
            if len(new_password) < 6:
                page.snack_bar = ft.SnackBar(ft.Text("Password must be at least 6 characters"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()
                return
        
        # Load users data
        users = _load_users()
        old_key = current_user.lower()
        
        # Ensure the current user exists
        if old_key not in users:
            page.snack_bar = ft.SnackBar(ft.Text("User record not found. Please log in again."), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
            page.go("/login")
            return

        # Check if new username already exists (if username changed)
        if new_username != old_key and new_username in users:
            page.snack_bar = ft.SnackBar(ft.Text("Username already exists"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
        
        # Update user data
        user_rec = users.get(old_key, {})
        
        # If username changed, create new entry and delete old one
        if new_username != old_key:
            users[new_username] = user_rec
            del users[old_key]
            current_user_key = new_username
        else:
            current_user_key = old_key
        
        # Update fields
        users[current_user_key]["name"] = new_name
        users[current_user_key]["email"] = new_email
        
        # Update password if provided
        if new_password:
            users[current_user_key]["password_hash"] = _hash_password(new_password)
        
        # Save changes
        _save_users(users)
        
        # Update session if username changed
        if new_username != old_key:
            page.session.set("current_user", new_username)
            display_username.value = new_username
        else:
            display_username.value = current_user
        
        # Log activity
        log_activity("profile_updated", new_username, f"User {new_username} updated profile")
        
        # Clear password fields
        current_password_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        
        page.snack_bar = ft.SnackBar(ft.Text("Profile updated successfully!"), bgcolor=ft.Colors.GREEN_700)
        page.snack_bar.open = True
        page.update()
    
    def on_logout(e):
        log_activity("logout", current_user, f"User {current_user} logged out")
        page.session.set("current_user", "")
        page.session.set("user_role", "User")
        page.go("/login")
    
    def on_switch_profile(e):
        # Toggle between admin and user profile views (admin-only)
        if user_role != "Admin":
            return
        if is_admin_view:
            page.go("/profile")
        else:
            page.go("/profile/admin")

    # Basic Information Card - Compact
    basic_info_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Username", size=9, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                    username_field,
                ], spacing=2, expand=True),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("Name", size=9, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                    name_field,
                ], spacing=2, expand=True),
            ], spacing=0),
            ft.Container(height=8),
            ft.Column([
                ft.Text("Email", size=9, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                email_field,
            ], spacing=2),
        ], spacing=0),
        padding=padding.all(10),
        bgcolor=BG_WHITE,
        border_radius=border_radius.all(6),
        border=ft.border.all(1, BORDER_COLOR),
    )
    
    # Change Password Card - Compact
    change_password_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Current Password", size=9, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                    current_password_field,
                ], spacing=2, expand=True),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("New Password", size=9, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                    new_password_field,
                ], spacing=2, expand=True),
            ], spacing=0),
            ft.Container(height=8),
            ft.Column([
                ft.Text("Confirm Password", size=9, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
                confirm_password_field,
            ], spacing=2),
        ], spacing=0),
        padding=padding.all(10),
        bgcolor=BG_WHITE,
        border_radius=border_radius.all(6),
        border=ft.border.all(1, BORDER_COLOR),
    )
    
    # Left Column with scrollable content - COMPACT
    left_column = ft.Column(
        [
            # Basic Information Section
            ft.Text("Basic Information", size=12, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            ft.Container(height=8),
            basic_info_card,
            
            ft.Container(height=12),
            
            # Change Password Section
            ft.Text("Change Password", size=12, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            ft.Container(height=8),
            change_password_card,
            
            ft.Container(height=12),  # Bottom padding
        ],
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
    
    # Right Column: Profile Picture and Actions - COMPACT
    right_column = ft.Column(
        [
            # Profile Picture - Smaller for more space
            ft.Container(
                content=ft.Icon(Icons.PERSON, size=90, color=ft.Colors.WHITE),
                width=160,
                height=160,
                border_radius=border_radius.all(80),
                bgcolor=SECONDARY_COLOR,
                alignment=ft.alignment.center,
                border=ft.border.all(2, PRIMARY_COLOR),
            ),
            ft.Container(height=10),
            
            ft.TextButton(
                "Change Picture",
                on_click=None,
                style=ft.ButtonStyle(
                    color={ControlState.DEFAULT: PRIMARY_COLOR},
                    text_style=ft.TextStyle(size=11, weight=ft.FontWeight.W_600)
                )
            ),
            
            ft.Container(height=12),
            
            # User Info Display - More compact
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Username:", size=10, weight=ft.FontWeight.W_600, color=LIGHT_TEXT),
                        display_username,
                    ], spacing=4),
                    ft.Container(height=6),
                    ft.Row([
                        ft.Text("Role:", size=10, weight=ft.FontWeight.W_600, color=LIGHT_TEXT),
                        ft.Container(
                            content=display_role,
                            padding=padding.symmetric(horizontal=6, vertical=2),
                            bgcolor=PRIMARY_COLOR,
                            border_radius=border_radius.all(3),
                        ),
                    ], spacing=4),
                ], spacing=0),
                padding=padding.all(8),
                bgcolor=BG_LIGHT,
                border_radius=border_radius.all(4),
            ),
            
            ft.Container(height=12),
            
            # Update Profile Button - Compact
            ft.ElevatedButton(
                "Update Profile",
                bgcolor=PRIMARY_COLOR,
                color=ft.Colors.WHITE,
                width=150,
                height=40,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    text_style=ft.TextStyle(size=11, weight=ft.FontWeight.W_600),
                ),
                on_click=on_update_profile,
            ),
            
            ft.Container(height=8),
            
            # Logout Button - Compact
            ft.ElevatedButton(
                "Log Out",
                bgcolor=BG_LIGHT,
                color=PRIMARY_COLOR,
                width=150,
                height=40,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    text_style=ft.TextStyle(size=11, weight=ft.FontWeight.W_600),
                    side=ft.BorderSide(1.5, PRIMARY_COLOR),
                ),
                on_click=on_logout,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )
    
    # Main Profile Card - Reduced padding
    profile_card = ft.Container(
        content=ft.Column(
            [
                # Left and Right side in a row with scroll
                ft.Container(
                    content=ft.Row(
                        [
                            # Left Column: Profile Information
                            ft.Container(
                                content=left_column,
                                expand=True,
                                padding=padding.only(right=12),
                            ),
                            # Divider
                            ft.VerticalDivider(width=1, color=BORDER_COLOR),
                            # Right Column: Picture and Actions
                            ft.Container(
                                content=right_column,
                                width=200,
                                padding=padding.only(left=12),
                            ),
                        ],
                        spacing=0,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    expand=True,
                )
            ],
            spacing=0,
            expand=True,
        ),
        padding=padding.all(16),
        bgcolor=BG_WHITE,
        border_radius=border_radius.all(12),
        border=ft.border.all(1, BORDER_COLOR),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        expand=True,
    )

    # Header with title and role indicator
    header = ft.Row(
        [
            ft.Text("My Profile", size=26, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(Icons.ADMIN_PANEL_SETTINGS, color=ft.Colors.WHITE, size=16),
                    ft.Text("Admin View", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600, size=12),
                    ft.Icon(Icons.ARROW_DROP_DOWN, color=ft.Colors.WHITE, size=16)
                ], spacing=3),
                padding=padding.symmetric(horizontal=10, vertical=6),
                bgcolor=PRIMARY_COLOR,
                border_radius=border_radius.all(5),
                on_click=on_switch_profile,
                ink=True
            ) if user_role == "Admin" else ft.Container()
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # FIX: Added expand=True to this Column to ensure the content fully utilizes the available height
    content = ft.Column(
        [
            header,
            ft.Container(height=16),
            profile_card,
            ft.Container(height=16),
        ],
        spacing=0,
        expand=True, # ADDED: Ensures the content pushes down and is fully scrollable in the main layout.
    )
    
    return create_main_layout(page, content, "/profile", user_role)
