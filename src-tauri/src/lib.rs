// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use tokio::process::Command as AsyncCommand;

#[derive(Debug, Serialize, Deserialize)]
struct PythonResponse {
    success: bool,
    data: Option<serde_json::Value>,
    error: Option<String>,
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

/// Import OHLCV data from CSV file
#[tauri::command]
async fn import_ohlcv_data(file_path: String, name: Option<String>) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("import_ohlcv.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "file_path": file_path,
        "name": name
    });
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin
    if let Some(mut stdin) = child.stdin.take() {
        use tokio::io::AsyncWriteExt;
        stdin.write_all(input.to_string().as_bytes())
            .await
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
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

/// Collect OHLCV data from external API
#[tauri::command]
async fn collect_from_api(
    source: String,
    symbol: String,
    start_date: String,
    end_date: String,
    name: Option<String>,
    api_key: Option<String>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("collect_from_api.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "source": source,
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "name": name,
        "api_key": api_key
    });
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin
    if let Some(mut stdin) = child.stdin.take() {
        use tokio::io::AsyncWriteExt;
        stdin.write_all(input.to_string().as_bytes())
            .await
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
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

/// Get list of data sets
#[tauri::command]
async fn get_data_list() -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_data_list.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let output = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?
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

/// Delete a data set
#[tauri::command]
async fn delete_data_set(data_set_id: i32) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("delete_data_set.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "data_set_id": data_set_id
    });
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin
    if let Some(mut stdin) = child.stdin.take() {
        use tokio::io::AsyncWriteExt;
        stdin.write_all(input.to_string().as_bytes())
            .await
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
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

/// Run data analysis job
#[tauri::command]
async fn run_data_analysis(data_set_id: i32) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("run_data_analysis.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "data_set_id": data_set_id
    });
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin
    if let Some(mut stdin) = child.stdin.take() {
        use tokio::io::AsyncWriteExt;
        stdin.write_all(input.to_string().as_bytes())
            .await
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
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

/// Get analysis job status
#[tauri::command]
async fn get_analysis_status(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_analysis_status.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "job_id": job_id
    });
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin
    if let Some(mut stdin) = child.stdin.take() {
        use tokio::io::AsyncWriteExt;
        stdin.write_all(input.to_string().as_bytes())
            .await
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
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

/// Get analysis results
#[tauri::command]
async fn get_analysis_results(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_analysis_results.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "job_id": job_id
    });
    
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;
    
    // Write input to stdin
    if let Some(mut stdin) = child.stdin.take() {
        use tokio::io::AsyncWriteExt;
        stdin.write_all(input.to_string().as_bytes())
            .await
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
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

fn get_python_script_path(script_name: &str) -> Result<PathBuf, String> {
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

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            greet,
            import_ohlcv_data,
            collect_from_api,
            get_data_list,
            delete_data_set,
            run_data_analysis,
            get_analysis_status,
            get_analysis_results
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
