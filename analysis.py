# 正解データの読み込み
fname_result = "result.txt"
with open(fname_result, "r") as f:
	head = f.readline()
	data = f.read()

# 正解データの加工
# data[line][num]
# num 0: time
# num 1: runner nothing
# num 2: runner 1
# num 3: runner 2
# num 4: runner 3
# num 5: runner 1 and 2
# num 6: runner 1 and 3
# num 7: runner 2 and 3
# num 8: runner 1 and 2 and 3
# num 9: out 0
# num 10: out 1
# num 11: out 2
# num 12: tokuten scene
# num 13: homerun scene
# num 14: ball 0
# num 15: ball 1
# num 16: ball 2
# num 17: ball 3
# num 18: strike 0
# num 19: strike 1
# num 20: strike 2
# num 21: gameset
# num 22: tokuten_in_homerun_and_gameset
# num 23: score_ocr_first
# num 24: score_ocr_last
# num 25: tokuten_ocr_first
# num 26: tokuten_ocr_last
data = data.split("\n")
for i,d in enumerate(data):
	data[i] = d.split(", ")
data = [i for i in data if i != ['']]

#file names
fname_r0 = "ランナー：なし"
fname_r1 = "ランナー：一塁"
fname_r2 = "ランナー：二塁"
fname_r3 = "ランナー：三塁"
fname_r12 = "ランナー：一・二塁"
fname_r13 = "ランナー：一・三塁"
fname_r23 = "ランナー：二・三塁"
fname_r123 = "ランナー：満塁"
fname_o0 = "アウト：０"
fname_o1 = "アウト：１"
fname_o2 = "アウト：２"
fname_tokuten = "得点シーン"
fname_homerun = "ホームラン"
fname_b0 = "ボール：０"
fname_b1 = "ボール：１"
fname_b2 = "ボール：２"
fname_b3 = "ボール：３"
fname_s0 = "ストライク：０"
fname_s1 = "ストライク：１"
fname_s2 = "ストライク：２"
fname_gameset = "ゲームセット"
fname_tokuten_in_homerun_and_gameset = "ホームラン＆ゲームセット"
fname_score_ocr_first = "スコア：先攻"
fname_score_ocr_last = "スコア：後攻"
fname_tokuten_ocr_first = "得点シーン：先攻"
fname_tokuten_ocr_last = "得点シーン：後攻"

# runner nothing
with open(fname_r0, "r") as f:
	data_1_raw = f.read()

data_1_raw = data_1_raw.split("\n")
data_1 = {}
for d in data_1_raw:
	line = d.split(", ")
	try:
		data_1[line[0]] = line[1]
	except:
		pass

# runner 1
with open(fname_r1, "r") as f:
	data_2_raw = f.read()

data_2_raw = data_2_raw.split("\n")
data_2 = {}
for d in data_2_raw:
	line = d.split(", ")
	try:
		data_2[line[0]] = line[1]
	except:
		pass

# runner 2
with open(fname_r2, "r") as f:
	data_3_raw = f.read()

data_3_raw = data_3_raw.split("\n")
data_3 = {}
for d in data_3_raw:
	line = d.split(", ")
	try:
		data_3[line[0]] = line[1]
	except:
		pass

# runner 3
with open(fname_r3, "r") as f:
	data_4_raw = f.read()

data_4_raw = data_4_raw.split("\n")
data_4 = {}
for d in data_4_raw:
	line = d.split(", ")
	try:
		data_4[line[0]] = line[1]
	except:
		pass

# runner 1 and 2
with open(fname_r12, "r") as f:
	data_5_raw = f.read()

data_5_raw = data_5_raw.split("\n")
data_5 = {}
for d in data_5_raw:
	line = d.split(", ")
	try:
		data_5[line[0]] = line[1]
	except:
		pass

# runner 1 and 3
with open(fname_r13, "r") as f:
	data_6_raw = f.read()

data_6_raw = data_6_raw.split("\n")
data_6 = {}
for d in data_6_raw:
	line = d.split(", ")
	try:
		data_6[line[0]] = line[1]
	except:
		pass

# runner 2 and 3
with open(fname_r23, "r") as f:
	data_7_raw = f.read()

