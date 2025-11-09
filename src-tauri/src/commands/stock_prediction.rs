use crate::utils::execute_python_script;

/// Generate stock predictions
#[tauri::command]
pub async fn generate_stock_predictions(
    news_job_id: Option<String>,
    num_predictions: Option<i32>,
    user_preferences: Option<serde_json::Value>,
    market_trends: Option<String>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "news_job_id": news_job_id,
        "num_predictions": num_predictions.unwrap_or(5),
        "user_preferences": user_preferences,
        "market_trends": market_trends
    });
    execute_python_script("generate_stock_predictions.py", Some(input)).await
}

/// Get stock prediction generation job status
#[tauri::command]
pub async fn get_stock_prediction_status(
    job_id: String,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_stock_prediction_status.py", Some(input)).await
}

/// Get stock predictions for a job
#[tauri::command]
pub async fn get_stock_predictions(job_id: String) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_stock_predictions.py", Some(input)).await
}

/// Save a user's action for a stock prediction
#[tauri::command]
pub async fn save_prediction_action(
    prediction_id: String,
    action: String,
    notes: Option<String>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "prediction_id": prediction_id,
        "action": action,
        "notes": notes
    });
    execute_python_script("save_prediction_action.py", Some(input)).await
}

/// Get prediction history with filtering and accuracy statistics
#[tauri::command]
pub async fn get_prediction_history(
    limit: Option<u32>,
    start_date: Option<String>,
    end_date: Option<String>,
    symbol: Option<String>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "limit": limit,
        "start_date": start_date,
        "end_date": end_date,
        "symbol": symbol
    });
    execute_python_script("get_prediction_history.py", Some(input)).await
}

/// Update prediction accuracy with actual results
#[tauri::command]
pub async fn update_prediction_accuracy(
    prediction_id: String,
    actual_price: f64,
    actual_direction: String,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "prediction_id": prediction_id,
        "actual_price": actual_price,
        "actual_direction": actual_direction
    });
    execute_python_script("update_prediction_accuracy.py", Some(input)).await
}

