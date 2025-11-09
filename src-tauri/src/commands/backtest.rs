use crate::utils::execute_python_script;

/// Run backtest job
#[tauri::command]
pub async fn run_backtest(
    algorithm_ids: Vec<i32>,
    start_date: String,
    end_date: String,
    data_set_id: Option<i32>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "algorithm_ids": algorithm_ids,
        "start_date": start_date,
        "end_date": end_date,
        "data_set_id": data_set_id
    });
    execute_python_script("run_backtest.py", Some(input)).await
}

/// Get backtest job status
#[tauri::command]
pub async fn get_backtest_status(job_id: String) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_backtest_status.py", Some(input)).await
}

/// Get backtest results
#[tauri::command]
pub async fn get_backtest_results(job_id: String) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_backtest_results.py", Some(input)).await
}

/// Get backtest results summary for multiple algorithms
#[tauri::command]
pub async fn get_backtest_results_summary(
    algorithm_ids: Option<Vec<i64>>,
    limit: Option<i64>,
) -> Result<serde_json::Value, String> {
    let mut input = serde_json::json!({});
    if let Some(ids) = algorithm_ids {
        input["algorithm_ids"] = serde_json::json!(ids);
    }
    if let Some(l) = limit {
        input["limit"] = serde_json::json!(l);
    }
    execute_python_script("get_backtest_results_summary.py", Some(input)).await
}

