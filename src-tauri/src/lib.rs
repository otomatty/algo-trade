// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/

mod utils;
mod commands;

use commands::{
    algorithm, backtest, data_analysis, data_collection, data_management, misc, news,
    stock_prediction,
};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            // Misc
            misc::greet,
            // Data Management
            data_management::import_ohlcv_data,
            data_management::collect_from_api,
            data_management::get_data_list,
            data_management::delete_data_set,
            data_management::get_data_preview,
            data_management::update_data_set,
            data_management::check_data_integrity,
            // Data Analysis
            data_analysis::run_data_analysis,
            data_analysis::get_analysis_status,
            data_analysis::get_analysis_results,
            data_analysis::get_latest_analysis_results,
            // Algorithm
            algorithm::generate_algorithm_proposals,
            algorithm::get_proposal_generation_status,
            algorithm::get_algorithm_proposals,
            algorithm::select_algorithm,
            algorithm::get_selected_algorithms,
            algorithm::delete_algorithm,
            // Backtest
            backtest::run_backtest,
            backtest::get_backtest_status,
            backtest::get_backtest_results,
            backtest::get_backtest_results_summary,
            // News
            news::collect_market_news,
            news::get_news_collection_status,
            news::get_collected_news,
            // Stock Prediction
            stock_prediction::generate_stock_predictions,
            stock_prediction::get_stock_prediction_status,
            stock_prediction::get_stock_predictions,
            stock_prediction::save_prediction_action,
            stock_prediction::get_prediction_history,
            stock_prediction::update_prediction_accuracy,
            // Data Collection
            data_collection::configure_data_collection,
            data_collection::get_data_collection_schedules,
            data_collection::get_data_collection_status,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
