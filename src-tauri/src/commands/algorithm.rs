use crate::utils::execute_python_script;

/// Generate algorithm proposals
#[tauri::command]
pub async fn generate_algorithm_proposals(
    data_set_id: i32,
    analysis_id: Option<i32>,
    num_proposals: Option<i32>,
    user_preferences: Option<serde_json::Value>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "data_set_id": data_set_id,
        "analysis_id": analysis_id,
        "num_proposals": num_proposals.unwrap_or(5),
        "user_preferences": user_preferences
    });
    execute_python_script("generate_algorithm_proposals.py", Some(input)).await
}

/// Get proposal generation job status
#[tauri::command]
pub async fn get_proposal_generation_status(
    job_id: String,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_proposal_generation_status.py", Some(input)).await
}

/// Get algorithm proposals for a job
#[tauri::command]
pub async fn get_algorithm_proposals(job_id: String) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_algorithm_proposals.py", Some(input)).await
}

/// Select an algorithm proposal and save it to algorithms table
#[tauri::command]
pub async fn select_algorithm(
    proposal_id: String,
    custom_name: Option<String>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "proposal_id": proposal_id,
        "custom_name": custom_name
    });
    execute_python_script("select_algorithm.py", Some(input)).await
}

/// Get selected algorithms from algorithms table
#[tauri::command]
pub async fn get_selected_algorithms() -> Result<serde_json::Value, String> {
    // Empty JSON object as input (script expects JSON input)
    let input = serde_json::json!({});
    execute_python_script("get_selected_algorithms.py", Some(input)).await
}

/// Delete an algorithm from algorithms table
#[tauri::command]
pub async fn delete_algorithm(algo_id: i32) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "algo_id": algo_id
    });
    execute_python_script("delete_algorithm.py", Some(input)).await
}

