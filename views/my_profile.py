import flet as ft
from flet import padding, border_radius, Icons, ControlState
from layouts import create_main_layout
from components import create_text_field, create_admin_button, PRIMARY_COLOR, SECONDARY_COLOR
from activity_log import log_activity

def profile_view(page: ft.Page, is_admin_view=False):
    # Create a container to hold the profile picture
    profile_picture = ft.Container(
        ft.Icon(Icons.PERSON, size=80, color=ft.Colors.BLACK54),
        width=120,
        height=150,
        border_radius=border_radius.all(75),
        bgcolor=SECONDARY_COLOR,
        alignment=ft.alignment.center
    )
    
    # Create text field references (these return wrappers from your component)
    name_field_col = create_text_field("Name", hint_text="Enter new username", width=600)
    email_field_col = create_text_field("Email", hint_text="Enter new email", width=600)
    current_password_field_col = create_text_field("Current Password:", password=True, width=600)
    new_password_field_col = create_text_field("New Password:", password=True, width=600)

    # Helper: recursively find a TextField inside any wrapper
    def find_text_field(control):
        if control is None:
            return None
        if isinstance(control, ft.TextField):
            return control
        if hasattr(control, "content") and control.content is not None:
            tf = find_text_field(control.content)
            if tf:
                return tf
        if hasattr(control, "controls") and control.controls:
            for child in control.controls:
                tf = find_text_field(child)
                if tf:
                    return tf
        return None

    def on_logout(e):
        log_activity("logout", "admin" if is_admin_view else "user", "User logged out")
        page.session.set("current_user", "")
        page.session.set("user_role", "User")
        page.go("/login")
    
    def on_image_picked(e: ft.FilePickerResultEvent):
        """Handle image selection from file picker."""
        try:
            if e.files:
                selected_file = e.files[0].path
                # Replace the icon with the actual image
                profile_picture.content = ft.Image(
                    src=selected_file,
                    width=120,
                    height=150,
                    fit=ft.ImageFit.COVER,
                )
                profile_picture.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Image load error: {ex}"))
            page.snack_bar.open = True
            page.update()
    
    def on_update_profile(e):
        """Handle profile update - saves username, email, password, and profile picture."""
        try:
            # Find underlying TextField controls
            name_field = find_text_field(name_field_col)
            email_field = find_text_field(email_field_col)
            current_password_field = find_text_field(current_password_field_col)
            new_password_field = find_text_field(new_password_field_col)

            if not all([name_field, email_field, current_password_field, new_password_field]):
                page.snack_bar = ft.SnackBar(ft.Text("Form fields not initialized correctly."))
                page.snack_bar.open = True
                page.update()
                return
            
            # Read values
            new_username = (name_field.value or "").strip()
            new_email = (email_field.value or "").strip()
            current_password = (current_password_field.value or "").strip()
            new_password = (new_password_field.value or "").strip()
            
            # Validate
            if not new_username or not new_email:
                page.snack_bar = ft.SnackBar(ft.Text("Username and Email are required!"))
                page.snack_bar.open = True
                page.update()
                return
            
            # Save username and email to session (or your persistent store)
            page.session.set("username", new_username)
            page.session.set("email", new_email)
            
            # Save password if provided
            if new_password:
                if not current_password:
                    page.snack_bar = ft.SnackBar(ft.Text("Current password is required to set new password!"))
                    page.snack_bar.open = True
                    page.update()
                    return
                page.session.set("password", new_password)
            
            # Save profile picture path if an image is present
            if isinstance(profile_picture.content, ft.Image):
                page.session.set("profile_picture", profile_picture.content.src)

            # Log the activity
            log_activity("profile_update", "admin" if is_admin_view else "user", f"Profile updated for {new_username}")

            # Update UI controls
            name_field.value = new_username
            email_field.value = new_email
            current_password_field.value = ""
            new_password_field.value = ""

            saved_pp = page.session.get("profile_picture")
            if saved_pp:
                profile_picture.content = ft.Image(
                    src=saved_pp,
                    width=120,
                    height=150,
                    fit=ft.ImageFit.COVER,
                )

            # Show confirmation
            page.snack_bar = ft.SnackBar(ft.Text("Profile updated successfully!"))
            page.snack_bar.open = True

            name_field.update()
            email_field.update()
            current_password_field.update()
            new_password_field.update()
            profile_picture.update()
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Update failed: {ex}"))
            page.snack_bar.open = True
            page.update()
            raise

    # Preload saved values
    saved_username = page.session.get("username")
    saved_email = page.session.get("email")
    saved_profile_picture = page.session.get("profile_picture")

    name_tf = find_text_field(name_field_col)
    email_tf = find_text_field(email_field_col)

    if name_tf and saved_username:
        name_tf.value = saved_username
    if email_tf and saved_email:
        email_tf.value = saved_email
    if saved_profile_picture:
        profile_picture.content = ft.Image(
            src=saved_profile_picture,
            width=120,
            height=150,
            fit=ft.ImageFit.COVER,
        )

    # Create file picker
    file_picker = ft.FilePicker(on_result=on_image_picked)
    page.overlay.append(file_picker)

    # --- FIXED PART: Bind click to REAL button inside wrapper ---

    update_btn = create_admin_button("Update Profile", is_primary=True)

    def set_click_recursive(ctrl):
        """Recursively find the real button and attach on_click."""
        if hasattr(ctrl, "on_click"):
            ctrl.on_click = on_update_profile
        if hasattr(ctrl, "controls"):
            for c in ctrl.controls:
                set_click_recursive(c)
        if hasattr(ctrl, "content") and ctrl.content:
            set_click_recursive(ctrl.content)

    set_click_recursive(update_btn)

    # Logout button
    logout_btn = create_admin_button("Logout", is_primary=False)
    set_click_recursive(logout_btn)  # also fix logout button
    # Ensure logout still calls its handler
    def fix_logout(ctrl):
        if hasattr(ctrl, "on_click"):
            ctrl.on_click = on_logout
        if hasattr(ctrl, "controls"):
            for c in ctrl.controls:
                fix_logout(c)
        if hasattr(ctrl, "content") and ctrl.content:
            fix_logout(ctrl.content)
    fix_logout(logout_btn)

    # UI Layout
    profile_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        name_field_col,
                        ft.Container(height=10),
                        email_field_col,
                        ft.Container(height=20),
                        ft.Text("Change Password", size=18, weight=ft.FontWeight.BOLD),
                        current_password_field_col,
                        new_password_field_col,
                    ],
                    expand=True,
                    spacing=0
                ),
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        profile_picture,
                        ft.TextButton(
                            "Change picture",
                            on_click=lambda e: file_picker.pick_files(
                                allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp"]
                            ),
                            style=ft.ButtonStyle(
                                bgcolor={ControlState.DEFAULT: ft.Colors.PURPLE_200},
                                color={ControlState.DEFAULT: ft.Colors.BLACK}
                            )
                        ),
                        ft.Container(height=40),
                        update_btn,
                        ft.Container(height=15),
                        logout_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            spacing=30
        ),
        padding=100,
        bgcolor=ft.Colors.WHITE,
        border_radius=border_radius.all(10),
        expand=True,
    )

    title_row = ft.Row(
        [
            ft.Text("My Profile", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Row([
                    ft.Text("Admin 1", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Icon(Icons.ARROW_DROP_DOWN, color=ft.Colors.WHITE)
                ]),
                padding=padding.symmetric(horizontal=15, vertical=5),
                bgcolor=PRIMARY_COLOR,
                border_radius=border_radius.all(5),
            ) if is_admin_view else ft.Container()
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    content = ft.Column(
        [
            title_row,
            profile_card
        ],
        expand=True
    )

    user_role = page.session.get("user_role") or "User"
    return create_main_layout(page, content, "/profile", user_role)
