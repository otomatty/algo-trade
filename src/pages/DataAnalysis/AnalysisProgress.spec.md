# AnalysisProgress Component Specification

## Related Files

- Implementation: `src/pages/DataAnalysis/AnalysisProgress.tsx`
- Tests: `src/pages/DataAnalysis/AnalysisProgress.test.tsx`

## Related Documentation

- Plan: `docs/03_plans/data-analysis/README.md`
- API Spec: `docs/03_plans/data-analysis/api-spec.md`
- Main Spec: `src/pages/DataAnalysis/DataAnalysis.spec.md`

## Requirements

### RQ-001: 進捗表示機能
- 解析ジョブの進捗をリアルタイムで表示
- 進捗バーで進捗率を可視化（0-100%）
- ジョブ状態を表示（pending/running/completed/failed）
- メッセージを表示

### RQ-002: ポーリング機能
- `get_analysis_status(job_id)` Tauriコマンドを定期的に呼び出す
- ポーリング間隔は2秒（設定可能）
- ジョブが完了または失敗したらポーリングを停止

### RQ-003: エラー表示
- ジョブが失敗した場合、エラーメッセージを表示
- エラー状態を視覚的に区別

### RQ-004: 自動非表示
- ジョブが完了したら、一定時間後に自動的に非表示（オプション）
- または、手動で閉じるボタンを提供

## Test Cases

### TC-001: コンポーネントのレンダリング
**Given**: AnalysisProgressコンポーネントがマウントされる  
**When**: jobIdが提供される  
**Then**: 
- 進捗バーが表示される
- ジョブ状態が表示される
- ポーリングが開始される

### TC-002: 進捗更新の表示
**Given**: ジョブが実行中  
**When**: `get_analysis_status()`が進捗を返す  
**Then**: 
- 進捗バーが更新される
- メッセージが更新される

### TC-003: ジョブ完了時の処理
**Given**: ジョブが実行中  
**When**: ジョブが完了する  
**Then**: 
- 進捗バーが100%になる
- 状態が'completed'になる
- ポーリングが停止する
- 完了コールバックが呼ばれる（オプション）

### TC-004: ジョブ失敗時の処理
**Given**: ジョブが実行中  
**When**: ジョブが失敗する  
**Then**: 
- 状態が'failed'になる
- エラーメッセージが表示される
- ポーリングが停止する

### TC-005: ポーリングの停止
**Given**: ポーリングが実行中  
**When**: コンポーネントがアンマウントされる  
**Then**: 
- ポーリングが停止する
- メモリリークが発生しない

## Component Structure

```
AnalysisProgress
├── Progress Bar (Mantine Progress)
├── Status Text
├── Message Text
└── Error Alert (conditional)
```

## State Management

```typescript
interface AnalysisProgressState {
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string;
  error: string | null;
}
```

## API Integration

### Tauri Commands

#### `get_analysis_status(job_id: string)`
- **Purpose**: 解析ジョブの進捗を取得
- **Request**: `{ job_id: string }`
- **Response**: `{ status, progress, message, error? }`
- **Polling**: 2秒間隔

