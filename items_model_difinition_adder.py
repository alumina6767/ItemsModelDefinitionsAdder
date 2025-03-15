"""
    とりあえずのアイテムモデル定義ファイルを作成
    すでにある場合は上書きしない
    assetsと同じ階層で実行すること
"""

import os
import glob

# アイテム定義ファイルのテンプレ
ITEM_DIFINITION_TEMP = r'{"model": {"type": "minecraft:model","model": "$model_path"}}'


def check_dir(path):
    if os.path.isdir(path) == False:
        print(f"{path} フォルダを作成します。")
        os.mkdir(path)


if __name__ == "__main__":
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
        print("==========================================================")
        print(f"名前空間 {ns} のアイテムモデルを探索します。")
        models = glob.glob(os.path.join("assets", ns, "models", "item", "**/*.json"), recursive=True)

        # モデルがない場合終了
        if len(models) == 0:
            print("アイテムモデルが見つかりませんでした。")
            continue

        # 定義ファイルフォルダがない場合作成
        difinition_folder = os.path.join("assets", ns, "items")
        check_dir(difinition_folder)

        # モデル毎に定義ファイルを探索
        no_of_export_items = 0
        for model in models:
            resource_path = model.split(os.path.join("models", "item", ""))[1].replace(".json", "")
            item_difinition = os.path.join(
                difinition_folder, resource_path + ".json")

            # 定義ファイルがない場合作成
            if os.path.isfile(item_difinition) == False:

                # 書き込み先のディレクトリの確認
                check_dir(os.path.dirname(item_difinition))

                # ファイルの作成
                with open(item_difinition, "w", encoding="utf-8") as f:
                    f.write(ITEM_DIFINITION_TEMP.replace("$model_path", f"{ns}:item/{resource_path.replace('\\', '/')}"))

                print(f"{item_difinition} を作成しました。")
                no_of_export_items += 1

        # 結果通知
        if no_of_export_items != 0:
            print(f"{len(models)} 個のモデルファイルから {no_of_export_items} 個のアイテム定義ファイルを作成しました。")
        else:
            print(f"{len(models)} 個のモデルファイルが見つかりましたが、既にアイテム定義ファイルは存在したため作成しませんでした。")

    print("\n正常終了しました。")
    print("エンターキーで終了。")
    input()
