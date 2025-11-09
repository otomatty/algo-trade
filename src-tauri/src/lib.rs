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

/// Get latest analysis results for a data set
#[tauri::command]
async fn get_latest_analysis_results(data_set_id: i32) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_latest_analysis_results.py")?;
    
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

/// Generate algorithm proposals
#[tauri::command]
async fn generate_algorithm_proposals(
    data_set_id: i32,
    analysis_id: Option<i32>,
    num_proposals: Option<i32>,
    user_preferences: Option<serde_json::Value>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("generate_algorithm_proposals.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "data_set_id": data_set_id,
        "analysis_id": analysis_id,
        "num_proposals": num_proposals.unwrap_or(5),
        "user_preferences": user_preferences
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

/// Get proposal generation job status
#[tauri::command]
async fn get_proposal_generation_status(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_proposal_generation_status.py")?;
    
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

/// Get algorithm proposals for a job
#[tauri::command]
async fn get_algorithm_proposals(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_algorithm_proposals.py")?;
    
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

/// Select an algorithm proposal and save it to algorithms table
#[tauri::command]
async fn select_algorithm(
    proposal_id: String,
    custom_name: Option<String>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("select_algorithm.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "proposal_id": proposal_id,
        "custom_name": custom_name
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

/// Get selected algorithms from algorithms table
#[tauri::command]
async fn get_selected_algorithms() -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_selected_algorithms.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    // Empty JSON object as input (script expects JSON input)
    let input = serde_json::json!({});
    
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

/// Delete an algorithm from algorithms table
#[tauri::command]
async fn delete_algorithm(algo_id: i32) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("delete_algorithm.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "algo_id": algo_id
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

/// Run backtest job
#[tauri::command]
async fn run_backtest(
    algorithm_ids: Vec<i32>,
    start_date: String,
    end_date: String,
    data_set_id: Option<i32>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("run_backtest.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "algorithm_ids": algorithm_ids,
        "start_date": start_date,
        "end_date": end_date,
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

/// Get backtest job status
#[tauri::command]
async fn get_backtest_status(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_backtest_status.py")?;
    
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

/// Get backtest results
#[tauri::command]
async fn get_backtest_results(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_backtest_results.py")?;
    
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

/// Get backtest results summary for multiple algorithms
#[tauri::command]
async fn get_backtest_results_summary(
    algorithm_ids: Option<Vec<i64>>,
    limit: Option<i64>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_backtest_results_summary.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let mut input = serde_json::json!({});
    if let Some(ids) = algorithm_ids {
        input["algorithm_ids"] = serde_json::json!(ids);
    }
    if let Some(l) = limit {
        input["limit"] = serde_json::json!(l);
    }
    
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

/// Collect market news from RSS feeds and/or NewsAPI
#[tauri::command]
async fn collect_market_news(
    use_rss: Option<bool>,
    use_api: Option<bool>,
    api_key: Option<String>,
    keywords: Option<Vec<String>>,
    max_articles: Option<i32>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("collect_market_news.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "use_rss": use_rss.unwrap_or(true),
        "use_api": use_api.unwrap_or(false),
        "api_key": api_key,
        "keywords": keywords,
        "max_articles": max_articles.unwrap_or(50)
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

/// Get news collection job status
#[tauri::command]
async fn get_news_collection_status(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_news_collection_status.py")?;
    
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

/// Get collected news from database
#[tauri::command]
async fn get_collected_news(
    limit: Option<i32>,
    offset: Option<i32>,
    source: Option<String>,
    order_by: Option<String>,
    order_desc: Option<bool>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_collected_news.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "limit": limit.unwrap_or(100),
        "offset": offset.unwrap_or(0),
        "source": source,
        "order_by": order_by.unwrap_or_else(|| "published_at".to_string()),
        "order_desc": order_desc.unwrap_or(true)
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

/// Generate stock predictions
#[tauri::command]
async fn generate_stock_predictions(
    news_job_id: Option<String>,
    num_predictions: Option<i32>,
    user_preferences: Option<serde_json::Value>,
    market_trends: Option<String>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("generate_stock_predictions.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "news_job_id": news_job_id,
        "num_predictions": num_predictions.unwrap_or(5),
        "user_preferences": user_preferences,
        "market_trends": market_trends
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

/// Get stock prediction generation job status
#[tauri::command]
async fn get_stock_prediction_status(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_stock_prediction_status.py")?;
    
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

/// Get stock predictions for a job
#[tauri::command]
async fn get_stock_predictions(job_id: String) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_stock_predictions.py")?;
    
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

/// Save a user's action for a stock prediction
#[tauri::command]
async fn save_prediction_action(
    prediction_id: String,
    action: String,
    notes: Option<String>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("save_prediction_action.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "prediction_id": prediction_id,
        "action": action,
        "notes": notes
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

/// Get prediction history with filtering and accuracy statistics
#[tauri::command]
async fn get_prediction_history(
    limit: Option<u32>,
    start_date: Option<String>,
    end_date: Option<String>,
    symbol: Option<String>,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("get_prediction_history.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "limit": limit,
        "start_date": start_date,
        "end_date": end_date,
        "symbol": symbol
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

/// Update prediction accuracy with actual results
#[tauri::command]
async fn update_prediction_accuracy(
    prediction_id: String,
    actual_price: f64,
    actual_direction: String,
) -> Result<serde_json::Value, String> {
    let script_path = get_python_script_path("update_prediction_accuracy.py")?;
    
    let mut cmd = AsyncCommand::new("python3");
    cmd.arg(&script_path);
    cmd.stdin(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::piped());
    cmd.stderr(std::process::Stdio::piped());
    
    let input = serde_json::json!({
        "prediction_id": prediction_id,
        "actual_price": actual_price,
        "actual_direction": actual_direction
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
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            greet,
            import_ohlcv_data,
            collect_from_api,
            get_data_list,
            delete_data_set,
            run_data_analysis,
            get_analysis_status,
            get_analysis_results,
            get_latest_analysis_results,
            generate_algorithm_proposals,
            get_proposal_generation_status,
            get_algorithm_proposals,
            select_algorithm,
            get_selected_algorithms,
            run_backtest,
            get_backtest_status,
            get_backtest_results,
            get_backtest_results_summary,
            delete_algorithm,
            collect_market_news,
            get_news_collection_status,
            get_collected_news,
            generate_stock_predictions,
            get_stock_prediction_status,
            get_stock_predictions,
            save_prediction_action,
            get_prediction_history,
            update_prediction_accuracy
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
