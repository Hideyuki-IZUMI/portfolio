# 必要なライブラリをインポート
import pandas as pd
import requests
import csv
import time


# 住所から緯度と経度を取得(ジオコーディング)する関数の定義
def latitude_longitude(address, api_key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'  # Google MapsジオコーディングAPIのURL
    params = {
        'address': address,  # APIに渡す住所パラメータ
        'key': api_key  # APIキーパラメータ
    }

    response = requests.get(base_url, params=params)  # APIリクエストを送信
    data = response.json()  # JSONレスポンスを解析

    # レスポンス内に結果が存在するかどうかをチェック
    if 'results' in data and len(data['results']) > 0:
        latitude = data["results"][0]["geometry"]["location"]["lat"]  # 緯度を抽出
        longitude = data["results"][0]["geometry"]["location"]["lng"]  # 経度を抽出
        print(latitude, longitude)  # 緯度と経度を表示
        return latitude, longitude
    else:
        print(f'結果が見つかりませんでした: {address}')  # 結果がない場合のエラーメッセージを表示
        return None


# CSVファイル内の住所を緯度と経度に変換する関数の定義
def convert_addresses_to_lat_lng(csv_file_path, api_key):
    data = pd.read_csv(csv_file_path)  # CSVファイルからデータの読み込み
    latitudes = []  # 緯度を格納するリスト
    longitudes = []  # 経度を格納するリスト
    successful_addresses = []  # 処理済み住所を格納するリスト

    for address in data['所在地']:  # CSVファイル内の住所を順に処理
        result = latitude_longitude(address, api_key)  # 各住所の緯度と経度を取得
        successful_addresses.append(address)  # 処理済み住所リストに追加
        if result:
            latitude, longitude = result  # 緯度と経度を取得
            latitudes.append(latitude)  # 緯度をリストに追加
            longitudes.append(longitude)  # 経度をリストに追加
        else:
            latitudes.append(float('nan'))  # 結果がない場合、緯度リストにNanを追加
            longitudes.append(float('nan'))  # 結果がない場合、経度リストにNanを追加

        time.sleep(1.0)  # APIの負荷を減らすために1.0秒待機

    return successful_addresses, latitudes, longitudes


# Google MapsのAPIキーとCSVファイルのパスを指定して実行
api_key = 'AIzaSyATSnh_C9y_yIVT7zHA6DyXubozm7FqKZU'  # Google MapsのAPIキー
csv_file_path = '140007_park_(神奈川県公園データ).csv'  # CSVファイルのパスを指定

successful_addresses, latitudes, longitudes = convert_addresses_to_lat_lng(csv_file_path, api_key)  # 住所を緯度・経度に変換

output_csv_file = 'ジオコーディング.csv'  # 出力するCSVファイルの名前
with open(output_csv_file, 'w', newline='') as csvfile:  # 出力CSVファイルを書き込みモードでオープン
    fieldnames = ['所在地', '緯度', '経度']  # CSVのヘッダー名を指定
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # CSV DictWriterオブジェクトを作成
    writer.writeheader()  # ヘッダーをCSVに書き込み

    for i in range(len(successful_addresses)):  # 処理済み住所を順に処理
        writer.writerow({'所在地': successful_addresses[i], '緯度': latitudes[i], '経度': longitudes[i]})  # 各行をCSVに書き込み
