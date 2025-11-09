use crate::utils::execute_python_script;

/// Import OHLCV data from CSV file
#[tauri::command]
pub async fn import_ohlcv_data(
    file_path: String,
    name: Option<String>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "file_path": file_path,
        "name": name
    });
    execute_python_script("import_ohlcv.py", Some(input)).await
}

/// Collect OHLCV data from external API
#[tauri::command]
pub async fn collect_from_api(
    source: String,
    symbol: String,
    start_date: String,
    end_date: String,
    name: Option<String>,
    api_key: Option<String>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "source": source,
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "name": name,
        "api_key": api_key
    });
    execute_python_script("collect_from_api.py", Some(input)).await
}

/// Get list of data sets
#[tauri::command]
pub async fn get_data_list() -> Result<serde_json::Value, String> {
    execute_python_script("get_data_list.py", None).await
}

/// Delete a data set
#[tauri::command]
pub async fn delete_data_set(data_set_id: i32) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "data_set_id": data_set_id
    });
    execute_python_script("delete_data_set.py", Some(input)).await
}

/// Get data preview for a data set
#[tauri::command]
pub async fn get_data_preview(
    data_set_id: i32,
    limit: Option<u32>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "data_set_id": data_set_id,
        "limit": limit.unwrap_or(100)
    });
    execute_python_script("get_data_preview.py", Some(input)).await
}

/// Update dataset with new data
#[tauri::command]
pub async fn update_data_set(
    data_set_id: i32,
    start_date: Option<String>,
    end_date: Option<String>,
) -> Result<serde_json::Value, String> {
    let mut input = serde_json::json!({
        "data_set_id": data_set_id
    });
    if let Some(s) = start_date {
        input["start_date"] = serde_json::Value::String(s);
    }
    if let Some(e) = end_date {
        input["end_date"] = serde_json::Value::String(e);
    }
    execute_python_script("update_data_set.py", Some(input)).await
}

/// Check data integrity
#[tauri::command]
pub async fn check_data_integrity(data_set_id: i32) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "data_set_id": data_set_id
    });
    execute_python_script("check_data_integrity.py", Some(input)).await
}

