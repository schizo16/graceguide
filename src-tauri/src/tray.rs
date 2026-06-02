use tauri::{
    menu::{Menu, MenuItem},
    tray::TrayIconBuilder,
    AppHandle,
};

pub fn setup(app: &AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    let show_item = MenuItem::with_id(app, "show", "Show Overlay", true, None::<&str>)?;
    let quit_item = MenuItem::with_id(app, "quit", "Quit GraceGuide", true, None::<&str>)?;
    let menu = Menu::with_items(app, &[&show_item, &quit_item])?;

    let icon = app.default_window_icon().cloned().ok_or("no default icon")?;

    TrayIconBuilder::new()
        .icon(icon)
        .menu(&menu)
        .tooltip("GraceGuide")
        .on_menu_event(|app, event| match event.id().as_ref() {
            "show" => {
                let _ = crate::overlay::toggle(app);
            }
            "quit" => {
                app.exit(0);
            }
            _ => {}
        })
        .build(app)?;

    Ok(())
}