data_7_raw = data_7_raw.split("\n")
data_7 = {}
for d in data_7_raw:
	line = d.split(", ")
	try:
		data_7[line[0]] = line[1]
	except:
		pass

# runner 1 and 2 and 3
with open(fname_r123, "r") as f:
	data_8_raw = f.read()

data_8_raw = data_8_raw.split("\n")
data_8 = {}
for d in data_8_raw:
	line = d.split(", ")
	try:
		data_8[line[0]] = line[1]
	except:
		pass

# out 0
with open(fname_o0, "r") as f:
	data_9_raw = f.read()

data_9_raw = data_9_raw.split("\n")
data_9 = {}
for d in data_9_raw:
	line = d.split(", ")
	try:
		data_9[line[0]] = line[1]
	except:
		pass

# out 1
with open(fname_o1, "r") as f:
	data_10_raw = f.read()

data_10_raw = data_10_raw.split("\n")
data_10 = {}
for d in data_10_raw:
	line = d.split(", ")
	try:
		data_10[line[0]] = line[1]
	except:
		pass

# out 2
with open(fname_o2, "r") as f:
	data_11_raw = f.read()

data_11_raw = data_11_raw.split("\n")
data_11 = {}
for d in data_11_raw:
	line = d.split(", ")
	try:
		data_11[line[0]] = line[1]
	except:
		pass

# tokuten scene
with open(fname_tokuten, "r") as f:
	data_12_raw = f.read()

data_12_raw = data_12_raw.split("\n")
data_12 = {}
for d in data_12_raw:
	line = d.split(", ")
	try:
		data_12[line[0]] = line[1]
	except:
		pass

# homerun scene
with open(fname_homerun, "r") as f:
	data_13_raw = f.read()

data_13_raw = data_13_raw.split("\n")
data_13 = {}
for d in data_13_raw:
	line = d.split(", ")
	try:
		data_13[line[0]] = line[1]
	except:
		pass

# ball 0
with open(fname_b0, "r") as f:
	data_14_raw = f.read()

data_14_raw = data_14_raw.split("\n")
data_14 = {}
for d in data_14_raw:
	line = d.split(", ")
	try:
		data_14[line[0]] = line[1]
	except:
		pass

# ball 1
with open(fname_b1, "r") as f:
	data_15_raw = f.read()

data_15_raw = data_15_raw.split("\n")
data_15 = {}
for d in data_15_raw:
	line = d.split(", ")
	try:
		data_15[line[0]] = line[1]
	except:
		pass

# ball 2
with open(fname_b2, "r") as f:
	data_16_raw = f.read()

data_16_raw = data_16_raw.split("\n")
data_16 = {}
for d in data_16_raw:
	line = d.split(", ")
	try:
		data_16[line[0]] = line[1]
	except:
		pass

# ball 3
with open(fname_b3, "r") as f:
	data_17_raw = f.read()

data_17_raw = data_17_raw.split("\n")
data_17 = {}
for d in data_17_raw:
	line = d.split(", ")
	try:
		data_17[line[0]] = line[1]
	except:
		pass

# strike 0
with open(fname_s0, "r") as f:
	data_18_raw = f.read()

data_18_raw = data_18_raw.split("\n")
data_18 = {}
for d in data_18_raw:
	line = d.split(", ")
	try:
		data_18[line[0]] = line[1]
	except:
		pass

# strike 1
with open(fname_s1, "r") as f:
	data_19_raw = f.read()

data_19_raw = data_19_raw.split("\n")
data_19 = {}
for d in data_19_raw:
	line = d.split(", ")
	try:
		data_19[line[0]] = line[1]
	except:
		pass

# strike 2
with open(fname_s2, "r") as f:
	data_20_raw = f.read()

data_20_raw = data_20_raw.split("\n")
data_20 = {}
for d in data_20_raw:
	line = d.split(", ")
	try:
		data_20[line[0]] = line[1]
	except:
		pass

# gameset
#with open(fname_gameset, "r") as f:
#	data_21_raw = f.read()
#
#data_21_raw = data_21_raw.split("\n")
#data_21 = {}
#for d in data_21_raw:
#	line = d.split(", ")
#	try:
#		data_21[line[0]] = line[1]
#	except:
#		pass

