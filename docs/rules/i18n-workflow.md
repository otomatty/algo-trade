# 国際化対応（i18n）開発ワークフロー

## 概要

新規コンポーネント作成時に、国際化対応を最初から実装するための標準ワークフローを定義します。

## ワークフロー

### ステップ1: コンポーネント設計時に翻訳キーを設計

コンポーネントを実装する前に、必要な翻訳キーを設計します。

**作業内容**:
1. コンポーネントに表示される全てのテキストをリストアップ
2. 各テキストに対して適切な翻訳キー名を決定
3. 名前空間を決定（`common` を使用するか、機能別名前空間を作成するか）
4. 翻訳キーの階層構造を設計

**例**:
```
コンポーネント: UserProfileForm
表示テキスト:
  - "ユーザー情報"
  - "名前"
  - "メールアドレス"
  - "保存"
  - "キャンセル"

翻訳キー設計:
  namespace: user-profile
  keys:
    - title: "ユーザー情報"
    - fields.name: "名前"
    - fields.email: "メールアドレス"
    - buttons.save: "保存" (common を使用)
    - buttons.cancel: "キャンセル" (common を使用)
```

### ステップ2: 翻訳ファイルを先に作成（ja/en）

コンポーネント実装前に、翻訳ファイルを作成します。

**作業内容**:
1. `src/i18n/locales/ja/{namespace}.json` を作成
2. `src/i18n/locales/en/{namespace}.json` を作成
3. 設計した翻訳キーを両方のファイルに追加
4. JSON構造が一致していることを確認

**例**:
```json
// src/i18n/locales/ja/user-profile.json
{
  "title": "ユーザー情報",
  "fields": {
    "name": "名前",
    "email": "メールアドレス"
  }
}

// src/i18n/locales/en/user-profile.json
{
  "title": "User Profile",
  "fields": {
    "name": "Name",
    "email": "Email Address"
  }
}
```

### ステップ3: i18n設定ファイルを更新

翻訳ファイルを作成したら、i18n設定を更新します。

**作業内容**:
1. `src/i18n/index.ts` に翻訳リソースをインポート
2. `resources` オブジェクトに追加
3. `ns` 配列に名前空間を追加
4. 型定義ファイル（`src/i18n/resources.ts`）を更新（必要に応じて）

**例**:
```typescript
// src/i18n/index.ts
import userProfileJa from './locales/ja/user-profile.json';
import userProfileEn from './locales/en/user-profile.json';

resources: {
  ja: {
    // ... existing
    userProfile: userProfileJa,
  },
  en: {
    // ... existing
    userProfile: userProfileEn,
  },
},
ns: ['common', 'navigation', 'userProfile'],
```

### ステップ4: コンポーネント実装時に国際化対応

コンポーネントを実装する際、国際化対応を最初から組み込みます。

**作業内容**:
1. `useTranslation()` フックをインポート
2. 適切な名前空間を指定して `useTranslation()` を呼び出し
3. 全てのテキストを翻訳キーに置き換え
4. ハードコードされたテキストが存在しないことを確認

**例**:
```typescript
import { useTranslation } from 'react-i18next';
import { TextInput, Button } from '@mantine/core';

export function UserProfileForm() {
  const { t } = useTranslation(['common', 'userProfile']);
  
  return (
    <form>
      <h1>{t('userProfile:title')}</h1>
      <TextInput label={t('userProfile:fields.name')} />
      <TextInput label={t('userProfile:fields.email')} />
      <Button>{t('common:buttons.save')}</Button>
      <Button>{t('common:buttons.cancel')}</Button>
    </form>
  );
}
```

### ステップ5: テストで国際化対応を確認

テストファイルを作成し、国際化対応が正しく動作することを確認します。

**作業内容**:
1. テストファイルで `I18nextProvider` を使用
2. 翻訳キーの存在確認テストを追加
3. 言語切り替えのテストを追加（必要に応じて）
4. 全てのテストが通過することを確認

**例**:
```typescript
import { render, screen } from '@testing-library/react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { UserProfileForm } from './UserProfileForm';

describe('UserProfileForm', () => {
  test('renders with translation', () => {
    render(
      <I18nextProvider i18n={i18n}>
        <UserProfileForm />
      </I18nextProvider>
    );
    
    expect(screen.getByText('ユーザー情報')).toBeInTheDocument();
  });
  
  test('translation keys exist', () => {
    const { t } = useTranslation('userProfile');
    expect(t('title')).toBeTruthy();
    expect(t('fields.name')).toBeTruthy();
  });
});
```

### ステップ6: コードレビューで国際化対応をチェック

コードレビュー時に、チェックリストを使用して国際化対応を確認します。

**確認項目**:
- [ ] ハードコードされたテキストがないか
- [ ] 翻訳キーの命名規則に従っているか
- [ ] 名前空間の使用が適切か
- [ ] 翻訳ファイルの構造が適切か
- [ ] 既存の翻訳キーを再利用しているか
- [ ] テストで国際化対応を確認しているか

**参照**: `docs/rules/i18n-checklist.md`

## ワークフローの利点

1. **一貫性**: 全ての新規コンポーネントが同じ手順で国際化対応される
2. **効率性**: 翻訳ファイルを先に作成することで、実装時に迷わない
3. **品質**: チェックリストを使用することで、見落としを防ぐ
4. **保守性**: 標準化されたワークフローにより、後から理解しやすい

## よくある質問

### Q: 既存の `common` 名前空間のキーを使うべきか、新しい名前空間を作るべきか？

A: 以下の基準で判断してください：
- **`common` を使用**: 複数の機能で再利用される可能性が高いUI要素（ボタン、ラベル、メッセージなど）
- **機能別名前空間**: その機能固有のテキスト（例: `dashboard.title`, `userProfile.fields.name`）

### Q: 翻訳ファイルを先に作成する必要があるか？

A: はい。翻訳ファイルを先に作成することで：
- 実装時に翻訳キー名を迷わない
- 翻訳キーの構造を明確にできる
- 実装と翻訳の作業を並行できる

### Q: テストは必須か？

A: はい。テストを書くことで：
- 翻訳キーの存在を確認できる
- 言語切り替えが正しく動作することを確認できる
- リファクタリング時の安全性が向上する

## 関連ドキュメント

- チェックリスト: `docs/rules/i18n-checklist.md`
- ガイドライン: `docs/rules/i18n-guidelines.md`
- テンプレート: `docs/rules/i18n-template.md`

