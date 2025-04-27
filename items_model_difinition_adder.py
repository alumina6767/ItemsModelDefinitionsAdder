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
REF_ITEM_ID = "command_block_minecart"


def check_dir(path):
    """ ディレクトリの存在を確認し、なければ作成する。 """

    if not os.path.isdir(path):
        print(f"{path} フォルダを作成します。")
        os.makedirs(path)


def get_ref_item(path):
    """
    参照用アイテムの定義ファイルを読み込む。
    存在しなければ作成する。

    :param path: 参照用アイテムの定義ファイルのパス
    :return: JSONのアイテム定義
    """

    # フォルダの作成
    check_dir(os.path.dirname(path))

    # 定義ファイルの作成
    if not os.path.isfile(path):
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


def add_ref_item(item, ns, res_path):
    """
    参照用アイテムの定義にモデルを追加する。

    :param item: JSONのアイテム定義
    :param ns: 名前空間
    :param res_path: 追加するモデルのリソースパス
    :return: JSONのアイテム定義
    """

    case = [ref["when"] for ref in item["model"]["cases"]]
    if ns + ":" + res_path not in case:
        item["model"]["cases"].append(
            {
                "when": f"{ns}:{res_path}",
                "model":
                    {
                        "type": "minecraft:model",
                        "model": f"{ns}:item/{res_path}"
                }
            }
        )
        print(f"{res_path} の参照用モデルを追加しました。")
    return item


if __name__ == "__main__":
    # 実行ディレクトリの確認
    if not os.path.isdir("assets"):
        print("assetsフォルダが見つかりません。assetsと同じ階層で実行してください。\nエンターキーで終了します。")
        input()
        exit()

    # 参照用のアイテムモデルを作成するか確認
    is_make_ref_item = False
    print("Axiomなど用に参照用のアイテム定義ファイルを作成しますか?\ny: 作成する\nn: 作成しない")
    if input() == "y":
        is_make_ref_item = True
        ref_item_path = os.path.join(
            "assets", "minecraft", "items", f"{REF_ITEM_ID}.json")
        ref_item = get_ref_item(ref_item_path)

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
            res_path = model.\
                split(os.path.join("models", "item", ""))[1].\
                replace(".json", "").\
                replace('\\', '/')

            # 定義ファイルのパス
            item_path = os.path.join(items_dir, res_path + ".json")

            # 定義ファイルがない場合作成
            if not os.path.isfile(item_path):

                # 書き込み先のディレクトリの確認
                check_dir(os.path.dirname(item_path))

                # ファイルの作成
                with open(item_path, "w", encoding="utf-8") as f:
                    f.write(ITEM_TEMP.replace(
                        "$model_path", f"{ns}:item/{res_path}"))

                print(f"{item_path} を作成しました。")
                no_of_export_items += 1

            # 参照用モデルを作成
            if is_make_ref_item:
                add_ref_item(ref_item, ns, res_path)

        # 結果通知
        if no_of_export_items != 0:
            print(
                f"{len(models)} 個のモデルファイルから {no_of_export_items} 個のアイテム定義ファイルを作成しました。")
        else:
            print(f"{len(models)} 個のモデルファイルが見つかりましたが、既にアイテム定義ファイルは存在したため作成しませんでした。")

    # 参照用モデルを更新
    if is_make_ref_item:
        with open(ref_item_path, "w", encoding="utf-8") as f:
            json.dump(ref_item, f, indent=4)

    # 終了メッセージ
    print("\n正常終了しました。\nエンターキーで終了します。")
    input()
