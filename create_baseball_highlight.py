import cv2
import numpy as np
import datetime
import time
import sys
import copy
from PIL import Image
import pyocr
import re
from multiprocessing import Process
import logging
from google.cloud import vision
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# 閾値調整
runnerpoint = () 	# テンプレートマッチング（ランナー）の座標
runner_threshold = 0.8	# テンプレートマッチング（ランナー）の閾値
outpoint = () 		# テンプレートマッチング（アウト）の座標
out_threshold = 0.9 	# テンプレートマッチング（アウト）の閾値
strikepoint = ()        # テンプレートマッチング（ストライク）の座標
strike_threshold = 0.9  # テンプレートマッチング（ストライク）の閾値
ballpoint = ()          # テンプレートマッチング（ボール）の座標
ball_threshold = 0.9    # テンプレートマッチング（ボール）の閾値
homerunpoint = ()	# テンプレートマッチング（ホームラン）の座標
homerun_threshold = 0.3 # テンプレートマッチング（ホームラン）の閾値
#ocrpoint = () 		# OCRの座標
tokutenpoint = () 	# カラーヒストグラム比較・テンプレートマッチング（得点シーン）の座標
cmp_threshold = 0.65 	# カラーヒストグラム比較の閾値
tokuten_threshold = 0.5 # テンプレートマッチング（得点シーン）の閾値
gamesetpoint = ()       # テンプレートマッチング（ゲームセット）の座標
gameset_threshold = 0.5 # テンプレートマッチング（ゲームセット）の閾値
homerun_and_gameset_point = () # テンプレートマッチング（ホームラン＆ゲームセット）の座標
homerun_and_gameset_threshold = 0.8 # テンプレートマッチング（ホームラン＆ゲームセット）の閾値

# OCRツール選択
ocr_tools = ["tesseract", "cloud vision api", "azure ai vision"]
ocr_tool = ocr_tools[0]

# ログ出力設定
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
handler1 = logging.StreamHandler()
handler1.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
handler2 = logging.FileHandler(filename="matchdata.log")
handler2.setLevel(logging.INFO)
handler2.setFormatter(logging.Formatter("%(message)s"))

logger.addHandler(handler1)
logger.addHandler(handler2)


# 正解画像を切り出し
def create_true_image(movie, time, out_fname):
	if os.path.isfile(out_fname):
		return 0

	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = int(cap.get(cv2.CAP_PROP_FPS))

	# 時間指定を秒に変換
	try:
		d = datetime.datetime.strptime(time, "%H:%M:%S")
	except:
		try:
			d = datetime.datetime.strptime(time, "%M:%S")
		except:
			d = datetime.datetime.strptime(time, "%S")
	second = datetime.timedelta(hours=d.hour, minutes=d.minute, seconds=d.second).total_seconds()

	cap.set(cv2.CAP_PROP_POS_FRAMES, fps*second)
	ret, frame = cap.read()
	if ret:
		cv2.imwrite(out_fname, frame)


# テンプレートマッチングやOCRで使用する領域を取得
drawing = False # true if mouse is pressed
ix,iy = -1,-1 # 開始点（左上）
vx,vy = -1,-1 # 終了点（右下）
cache = None
def select_rectangle(event,x,y,flags,param):
	global ix,iy,vx,vy,drawing,img,cache

	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		ix,iy = x,y
		if cache is not None:
			img = copy.deepcopy(cache)
			cv2.imshow('image', img)
		else:
			cache = copy.deepcopy(img)
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			img = copy.deepcopy(cache)
			cv2.imshow('image', img)
			cv2.rectangle(img,(ix,iy),(x,y),(0,0,255))
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False
		vx,vy = x,y
		cv2.rectangle(img,(ix,iy),(x,y),(0,0,255))


