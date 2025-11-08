# AnalysisResults Component Specification

## Related Files

- Implementation: `src/pages/DataAnalysis/AnalysisResults.tsx`
- Sub-components:
  - `src/pages/DataAnalysis/TrendAnalysis.tsx`
  - `src/pages/DataAnalysis/TechnicalIndicators.tsx`
  - `src/pages/DataAnalysis/Statistics.tsx`
- Tests: `src/pages/DataAnalysis/AnalysisResults.test.tsx`

## Related Documentation

- Plan: `docs/03_plans/data-analysis/README.md`
- API Spec: `docs/03_plans/data-analysis/api-spec.md`

## Requirements

### RQ-001: 解析結果の取得と表示
- `get_analysis_results(job_id)` Tauriコマンドで結果を取得
- 解析結果サマリーを表示
- テクニカル指標を表示
- 統計情報を表示

### RQ-002: サブコンポーネント
- TrendAnalysis: トレンド分析結果の表示
- TechnicalIndicators: テクニカル指標の表示
- Statistics: 統計情報の表示

## Test Cases

### TC-001: 解析結果の表示
**Given**: ジョブが完了している  
**When**: コンポーネントがマウントされる  
**Then**: 
- 解析結果が表示される
- サマリー、指標、統計が表示される

