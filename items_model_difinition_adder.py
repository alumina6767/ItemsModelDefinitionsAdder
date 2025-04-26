"""
    とりあえずのアイテムモデル定義ファイルを作成
    すでにある場合は上書きしない
    assetsと同じ階層で実行すること
"""

import os
import glob
import json

# アイテム定義ファイルのテンプレ
ITEM_TEMP = r'{"model": {"type": "minecraft:model","model": "$model_path"}}'

# 参照用モデルに使うアイテム
REFERENCE_ITEM_ID = "command_block_minecart"


def check_dir(path):
    if os.path.isdir(path) == False:
        print(f"{path} フォルダを作成します。")
        os.makedirs(path)


def get_reference_item(path):

    # フォルダの作成
    check_dir(os.path.dirname(path))

    # 定義ファイルの作成
    if os.path.isfile(path) == False:
        with open(path, "w", encoding="utf-8") as f:
            j = {
                "model": {
                    "type": "minecraft:select",
                    "property": "minecraft:custom_model_data",
                    "cases": [],
                    "fallback": {
                            "type": "minecraft:model",
                            "model": "minecraft:item/command_block_minecart"
                    }
                }
            }

            json.dump(j, f, indent=4)
            print(f"新しく参照用のアイテム定義ファイル {path} を作成します。")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_reference_item(item, ns, resource_path):
    items_list = [ref["when"] for ref in item["model"]["cases"]]
    if ns + ":" + resource_path not in items_list:
        item["model"]["cases"].append(
            {
                "when": ns + ":" + resource_path,
                "model":
                    {
                        "type": "minecraft:model",
                        "model": ns + ":item/" + resource_path
                    }
            }
        )
        print(f"{resource_path} の参照用モデルを追加しました。")
    return item


if __name__ == "__main__":
    # 実行ディレクトリの確認
    if os.path.isdir("assets") == False:
        print("assetsフォルダが見つかりません。assetsと同じ階層で実行してください。\nエンターキーで終了します。")
        input()
        exit()

    # 参照用のアイテムモデルを作成するか確認
    is_make_reference_item = False
    print("Axiomなど用に参照用のアイテム定義ファイルを作成しますか?\ny: 作成する\nn: 作成しない")
    if input() == "y":
        is_make_reference_item = True
        reference_item_path = os.path.join(
            "assets", "minecraft", "items", f"{REFERENCE_ITEM_ID}.json")
        reference_item = get_reference_item(reference_item_path)

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
        models = glob.glob(os.path.join(
            "assets", ns, "models", "item", "**/*.json"), recursive=True)

        # モデルがない場合終了
        if len(models) == 0:
            print("アイテムモデルが見つかりませんでした。")
            continue

        # 定義ファイルフォルダがない場合作成
        items_dir = os.path.join("assets", ns, "items")
        check_dir(items_dir)

        # モデル毎に定義ファイルを探索
        no_of_export_items = 0
        for model in models:
            resource_path = model.\
                split(os.path.join("models", "item", ""))[1].\
                replace(".json", "").\
                replace('\\', '/')

            # 定義ファイルのパス
            item_path = os.path.join(items_dir, resource_path + ".json")

            # 定義ファイルがない場合作成
            if os.path.isfile(item_path) == False:

                # 書き込み先のディレクトリの確認
                check_dir(os.path.dirname(item_path))

                # ファイルの作成
                with open(item_path, "w", encoding="utf-8") as f:
                    f.write(ITEM_TEMP.replace("$model_path",
                            f"{ns}:item/{resource_path}"))

                print(f"{item_path} を作成しました。")
                no_of_export_items += 1

            # 参照用モデルを作成
            if is_make_reference_item:
                add_reference_item(reference_item, ns, resource_path)

        # 結果通知
        if no_of_export_items != 0:
            print(
                f"{len(models)} 個のモデルファイルから {no_of_export_items} 個のアイテム定義ファイルを作成しました。")
        else:
            print(f"{len(models)} 個のモデルファイルが見つかりましたが、既にアイテム定義ファイルは存在したため作成しませんでした。")

    # 参照用モデルを更新
    if is_make_reference_item:
        with open(reference_item_path, "w", encoding="utf-8") as f:
            json.dump(reference_item, f, indent=4)

    # 終了メッセージ
    print("\n正常終了しました。\nエンターキーで終了します。")
    input()
