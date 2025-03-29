import cv2
import time
import datetime
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from multiprocessing import Process

movie = "output.mp4"

model = load_model("model.h5")

def score_digit_recognition(movie, tmppoint, msg):
	# 処理時間計測
	start_time = time.time()

	# ストライクカウントでスコア情報の有無を判定
	score_scene = set()
	with open("ストライク：０", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if d != ""]

	for d in data:
		score_scene.add(float(d[0]))

	with open("ストライク：１", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if d != ""]

	for d in data:
		score_scene.add(float(d[0]))

	with open("ストライク：２", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if d != ""]

	for d in data:
		score_scene.add(float(d[0]))

	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = cap.get(cv2.CAP_PROP_FPS)

	ix = tmppoint[0]
	iy = tmppoint[1]
	x = tmppoint[2]
	y = tmppoint[3]

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			# １秒単位の解析
			if int(c%fps) == 0:
				# スコア情報を含む秒数の場合
				if float(c/fps) in score_scene:
					# OCRの位置特定
					frame_point = frame[iy:y, ix:x]

					# 文字分割の事前準備
					frame_point = cv2.cvtColor(frame_point, cv2.COLOR_BGR2GRAY)
					ret, frame_point = cv2.threshold(frame_point, 220, 255, cv2.THRESH_BINARY)

					# 文字分割
					vpp = np.sum(frame_point, axis=0)
					character_list = []
					start = None
					end = None
					for i,val in enumerate(vpp):
						if val != 0:
							if start == None:
								start = i
						elif start != None:
							end = i-1
							character_list.append((start, end))
							start = None
							end = None
						else:
							pass
					character_img_list = [frame_point[:,cl[0]:cl[1]] for cl in character_list]

					result = ""
					for cil in character_img_list:
						# OCRの事前準備
						img_ = cv2.copyMakeBorder(cil, 0, 0, 15, 15, cv2.BORDER_CONSTANT, (0,0,0))
						#kernel = np.ones((5, 5), np.uint8)
						#img_ = cv2.dilate(img_, kernel, iterations=1)
						#img_ = 255-img_
						img_ = cv2.resize(img_, (28,28))
						img_array = img_to_array(img_)/255.0
						img_array = img_array.reshape(-1,28,28,1)

						# OCR
						pred = model.predict(img_array)
						result += str(pred.argmax())

					f.write("{}, {}\n".format(c//fps, result))
		else:
			break
		c += 1
	f.close()
	cap.release()

	# 処理時間計測
	end_time = time.time()

	# 処理時間記載
	# close時に追記されるのでファイルロックは不要
	f = open("processtime.log", "a")
	f.write("{}, {}\n".format(msg, datetime.timedelta(seconds=end_time-start_time)))
	f.close()


def tokuten_digit_recognition(movie, tmppoint, msg):
	# 処理時間計測
	start_time = time.time()

	# 得点シーンでスコア情報の有無を判定
	tokuten_scene = set()
	with open("得点シーン", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if d != ""]

	for d in data:
		tokuten_scene.add(float(d[0]))

	cap = cv2.VideoCapture(movie)
	if not cap.isOpened():
		sys.exit()
	fps = cap.get(cv2.CAP_PROP_FPS)

	ix = tmppoint[0]
	iy = tmppoint[1]
	x = tmppoint[2]
	y = tmppoint[3]

	f = open(msg, mode='a')
	c = 0
	while True:
		ret, frame = cap.read()
		if ret:
			# １秒単位の解析
			if int(c%fps) == 0:
				# スコア情報を含む秒数の場合
				if float(c/fps) in tokuten_scene:
					# OCRの位置特定
					frame_point = frame[iy:y, ix:x]

					# 文字分割の事前準備
					frame_point = cv2.cvtColor(frame_point, cv2.COLOR_BGR2GRAY)
					ret, frame_point = cv2.threshold(frame_point, 220, 255, cv2.THRESH_BINARY)

					# 文字分割
					vpp = np.sum(frame_point, axis=0)
					character_list = []
					start = None
					end = None
					for i,val in enumerate(vpp):
						if val != 0:
							if start == None:
								start = i
						elif start != None:
							end = i-1
							character_list.append((start, end))
							start = None
							end = None
						else:
							pass
					character_img_list = [frame_point[:,cl[0]:cl[1]] for cl in character_list]

					result = ""
					for cil in character_img_list:
						# OCRの事前準備
						img_ = cv2.copyMakeBorder(cil, 0, 0, 15, 15, cv2.BORDER_CONSTANT, (0,0,0))
						#kernel = np.ones((5, 5), np.uint8)
						#img_ = cv2.dilate(img_, kernel, iterations=1)
						#img_ = 255-img_
						img_ = cv2.resize(img_, (28,28))
						img_array = img_to_array(img_)/255.0
						img_array = img_array.reshape(-1,28,28,1)

						# OCR
						pred = model.predict(img_array)
						result += str(pred.argmax())

					f.write("{}, {}\n".format(c//fps, result))
		else:
			break
		c += 1
	f.close()
	cap.release()

	# 処理時間計測
	end_time = time.time()

	# 処理時間記載
	# close時に追記されるのでファイルロックは不要
	f = open("processtime.log", "a")
	f.write("{}, {}\n".format(msg, datetime.timedelta(seconds=end_time-start_time)))
	f.close()


if __name__ == "__main__":
	multi_start = time.time()

	# OCRの座標取得（スコア：先攻）
	#print("example # 47:24")
	#tmp_time = input("time where score object exists (00:00:00) : ")
	#create_true_image(movie_fname, tmp_time, "score_true_image.png")

	#img = cv2.imread("score_true_image.png")
	#cache = None
	#cv2.namedWindow('image')
	#cv2.setMouseCallback('image',select_rectangle)
	#while(1):
	#       cv2.imshow('image',img)	
	#       k = cv2.waitKey(1) & 0xFF
	#       if k == 13: # enter key
	#               break
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
	#       cv2.imshow('image',img)
	#       k = cv2.waitKey(1) & 0xFF
	#       if k == 13: # enter key
	#               break
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
	#       cv2.imshow('image',img)
	#       k = cv2.waitKey(1) & 0xFF
	#       if k == 13: # enter key
	#               break
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
	#       cv2.imshow('image',img)
	#       k = cv2.waitKey(1) & 0xFF
	#       if k == 13: # enter key
	#               break
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#ocrpoint_lasttokuten = (ix, iy, vx, vy)
	ocrpoint_lasttokuten = (437, 561, 482, 596)
	#print(ocrpoint_lasttokuten)

	process_list = []

	process1 = Process(target=score_digit_recognition,
			kwargs={"movie":"output.mp4",
				"tmppoint":ocrpoint_firstscore,
				"msg":"スコア：先攻"})
	process1.start() 
	process_list.append(process1)

	process2 = Process(target=score_digit_recognition,
			kwargs={"movie":"output.mp4",
				"tmppoint":ocrpoint_lastscore,
				"msg":"スコア：後攻"})
	process2.start() 
	process_list.append(process2)

	process3 = Process(target=tokuten_digit_recognition,
			kwargs={"movie":"output.mp4",
				"tmppoint":ocrpoint_firsttokuten,
				"msg":"得点シーン：先攻"})
	process3.start()
	process_list.append(process3)

	process4 = Process(target=tokuten_digit_recognition,
			kwargs={"movie":"output.mp4",
				"tmppoint":ocrpoint_lasttokuten,
				"msg":"得点シーン：後攻"})
	process4.start() 
	process_list.append(process4)

	for p in process_list:
		p.join()

	multi_end = time.time()

	single_start = time.time()

	score_digit_recognition("output.mp4", ocrpoint_firstscore, "スコア：先攻")
	score_digit_recognition("output.mp4", ocrpoint_lastscore, "スコア：後攻")
	tokuten_digit_recognition("output.mp4", ocrpoint_firsttokuten, "得点シーン：先攻")
	tokuten_digit_recognition("output.mp4", ocrpoint_lasttokuten, "得点シーン：後攻")

	single_end = time.time()

	print("マルチプロセスの処理時間：", multi_end-multi_start)
	print("シングルプロセスの処理時間：", single_end-single_start)