# tokuten in homerun and gameset
with open(fname_tokuten_in_homerun_and_gameset, "r") as f:
	data_22_raw = f.read()

data_22_raw = data_22_raw.split("\n")
data_22 = {}
for d in data_22_raw:
	line = d.split(", ")
	try:
		data_22[line[0]] = line[1]
	except:
		pass

# score ocr first
with open(fname_score_ocr_first, "r") as f:
	data_23_raw = f.read()

data_23_raw = data_23_raw.split("\n")
data_23 = {}
for d in data_23_raw:
	line = d.split(", ")
	try:
		data_23[line[0]] = line[1]
	except:
		pass

# score ocr last
with open(fname_score_ocr_last, "r") as f:
	data_24_raw = f.read()

data_24_raw = data_24_raw.split("\n")
data_24 = {}
for d in data_24_raw:
	line = d.split(", ")
	try:
		data_24[line[0]] = line[1]
	except:
		pass

# tokuten ocr first
with open(fname_tokuten_ocr_first, "r") as f:
	data_25_raw = f.read()

data_25_raw = data_25_raw.split("\n")
data_25 = {}
for d in data_25_raw:
	line = d.split(", ")
	try:
		data_25[line[0]] = line[1]
	except:
		pass

# tokuten ocr last
with open(fname_tokuten_ocr_last, "r") as f:
	data_26_raw = f.read()

data_26_raw = data_26_raw.split("\n")
data_26 = {}
for d in data_26_raw:
	line = d.split(", ")
	try:
		data_26[line[0]] = line[1]
	except:
		pass

# 正解データと比較し、正答率、再現率、適合率を算出
# 正解数、誤検出ポイントも表示
r0_tp = r0_fn = r0_fp = r0_tn = 0
r0_fp_list = []
r0_true = 0
r1_tp = r1_fn = r1_fp = r1_tn = 0
r1_fp_list = []
r1_true = 0
r2_tp = r2_fn = r2_fp = r2_tn = 0
r2_fp_list = []
r2_true = 0
r3_tp = r3_fn = r3_fp = r3_tn = 0
r3_fp_list = []
r3_true = 0
r12_tp = r12_fn = r12_fp = r12_tn = 0
r12_fp_list = []
r12_true = 0
r13_tp = r13_fn = r13_fp = r13_tn = 0
r13_fp_list = []
r13_true = 0
r23_tp = r23_fn = r23_fp = r23_tn = 0
r23_fp_list = []
r23_true = 0
r123_tp = r123_fn = r123_fp = r123_tn = 0
r123_fp_list = []
r123_true = 0
o0_tp = o0_fn = o0_fp = o0_tn = 0
o0_fp_list = []
o0_true = 0
o1_tp = o1_fn = o1_fp = o1_tn = 0
o1_fp_list = []
o1_true = 0
o2_tp = o2_fn = o2_fp = o2_tn = 0
o2_fp_list = []
o2_true = 0
tokuten_tp = tokuten_fn = tokuten_fp = tokuten_tn = 0
tokuten_fp_list = []
tokuten_true = 0
homerun_tp = homerun_fn = homerun_fp = homerun_tn = 0
homerun_fp_list = []
homerun_true = 0
b0_tp = b0_fn = b0_fp = b0_tn = 0
b0_fp_list = []
b0_true = 0
b1_tp = b1_fn = b1_fp = b1_tn = 0
b1_fp_list = []
b1_true = 0
b2_tp = b2_fn = b2_fp = b2_tn = 0
b2_fp_list = []
b2_true = 0
b3_tp = b3_fn = b3_fp = b3_tn = 0
b3_fp_list = []
b3_true = 0
s0_tp = s0_fn = s0_fp = s0_tn = 0
s0_fp_list = []
s0_true = 0
s1_tp = s1_fn = s1_fp = s1_tn = 0
s1_fp_list = []
s1_true = 0
s2_tp = s2_fn = s2_fp = s2_tn = 0
s2_fp_list = []
s2_true = 0
gameset_tp = gameset_fn = gameset_fp = gameset_tn = 0
gameset_fp_list = []
gameset_true = 0
tokuten_in_homerun_and_gameset_tp = 0
tokuten_in_homerun_and_gameset_fn = 0
tokuten_in_homerun_and_gameset_fp = 0
tokuten_in_homerun_and_gameset_tn = 0
tokuten_in_homerun_and_gameset_fp_list = []
tokuten_in_homerun_and_gameset_true = 0
score_ocr_first_true_match = 0
score_ocr_first_unmatch = 0
score_ocr_first_undetect = 0
score_ocr_first_false_match = 0
score_ocr_first_misdetect = 0
score_ocr_first_true = 0
score_ocr_first_false = 0
score_ocr_last_true_match = 0
score_ocr_last_unmatch = 0
score_ocr_last_undetect = 0
score_ocr_last_false_match = 0
score_ocr_last_misdetect = 0
score_ocr_last_true = 0
score_ocr_last_false = 0
tokuten_ocr_first_true_match = 0
tokuten_ocr_first_unmatch = 0
tokuten_ocr_first_undetect = 0
tokuten_ocr_first_false_match = 0
tokuten_ocr_first_misdetect = 0
tokuten_ocr_first_true = 0
tokuten_ocr_first_false = 0
tokuten_ocr_last_true_match = 0
tokuten_ocr_last_unmatch = 0
tokuten_ocr_last_undetect = 0
tokuten_ocr_last_false_match = 0
tokuten_ocr_last_misdetect = 0
tokuten_ocr_last_true = 0
tokuten_ocr_last_false = 0

