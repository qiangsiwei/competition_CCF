# encoding: utf-8

import fileinput
import numpy as np

classified_event = {}
for line in fileinput.input("../data/events/classified_event.txt"):
	part = line.strip().split("|")
	event, tag = int(part[0]), int(part[1])
	classified_event[event] = {"tag":tag}
fileinput.close()

classified_news = {}
for line in fileinput.input("../data/events/classified_news.txt"):
	part = line.strip().split("\t")
	event, tag, day_offset, cid = int(part[0]), int(part[1]), int(part[2]), part[3]
	if not classified_news.has_key(event):
		classified_news[event] = []
	classified_news[event].append({"day_offset":day_offset, "cid":cid})
fileinput.close()

classified_weibo = {}
for line in fileinput.input("../data/events/classified_weibo.txt"):
	part = line.strip().split("\t")
	event, tag, day_offset, cid = int(part[0]), int(part[1]), int(part[2]), part[3]
	if not classified_weibo.has_key(event):
		classified_weibo[event] = []
	classified_weibo[event].append({"day_offset":day_offset, "cid":cid})
fileinput.close()

event_location = {}
for line in fileinput.input("../data/mysql/event_loc.txt"):
	part = line.strip().split("\t")
	event, area, province, city = int(part[0]), part[1][1:-1], part[2][1:-1], part[3][1:-1]
	event_location[event] = {"area":area, "province":province, "city":city}
fileinput.close()

# gdp_city = {}
# for line in fileinput.input("../data/mysql/gdp_city.txt"):
# 	part = line.strip().split("\t")
# 	ranking, city, gdp_2012, gdp_2013, gdp_inc, province = part[0][1:-1], part[1][1:-1], part[2][1:-1], part[3][1:-1], part[4][1:-1], part[5][1:-1]
# 	if not gdp_city.has_key(city):
# 		gdp_city[city] = {"ranking":ranking, "gdp_2012":gdp_2012, "gdp_2013":gdp_2013, "gdp_inc":gdp_inc, "province":province}
# fileinput.close()

gdp_province = {}
for line in fileinput.input("../data/mysql/gdp_province.txt"):
	part = line.strip().split("\t")
	ranking, province, gdp_2013 = part[0][1:-1], part[1][1:-1], part[2][1:-1]
	if not gdp_province.has_key(province):
		gdp_province[province] = {"ranking":ranking, "gdp_2013":gdp_2013}
fileinput.close()
for line in fileinput.input("../data/mysql/gdp_province_avg.txt"):
	part = line.strip().split("\t")
	avg_ranking, province, pnum_2013, avg_gdp_2013 = part[0][1:-1], part[1][1:-1], part[3][1:-1], part[4][1:-1]
	gdp_province[province].update({"avg_ranking":avg_ranking, "pnum_2013":pnum_2013, "avg_gdp_2013":avg_gdp_2013})
fileinput.close()
for line in fileinput.input("../data/mysql/ratio_province.txt"):
	part = line.strip().split("\t")
	province, hz_ratio = part[0][1:-1], part[1][1:-1]
	gdp_province[province].update({"hz_ratio":hz_ratio})
fileinput.close()

crc_map = {}
for line in fileinput.input("../data/mysql/t_lable_filtered_crc.txt"):
	part = line.strip().split("\t")
	cid, crc = part[0][1:-1], part[1]
	crc_map[cid] = crc 
fileinput.close()

sitecrc_map = {}
for line in fileinput.input("../data/mysql/t_lable_filtered_sitecrc.txt"):
	part = line.strip().split("\t")
	cid, sitecrc = part[0][1:-1], part[1]
	sitecrc_map[cid] = sitecrc 
fileinput.close()

media_map = {}
for line in fileinput.input("../data/mysql/t_lable_filtered_media.txt"):
	part = line.strip().split("\t")
	cid, media, word = part[0][1:-1], part[1][1:-1], int(part[2])
	media_map[cid] = {"media":media, "word":word}
