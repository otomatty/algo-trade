use crate::utils::execute_python_script;

/// Collect market news from RSS feeds and/or NewsAPI
#[tauri::command]
pub async fn collect_market_news(
    use_rss: Option<bool>,
    use_api: Option<bool>,
    api_key: Option<String>,
    keywords: Option<Vec<String>>,
    max_articles: Option<i32>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "use_rss": use_rss.unwrap_or(true),
        "use_api": use_api.unwrap_or(false),
        "api_key": api_key,
        "keywords": keywords,
        "max_articles": max_articles.unwrap_or(50)
    });
    execute_python_script("collect_market_news.py", Some(input)).await
}

/// Get news collection job status
#[tauri::command]
pub async fn get_news_collection_status(
    job_id: String,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "job_id": job_id
    });
    execute_python_script("get_news_collection_status.py", Some(input)).await
}

/// Get collected news from database
#[tauri::command]
pub async fn get_collected_news(
    limit: Option<i32>,
    offset: Option<i32>,
    source: Option<String>,
    order_by: Option<String>,
    order_desc: Option<bool>,
) -> Result<serde_json::Value, String> {
    let input = serde_json::json!({
        "limit": limit.unwrap_or(100),
        "offset": offset.unwrap_or(0),
        "source": source,
        "order_by": order_by.unwrap_or_else(|| "published_at".to_string()),
        "order_desc": order_desc.unwrap_or(true)
    });
    execute_python_script("get_collected_news.py", Some(input)).await
}

