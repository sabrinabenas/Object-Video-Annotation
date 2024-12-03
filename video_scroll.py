import cv2
import numpy as np
import os, glob
import pandas as pd
#from pynput import keyboard
#from pynput.keyboard import Key

def video_scroll(vid, names, keys,frame_to_show):

	dic = {}
	for i in names:
		dic[i]=[]

	n_dic = {}
	
	for i,j in zip(names,keys):
		n_dic[i]=j
	top_label = str(n_dic)[1:-1]
	top_label=top_label.replace("'","")

	split = vid.split('.')
	#vid_name = os.path.basename(split[0])
	cap = cv2.VideoCapture(vid)
	#fps =  cap.get(cv2.CAP_PROP_FPS)
	length = len(frame_to_show) -1

	def onChange(trackbarValue):
		trackbarValue = frame_to_show[trackbarValue]
		cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
		err,img = cap.read()
		h,w,d = img.shape
		text = 'FN = ' + str(trackbarValue)
		if cnt == 1:  
			n_img = cv2.putText(img,  text + '  -  '+ name , (10, 20), cv2.FONT_HERSHEY_SIMPLEX , 0.5,(255, 255, 255), 1, cv2.LINE_AA, False)
			cv2.imshow(top_label, n_img)

		if cnt == 0:
			n_img = cv2.putText(img,text , (10, 20), cv2.FONT_HERSHEY_SIMPLEX , 0.5,(255, 255, 255), 1, cv2.LINE_AA, False)
			cv2.imshow(top_label, n_img)

		if reset == 1:
			n_img = cv2.putText(img, 'reset', (w-70, 20), cv2.FONT_HERSHEY_SIMPLEX , 0.3,  
	                 (255, 255, 255), 1, cv2.LINE_AA, False)
			cv2.imshow(top_label, n_img)

		if show == 1:
			dic_temp = {}
			temp = list(dic.values())
			for i,j in zip(range(len(temp)),dic.keys()):
				l = temp[i][-2:]
				l.append(str(len(temp[i])))
				dic_temp[j]=l
			n_img = cv2.putText(img, str(dic_temp), (10, 20), cv2.FONT_HERSHEY_SIMPLEX , 0.3,  
	                 (255, 255, 255), 1, cv2.LINE_AA, False)
			cv2.imshow(top_label, n_img)


	def getmax(data):
		m_list = []
		t = list(data.values())
		for i in t:
			if i != []:
				m_list.append(max(i))
			else:
				m_list.append(0)
		return m_list.index(max(m_list))

	global cnt
	global reset
	global l
	global name
	global show

	cnt = 0
	reset = 0
	show = 0
	compare = []
	cv2.namedWindow(top_label, cv2.WINDOW_NORMAL)
	cv2.createTrackbar( 'pos', top_label, 0 , length, onChange )
	onChange(0)
	while cap.isOpened():
		
		k = cv2.waitKey(0) #& 0xff
		#print(k)
		
		#obj
		for i in range(len(keys)):
			if k == ord(keys[i]):
				if compare == [] or keys[i] == compare[0]:
					compare.append(keys[i])
					pos = cv2.getTrackbarPos('pos',top_label)
					dic[list(dic)[i]].append(frame_to_show[pos])
					name = list(dic)[i]
					l = len(list(dic.values())[i])

					if l % 2 != 0:
						cnt = 1

					if l % 2 == 0:
						cnt = 0
						compare = []
					
					onChange(pos)

		#reset
		if k == 8: ##8 ubuntu
			reset = 1
			pos = cv2.getTrackbarPos('pos',top_label)
			onChange(pos)
			if compare != []:
					compare = compare[:-1]
			i = getmax(dic)
			del dic[names[i]][-1]
			
			if cnt == 1:
				cnt = 0
			else:
				cnt = 1

			reset = 0

		#show	
		if k == ord('p'):
			show = 1
			pos = cv2.getTrackbarPos('pos',top_label)
			onChange(pos)
			show = 0

		elif k == 27:
			for i in range(len(dic)):
				if len(dic[names[i]]) % 2 != 0:
					pos = cv2.getTrackbarPos('pos',top_label)
					dic[list(dic)[i]].append(frame_to_show[pos])
			return dic
			break
	
	if k == ord('q'):
		cap.release()
		cv2.destroyAllWindows()