# テンプレートマッチング
def tmpmatching(movie, tmppoint, tmpname, threshold, msg):
	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = cap.get(cv2.CAP_PROP_FPS)

	template = cv2.imread(tmpname)
	ix = tmppoint[0]
	iy = tmppoint[1]
	x = tmppoint[2]
	y = tmppoint[3]

	methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
	method = eval("cv2.TM_CCOEFF_NORMED")

	# 処理時間計測
	start = time.time()

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			# １秒単位の解析
			if int(c%fps) == 0:
				for scale in np.linspace(0.8, 1.8, 6):
					frame_point = frame[iy:y, ix:x]
					tmp_resized = cv2.resize(template, dsize=None, fx=scale, fy=scale)
					#print(datetime.timedelta(seconds=c//fps), scale)
					#cv2.imwrite("kaiseki.png", frame_point)
					# テンプレートサイズがフレームサイズより大きい場合
					try:
						res = cv2.matchTemplate(frame_point, tmp_resized, method)
					except:
						logger.debug("template matching error, {}, {}".format(msg, scale))
						continue
					_, max_val, _, max_loc = cv2.minMaxLoc(res)
					if 1.0 > max_val > threshold:
						logger.info("{}, {}, {}, {}".format(c//fps, msg, max_val, scale))
						f.write("{}, {}, {}".format(c//fps, max_val, scale))
						f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()

	# 処理時間計測
	end = time.time()

	# 処理時間記載
	# close時に追記されるのでファイルロックは不要
	f = open("processtime.log", "a")
	f.write("{}, {}\n".format(msg, datetime.timedelta(seconds=end-start)))
	f.close()


# OCR（数字）
def ocr(movie, ocrpoint, msg):
	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = cap.get(cv2.CAP_PROP_FPS)

	tools = pyocr.get_available_tools()
	tool = tools[0]

	ix = ocrpoint[0]
	iy = ocrpoint[1]
	x = ocrpoint[2]
	y = ocrpoint[3]

	# 処理時間計測
	start = time.time()

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			if int(c%fps) == 0:
				# 比較検証用
				img = frame[iy:y, ix:x]
				h, w = img.shape[:2]
				img = cv2.resize(img, dsize=None, fx=50/w, fy=50/h)
				# 実処理用
				#img = cv2.resize(frame[iy:y, ix:x], dsize=None, fx=1.0, fy=1.0)
				txt = tool.image_to_string(
					Image.fromarray(img),
					lang="eng",
					builder=pyocr.builders.TextBuilder(tesseract_layout=6))
				m = re.search("\d+", txt)
				if m:
					logger.info("{}, {}, {}".format(c//fps, msg, m.group()))
					f.write("{}, {}".format(c//fps, m.group()))
					f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()

	# 処理時間計測
	end = time.time()

	# 処理時間記載
	# close時に追記されるのでファイルロックは不要
	f = open("processtime.log", "a")
	f.write("{}, {}\n".format(msg, datetime.timedelta(seconds=end-start)))
	f.close()


# OCR（数字）: Gloud Vision API
def ocr_google(movie, ocrpoint, msg):
	# API準備
	if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ.keys():
		print("Missing environment variable 'GOOGLE_APPLICATION_CREDENTIALS'")
		exit()

	client = vision.ImageAnnotatorClient()

	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = cap.get(cv2.CAP_PROP_FPS)

	tools = pyocr.get_available_tools()
	tool = tools[0]

	ix = ocrpoint[0]
	iy = ocrpoint[1]
	x = ocrpoint[2]
	y = ocrpoint[3]

	# 処理時間計測
	start = time.time()

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			if int(c%fps) == 0:
				# 比較検証用
				img = frame[iy:y, ix:x]
				h, w = img.shape[:2]
				img = cv2.resize(img, dsize=None, fx=50/w, fy=50/h)
				# 実処理用
				#img = cv2.resize(frame[iy:y, ix:x], dsize=None, fx=1.0, fy=1.0)
				img_byte = cv2.imencode(".png", img)[1].tobytes()
				img_target = vision.Image(content=img_byte)
				response = client.text_detection(image=img_target)
				txt = response.full_text_annotation.text

				m = re.search("\d+", txt)
				if m:
					logger.info("{}, {}, {}".format(c//fps, msg, m.group()))
					f.write("{}, {}".format(c//fps, m.group()))
					f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()

	# 処理時間計測
	end = time.time()

	# 処理時間記載
	# close時に追記されるのでファイルロックは不要
	f = open("processtime.log", "a")
	f.write("{}, {}\n".format(msg, datetime.timedelta(seconds=end-start)))
	f.close()


# OCR（数字）: Azure AI Vision
def ocr_azure(movie, ocrpoint, msg):
	# API準備
	try:
		endpoint = os.environ["VISION_ENDPOINT"]
		key = os.environ["VISION_KEY"]
	except KeyError:
		print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
		print("Set them before running this sample.")
		exit()

	client = ImageAnalysisClient(
		endpoint=endpoint,
		credential=AzureKeyCredential(key)
	)

	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = cap.get(cv2.CAP_PROP_FPS)

	tools = pyocr.get_available_tools()
	tool = tools[0]

	ix = ocrpoint[0]
	iy = ocrpoint[1]
	x = ocrpoint[2]
	y = ocrpoint[3]

	# 処理時間計測
	start = time.time()

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			if int(c%fps) == 0:
				img = frame[iy:y, ix:x]
				h, w = img.shape[:2]
				img = cv2.resize(img, dsize=None, fx=50/w, fy=50/h)
				img_byte = cv2.imencode(".png", img)[1].tobytes()
				result = client.analyze(image_data=img_byte, visual_features=[VisualFeatures.READ])
				if result.read is not None:
					if result.read.blocks != []:
						txt_lines = [line.text for line in result.read.blocks[0].lines]
						txt = "\n".join(txt_lines)

						m = re.search("\d+", txt)
						if m:
							logger.info("{}, {}, {}".format(c//fps, msg, m.group()))
							f.write("{}, {}".format(c//fps, m.group()))
							f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()

	# 処理時間計測
	end = time.time()

	# 処理時間記載
	# close時に追記されるのでファイルロックは不要
	f = open("processtime.log", "a")
	f.write("{}, {}\n".format(msg, datetime.timedelta(seconds=end-start)))


# 得点シーンの特定（カラーヒストグラム比較）
def compare_color_tokuten_scene(movie, compareimage, comparepoint, msg):
	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
                sys.exit()

	fps = cap.get(cv2.CAP_PROP_FPS)

	ix = comparepoint[0]
	iy = comparepoint[1]
	x = comparepoint[2]
	y = comparepoint[3]

	compare_img = cv2.imread(compareimage,0)
	compare_img = compare_img[iy:y, ix:x]
	compare_hist = cv2.calcHist([compare_img], [0], None, [256], [0, 256])

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			if int(c%fps) == 0:
				img = frame[iy:y, ix:x]
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				img_hist = cv2.calcHist([img], [0], None, [256], [0, 256])
				
				ret = cv2.compareHist(img_hist, compare_hist, 0)
				if ret > cmp_threshold:
					logger.info("{}, {}, {}".format(c//fps, msg, ret))
					f.write("{}, {}".format(c//fps, ret))
					f.write("\n")
		else:
			break
		c += 1
	f.close()


if __name__=="__main__":
	movie_fname = input("movie file for analysis : ")

	# テンプレートマッチングの座標取得(ランナー)
	#print("example # 10:00")
	#tmp_time = input("time where runnner object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "runner_true_image.png")
	
	#img = cv2.imread("runner_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#runnerpoint = (ix, iy, vx, vy)
	runnerpoint = (149, 112, 225, 152)
	#print(runnerpoint)

	# テンプレートマッチングの座標取得(アウト)
	#print("example # 10:00")
	#tmp_time = input("time where out count object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "out_true_image.png")
	
	#img = cv2.imread("out_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#outpoint = (ix, iy, vx, vy)
	outpoint = (148, 179, 223, 203)
	#print(outpoint)

	# テンプレートマッチングの座標取得(ストライク)
	#print("example # 10:00")
	#tmp_time = input("time where strike count object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "strike_true_image.png")
	
	#img = cv2.imread("strike_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#strikepoint = (ix, iy, vx, vy)
	#strikepoint = (148, 165, 223, 179)
	strikepoint = (148, 163, 210, 183)
	#print(strikepoint)

	# テンプレートマッチングの座標取得(ボール)
	#print("example # 10:00")
	#tmp_time = input("time where ball count object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "ball_true_image.png")
	
	#img = cv2.imread("ball_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#ballpoint = (ix, iy, vx, vy)
	ballpoint = (148, 149, 223, 165)
	#print(ballpoint)

	# テンプレートマッチングの座標取得（ホームラン）
	#print("example # 51:51")
	#tmp_time = input("time where homerun object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "homerun_true_image.png")
	
	#img = cv2.imread("homerun_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#homerunpoint = (ix, iy, vx, vy)
	homerunpoint = (172, 176, 880, 542)
	#print(homerunpoint)

	# カラーヒストグラム比較・テンプレートマッチング（得点シーン）の座標取得
	#print("example # 13:24")
	#compare_time = input("time where tokuten object exists (00:00:00) : ")
	#create_true_image(movie_fname, compare_time, "compare_true_image.png")

	#img = cv2.imread("compare_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#tokutenpoint = (ix, iy, vx, vy)
	tokutenpoint = (507, 547, 547, 609)
	#print(tokutenpoint)

	# テンプレートマッチングの座標取得（ゲームセット文字）
	#print("example # 56:57")
	#tmp_time = input("time where gameset object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "gameset_true_image.png")
	
	#img = cv2.imread("gameset_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#gamesetpoint = (ix, iy, vx, vy)
	gamesetpoint = (391, 146, 673, 435)
	#print(gamesetpoint)

	# テンプレートマッチングの座標取得（ホームラン＆ゲームセット）
	#print("example # 23:35")
	#tmp_time = input("time where homerun and gameset object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "homerun_and_gameset_true_image.png")
	
	#img = cv2.imread("homerun_and_gameset_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#homerun_and_gameset_point = (ix, iy, vx, vy)
	homerun_and_gameset_point = (466, 302, 583, 376)
	#print(homerun_and_gameset_point)

	# OCRの座標取得（スコア：先攻）
	#print("example # 47:24")
	#tmp_time = input("time where score object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "score_true_image.png")
	
	#img = cv2.imread("score_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#ocrpoint_firstscore = (ix, iy, vx, vy)
	ocrpoint_firstscore = (105, 136, 147, 170)
	#print(ocrpoint_firstscore)

	# OCRの座標取得（スコア：後攻）
	#print("example # 47:24")
	#tmp_time = input("time where score object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "score_true_image.png")
	
	#img = cv2.imread("score_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#ocrpoint_lastscore = (ix, iy, vx, vy)
	ocrpoint_lastscore = (103, 170, 147, 203)
	#print(ocrpoint_lastscore)

	# OCRの座標取得（得点シーン：先攻）
	#print("example # 47:32")
	#tmp_time = input("time where score object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "tokuten_true_image.png")
	
	#img = cv2.imread("tokuten_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#ocrpoint_firsttokuten = (ix, iy, vx, vy)
	ocrpoint_firsttokuten = (569, 561, 610, 596)
	#print(ocrpoint_firsttokuten)
	
	# OCRの座標取得（得点シーン：後攻）
	#print("example # 47:32")
	#tmp_time = input("time where score object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "tokuten_true_image.png")
	
	#img = cv2.imread("tokuten_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#	cv2.imshow('image',img)
	#	k = cv2.waitKey(1) & 0xFF
	#	if k == 13: # enter key
	#		break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#ocrpoint_lasttokuten = (ix, iy, vx, vy)
	ocrpoint_lasttokuten = (437, 561, 482, 596)
	#print(ocrpoint_lasttokuten)


        # point座標を表示して途中終了するための待機処理
	#time.sleep(1000)


	start = time.time()

	# テンプレートマッチングの実行（ランナー）
	process_list = []

	process1 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r0.png",
			"threshold":runner_threshold,
			"msg":"ランナー：なし"})
	process1.start()
	process_list.append(process1)
	process2 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r1.png",
			"threshold":runner_threshold,
			"msg":"ランナー：一塁"})
	process2.start()
	process_list.append(process2)
	process3 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r2.png",
			"threshold":runner_threshold,
			"msg":"ランナー：二塁"})
	process3.start()
	process_list.append(process3)
	process4 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r3.png",
			"threshold":runner_threshold,
			"msg":"ランナー：三塁"})
	process4.start()
	process_list.append(process4)
	process5 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r12.png",
			"threshold":runner_threshold,
			"msg":"ランナー：一・二塁"})
	process5.start()
	process_list.append(process5)
	process6 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r13.png",
			"threshold":runner_threshold,
			"msg":"ランナー：一・三塁"})
	process6.start()
	process_list.append(process6)
	process7 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r23.png",
			"threshold":runner_threshold,
			"msg":"ランナー：二・三塁"})
	process7.start()
	process_list.append(process7)
	process8 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r123.png",
			"threshold":runner_threshold,
			"msg":"ランナー：満塁"})
	process8.start()
	process_list.append(process8)

	# テンプレートマッチングの実行（アウト）
	process9 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":outpoint,
			"tmpname":"o0.png",
			"threshold":out_threshold,
			"msg":"アウト：０"})
	process9.start()
	process_list.append(process9)
	process10 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":outpoint,
			"tmpname":"o1.png",
			"threshold":out_threshold,
			"msg":"アウト：１"})
	process10.start()
	process_list.append(process10)
	process11 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":outpoint,
			"tmpname":"o2.png",
			"threshold":out_threshold,
			"msg":"アウト：２"})
	process11.start()
	process_list.append(process11)
	
	# テンプレートマッチングの実行（ストライク）
	process12 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":strikepoint,
			"tmpname":"s0.png",
			"threshold":strike_threshold,
			"msg":"ストライク：０"})
	process12.start()
	process_list.append(process12)
	process13 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":strikepoint,
			"tmpname":"s1.png",
			"threshold":strike_threshold,
			"msg":"ストライク：１"})
	process13.start()
	process_list.append(process13)
	process14 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":strikepoint,
			"tmpname":"s2.png",
			"threshold":strike_threshold,
			"msg":"ストライク：２"})
	process14.start()
	process_list.append(process14)
	
	# テンプレートマッチングの実行（ボール）
	process15 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":ballpoint,
			"tmpname":"b0.png",
			"threshold":ball_threshold,
			"msg":"ボール：０"})
	process15.start()
	process_list.append(process15)
	process16 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":ballpoint,
			"tmpname":"b1.png",
			"threshold":ball_threshold,
			"msg":"ボール：１"})
	process16.start()
	process_list.append(process16)
	process17 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":ballpoint,
			"tmpname":"b2.png",
			"threshold":ball_threshold,
			"msg":"ボール：２"})
	process17.start()
	process_list.append(process17)
	process18 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":ballpoint,
			"tmpname":"b3.png",
			"threshold":ball_threshold,
			"msg":"ボール：３"})
	process18.start()
	process_list.append(process18)
	
	# テンプレートマッチングの実行（得点シーン）
	process19 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":tokutenpoint,
			"tmpname":"tokuten.png",
			"threshold":tokuten_threshold,
			"msg":"得点シーン"})
	process19.start()
	process_list.append(process19)

        # テンプレートマッチングの実行（ホームラン）
	process20 = Process(target=tmpmatching, 
		kwargs={"movie":"output.mp4",
			"tmppoint":homerunpoint,
			"tmpname":"homerun_true.png",
			"threshold":homerun_threshold,
			"msg":"ホームラン"})
	process20.start()
	process_list.append(process20)

	# テンプレートマッチングの実行（ホームラン＆ゲームセット）
	process21 = Process(target=tmpmatching,
		kwargs={"movie":"output.mp4",
			"tmppoint":homerun_and_gameset_point,
			"tmpname":"tokuten2.png",
			"threshold":homerun_and_gameset_threshold,
			"msg":"ホームラン＆ゲームセット"})
	process21.start()
	process_list.append(process21)

	# Tesseractを用いたOCR
	if ocr_tool == "tesseract":
		# OCRの実行（スコア：先攻）
		process22 = Process(target=ocr, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_firstscore,
				"msg":"スコア：先攻"})
		process22.start()
		process_list.append(process22)

		# OCRの実行（スコア：後攻）
		process23 = Process(target=ocr, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_lastscore,
				"msg":"スコア：後攻"})
		process23.start()
		process_list.append(process23)
	
		# OCRの実行（得点シーン：先攻）
		process24 = Process(target=ocr, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_firsttokuten,
				"msg":"得点シーン：先攻"})
		process24.start()
		process_list.append(process24)
	
		# OCRの実行（得点シーン：後攻）
		process25 = Process(target=ocr, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_lasttokuten,
				"msg":"得点シーン：後攻"})
		process25.start()
		process_list.append(process25)

	# Cloud Vision APIを用いたOCR
	if ocr_tool == "cloud vision api":
		# OCRの実行（スコア：先攻）
		process22 = Process(target=ocr_google, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_firstscore,
				"msg":"スコア：先攻"})
		process22.start()
		process_list.append(process22)
	
		# OCRの実行（スコア：後攻）
		process23 = Process(target=ocr_google, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_lastscore,
				"msg":"スコア：後攻"})
		process23.start()
		process_list.append(process23)
	
		# OCRの実行（得点シーン：先攻）
		process24 = Process(target=ocr_google, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_firsttokuten,
				"msg":"得点シーン：先攻"})
		process24.start()
		process_list.append(process24)
	
		# OCRの実行（得点シーン：後攻）
		process25 = Process(target=ocr_google, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_lasttokuten,
				"msg":"得点シーン：後攻"})
		process25.start()
		process_list.append(process25)

	# Azure AI Visionを用いたOCR
	if ocr_tool == "azure ai vision":
		# OCRの実行（スコア：先攻）
		process22 = Process(target=ocr_azure, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_firstscore,
				"msg":"スコア：先攻"})
		process22.start()
		process_list.append(process22)
	
		# OCRの実行（スコア：後攻）
		process23 = Process(target=ocr_azure, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_lastscore,
				"msg":"スコア：後攻"})
		process23.start()
		process_list.append(process23)
	
		# OCRの実行（得点シーン：先攻）
		process24 = Process(target=ocr_azure, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_firsttokuten,
				"msg":"得点シーン：先攻"})
		process24.start()
		process_list.append(process24)
	
		# OCRの実行（得点シーン：後攻）
		process25 = Process(target=ocr_azure, 
			kwargs={"movie":"output.mp4",
				"ocrpoint":ocrpoint_lasttokuten,
				"msg":"得点シーン：後攻"})
		process25.start()
		process_list.append(process25)

	# カラーヒストグラム比較の実行
	#process00 = Process(target=compare_color_tokuten_scene, 
	#	kwargs={"movie":"output.mp4",
	#		"compareimage":"compare_true_image.png",
	#		"comparepoint":tokutenpoint,
	#		"msg":"得点シーン"})
	#process00.start()
	#process_list.append(process00)

	for p in process_list:
		p.join()

	end = time.time()
	print("処理時間:", datetime.timedelta(seconds=end-start))
