use std::process::{Child, Command};
use std::sync::Mutex;

pub struct Sidecar {
    pub process: Mutex<Option<Child>>,
}

impl Sidecar {
    pub fn start() -> Result<Self, String> {
        let child = Command::new("python")
            .arg("backend/main.py")
            .spawn();

        match child {
            Ok(c) => {
                println!("Python sidecar started (PID: {})", c.id());
                Ok(Self {
                    process: Mutex::new(Some(c)),
                })
            }
            Err(e) => {
                eprintln!("Warning: Could not start Python sidecar: {}", e);
                // Return sidecar without process — will retry on chat
                Ok(Self {
                    process: Mutex::new(None),
                })
            }
        }
    }

    pub fn stop(&self) {
        if let Ok(mut guard) = self.process.lock() {
            if let Some(mut child) = guard.take() {
                let _ = child.kill();
                let _ = child.wait();
                println!("Python sidecar stopped");
            }
        }
    }

    pub fn is_running(&self) -> bool {
        if let Ok(guard) = self.process.lock() {
            guard.is_some()
        } else {
            false
        }
    }
}
