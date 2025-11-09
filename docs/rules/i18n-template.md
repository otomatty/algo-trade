# 国際化対応テンプレート

## 新規コンポーネント実装時の国際化対応

新規コンポーネントを実装する際は、以下のテンプレートに従って国際化対応を行ってください。

### 1. 基本的な使用方法

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation('namespace'); // 名前空間を指定
  
  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
    </div>
  );
}
```

### 2. 名前空間の使い分け

- **`common`**: 共通UI要素（ボタン、ラベル、メッセージなど）
- **`navigation`**: ナビゲーション関連（Sidebar, Header）
- **`dashboard`**: ダッシュボード機能固有
- **`data-management`**: データ管理機能固有
- **`data-analysis`**: データ解析機能固有
- **`algorithm-proposal`**: アルゴリズム提案機能固有
- **`backtest`**: バックテスト機能固有
- **`stock-prediction`**: 銘柄予測機能固有
- **`news`**: ニュース関連

### 3. 複数の名前空間を使用する場合

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation(['common', 'dashboard']);
  
  return (
    <div>
      <button>{t('common:buttons.save')}</button>
      <h1>{t('dashboard:title')}</h1>
    </div>
  );
}
```

### 4. 翻訳キーの命名規則

- **camelCase**を使用（例: `dataManagement`, `algorithmProposal`）
- 意味が明確になるように命名
- 階層構造を活用（例: `buttons.save`, `labels.loading`）

### 5. 翻訳ファイルの追加方法

1. `src/i18n/locales/ja/` と `src/i18n/locales/en/` に新しいJSONファイルを作成
2. `src/i18n/index.ts` の `resources` に追加
3. `src/i18n/resources.ts` の型定義を更新（必要に応じて）

### 6. 例: 新機能の翻訳ファイル追加

**`src/i18n/locales/ja/my-feature.json`**:
```json
{
  "title": "新機能",
  "description": "これは新機能です",
  "actions": {
    "create": "作成",
    "update": "更新"
  }
}
```

**`src/i18n/locales/en/my-feature.json`**:
```json
{
  "title": "New Feature",
  "description": "This is a new feature",
  "actions": {
    "create": "Create",
    "update": "Update"
  }
}
```

**`src/i18n/index.ts` の更新**:
```typescript
import myFeatureJa from './locales/ja/my-feature.json';
import myFeatureEn from './locales/en/my-feature.json';

resources: {
  ja: {
    // ... existing
    myFeature: myFeatureJa,
  },
  en: {
    // ... existing
    myFeature: myFeatureEn,
  },
},
```

### 7. コンポーネント実装例

```typescript
/**
 * My Feature Component
 * 
 * DEPENDENCY MAP:
 * 
 * Dependencies (External files that this file imports):
 *   └─ react-i18next
 * 
 * Related Documentation:
 *   └─ Spec: src/pages/MyFeature/MyFeature.spec.md
 */
import { useTranslation } from 'react-i18next';
import { Button } from '@mantine/core';

export function MyFeature() {
  const { t } = useTranslation('myFeature');
  
  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
      <Button>{t('actions.create')}</Button>
    </div>
  );
}
```

### 8. 動的な翻訳キーの使用方法

パラメータを渡して動的に翻訳を生成する場合：

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation('myFeature');
  const userName = 'John';
  const itemCount = 5;
  
  return (
    <div>
      {/* 単一パラメータ */}
      <p>{t('welcome', { name: userName })}</p>
      {/* 出力: "ようこそ、Johnさん" */}
      
      {/* 複数パラメータ */}
      <p>{t('itemCount', { count: itemCount })}</p>
      {/* 出力: "5個のアイテムがあります" */}
    </div>
  );
}
```

**翻訳ファイル**:
```json
{
  "welcome": "ようこそ、{{name}}さん",
  "itemCount": "{{count}}個のアイテムがあります"
}
```

### 9. 数値や日付のフォーマット方法

数値や日付をフォーマットする場合：

```typescript
import { useTranslation } from 'react-i18next';
import dayjs from 'dayjs';

function MyComponent() {
  const { t, i18n } = useTranslation('myFeature');
  const date = new Date();
  const price = 1234.56;
  
  // 日付のフォーマット
  const formattedDate = dayjs(date).format('YYYY-MM-DD');
  
  // 数値のフォーマット（ロケールに応じて）
  const formattedPrice = new Intl.NumberFormat(i18n.language, {
    style: 'currency',
    currency: 'JPY'
  }).format(price);
  
  return (
    <div>
      <p>{t('date', { date: formattedDate })}</p>
      <p>{t('price', { price: formattedPrice })}</p>
    </div>
  );
}
```

### 10. エラーメッセージの国際化対応例

エラーメッセージを国際化対応する場合：

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation(['common', 'myFeature']);
  const [error, setError] = useState<string | null>(null);
  
  const handleSubmit = async () => {
    try {
      // API呼び出し
    } catch (err) {
      // エラータイプに応じて翻訳キーを選択
      if (err instanceof NetworkError) {
        setError(t('common:messages.networkError'));
      } else if (err instanceof ValidationError) {
        setError(t('myFeature:errors.validation'));
      } else {
        setError(t('common:messages.operationFailed'));
      }
    }
  };
  
  return (
    <div>
      {error && <Text color="red">{error}</Text>}
    </div>
  );
}
```

**翻訳ファイル**:
```json
// common.json
{
  "messages": {
    "networkError": "ネットワークエラーが発生しました",
    "operationFailed": "操作に失敗しました"
  }
}

// my-feature.json
{
  "errors": {
    "validation": "入力値が正しくありません"
  }
}
```

### 11. テストファイルでの国際化対応例

テストファイルで国際化対応を確認する場合：

```typescript
import { render, screen } from '@testing-library/react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { MyComponent } from './MyComponent';

describe('MyComponent', () => {
  beforeEach(() => {
    i18n.changeLanguage('ja');
  });
  
  test('renders with Japanese translation', () => {
    render(
      <I18nextProvider i18n={i18n}>
        <MyComponent />
      </I18nextProvider>
    );
    
    expect(screen.getByText('ようこそ')).toBeInTheDocument();
  });
  
  test('renders with English translation', () => {
    i18n.changeLanguage('en');
    render(
      <I18nextProvider i18n={i18n}>
        <MyComponent />
      </I18nextProvider>
    );
    
    expect(screen.getByText('Welcome')).toBeInTheDocument();
  });
  
  test('translation keys exist', () => {
    const { t } = useTranslation('myFeature');
    expect(t('title')).toBeTruthy();
    expect(t('description')).toBeTruthy();
  });
});
```

### 12. 条件付き翻訳の使用例

条件に応じて異なる翻訳を表示する場合：

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation('myFeature');
  const status = 'completed';
  
  return (
    <div>
      {/* 条件に応じた翻訳キーを選択 */}
      <Text>{t(`status.${status}`)}</Text>
      {/* status.completed の翻訳が表示される */}
    </div>
  );
}
```

**翻訳ファイル**:
```json
{
  "status": {
    "pending": "待機中",
    "running": "実行中",
    "completed": "完了",
    "failed": "失敗"
  }
}
```

### 13. 注意事項

- **ハードコードされたテキストは使用しない**
- 翻訳キーは名前空間付きで記述（例: `t('namespace.key')`）
- デフォルト言語は日本語（`ja`）
- フォールバック言語も日本語（`ja`）
- 翻訳キーが存在しない場合は、キー自体が表示される（開発時に気づきやすい）
- 動的な翻訳キーを使用する場合は、パラメータの型を確認する
- 数値や日付のフォーマットは、ロケールに応じて適切に処理する