for d in data:
	time = d[0]
	r0 = d[1]
	r1 = d[2]
	r2 = d[3]
	r3 = d[4]
	r12 = d[5]
	r13 = d[6]
	r23 = d[7]
	r123 = d[8]
	o0 = d[9]
	o1 = d[10]
	o2 = d[11]
	tokuten = d[12]
	homerun = d[13]
	b0 = d[14]
	b1 = d[15]
	b2 = d[16]
	b3 = d[17]
	s0 = d[18]
	s1 = d[19]
	s2 = d[20]
	#gameset = d[21]
	tokuten_in_homerun_and_gameset = d[22]
	score_ocr_first = d[23]
	score_ocr_last = d[24]
	tokuten_ocr_first = d[25]
	tokuten_ocr_last = d[26]

	# TP, FN, FP, TNを計算
	if r0 == "1":
		r0_true += 1
		if time in data_1:
			r0_tp += 1
		else:
			r0_fn += 1
	else:
		if time in data_1:
			r0_fp += 1
			r0_fp_list.append((time,data_1[time]))
		else:
			r0_tn += 1

	if r1 == "1":
		r1_true += 1
		if time in data_2:
			r1_tp += 1
		else:
			r1_fn += 1
	else:
		if time in data_2:
			r1_fp += 1
			r1_fp_list.append((time,data_2[time]))
		else:
			r1_tn += 1

	if r2 == "1":
		r2_true += 1
		if time in data_3:
			r2_tp += 1
		else:
			r2_fn += 1
	else:
		if time in data_3:
			r2_fp += 1
			r2_fp_list.append((time,data_3[time]))
		else:
			r2_tn += 1

	if r3 == "1":
		r3_true += 1
		if time in data_4:
			r3_tp += 1
		else:
			r3_fn += 1
	else:
		if time in data_4:
			r3_fp += 1
			r3_fp_list.append((time,data_4[time]))
		else:
			r3_tn += 1

	if r12 == "1":
		r12_true += 1
		if time in data_5:
			r12_tp += 1
		else:
			r12_fn += 1
	else:
		if time in data_5:
			r12_fp += 1
			r12_fp_list.append((time,data_5[time]))
		else:
			r12_tn += 1

	if r13 == "1":
		r13_true += 1
		if time in data_6:
			r13_tp += 1
		else:
			r13_fn += 1
	else:
		if time in data_6:
			r13_fp += 1
			r13_fp_list.append((time,data_6[time]))
		else:
			r13_tn += 1

	if r23 == "1":
		r23_true += 1
		if time in data_7:
			r23_tp += 1
		else:
			r23_fn += 1
	else:
		if time in data_7:
			r23_fp += 1
			r23_fp_list.append((time,data_7[time]))
		else:
			r23_tn += 1

	if r123 == "1":
		r123_true += 1
		if time in data_8:
			r123_tp += 1
		else:
			r123_fn += 1
	else:
		if time in data_8:
			r123_fp += 1
			r123_fp_list.append((time, data_8[time]))
		else:
			r123_tn += 1

	if o0 == "1":
		o0_true += 1
		if time in data_9:
			o0_tp += 1
		else:
			o0_fn += 1
	else:
		if time in data_9:
			o0_fp += 1
			o0_fp_list.append((time,data_9[time]))
		else:
			o0_tn += 1

	if o1 == "1":
		o1_true += 1
		if time in data_10:
			o1_tp += 1
		else:
			o1_fn += 1
	else:
		if time in data_10:
			o1_fp += 1
			o1_fp_list.append((time,data_10[time]))
		else:
			o1_tn += 1

	if o2 == "1":
		o2_true += 1
		if time in data_11:
			o2_tp += 1
		else:
			o2_fn += 1
	else:
		if time in data_11:
			o2_fp += 1
			o2_fp_list.append((time,data_11[time]))
		else:
			o2_tn += 1

	if tokuten == "1":
		tokuten_true += 1
		if time in data_12:
			tokuten_tp += 1
		else:
			tokuten_fn += 1
	else:
		if time in data_12:
			tokuten_fp += 1
			tokuten_fp_list.append((time, data_12[time]))
		else:
			tokuten_tn += 1

	if homerun == "1":
		homerun_true += 1
		if time in data_13:
			homerun_tp += 1
		else:
			homerun_fn += 1
	else:
		if time in data_13:
			homerun_fp += 1
			homerun_fp_list.append((time, data_13[time]))
		else:
			homerun_tn += 1

	if b0 == "1":
		b0_true += 1
		if time in data_14:
			b0_tp += 1
		else:
			b0_fn += 1
	else:
		if time in data_14:
			b0_fp += 1
			b0_fp_list.append((time, data_14[time]))
		else:
			b0_tn += 1

	if b1 == "1":
		b1_true += 1
		if time in data_15:
			b1_tp += 1
		else:
			b1_fn += 1
	else:
		if time in data_15:
			b1_fp += 1
			b1_fp_list.append((time, data_15[time]))
		else:
			b1_tn += 1

	if b2 == "1":
		b2_true += 1
		if time in data_16:
			b2_tp += 1
		else:
			b2_fn += 1
	else:
		if time in data_16:
			b2_fp += 1
			b2_fp_list.append((time, data_16[time]))
		else:
			b2_tn += 1

	if b3 == "1":
		b3_true += 1
		if time in data_17:
			b3_tp += 1
		else:
			b3_fn += 1
	else:
		if time in data_17:
			b3_fp += 1
			b3_fp_list.append((time, data_17[time]))
		else:
			b3_tn += 1

	if s0 == "1":
		s0_true += 1
		if time in data_18:
			s0_tp += 1
		else:
			s0_fn += 1
	else:
		if time in data_18:
			s0_fp += 1
			s0_fp_list.append((time, data_18[time]))
		else:
			s0_tn += 1

	if s1 == "1":
		s1_true += 1
		if time in data_19:
			s1_tp += 1
		else:
			s1_fn += 1
	else:
		if time in data_19:
			s1_fp += 1
			s1_fp_list.append((time, data_19[time]))
		else:
			s1_tn += 1

	if s2 == "1":
		s2_true += 1
		if time in data_20:
			s2_tp += 1
		else:
			s2_fn += 1
	else:
		if time in data_20:
			s2_fp += 1
			s2_fp_list.append((time, data_20[time]))
		else:
			s2_tn += 1

	#if gameset == "1":
	#	gameset_true += 1
	#	if time in data_21:
	#		gameset_tp += 1
	#	else:
	#		gameset_fn += 1
	#else:
	#	if time in data_21:
	#		gameset_fp += 1
	#		gameset_fp_list.append((time, data_21[time]))
	#	else:
	#		gameset_tn += 1

	if tokuten_in_homerun_and_gameset == "1":
		tokuten_in_homerun_and_gameset_true += 1
		if time in data_22:
			tokuten_in_homerun_and_gameset_tp += 1
		else:
			tokuten_in_homerun_and_gameset_fn += 1
	else:
		if time in data_22:
			tokuten_in_homerun_and_gameset_fp += 1
			tokuten_in_homerun_and_gameset_fp_list.append((time, data_22[time]))
		else:
			tokuten_in_homerun_and_gameset_tn += 1

	if score_ocr_first != "False":
		score_ocr_first_true += 1
		if time in data_23:
			if score_ocr_first == data_23[time]:
				score_ocr_first_true_match += 1
			else:
				score_ocr_first_unmatch += 1
		else:
			score_ocr_first_undetect += 1
	else:
		score_ocr_first_false += 1
		if time in data_23:
			score_ocr_first_misdetect += 1
		else:
			score_ocr_first_false_match += 1

	if score_ocr_last != "False":
		score_ocr_last_true += 1
		if time in data_24:
			if score_ocr_last == data_24[time]:
				score_ocr_last_true_match += 1
			else:
				score_ocr_last_unmatch += 1
		else:
			score_ocr_last_undetect += 1
	else:
		score_ocr_last_false += 1
		if time in data_24:
			score_ocr_last_misdetect += 1
		else:
			score_ocr_last_false_match += 1

	if tokuten_ocr_first != "False":
		tokuten_ocr_first_true += 1
		if time in data_25:
			if tokuten_ocr_first == data_25[time]:
				tokuten_ocr_first_true_match += 1
			else:
				tokuten_ocr_first_unmatch += 1
		else:
			tokuten_ocr_first_undetect += 1
	else:
		tokuten_ocr_first_false += 1
		if time in data_25:
			tokuten_ocr_first_misdetect += 1
		else:
			tokuten_ocr_first_false_match += 1

	if tokuten_ocr_last != "False":
		tokuten_ocr_last_true += 1
		if time in data_26:
			if tokuten_ocr_last == data_26[time]:
				tokuten_ocr_last_true_match += 1
			else:
				tokuten_ocr_last_unmatch += 1
		else:
			tokuten_ocr_last_undetect += 1
	else:
		tokuten_ocr_last_false += 1
		if time in data_26:
			tokuten_ocr_last_misdetect += 1
		else:
			tokuten_ocr_last_false_match += 1