fileinput.close()

t_dpt_distinct = {}
for line in fileinput.input("../data/mysql/t_dpt_distinct.txt"):
	part = line.strip().split("\t")
	url_crc, comment, quote, attitude = part[0], int(part[2]), int(part[3]), int(part[4])
	t_dpt_distinct[url_crc] = {"comment":comment, "quote":quote, "attitude":attitude}
fileinput.close()

w_user_info_distinct = {}
for line in fileinput.input("../data/mysql/w_user_info_distinct.txt"):
	part = line.strip().split("\t")
	try:
		url_crc, province = part[0], part[2]
		w_user_info_distinct[url_crc] = {"province":province}
	except:
		continue
fileinput.close()

sentiment_map = {}
for line in fileinput.input("../data/mysql/sentiment_news_ratio.txt"):
	part = line.strip().split("\t")
	cid, v1, v2, v3, v4, v5, v6 = part[0], int(part[1]), int(part[2]), int(part[3]), int(part[4]), int(part[5]), int(part[6])
	sentiment_map[cid] = {"value":[v1, v2, v3, v4, v5, v6]}
fileinput.close()
for line in fileinput.input("../data/mysql/sentiment_weibo_ratio.txt"):
	part = line.strip().split("\t")
	cid, v1, v2, v3, v4, v5, v6 = part[0], int(part[1]), int(part[2]), int(part[3]), int(part[4]), int(part[5]), int(part[6])
	sentiment_map[cid] = {"value":[v1, v2, v3, v4, v5, v6]}
fileinput.close()

