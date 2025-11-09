use crate::utils::execute_python_script;

/// Run data analysis job
#[tauri::command]
pub async fn run_data_analysis(data_set_id: i32) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "data_set_id": data_set_id
    });
    execute_python_script("run_data_analysis.py", Some(input)).await
}

/// Get analysis job status
#[tauri::command]
pub async fn get_analysis_status(job_id: String) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_analysis_status.py", Some(input)).await
}

/// Get analysis results
#[tauri::command]
pub async fn get_analysis_results(job_id: String) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_analysis_results.py", Some(input)).await
}

/// Get latest analysis results for a data set
#[tauri::command]
pub async fn get_latest_analysis_results(
    data_set_id: i32,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "data_set_id": data_set_id
    });
    execute_python_script("get_latest_analysis_results.py", Some(input)).await
}