# 計算結果の表示
print("r0 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r0_true,
	(r0_tp+r0_tn)/(r0_tp+r0_fn+r0_fp+r0_tn),
	r0_tp/((r0_tp+r0_fn) or 1),
	r0_tp/((r0_tp+r0_fp) or 1)
	))
print(r0_fp_list)

print("r1 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r1_true,
	(r1_tp+r1_tn)/(r1_tp+r1_fn+r1_fp+r1_tn),
	r1_tp/((r1_tp+r1_fn) or 1),
	r1_tp/((r1_tp+r1_fp) or 1)
	))
print(r1_fp_list)

print("r2 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r2_true,
	(r2_tp+r2_tn)/(r2_tp+r2_fn+r2_fp+r2_tn),
	r2_tp/((r2_tp+r2_fn) or 1),
	r2_tp/((r2_tp+r2_fp) or 1)
	))
print(r2_fp_list)

print("r3 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r3_true,
	(r3_tp+r3_tn)/(r3_tp+r3_fn+r3_fp+r3_tn),
	r3_tp/((r3_tp+r3_fn) or 1),
	r3_tp/((r3_tp+r3_fp) or 1)
	))
print(r3_fp_list)

print("r12 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r12_true,
	(r12_tp+r12_tn)/(r12_tp+r12_fn+r12_fp+r12_tn),
	r12_tp/((r12_tp+r12_fn) or 1),
	r12_tp/((r12_tp+r12_fp) or 1)
	))