with open("../data/events/event_attributes-results.txt","w")
	for k,v in classified_event.iteritems():
		tag = v["tag"]
		# feature extraction
		start_offset_news = np.array([item["day_offset"] for item in classified_news[k]]).min() if classified_news.has_key(k) else -1
		start_offset_weibo = np.array([item["day_offset"] for item in classified_weibo[k]]).min() if classified_weibo.has_key(k) else -1
		end_offset_news = np.array([item["day_offset"] for item in classified_news[k]]).max() if classified_news.has_key(k) else -1
		end_offset_weibo = np.array([item["day_offset"] for item in classified_weibo[k]]).max() if classified_weibo.has_key(k) else -1
		duration_news = end_offset_news-start_offset_news+1 if start_offset_news!=-1 and end_offset_news!=-1 else 0
		duration_weibo = end_offset_weibo-start_offset_weibo+1 if start_offset_weibo!=-1 and end_offset_weibo!=-1 else 0
		duration_news_25 = sorted(classified_news[k], key=lambda x:x["day_offset"])[int(len(classified_news[k])*0.25)]["day_offset"]-start_offset_news+1 if start_offset_news!=-1 else 0
		duration_news_50 = sorted(classified_news[k], key=lambda x:x["day_offset"])[int(len(classified_news[k])*0.50)]["day_offset"]-start_offset_news+1 if start_offset_news!=-1 else 0
		duration_news_75 = sorted(classified_news[k], key=lambda x:x["day_offset"])[int(len(classified_news[k])*0.75)]["day_offset"]-start_offset_news+1 if start_offset_news!=-1 else 0
		duration_weibo_25 = sorted(classified_weibo[k], key=lambda x:x["day_offset"])[int(len(classified_weibo[k])*0.25)]["day_offset"]-start_offset_weibo+1 if start_offset_weibo!=-1 else 0
		duration_weibo_50 = sorted(classified_weibo[k], key=lambda x:x["day_offset"])[int(len(classified_weibo[k])*0.50)]["day_offset"]-start_offset_weibo+1 if start_offset_weibo!=-1 else 0
		duration_weibo_75 = sorted(classified_weibo[k], key=lambda x:x["day_offset"])[int(len(classified_weibo[k])*0.75)]["day_offset"]-start_offset_weibo+1 if start_offset_weibo!=-1 else 0
		# print duration_news, duration_weibo, duration_news_25, duration_news_50, duration_news_75, duration_weibo_25, duration_weibo_50, duration_weibo_75
		happend_area = event_location[k]["area"] if event_location[k]["area"]!="" else "NULL"
		happend_province = event_location[k]["province"] if event_location[k]["area"]!="" else "NULL"
		happend_city = event_location[k]["city"] if event_location[k]["area"]!="" else "NULL"
		happend_province = happend_province.replace("省","").replace("市","").replace("自治区","")
		# print happend_area, happend_province, happend_city
		gdp = gdp_province[happend_province] if gdp_province.has_key(happend_province) else None
		gdp_ranking = gdp["ranking"] if gdp!=None else "NULL"
		gdp_2013 = gdp["gdp_2013"] if gdp!=None else "NULL"
		gdp_ranking_avg = gdp["avg_ranking"] if gdp!=None else "NULL"
		gdp_2013_avg = gdp["avg_gdp_2013"] if gdp!=None else "NULL"
		pnum_2013 = gdp["pnum_2013"] if gdp!=None else "NULL"
		hz_ratio = gdp["hz_ratio"] if gdp!=None else "NULL"
		# print gdp_ranking, gdp_2013, gdp_ranking_avg, gdp_2013_avg, pnum_2013, hz_ratio
		cnt_news = len(classified_news[k]) if classified_news.has_key(k) else 0
		cnt_weibo = len(classified_weibo[k]) if classified_weibo.has_key(k) else 0
		crc_news = [crc_map[item["cid"]] for item in classified_news[k]] if classified_news.has_key(k) else []
		crc_weibo = [crc_map[item["cid"]] for item in classified_weibo[k]] if classified_weibo.has_key(k) else []
		# print cnt_news, cnt_weibo
		t_dpt_distinct_news = [t_dpt_distinct[crc] if t_dpt_distinct.has_key(crc) else {"comment":0, "quote":0, "attitude":0} for crc in crc_news]
		t_dpt_distinct_weibo = [t_dpt_distinct[crc] if t_dpt_distinct.has_key(crc) else {"comment":0, "quote":0, "attitude":0} for crc in crc_weibo]
		comment_news = sum([item["comment"] for item in t_dpt_distinct_news])
		comment_weibo = sum([item["comment"] for item in t_dpt_distinct_weibo])
		quote_news = sum([item["quote"] for item in t_dpt_distinct_news])
		quote_weibo = sum([item["quote"] for item in t_dpt_distinct_weibo])
		attitude_news = sum([item["attitude"] for item in t_dpt_distinct_news])
		attitude_weibo = sum([item["attitude"] for item in t_dpt_distinct_weibo])
		# print comment_news, comment_weibo, quote_news, quote_weibo, attitude_news, attitude_weibo
		words_news = [media_map[item["cid"]]["word"] for item in classified_news[k]] if classified_news.has_key(k) else []
		words_weibo = [media_map[item["cid"]]["word"] for item in classified_weibo[k]] if classified_weibo.has_key(k) else []
		words_news_mean, words_news_med = sum(words_news)/len(words_news) if len(words_news)!=0 else 0, words_news[len(words_news)/2] if len(words_news)!=0 else 0
		words_weibo_mean, words_weibo_med = sum(words_weibo)/len(words_weibo) if len(words_weibo)!=0 else 0, words_weibo[len(words_weibo)/2] if len(words_weibo)!=0 else 0
		# print words_news_mean, words_news_med, words_weibo_mean, words_weibo_med
		media_news = [media_map[item["cid"]]["media"] for item in classified_news[k]] if classified_news.has_key(k) else []
		media_cnt_news = len(set(media_news))
		# print media_cnt_news
		person_weibo = [sitecrc_map[item["cid"]] for item in classified_weibo[k]] if classified_weibo.has_key(k) else []
		person_cnt_weibo = len(set(person_weibo))
		# print person_weibo
		location_weibo = [w_user_info_distinct[sitecrc_map[item["cid"]]]["province"] if w_user_info_distinct.has_key(sitecrc_map[item["cid"]]) else "NULL" for item in classified_weibo[k]] if classified_weibo.has_key(k) else []
		location_cnt_weibo = len(set(location_weibo))
		# print location_cnt_weibo
		sentiment_news = [sentiment_map[item["cid"]] for item in classified_news[k]] if classified_news.has_key(k) else []
		sentiment_weibo = [sentiment_map[item["cid"]] for item in classified_weibo[k]] if classified_weibo.has_key(k) else []
		sentiment_news = [sum([sentiment_news[x]["value"][i] for x in xrange(len(sentiment_news))])/len(sentiment_news) for i in xrange(6)] if len(sentiment_news)!=0 else [0]*6
		sentiment_weibo = [sum([sentiment_weibo[x]["value"][i] for x in xrange(len(sentiment_weibo))])/len(sentiment_weibo) for i in xrange(6)] if len(sentiment_weibo)!=0 else [0]*6
		# print sentiment_news, sentiment_weibo
		f.write(str(k)+"\t"+str(tag)+"\t")
		f.write(str(start_offset_news)+"\t"+str(start_offset_weibo)+"\t"+str(end_offset_news)+"\t"+str(end_offset_weibo)+"\t"+str(duration_news)+"\t"+str(duration_weibo)+"\t"+str(duration_news_25)+"\t"+str(duration_news_50)+"\t"+str(duration_news_75)+"\t"+str(duration_weibo_25)+"\t"+str(duration_weibo_50)+"\t"+str(duration_weibo_75)+"\t")
		f.write(str(happend_area)+"\t"+str(happend_province)+"\t"+str(happend_city)+"\t")
		f.write(str(gdp_ranking)+"\t"+str(gdp_2013)+"\t"+str(gdp_ranking_avg)+"\t"+str(gdp_2013_avg)+"\t"+str(pnum_2013)+"\t"+str(hz_ratio)+"\t")
		f.write(str(cnt_news)+"\t"+str(cnt_weibo)+"\t"+str(comment_news)+"\t"+str(comment_weibo)+"\t"+str(quote_news)+"\t"+str(quote_weibo)+"\t"+str(attitude_news)+"\t"+str(attitude_weibo)+"\t"+str(words_news_mean)+"\t"+str(words_news_med)+"\t"+str(words_weibo_mean)+"\t"+str(words_weibo_med)+"\t")
		f.write(str(media_cnt_news)+"\t"+str(person_cnt_weibo)+"\t"+str(location_cnt_weibo)+"\t"+"\t".join([str(s) for s in sentiment_news])+"\t"+"\t".join([str(s) for s in sentiment_weibo])+"\n")

######## 格式说明 ########
# k
# tag
# start_offset_news
# start_offset_weibo
# end_offset_news
# end_offset_weibo
# duration_news
# duration_weibo
# duration_news_25
# duration_news_50
# duration_news_75
# duration_weibo_25
# duration_weibo_50
# duration_weibo_75
# happend_area
# happend_province
# happend_city
# gdp_ranking
# gdp_2013
# gdp_ranking_avg
# gdp_2013_avg
# pnum_2013
# hz_ratio
# cnt_news
# cnt_weibo
# comment_news
# comment_weibo
# quote_news
# quote_weibo
# attitude_news
# attitude_weibo
# words_news_mean
# words_news_med
# words_weibo_mean
# words_weibo_med
# media_cnt_news
# person_cnt_weibo
# location_cnt_weibo
# sentiment_news_v1
# sentiment_news_v2
# sentiment_news_v3
# sentiment_news_v4
# sentiment_news_v5
# sentiment_news_v6
# sentiment_weibo_v1
# sentiment_weibo_v2
# sentiment_weibo_v3
# sentiment_weibo_v4
# sentiment_weibo_v5
# sentiment_weibo_v6
