# 国際化対応（i18n）開発ガイドライン

## 概要

本ガイドラインは、プロジェクト全体で国際化対応を実装する際のベストプラクティスと手順を定義します。

## 基本原則

1. **新規コンポーネントは最初から国際化対応**
   - ハードコードされたテキストは使用しない
   - `useTranslation()` フックを使用して翻訳を取得

2. **既存コンポーネントは段階的に移行**
   - 優先度の高い機能から順次移行
   - 機能単位で完全移行を実施

3. **翻訳キーは名前空間付きで記述**
   - 例: `t('navigation.dashboard')`
   - 名前空間を明示することで、どの機能の翻訳かが明確になる

## 実装手順

### 新規コンポーネントの実装

1. コンポーネントファイルを作成
2. `useTranslation()` フックをインポート
3. 適切な名前空間を指定して `useTranslation()` を呼び出し
4. ハードコードされたテキストを翻訳キーに置き換え
5. 翻訳ファイル（`ja/` と `en/`）を作成・更新
6. `src/i18n/index.ts` に翻訳リソースを追加

### 既存コンポーネントの移行

1. コンポーネント内のハードコードされたテキストを特定
2. 適切な名前空間を決定（既存の名前空間を使用するか、新規作成）
3. 翻訳ファイルに翻訳キーを追加
4. コンポーネント内で `useTranslation()` を使用
5. ハードコードされたテキストを翻訳キーに置き換え
6. テストを実行して動作確認

## 名前空間の使い分け

### 既存の名前空間

- **`common`**: 共通UI要素（ボタン、ラベル、メッセージなど）
  - 例: `buttons.save`, `labels.loading`, `messages.error`
- **`navigation`**: ナビゲーション関連（Sidebar, Header）
  - 例: `dashboard`, `algorithmProposal`, `appTitle`

### 機能別名前空間（今後追加予定）

- **`dashboard`**: ダッシュボード機能固有
- **`data-management`**: データ管理機能固有
- **`data-analysis`**: データ解析機能固有
- **`algorithm-proposal`**: アルゴリズム提案機能固有
- **`backtest`**: バックテスト機能固有
- **`stock-prediction`**: 銘柄予測機能固有
- **`news`**: ニュース関連

## 翻訳キーの命名規則

1. **camelCase**を使用
   - 例: `dataManagement`, `algorithmProposal`
2. 意味が明確になるように命名
   - 悪い例: `text1`, `label`
   - 良い例: `dashboardTitle`, `saveButton`
3. 階層構造を活用
   - 例: `buttons.save`, `labels.loading`, `messages.error`

## 翻訳ファイルの追加方法

### 1. 翻訳ファイルの作成

`src/i18n/locales/ja/` と `src/i18n/locales/en/` に新しいJSONファイルを作成します。

**例: `src/i18n/locales/ja/dashboard.json`**
```json
{
  "title": "ダッシュボード",
  "welcome": "ようこそ",
  "metrics": {
    "totalAlgorithms": "総アルゴリズム数",
    "totalBacktests": "総バックテスト数"
  }
}
```

### 2. i18n設定ファイルの更新

`src/i18n/index.ts` の `resources` に追加します。

```typescript
import dashboardJa from './locales/ja/dashboard.json';
import dashboardEn from './locales/en/dashboard.json';

resources: {
  ja: {
    // ... existing
    dashboard: dashboardJa,
  },
  en: {
    // ... existing
    dashboard: dashboardEn,
  },
},
```

### 3. 名前空間の登録

`src/i18n/index.ts` の `ns` 配列に追加します。

```typescript
ns: ['common', 'navigation', 'dashboard'],
```

## テスト時の注意事項

### 1. テストファイルでの国際化対応

テストファイルでも国際化を考慮する必要があります。

```typescript
import { render } from '@testing-library/react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';

test('renders component', () => {
  render(
    <I18nextProvider i18n={i18n}>
      <MyComponent />
    </I18nextProvider>
  );
});
```

### 2. 翻訳キーの存在確認テスト

翻訳キーが存在することを確認するテストを追加します。

```typescript
test('translation keys exist', () => {
  const { t } = useTranslation('navigation');
  expect(t('dashboard')).toBeTruthy();
  expect(t('algorithmProposal')).toBeTruthy();
});
```

## よくある問題と解決方法

### 1. 翻訳キーが表示されない

**問題**: 翻訳キー自体が表示される（例: `navigation.dashboard`）

**解決方法**:
- 翻訳ファイルにキーが存在するか確認
- 名前空間が正しく指定されているか確認
- `src/i18n/index.ts` の `resources` に追加されているか確認

