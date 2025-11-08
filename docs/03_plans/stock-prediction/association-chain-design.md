# 連想チェーン設計

## データ構造

```typescript
interface AssociationChain {
  steps: AssociationStep[];
}

interface AssociationStep {
  step: number;
  concept: string;
  connection: string;
}
```

## 可視化

- React FlowまたはD3.jsを使用
- ノード: 概念
- エッジ: 関連性
- ステップ番号で順序を表示

## 例

```
[AI技術の進展] 
    ↓ (関連: 需要増加)
[半導体需要増加]
    ↓ (関連: 主要サプライヤー)
[TSMCの株価上昇]
```

