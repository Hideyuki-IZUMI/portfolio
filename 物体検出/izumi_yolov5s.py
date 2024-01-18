"""
YOLOを使用した木の検出プログラム
"""

# 必要なライブラリをインポート
import torch
import cv2
import os

# ultralytics/yolov5 GitHubリポジトリからyolov5モデルをダウンロードしてロード
# yolov5sはモデルのバージョンを指定
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')

# モデルを評価モードに設定(推論モード)
model.eval()

# 画像フォルダのパスを定義
folder_path = 'images_resize_0-150'
files = os.listdir(folder_path)

# フォルダ内にある画像ファイルを読み込み
for file in files:
    image_path = os.path.join(folder_path, file)
    image = cv2.imread(image_path)

    # モデルを使用して指定した画像に対して物体検出を行う
    results = model(image, size=640)

    # 物体検出の結果を画像として表示
    results.show()

    # 物体検出の結果を画像として保存
    results.save()

# プログラムを終了
exit()
