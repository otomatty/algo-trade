use crate::utils::execute_python_script;

/// Configure data collection schedule
#[tauri::command]
pub async fn configure_data_collection(
    action: String,
    schedule_id: Option<String>,
    name: Option<String>,
    source: Option<String>,
    symbol: Option<String>,
    cron_expression: Option<String>,
    start_date: Option<String>,
    end_date: Option<String>,
    api_key: Option<String>,
    data_set_name: Option<String>,
    enabled: Option<bool>,
) -> Result<serde_json::Value, String> {
    let mut input = serde_json::json!({
        "action": action
    });
    
    if let Some(id) = schedule_id {
        input["schedule_id"] = serde_json::Value::String(id);
    }
    if let Some(n) = name {
        input["name"] = serde_json::Value::String(n);
    }
    if let Some(s) = source {
        input["source"] = serde_json::Value::String(s);
    }
    if let Some(s) = symbol {
        input["symbol"] = serde_json::Value::String(s);
    }
    if let Some(c) = cron_expression {
        input["cron_expression"] = serde_json::Value::String(c);
    }
    if let Some(s) = start_date {
        input["start_date"] = serde_json::Value::String(s);
    }
    if let Some(e) = end_date {
        input["end_date"] = serde_json::Value::String(e);
    }
    if let Some(k) = api_key {
        input["api_key"] = serde_json::Value::String(k);
    }
    if let Some(d) = data_set_name {
        input["data_set_name"] = serde_json::Value::String(d);
    }
    if let Some(e) = enabled {
        input["enabled"] = serde_json::Value::Bool(e);
    }
    
    execute_python_script("configure_data_collection.py", Some(input)).await
}

/// Get data collection schedules
#[tauri::command]
pub async fn get_data_collection_schedules(
    enabled_only: Option<bool>,
    schedule_id: Option<String>,
) -> Result<serde_json::Value, String> {
    let mut input = serde_json::json!({});
    if let Some(e) = enabled_only {
        input["enabled_only"] = serde_json::Value::Bool(e);
    }
    if let Some(id) = schedule_id {
        input["schedule_id"] = serde_json::Value::String(id);
    }
    execute_python_script("get_data_collection_schedules.py", Some(input)).await
}

/// Get data collection job status
#[tauri::command]
pub async fn get_data_collection_status(
    job_id: Option<String>,
    schedule_id: Option<String>,
) -> Result<serde_json::Value, String> {
    let mut input = serde_json::json!({});
    if let Some(id) = job_id {
        input["job_id"] = serde_json::Value::String(id);
    }
    if let Some(id) = schedule_id {
        input["schedule_id"] = serde_json::Value::String(id);
    }
    execute_python_script("get_data_collection_status.py", Some(input)).await
}

