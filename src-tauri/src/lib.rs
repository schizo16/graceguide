mod overlay;
mod tray;
mod ipc;

use tauri::Manager;

#[tauri::command]
async fn toggle_overlay(app: tauri::AppHandle) -> Result<(), String> {
    overlay::toggle(&app)
}

#[tauri::command]
async fn hide_overlay(app: tauri::AppHandle) -> Result<(), String> {
    overlay::hide(&app)
}

#[tauri::command]
async fn chat(message: String) -> Result<String, String> {
    let client = reqwest::Client::new();
    let payload = serde_json::json!({
        "message": message,
        "language": "en"
    });
    let resp = client
        .post("http://127.0.0.1:3721/chat")
        .json(&payload)
        .send()
        .await
        .map_err(|e| format!("Backend error: {}", e))?;
    let body: serde_json::Value = resp
        .json()
        .await
        .map_err(|e| format!("Parse error: {}", e))?;
    Ok(body["response"].as_str().unwrap_or("No response").to_string())
}

pub fn run() {
    let app = tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(
            tauri_plugin_global_shortcut::Builder::new()
                .with_shortcut("Ctrl+Alt+G").expect("valid shortcut")
                .with_handler(move |app, _shortcut, event| {
                    if event.state == tauri_plugin_global_shortcut::ShortcutState::Pressed {
                        let _ = overlay::toggle(app);
                    }
                })
                .build(),
        )
        .setup(|app| {
            // Start Python sidecar (optional)
            match ipc::Sidecar::start() {
                Ok(sidecar) => {
                    app.manage(sidecar);
                }
                Err(e) => {
                    eprintln!("Warning: Failed to start sidecar: {}", e);
                }
            }

            overlay::setup(app.handle())?;
            tray::setup(app.handle())?;

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![toggle_overlay, hide_overlay, chat])
        .build(tauri::generate_context!())
        .expect("error while building GraceGuide");

    app.run(|app_handle, event| {
        if let tauri::RunEvent::Exit = event {
            if let Some(sidecar) = app_handle.try_state::<ipc::Sidecar>() {
                sidecar.stop();
            }
        }
    });
}
