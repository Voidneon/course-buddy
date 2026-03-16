// src-tauri/src/lib.rs
use tauri_plugin_shell::ShellExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init()) // Initialize the plugin here
        .setup(|app| {
            // In v2, we use app.shell().sidecar()
            let sidecar_command = app.shell().sidecar("backend")
                .map_err(|e| e.to_string())?;

            let (mut _rx, _child) = sidecar_command.spawn()
                .map_err(|e| e.to_string())?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}