print(r12_fp_list)

print("r13 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r13_true,
	(r13_tp+r13_tn)/(r13_tp+r13_fn+r13_fp+r13_tn),
	r13_tp/((r13_tp+r13_fn) or 1),
	r13_tp/((r13_tp+r13_fp) or 1)
	))
print(r13_fp_list)

print("r23 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r23_true,
	(r23_tp+r23_tn)/(r23_tp+r23_fn+r23_fp+r23_tn),
	r23_tp/((r23_tp+r23_fn) or 1),
	r23_tp/((r23_tp+r23_fp) or 1)
	))
print(r23_fp_list)

print("r123 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	r123_true,
	(r123_tp+r123_tn)/(r123_tp+r123_fn+r123_fp+r123_tn),
	r123_tp/((r123_tp+r123_fn) or 1),
	r123_tp/((r123_tp+r123_fp) or 1)
	))
print(r123_fp_list)

print("o0 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	o0_true,
	(o0_tp+o0_tn)/(o0_tp+o0_fn+o0_fp+o0_tn),
	o0_tp/((o0_tp+o0_fn) or 1),
	o0_tp/((o0_tp+o0_fp) or 1)
	))
print(o0_fp_list)

print("o1 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	o1_true,
	(o1_tp+o1_tn)/(o1_tp+o1_fn+o1_fp+o1_tn),
	o1_tp/((o1_tp+o1_fn) or 1),
	o1_tp/((o1_tp+o1_fp) or 1)
	))
