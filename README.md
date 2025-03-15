# アイテムモデル定義ファイルつくるくん
1.21.3では直接componentから参照できたが、1.21.4ではアイテムモデル定義ファイルが必要になってしまった。

適用するアイテムについてちゃんと書けばいいんだが、1.21.3の取り回しが楽なので、すべてのアイテムモデルについてアイテムモデル定義ファイルがほしかった。

各名前空間について、assets/namespace/models/item内のモデルを探索しassets/namespace/items内にアイテムモデル定義ファイルを作成する。

Animeted Java についてはそもそも assets/animated_java/models/item ではなく assets/animated_java/models/blueprint にモデルを書き出すので探索の対象外になり、影響はない。

## ダウンロード
[ダウンロード](https://github.com/alumina6767/ItemsModelDefinitionsAdder/releases/latest)

## 環境
Windowsでしかテストやってない。

## 使い方
assetsと同じ階層で実行するだけ。
すでにあるアイテムモデル定義ファイルは上書きしない。
