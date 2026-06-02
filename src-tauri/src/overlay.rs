use tauri::{AppHandle, Manager};

pub fn setup(app: &AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    let window = app.get_webview_window("overlay").ok_or("overlay window not found")?;
    // Start hidden with click-through
    window.set_ignore_cursor_events(true)?;
    Ok(())
}

pub fn toggle(app: &AppHandle) -> Result<(), String> {
    let window = app.get_webview_window("overlay").ok_or("overlay window not found")?;
    if window.is_visible().unwrap_or(false) {
        hide(app)
    } else {
        show(app)
    }
}

pub fn show(app: &AppHandle) -> Result<(), String> {
    let window = app.get_webview_window("overlay").ok_or("overlay window not found")?;
    window.set_ignore_cursor_events(false).map_err(|e| e.to_string())?;
    window.show().map_err(|e| e.to_string())?;
    window.set_focus().map_err(|e| e.to_string())?;
    Ok(())
}

pub fn hide(app: &AppHandle) -> Result<(), String> {
    let window = app.get_webview_window("overlay").ok_or("overlay window not found")?;
    window.hide().map_err(|e| e.to_string())?;
    window.set_ignore_cursor_events(true).map_err(|e| e.to_string())?;
    Ok(())
}

pub fn set_click_through(app: &AppHandle, enabled: bool) -> Result<(), String> {
    let window = app.get_webview_window("overlay").ok_or("overlay window not found")?;
    window.set_ignore_cursor_events(enabled).map_err(|e| e.to_string())?;
    Ok(())
}
