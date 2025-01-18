"""
    とりあえずのアイテムモデル定義ファイルを作成
    すでにある場合は上書きしない
    assetsと同じ階層で実行すること
"""

import os
import glob

# アイテム定義ファイルのテンプレ
ITEM_DIFINITION_TEMP = r'{"model": {"type": "minecraft:model","model": "$model_path"}}'

# 実行ディレクトリの確認
if os.path.isdir("assets") == False:
    print("assetsフォルダが見つかりません。assetsと同じ階層で実行してください。")
    print("\nエンターキーで終了")
    input()
    exit()

# 名前空間の取得
namespaces = []
for dir in os.listdir("assets"):
    if os.path.isdir(os.path.join("assets", dir)):
        namespaces.append(dir)

print(f"見つかった名前空間: {", ".join(namespaces)}")

# 名前空間ごとに実行
for ns in namespaces:
    print("==========================================================\n")
    print(f"名前空間 {ns} のアイテムモデル定義ファイルを探索します。")
    models = glob.glob(os.path.join("assets", ns, "models",
                       "item", "**.json"), recursive=True)

    # モデルがない場合終了
    if len(models) == 0:
        print("アイテムモデルが見つかりませんでした。")
        continue

    # 定義ファイルフォルダがない場合作成
    difinition_folder = os.path.join("assets", ns, "items")
    if os.path.isdir(difinition_folder) == False:
        print(f"{difinition_folder} フォルダを作成します。")
        os.mkdir(difinition_folder)

    # モデル毎に定義ファイルを探索
    for model in models:
        resource_path = model.split(os.path.join("models", "item", ""))[
            1].replace(".json", "")
        item_difinition = os.path.join(
            difinition_folder, resource_path + ".json")

        # 定義ファイルがない場合作成
        if os.path.isfile(item_difinition) == False:
            with open(item_difinition, "w", encoding="utf-8") as f:
                f.write(ITEM_DIFINITION_TEMP.replace(
                    "$model_path", f"{ns}:item/{resource_path}"))
            print(f"{item_difinition} を作成しました。")

print("\n正常終了しました。")
print("エンターキーで終了。")
input()
