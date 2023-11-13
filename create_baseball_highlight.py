import cv2
import numpy as np
import datetime
import imutils
import time
import sys
import copy
from PIL import Image
#import pyocr
import re
from multiprocessing import Process
import logging

runnerpoint = () 	# テンプレートマッチング（ランナー）の座標
runner_threshold = 0.8	# テンプレートマッチング（ランナー）の閾値
outpoint = () 		# テンプレートマッチング（アウト）の座標
out_threshold = 0.9 	# テンプレートマッチング（アウト）の閾値
homerunpoint = ()	# テンプレートマッチング（ホームラン）の座標
homerun_threshold = 0.3 # テンプレートマッチング（ホームラン）の閾値
#ocrpoint = () 		# OCRの座標
tokutenpoint = () 	# カラーヒストグラム比較・テンプレートマッチング（得点シーン）の座標
cmp_threshold = 0.65 	# カラーヒストグラム比較の閾値
tokuten_threshold = 0.5 # テンプレートマッチング（得点シーン）の閾値

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


# ピンチ・チャンスシーンの特定（テンプレートマッチング）
def tmpmatching_pinch_chance_scene(movie, tmppoint, tmpname, msg):
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
						logger.debug("template matching error (runner), {}".format(scale))
						continue
					_, max_val, _, max_loc = cv2.minMaxLoc(res)
					if 1.0 > max_val > runner_threshold:
						logger.info("{}, {}, {}, {}".format(c//fps,  msg, max_val, scale))
						f.write("{}, {}, {}".format(c//fps, max_val, scale))
						f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()


# アウトカウントの特定（テンプレートマッチング）
def tmpmatching_outcount_scene(movie, tmppoint, tmpname, msg):
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
						logger.debug("template matching error (outcount), {}".format(scale))
						continue
					_, max_val, _, max_loc = cv2.minMaxLoc(res)
					if 1.0 > max_val > out_threshold:
						logger.info("{}, {}, {}, {}".format(c//fps, msg, max_val, scale))
						f.write("{}, {}, {}".format(c//fps, max_val, scale))
						f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()


# ホームランの特定（テンプレートマッチング）
def tmpmatching_homerun_scene(movie, tmppoint, tmpname, msg):
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
						logger.debug("template matching error (homerun), {}".format(scale))
						continue
					_, max_val, _, max_loc = cv2.minMaxLoc(res)
					if 1.0 > max_val > homerun_threshold:
						logger.info("{}, {}, {}, {}".format(c//fps, msg, max_val, scale))
						f.write("{}, {}, {}".format(c//fps, max_val, scale))
						f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()


# 得点シーンの特定（テンプレートマッチング）
def tmpmatching_tokuten_scene(movie, tmppoint, tmpname, msg):
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
						logger.debug("template matching error (homerun), {}".format(scale))
						continue
					_, max_val, _, max_loc = cv2.minMaxLoc(res)
					if 1.0 > max_val > tokuten_threshold:
						logger.info("{}, {}, {}, {}".format(c//fps, msg, max_val, scale))
						f.write("{}, {}, {}".format(c//fps, max_val, scale))
						f.write("\n")
		else:
			break
		c += 1
	f.close()
	cap.release()


# 得点シーンの特定（OCR）
def ocr_tokuten_scene(movie, ocrpoint, start=0, end=600):
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

	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			if int(c%fps) == 0 and start < c//fps < end:
				img = cv2.resize(frame[iy:y, ix:x], dsize=None, fx=3.0, fy=3.0)
				txt = tool.image_to_string(
					Image.fromarray(img),
					lang="jpn",
					builder=pyocr.builders.TextBuilder(tesseract_layout=7))
				num_txt = re.findall(r"\d+", txt)
				if num_txt != []:
					logger.info("{}, {}".format(c//fps, txt))
		else:
			break
		c += 1


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
	# 00:10:00, 00:10:00, 00:51:51, 00:13:24

	movie_fname = input("movie file for analysis (runner, out, tokuten) : ")

	# テンプレートの座標取得(ランナー)
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
	print(runnerpoint)

	# テンプレートの座標取得(アウト)
	#movie_fname = input("movie file for template matching (out) : ")
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
	print(outpoint)

	# テンプレートの座標取得（ホームラン）
	#movie_fname = input("movie file for template matching (out) : ")
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
	print(homerunpoint)

	# OCRの座標取得
	#movie_fname = input("movie file for ocr (tokuten) : ")
	#ocr_time = input("time where ocr object exists (00:00:00) : ")
	#create_true_image(movie_fname, ocr_time, "ocr_true_image.png")

	#img = cv2.imread("ocr_true_image.png")
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
	#ocrpoint = (ix, iy, vx, vy)
	#print(ocrpoint)

	# カラーヒストグラム比較・テンプレートマッチング（得点シーン）の座標取得
	#movie_fname = input("movie file for compare histgram (tokuten) : ")
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
	#tokutenpoint = (394, 556, 655, 601)
	#tokutenpoint = (519, 556, 536, 601)
	tokutenpoint = (507, 547, 547, 609)
	print(tokutenpoint)

	start = time.time()

	# テンプレートマッチングの実行（ランナー）
	process_list = []

	process1 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r0.png",
			"msg":"ランナー：なし"})
	process1.start()
	process_list.append(process1)
	process2 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r1.png",
			"msg":"ランナー：一塁"})
	process2.start()
	process_list.append(process2)
	process3 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r2.png",
			"msg":"ランナー：二塁"})
	process3.start()
	process_list.append(process3)
	process4 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r3.png",
			"msg":"ランナー：三塁"})
	process4.start()
	process_list.append(process4)
	process5 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r12.png",
			"msg":"ランナー：一・二塁"})
	process5.start()
	process_list.append(process5)
	process6 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r13.png",
			"msg":"ランナー：一・三塁"})
	process6.start()
	process_list.append(process6)
	process7 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r23.png",
			"msg":"ランナー：二・三塁"})
	process7.start()
	process_list.append(process7)
	process8 = Process(target=tmpmatching_pinch_chance_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":runnerpoint,
			"tmpname":"r123.png",
			"msg":"ランナー：満塁"})
	process8.start()
	process_list.append(process8)

	# テンプレートマッチングの実行（アウト）
	process9 = Process(target=tmpmatching_outcount_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":outpoint,
			"tmpname":"o0.png",
			"msg":"アウト：０"})
	process9.start()
	process_list.append(process9)
	process10 = Process(target=tmpmatching_outcount_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":outpoint,
			"tmpname":"o1.png",
			"msg":"アウト：１"})
	process10.start()
	process_list.append(process10)
	process11 = Process(target=tmpmatching_outcount_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":outpoint,
			"tmpname":"o2.png",
			"msg":"アウト：２"})
	process11.start()
	process_list.append(process11)
	
	# テンプレートマッチングの実行（得点シーン）
	process12 = Process(target=tmpmatching_tokuten_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":tokutenpoint,
			"tmpname":"tokuten.png",
			"msg":"得点シーン"})
	process12.start()
	process_list.append(process12)

	# カラーヒストグラム比較の実行
	#process12 = Process(target=compare_color_tokuten_scene, 
	#	kwargs={"movie":"output.mp4",
	#		"compareimage":"compare_true_image.png",
	#		"comparepoint":tokutenpoint,
	#		"msg":"得点シーン"})
	#process12.start()
	#process_list.append(process12)

        # テンプレートマッチングの実行（ホームラン）
	process13 = Process(target=tmpmatching_homerun_scene, 
		kwargs={"movie":"output.mp4",
			"tmppoint":homerunpoint,
			"tmpname":"homerun_true.png",
			"msg":"ホームラン"})
	process13.start()
	process_list.append(process13)

	for p in process_list:
		p.join()

	end = time.time()
	print("処理時間:", datetime.timedelta(seconds=end-start))
