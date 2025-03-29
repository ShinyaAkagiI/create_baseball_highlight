import copy
import cv2
from moviepy.editor import *
import time

video_fname = "output.mp4"
video_ofname = "output_highlight.mp4"

def create_highlight(movie_time=60):
	start_time = time.time()

	with open("ストライク：０", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		s0_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in s0_clock.keys():
				s0_clock.update(tmp)
			else:
				if d[1] > s0_clock[str(d[0])]:
					s0_clock.update(tmp)
				else:
					pass

	
	with open("ストライク：１", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		s1_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in s1_clock.keys():
				s1_clock.update(tmp)
			else:
				if d[1] > s1_clock[str(d[0])]:
					s1_clock.update(tmp)
				else:
					pass

	with open("ストライク：２", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		s2_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in s2_clock.keys():
				s2_clock.update(tmp)
			else:
				if d[1] > s2_clock[str(d[0])]:
					s2_clock.update(tmp)
				else:
					pass

	with open("ボール：０", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		b0_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in b0_clock.keys():
				b0_clock.update(tmp)
			else:
				if d[1] > b0_clock[str(d[0])]:
					b0_clock.update(tmp)
				else:
					pass

	with open("ボール：１", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		b1_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in b1_clock.keys():
				b1_clock.update(tmp)
			else:
				if d[1] > b1_clock[str(d[0])]:
					b1_clock.update(tmp)
				else:
					pass

	with open("ボール：２", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		b2_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in b2_clock.keys():
				b2_clock.update(tmp)
			else:
				if d[1] > b2_clock[str(d[0])]:
					b2_clock.update(tmp)
				else:
					pass

	with open("ボール：３", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		b3_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in b3_clock.keys():
				b3_clock.update(tmp)
			else:
				if d[1] > b3_clock[str(d[0])]:
					b3_clock.update(tmp)
				else:
					pass

	with open("アウト：０", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		o0_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in o0_clock.keys():
				o0_clock.update(tmp)
			else:
				if d[1] > o0_clock[str(d[0])]:
					o0_clock.update(tmp)
				else:
					pass

	with open("アウト：１", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		o1_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in o1_clock.keys():
				o1_clock.update(tmp)
			else:
				if d[1] > o1_clock[str(d[0])]:
					o1_clock.update(tmp)
				else:
					pass

	with open("アウト：２", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]
		
		o2_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in o2_clock.keys():
				o2_clock.update(tmp)
			else:
				if d[1] > o2_clock[str(d[0])]:
					o2_clock.update(tmp)
				else:
					pass

	video = cv2.VideoCapture(video_fname)
	fps = video.get(cv2.CAP_PROP_FPS)
	frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	video_time = int(frames/fps)

	cut_timeline = []

	before = [False,False,False]
	now = [False,False,False]
	for c in range(video_time):
		# nowを更新
		false_flag = True
		s_threshold = 0.0
		b_threshold = 0.0
		o_threshold = 0.0

		c = str(float(c))

		if c in s0_clock.keys():
			now[0] = 0
			s_threshold = s0_clock[c]
			false_flag = False

		if c in s1_clock.keys():
			if float(s1_clock[c]) > float(s_threshold):
				now[0] = 1
				s_threshold = s1_clock[c]
			else:
				pass
			false_flag = False

		if c in s2_clock.keys():
			if float(s2_clock[c]) > float(s_threshold):
				now[0] = 2
				s_threshold = s2_clock[c]
			else:
				pass
			false_flag = False

		if c in b0_clock.keys():
			if float(b0_clock[c]) > float(b_threshold):
				now[1] = 0
				b_threshold = b0_clock[c]
			else:
				pass
			false_flag = False

		if c in b1_clock.keys():
			if float(b1_clock[c]) > float(b_threshold):
				now[1] = 1
				b_threshold = b1_clock[c]
			else:
				pass
			false_flag = False

		if c in b2_clock.keys():
			if float(b2_clock[c]) > float(b_threshold):
				now[1] = 2
				b_threshold = b2_clock[c]
			else:
				pass
			false_flag = False

		if c in b3_clock.keys():
			if float(b3_clock[c]) > float(b_threshold):
				now[1] = 3
				b_threshold = b3_clock[c]
			else:
				pass
			false_flag = False

		if c in o0_clock.keys():
			if float(o0_clock[c]) > float(o_threshold):
				now[2] = 0
				o_threshold = o0_clock[c]
			else:
				pass
			false_flag = False

		if c in o1_clock.keys():
			if float(o1_clock[c]) > float(o_threshold):
				now[2] = 1
				o_threshold = o1_clock[c]
			else:
				pass
			false_flag = False

		if c in o2_clock.keys():	
			if float(o2_clock[c]) > float(o_threshold):
				now[2] = 2
				o_threshold = o2_clock[c]
			else:
				pass
			false_flag = False

		if false_flag:
			now = [False,False,False]

		# カウントのbeforeとnowを比較
		if str(before) == str(now):
			pass
		elif (before[0] == 2) and (before[2] != False) and (now[2] != False) and (now[0] == 0) and (now[1] == 0):
			cut_flag = True	
		elif (str(before) != "[False, False, False]") and (str(now) == "[False, False, False]"):
			try:
				if cut_flag:
					cut_timeline.append(c)
					cut_flag = False
			except:
				pass
		else:
			cut_timeline.append(c)

		# beforeを更新
		before = copy.deepcopy(now)

	with open("ホームラン＆ゲームセット", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]

		h_g_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in h_g_clock.keys():
				h_g_clock.update(tmp)
			else:
				if d[1] > h_g_clock[str(d[0])]:
					h_g_clock.update(tmp)
				else:
					pass

		# ホームランとゲームセットを分離
		homerun_clock = {}
		gameset_clock = {}

		for i in sorted(list(h_g_clock)):
			front_flag = True
			back_flag = True 
			for j in range(5):
				if str(float(i)+float(j)+1.0) not in list(h_g_clock):
					front_flag = False
				if str(float(i)-float(j)-1.0) not in list(h_g_clock):
					back_flag = False

			if front_flag or back_flag:
				gameset_clock[i] = h_g_clock[i]
			else:
				homerun_clock[i] = h_g_clock[i]

		#print(homerun_clock)
		#print(gameset_clock)

	# 末尾にゲームセット時間を追加
	gameset_time = sorted(list(gameset_clock))[0]
	set(cut_timeline).add(gameset_time)

	#print(cut_timeline)

	# 先頭、末尾だけ特別な処理を実施
	cut_timeline_dict = {}
	count = 2
	for c in range(int(float(cut_timeline[0])), video_time):
		c = str(float(c))
		try:
			if float(cut_timeline[0]) <= float(c) <= float(cut_timeline[1]):
				cut_timeline_dict[c] = float(cut_timeline[0])
			elif float(cut_timeline[-1]) == float(c):
				cut_timeline_dict[c] = float(cut_timeline[count])
				count += 1
			elif float(cut_timeline[count]) == float(c):
				cut_timeline_dict[c] = float(cut_timeline[count-1])+1.0
				count += 1
			else:
				cut_timeline_dict[c] = float(cut_timeline[count-1])+1.0
		except IndexError:
			break

	# 投球間隔データの取得完了
	#print(cut_timeline_dict)

	# 盛り上がり度数
	weight_highlight_time = {}

	# 得点シーンの盛り上がり度数を1.0にする
	with open("得点シーン", "r") as f:
		data = f.read()
		data = data.split("\n")
		data = [d.split(", ") for d in data if not d == ""]

		tokuten_clock = {}
		for d in data:
			tmp = {d[0]:d[1]}
			if d[0] not in tokuten_clock.keys():
				tokuten_clock.update(tmp)
				weight_highlight_time[str(d[0])] = 1.0
			else:
				if d[1] > tokuten_clock[str(d[0])]:
					tokuten_clock.update(tmp)
				else:
					pass

	# 同点シーンの盛り上がり度数を+1.0
	# 勝ち越しシーン, 逆転シーンの盛り上がり度数を+2.0にする
	with open("得点シーン：先攻_model1", "r") as f:
		data = f.read()
		data = data.split("\n")
		tokuten_senkou = {}
		for d in data:
			if d != "":
				tmp = d.split(", ")
				tokuten_senkou[str(tmp[0])] = tmp[1]

	with open("得点シーン：後攻_model1", "r") as f:
		data = f.read()
		data = data.split("\n")
		tokuten_koukou = {}
		for d in data:
			if d != "":
				tmp = d.split(", ")
				tokuten_koukou[str(tmp[0])] = tmp[1]

	with open("スコア：先攻_model1", "r") as f:
		data = f.read()
		data = data.split("\n")
		score_senkou = {}
		for d in data:
			if d != "":
				tmp = d.split(", ")
				score_senkou[str(tmp[0])] = tmp[1]

	with open("スコア：後攻_model1", "r") as f:
		data = f.read()
		data = data.split("\n")
		score_koukou = {}
		for d in data:
			if d != "":
				tmp = d.split(", ")
				score_koukou[str(tmp[0])] = tmp[1]

	for t in tokuten_clock.keys():
		if t in tokuten_senkou.keys() and t in tokuten_koukou.keys():
			# 同点シーン
			if tokuten_senkou[t] == tokuten_koukou[t]:
				weight_highlight_time[str(t)] += 1.0
			else:
				# スコア情報が取得できるまで、スコア情報を前方探索
				flag = True
				prev = cut_timeline_dict[t]
				ss = ""
				sk = ""
				while flag:
					try:
						if ss == "":
							ss = score_senkou[str(prev)]
						if sk == "":
							sk = score_koukou[str(prev)]
						flag = False
					except:
						prev = float(prev) - 1.0
						flag = True

				# 勝ち越しシーン、逆点シーン
				if int(ss) >= int(sk):
					if int(tokuten_senkou[t]) < int(tokuten_koukou[t]):
						weight_highlight_time[str(t)] += 2.0
				if int(ss) <= int(sk):
					if int(tokuten_senkou[t]) > int(tokuten_koukou[t]):
						weight_highlight_time[str(t)] += 2.0
	
	# ホームランシーンの重み付け	
	for i in homerun_clock.keys():
		# 基本は1.0
		weight_highlight_time[str(i)] = 1.0

		# スコア情報が取得できるまで、スコア情報を前方探索
		flag = True
		prev = cut_timeline_dict[i]
		before_ss = ""
		before_sk = ""
		while flag:
			try:
				if before_ss == "":
					before_ss = score_senkou[str(prev)]
				if before_sk == "":
					before_sk = score_koukou[str(prev)]
				flag = False
			except:
				prev = float(prev) - 1.0
				flag = True

		# スコア情報が取得できるシーンまで、スコア情報を後方探索
		flag = True
		later = i
		after_ss = ""
		after_sk = ""
		while flag:
			try:
				if after_ss == "":
					after_ss = score_senkou[str(later)]
				if after_sk == "":
					after_sk = score_koukou[str(later)]
				flag = False
			except:
				later = float(later) + 1.0
				flag = True
		
		# 同点ホームランシーン
		if after_ss == after_sk:
			weight_highlight_time[str(i)] += 1.0

		# 勝ち越し、逆転ホームランシーン
		if before_ss >= before_sk:
			if after_ss < after_sk:
				weight_highlight_time[str(i)] += 2.0
		if before_ss <= before_sk:
			if after_ss > after_sk:
				weight_highlight_time[str(i)] += 2.0

	# 勝ち越し・逆転ピンチ阻止シーン（ランナー：満塁、ランナー：二・三塁）
	with open("ランナー：満塁", "r") as f:
		data = f.read()
		data = data.split("\n")
		runner_123 = {}
		for d in data:
			if d != "":
				tmp = d.split(", ")
				runner_123[str(tmp[0])] = tmp[1]
	
	with open("ランナー：二・三塁", "r") as f:
		data = f.read()
		data = data.split("\n")
		runner_23 = {}
		for d in data:
			if d != "":
				tmp = d.split(", ")
				runner_23[str(tmp[0])] = tmp[1]
	
	for i in runner_123.keys():
		# ランナー満塁時の最後の結果（ファウルなどの分断を除く5秒以上間隔が空いたところ）
		if str(float(i)+5.0) not in runner_123.keys():
			# 最後の結果
			if str(float(i)+1.0) not in runner_123.keys():
				flag = True
				prev = i
				ss = ""
				sk = ""
				while flag:
					try:
						if ss == "":
							ss = score_senkou[str(prev)]
						if sk == "":
							sk = score_koukou[str(prev)]
						flag = False
					except:
						prev = float(prev) - 1.0
						flag = True
				# 接戦時の判定
				if abs(int(ss)-int(sk)) < 2:
					cut_timeline_dict_weight = [ cut_timeline_dict[str(i)] for i in weight_highlight_time.keys() ]
					# 得点シーン以外
					if cut_timeline_dict[i] not in cut_timeline_dict_weight:
						# シーン終了タイミングの取得
						#end_time = float(i)+1
						#while cut_timeline_dict[str(end_time)] == cut_timeline_dict[i]:
						#	end_time += 1
						# 暫定的に5秒後に指定
						end_time = float(i)+5

						# 重みを1.5に指定
						weight_highlight_time[str(end_time)] = 1.5
			else:
				pass


	for i in runner_23.keys():
		# ランナー満塁時の最後の結果（ファウルなどの分断を除く5秒以上間隔が空いたところ）
		if str(float(i)+5.0) not in runner_23.keys():
			# 最後の結果
			if str(float(i)+1.0) not in runner_23.keys():
				flag = True
				prev = i
				ss = ""
				sk = ""
				while flag:
					try:
						if ss == "":
							ss = score_senkou[str(prev)]
						if sk == "":
							sk = score_koukou[str(prev)]
						flag = False
					except:
						prev = float(prev) - 1.0
						flag = True
				# 接戦時の判定
				if abs(int(ss)-int(sk)) < 2:
					cut_timeline_dict_weight = [ cut_timeline_dict[str(i)] for i in weight_highlight_time.keys() ]
					# 得点シーン以外
					if cut_timeline_dict[i] not in cut_timeline_dict_weight:
						# シーン終了タイミングの取得
						#end_time = float(i)+1
						#while cut_timeline_dict[str(end_time)] == cut_timeline_dict[i]:
						#	end_time += 1
						# 暫定的に5秒後に指定
						end_time = float(i)+5

						# 重みを1.5に指定
						weight_highlight_time[str(end_time)] = 1.5
			else:
				pass

	# 連続する値を一つにまとめる
	weight_highlight_time_new = {}
	for i in weight_highlight_time.keys():
		tmp = float(i)+1
		if str(tmp) not in weight_highlight_time.keys():
			weight_highlight_time_new[i] = weight_highlight_time[i]

	# 重み辞書を値によってソート
	result = sorted(weight_highlight_time_new.items(), key=lambda x:(x[1], float(x[0])), reverse=True)

	print(result)

	# 動画の切り分けと結合
	divide_movie = []
	time_limit = movie_time

	# ゲームセットの追加
	gameset_time = float(gameset_time)
	divide_movie.append((cut_timeline_dict[str(gameset_time-1.0)], gameset_time+10.0))
	time_limit -= float(gameset_time+10) - float(cut_timeline_dict[str(gameset_time-1.0)])

	# 重み辞書を重み順で呼び出し、動画時間に収まるように場面を切り分け
	for i in result:
		start = cut_timeline_dict[i[0]]
		end = i[0]
		time_limit -= float(end) - float(start) + 1.0
		if time_limit < 0:
			break
		divide_movie.append((start, end))

	# 時間順に並び替え
	divide_movie = sorted(divide_movie, key=lambda x:x[0])
	#print(divide_movie)

	# 動画の結合
	videoclips = []
	for i in divide_movie:
		clip = VideoFileClip(video_fname).subclip(float(i[0]), float(i[1])+1.0)
		videoclips.append(clip)
	final_clip = concatenate_videoclips(videoclips)
	final_clip.write_videofile(video_ofname, audio_codec="aac")

	end_time = time.time()
	print("処理時間：", end_time-start_time)

if __name__ == "__main__":
	create_highlight(movie_time=180)