print(r123_fp_list)

print("o2 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	o2_true,
	(o2_tp+o2_tn)/(o2_tp+o2_fn+o2_fp+o2_tn),
	o2_tp/((o2_tp+o2_fn) or 1),
	o2_tp/((o2_tp+o2_fp) or 1)
	))
print(o2_fp_list)

print("tokuten 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	tokuten_true,
	(tokuten_tp+tokuten_tn)/(tokuten_tp+tokuten_fn+tokuten_fp+tokuten_tn),
	tokuten_tp/((tokuten_tp+tokuten_fn) or 1),
	tokuten_tp/((tokuten_tp+tokuten_fp) or 1)
	))
print(tokuten_fp_list)

print("homerun 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	homerun_true,
	(homerun_tp+homerun_tn)/(homerun_tp+homerun_fn+homerun_fp+homerun_tn),
	homerun_tp/((homerun_tp+homerun_fn) or 1),
	homerun_tp/((homerun_tp+homerun_fp) or 1)
	))
print(homerun_fp_list)

print("b0 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	b0_true,
	(b0_tp+b0_tn)/(b0_tp+b0_fn+b0_fp+b0_tn),
	b0_tp/((b0_tp+b0_fn) or 1),
	b0_tp/((b0_tp+b0_fp) or 1)
	))
print(b0_fp_list)

print("b1 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	b1_true,
	(b1_tp+b1_tn)/(b1_tp+b1_fn+b1_fp+b1_tn),
	b1_tp/((b1_tp+b1_fn) or 1),
	b1_tp/((b1_tp+b1_fp) or 1)
	))
print(b1_fp_list)

print("b2 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	b2_true,
	(b2_tp+b2_tn)/(b2_tp+b2_fn+b2_fp+b2_tn),
	b2_tp/((b2_tp+b2_fn) or 1),
	b2_tp/((b2_tp+b2_fp) or 1)
	))
print(b2_fp_list)

print("b3 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	b3_true,
	(b3_tp+b3_tn)/(b3_tp+b3_fn+b3_fp+b3_tn),
	b3_tp/((b3_tp+b3_fn) or 1),
	b3_tp/((b3_tp+b3_fp) or 1)
	))
print(b3_fp_list)

print("s0 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	s0_true,
	(s0_tp+s0_tn)/(s0_tp+s0_fn+s0_fp+s0_tn),
	s0_tp/((s0_tp+s0_fn) or 1),
	s0_tp/((s0_tp+s0_fp) or 1)
	))
print(s0_fp_list)

print("s1 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	s1_true,
	(s1_tp+s1_tn)/(s1_tp+s1_fn+s1_fp+s1_tn),
	s1_tp/((s1_tp+s1_fn) or 1),
	s1_tp/((s1_tp+s1_fp) or 1)
	))
print(s1_fp_list)