### 2. 言語切り替えが反映されない

**問題**: 言語を切り替えても表示が変わらない

**解決方法**:
- コンポーネントが再レンダリングされているか確認
- `i18n.changeLanguage()` が正しく呼ばれているか確認
- ローカルストレージに保存されているか確認

### 3. 型エラーが発生する

**問題**: TypeScriptの型エラーが発生する

**解決方法**:
- `src/i18n/resources.ts` の型定義を確認
- 新しい名前空間を追加した場合は、型定義も更新

## ベストプラクティス

1. **一貫性を保つ**
   - 同じ意味のテキストは同じ翻訳キーを使用
   - 命名規則に従う

2. **階層構造を活用**
   - 関連する翻訳キーはグループ化
   - 例: `buttons.save`, `buttons.cancel`, `buttons.delete`

3. **コメントを追加**
   - 翻訳ファイルにコメントを追加（JSON5を使用するか、別ファイルで管理）
   - コンテキストが分かるようにする

4. **テストを書く**
   - 翻訳キーの存在確認テスト
   - 言語切り替えのテスト

5. **レビューを実施**
   - 翻訳の品質を確認
   - 命名規則に従っているか確認

## コードレビューガイドライン

### レビュー時の確認ポイント

コードレビュー時には、以下の観点から国際化対応を確認してください。

#### 1. ハードコードされたテキストの検出

**確認方法**:
- コンポーネント内で日本語や英語の文字列リテラルを検索
- JSX内の `"` や `'` で囲まれたテキストを確認
- コメント以外の文字列リテラルが存在しないか確認

**検出例**:
```typescript
// ❌ 悪い例
<Button>保存</Button>
<Text>エラーが発生しました</Text>

// ✅ 良い例
<Button>{t('buttons.save')}</Button>
<Text>{t('messages.error')}</Text>
```

#### 2. 翻訳キーの命名規則チェック

**確認項目**:
- camelCase で命名されているか
- 意味が明確か（`text1`, `label` などの曖昧な名前ではないか）
- 階層構造を適切に使用しているか
- 既存の翻訳キーと重複していないか

**チェック例**:
```typescript
// ❌ 悪い例
t('text1')
t('label')
t('button')

// ✅ 良い例
t('dashboard.title')
t('buttons.save')
t('labels.loading')
```

#### 3. 名前空間の適切な使用

**確認項目**:
- 適切な名前空間を選択しているか
- `common` 名前空間の再利用可能なキーを使用しているか
- 複数の名前空間を使用する場合は、適切に使い分けているか

**チェック例**:
```typescript
// ❌ 悪い例
// 共通ボタンを機能別名前空間に定義
const { t } = useTranslation('dashboard');
<Button>{t('save')}</Button> // common を使うべき

// ✅ 良い例
// 共通ボタンは common を使用
const { t } = useTranslation(['common', 'dashboard']);
<Button>{t('common:buttons.save')}</Button>
<h1>{t('dashboard:title')}</h1>
```

#### 4. 翻訳ファイルの構造チェック

**確認項目**:
- 日本語と英語の翻訳ファイルの構造が一致しているか
- 全ての翻訳キーが両方の言語ファイルに存在するか
- JSON構造が適切か（階層構造の使用）

**チェック例**:
```json
// ❌ 悪い例 - 構造が不一致
// ja/dashboard.json
{ "title": "ダッシュボード" }

// en/dashboard.json
{ "dashboard": { "title": "Dashboard" } }

// ✅ 良い例 - 構造が一致
// ja/dashboard.json
{ "title": "ダッシュボード" }

// en/dashboard.json
{ "title": "Dashboard" }
```

#### 5. i18n設定の確認

**確認項目**:
- `src/i18n/index.ts` に新しい名前空間が追加されているか
- `ns` 配列に名前空間が追加されているか
- 型定義ファイルが更新されているか（必要に応じて）

#### 6. テストでの国際化対応確認

**確認項目**:
- テストファイルで `I18nextProvider` を使用しているか
- 翻訳キーの存在確認テストがあるか
- 言語切り替えのテストがあるか（必要に応じて）

## 参考資料

- [react-i18next公式ドキュメント](https://react.i18next.com/)
- [i18next公式ドキュメント](https://www.i18next.com/)
- テンプレート: `docs/rules/i18n-template.md`
- チェックリスト: `docs/rules/i18n-checklist.md`
- ワークフロー: `docs/rules/i18n-workflow.md`

