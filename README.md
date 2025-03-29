# 概要
テンプレートマッチングを使用して、野球ゲームの動画から盛り上がり箇所（ピンチ、チャンス、得点シーン、ホームラン、ゲームセット）を検出するとともに、光学文字認識を使用して、得点情報を抽出するためのプログラムを公開しています。  
精度評価用のプログラムも公開しており、テンプレートマッチについては正解率、再現率、適合率を計算でき、光学文字認識については正解率、認識精度、誤認識率、未検出率、誤検出率を計算できます。  
  
# 解析動画
YouTubeに公開されている「にじさんじ甲子園2022決勝」の１試合目を抽出しており、下記リンクのGoogleドライブからダウンロードできます。  
https://drive.google.com/file/d/1sJ0ygXSMOhBk9mCsJXWAqBgZ7Zq-A-jJ/view?usp=sharing  
  
# ファイル構成
output.mp4 ･･･ 解析動画ファイル  
result.txt ･･･ 解析動画の正解データセット  
create_baseball_highlight.py ･･･ テンプレートマッチング、OCR実行用プログラム  
digit_recognition.py ･･･ CNNベースの数字文字認識実行用プログラム  
create_highlight.py ･･･ ハイライト生成用プログラム  
get_image_point_in_movie.py ･･･ 動画の特定時間における画面確認用プログラム  
analysis.py ･･･ 精度評価用プログラム  
r0.png ･･･ ランナー：なしのテンプレート画像  
r1.png ･･･ ランナー：一塁のテンプレート画像  
r2.png ･･･ ランナー：二塁のテンプレート画像  
r3.png ･･･ ランナー：三塁のテンプレート画像  
r12.png ･･･ ランナー：一・二塁のテンプレート画像  
r13.png ･･･ ランナー：一・三塁のテンプレート画像  
r23.png ･･･ ランナー：二・三塁のテンプレート画像  
r123.png ･･･ ランナー：満塁のテンプレート画像  
o0.png ･･･ アウト：０のテンプレート画像  
o1.png ･･･ アウト：１のテンプレート画像  
o2.png ･･･ アウト：２のテンプレート画像  
b0.png ･･･ ボール：０のテンプレート画像  
b1.png ･･･ ボール：１のテンプレート画像  
b2.png ･･･ ボール：２のテンプレート画像  
b3.png ･･･ ボール：３のテンプレート画像  
s0.png ･･･ ストライク：０のテンプレート画像  
s1.png ･･･ ストライク：１のテンプレート画像  
s2.png ･･･ ストライク：２のテンプレート画像  
tokuten.png ･･･ 得点シーン抽出用のテンプレート画像  
tokuten2.png ･･･ ホームラン＆ゲームセット抽出用のテンプレート画像  
  
# 利用方法
(1) create_baseball_highlight.pyを実行することで、テンプレートマッチング、OCRが実行されます。  
　※閾値を変更したい場合は、グローバル変数として定義しているので、適宜修正して実行してください。  
　※OCRツールはデフォルトだとTesseractを使用する設定になっていますが、Cloud Vision API、Azure AI Visionにも対応可能であり、ocr_tool変数を変更するだけで良いです。  
　※OCRツールを利用しない場合は、ocr_tool変数をNoneなどにしておき、OCRモデルを用意した上でdigit_recognition.pyを実行してください。OCRモデルはKaggleのDigit Recognizerコンペティションから取得しました。  
(2) 処理が完了するとランナー、アウト、ボール、ストライク、得点シーン、ホームラン＆ゲームセットに関する分類結果がテキスト形式で出力されます。  
　※分析結果のテキストは1回実行ごとに名前を変えるなどしなければデータが追記されてしまいます。  
(3) analysis.pyを実行することで、精度評価結果が表示されます。  
(4) create_highlight.pyを実行することで、テキスト形式のデータ（動画タギングデータ）を使用して、ハイライト動画が生成されます。  
  
```
#python3 create_baseball_highlight.py
output.mp4

#python3 digit_recognition.py

#python3 analysis.py

#python3 create_highlight.py
```
  
# 論文
- 赤木信也: 盛り上がり検出のための音声解析の一考察
  - 情報科学技術フォーラム講演論文集(FIT), 22巻, 2号, pp.423-424, 2023-08-23
  - https://jglobal.jst.go.jp/detail?JGLOBAL_ID=202302237479734190
- 赤木信也: 野球ゲームにおける盛り上がり箇所の自動検出ー画像解析の一考察ー
  - 情報処理学会全国大会講演論文集, 86巻, 2号, pp.59-60, 2024-03-01
  - https://jglobal.jst.go.jp/detail?JGLOBAL_ID=202402222974179705
- 赤木信也: 野球ゲームにおける盛り上がり箇所の自動検出ー光学文字認識の一考察ー
  - 情報科学技術フォーラム講演論文集 (FIT), 23巻, 2号, pp.513-514, 2024-08-21
  - https://jglobal.jst.go.jp/detail?JGLOBAL_ID=202402274492046394
- 赤木信也: 野球ゲームにおける数字2文字の光学文字認識
  - 情報処理学会全国大会
  - https://www.ipsj.or.jp/event/taikai/87/
- 赤木信也：野球ゲームにおける動画タギングを用いたハイライト生成（発表予定）
  - FIT2025
  - https://www.ipsj.or.jp/event/fit/fit2025/
  
# ライセンス
ソースコードなどは公開はしていますが著作権を放棄していません。  
学術機関または個人的な研究目的での利用は問題ありませんが、商用利用などはお控えください。  
  
