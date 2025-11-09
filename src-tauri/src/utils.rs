use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use tokio::process::Command as AsyncCommand;

#[derive(Debug, Serialize, Deserialize)]
pub struct PythonResponse {
    pub success: bool,
    pub data: Option<serde_json::Value>,
    pub error: Option<String>,
}

/// Get the path to a Python script in src-python/scripts/
pub fn get_python_script_path(script_name: &str) -> Result<PathBuf, String> {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.pop(); // Go up from src-tauri
    path.push("src-python");
    path.push("scripts");
    path.push(script_name);
    
    if !path.exists() {
        return Err(format!("Python script not found: {}", path.display()));
    }
    
    Ok(path)
}

/// Execute a Python script with optional JSON input
pub async fn execute_python_script(
    script_name: &str,
    input: Option<serde_json::Value>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path(script_name)?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    // Set up stdin only if input is provided
    if input.is_some() {
        cmd.stdin(std::process::Stdio::piped());
    }
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin if provided
    if let Some(input_value) = input {
        if let Some(mut stdin) = child.stdin.take() {
            use tokio::io::AsyncWriteExt;
            stdin.write_all(input_value.to_string().as_bytes())
                .await
                .map_err(|e| format!("Failed to write to stdin: {}", e))?;
        }
    }
    
    let output = child
        .wait_with_output()
        .await
        .map_err(|e| format!("Failed to wait for Python process: {}", e))?;
    
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("Python script failed: {}", stderr));
    }
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    let response: PythonResponse = serde_json::from_str(&stdout)
        .map_err(|e| format!("Failed to parse Python response: {}", e))?;
    
    if response.success {
        Ok(response.data.unwrap_or(serde_json::Value::Null))
    } else {
        Err(response.error.unwrap_or_else(|| "Unknown error".to_string()))
    }
}