print("s2 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	s2_true,
	(s2_tp+s2_tn)/(s2_tp+s2_fn+s2_fp+s2_tn),
	s2_tp/((s2_tp+s2_fn) or 1),
	s2_tp/((s2_tp+s2_fp) or 1)
	))
print(s2_fp_list)

#print("gameset 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
#	gameset_true,
#	(gameset_tp+gameset_tn)/(gameset_tp+gameset_fn+gameset_fp+gameset_tn),
#	gameset_tp/((gameset_tp+gameset_fn) or 1),
#	gameset_tp/((gameset_tp+gameset_fp) or 1)
#	))
#print(gameset_fp_list)

print("tokuten_in_homerun_and_gameset 正解数：{} 正答率：{} 再現率：{} 適合率：{}".format(
	tokuten_in_homerun_and_gameset_true,
	(tokuten_in_homerun_and_gameset_tp+tokuten_in_homerun_and_gameset_tn)/(tokuten_in_homerun_and_gameset_tp+tokuten_in_homerun_and_gameset_fn+tokuten_in_homerun_and_gameset_fp+tokuten_in_homerun_and_gameset_tn),
	tokuten_in_homerun_and_gameset_tp/((tokuten_in_homerun_and_gameset_tp+tokuten_in_homerun_and_gameset_fn) or 1),
	tokuten_in_homerun_and_gameset_tp/((tokuten_in_homerun_and_gameset_tp+tokuten_in_homerun_and_gameset_fp) or 1)
	))
print(tokuten_in_homerun_and_gameset_fp_list)

print("score_ocr_first 正解数：{} 正答率：{} 認識精度：{} 誤認識率：{} 未検出率：{} 誤検出率：{}".format(
	score_ocr_first_true,
	(score_ocr_first_true_match+score_ocr_first_false_match)/(score_ocr_first_true+score_ocr_first_false),
	score_ocr_first_true_match/(score_ocr_first_true or 1),
	score_ocr_first_unmatch/(score_ocr_first_true or 1),
	score_ocr_first_undetect/(score_ocr_first_true or 1),
	score_ocr_first_misdetect/(score_ocr_first_false or 1)
	))

print("score_ocr_last 正解数：{} 正答率：{} 認識精度：{} 誤認識率：{} 未検出率：{} 誤検出率：{}".format(
	score_ocr_last_true,
	(score_ocr_last_true_match+score_ocr_last_false_match)/(score_ocr_last_true+score_ocr_last_false),
	score_ocr_last_true_match/(score_ocr_last_true or 1),
	score_ocr_last_unmatch/(score_ocr_last_true or 1),
	score_ocr_last_undetect/(score_ocr_last_true or 1),
	score_ocr_last_misdetect/(score_ocr_last_false or 1)
	))

print("tokuten_ocr_first 正解数：{} 正答率：{} 認識精度：{} 誤認識率：{} 未検出率：{} 誤検出率：{}".format(
	tokuten_ocr_first_true,
	(tokuten_ocr_first_true_match+tokuten_ocr_first_false_match)/(tokuten_ocr_first_true+tokuten_ocr_first_false),
	tokuten_ocr_first_true_match/(tokuten_ocr_first_true or 1),
	tokuten_ocr_first_unmatch/(tokuten_ocr_first_true or 1),
	tokuten_ocr_first_undetect/(tokuten_ocr_first_true or 1),
	tokuten_ocr_first_misdetect/(tokuten_ocr_first_false or 1)
	))

print("tokuten_ocr_last 正解数：{} 正答率：{} 認識精度：{} 誤認識率：{} 未検出率：{} 誤検出率：{}".format(
	tokuten_ocr_last_true,
	(tokuten_ocr_last_true_match+tokuten_ocr_last_false_match)/(tokuten_ocr_last_true+tokuten_ocr_last_false),
	tokuten_ocr_last_true_match/(tokuten_ocr_last_true or 1),
	tokuten_ocr_last_unmatch/(tokuten_ocr_last_true or 1),
	tokuten_ocr_last_undetect/(tokuten_ocr_last_true or 1),
	tokuten_ocr_last_misdetect/(tokuten_ocr_last_false or 1)
	))
