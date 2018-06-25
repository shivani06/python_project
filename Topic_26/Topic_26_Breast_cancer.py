from __future__ import print_function
from xml.dom import minidom
import os, shutil
import pygame
#python3 -m pip install -U pygame --user
#pip install opencv-python

try:
	from PIL import Image
except ImportError:
	import Image
import cv2
import matplotlib.pyplot as plt
import matplotlib.colors as plt_color
import numpy as np
import sys
import glob

search_list = []
search_item_array = []
file_name_array = []
file_name_array1 = []
file_score_array = []
file_score_array1 = []


Do_id_array = []
Journal_array = []
Doc_title_array = []
Doc_abstract_array = []
Doc_ChemicalList_array = []
Doc_meshdescriptors_array = []
Doc_meshqualifiers_array = []

Meeting_name_array = []
Doc_title1_array = []
Background_array = []

def get_array_order():
	for i in range(0,len(file_score_array)-1):
		temp_index = 0
		temp = 0
		for j in range(i+1,len(file_score_array)):
			if file_score_array[i] < file_score_array[j]:
				temp = file_score_array[i]
				file_score_array[i] = file_score_array[j]
				file_score_array[j] = temp

				temp = file_name_array[i]
				file_name_array[i] = file_name_array[j]
				file_name_array[j] = temp	

def get_score(element_length,word_count_array,word_weight_array):
	score_val = 0
	for i in range(0,len(word_weight_array)):
		score_val = score_val + int(word_count_array[i])*int(word_weight_array[i])/element_length
	return score_val

def get_file_word_length(index):

	element1_length = len(Do_id_array[index])
	element2_length = len(Journal_array[index])
	element3_length = len(Doc_title_array[index])
	element4_length = len(Doc_abstract_array[index])
	element5_length = len(Doc_ChemicalList_array[index])
	element6_length = len(Doc_meshdescriptors_array[index])
	element7_length = len(Doc_meshqualifiers_array[index])
	element_length = element1_length + element2_length +element3_length +element4_length+ element5_length+element6_length+element7_length
	return element_length

def get_file_word_length1(index):

	element1_length = len(Meeting_name_array[index])
	element2_length = len(Doc_title1_array[index])
	element3_length = len(Background_array[index])
	element_length = element1_length + element2_length +element3_length 
	return element_length

def load_files(path):

	i = 0
	for file_name in os.listdir(path):

		i = i + 1
		file_doc = minidom.parse(path + os.sep + file_name)	

		if file_name.rfind('A', 0, 1) == -1:

			Do_id = file_doc.getElementsByTagName('Do_id')
			Journal = file_doc.getElementsByTagName('Journal')
			Doc_title = file_doc.getElementsByTagName('Doc_title')
			Doc_abstract = file_doc.getElementsByTagName('Doc_abstract')
			Doc_ChemicalList = file_doc.getElementsByTagName('Doc_ChemicalList')
			Doc_meshdescriptors = file_doc.getElementsByTagName('Doc_meshdescriptors')
			Doc_meshqualifiers = file_doc.getElementsByTagName('Doc_meshqualifiers')

			Do_id_element_array = Do_id[0].firstChild.data.split()
			Journal_element_array = Journal[0].firstChild.data.split()
			Doc_title_element_array = Doc_title[0].firstChild.data.split()
			Doc_abstract_element_array = Doc_abstract[0].firstChild.data.split()
			Doc_ChemicalList_element_array = Doc_ChemicalList[0].firstChild.data.split()
			Doc_meshdescriptors_element_array = Doc_meshdescriptors[0].firstChild.data.split()
			Doc_meshqualifiers_element_array = Doc_meshqualifiers[0].firstChild.data.split()

			Do_id_array.append(Do_id_element_array)
			Journal_array.append(Journal_element_array)
			Doc_title_array.append(Doc_title_element_array)
			Doc_abstract_array.append(Doc_abstract_element_array)
			Doc_ChemicalList_array.append(Doc_ChemicalList_element_array)
			Doc_meshdescriptors_array.append(Doc_meshdescriptors_element_array)
			Doc_meshqualifiers_array.append(Doc_meshqualifiers_element_array)
			file_name_array.append(file_name)

		else:

			Meeting_name = file_doc.getElementsByTagName('Meeting_name')
			Doc_title1 = file_doc.getElementsByTagName('Doc_title')
			Background = file_doc.getElementsByTagName('Background')

			Meeting_name_element_array = Meeting_name[0].firstChild.data.split()
			Doc_title1_element_array = Doc_title1[0].firstChild.data.split()
			Background_element_array = Background[0].firstChild.data.split()

			Meeting_name_array.append(Meeting_name_element_array)
			Doc_title1_array.append(Doc_title1_element_array)
			Background_array.append(Background_element_array)
			file_name_array1.append(file_name)


def main():

	#print("Start-----")
	print("READ AND FOLLOW INSTRUCTIONS")
	print("Enter keywords with weightage")
	print("Press enter after each keyword")
	print("type quit at end")
	print("Example:")
	print("cancer-20 (press enter)")
	print("radiation-40 (press enter)")
	print("quit (press enter for execution)")
	print("END OF INSTRUCTIONS")
	print("Start typing keywords")
	

	while True:
		t=input()
		search_content = str(t)
		if search_content == "quit":
			break
		search_list.append(search_content)

	for i in range(0,len(search_list)):
		search_item = search_list[i].split('-')
		search_item_array.append(search_item)

	load_files('Breast_cancer')

	for i in range(0,len(Journal_array)):
		element_length = get_file_word_length(i)
		word_count_array = []
		word_weight_array = []
		for k in range(0,len(search_item_array)):

			word_count = 0
			for j in range(0,len(Journal_array[i])):
				if search_item_array[k][0] == Journal_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Doc_title_array[i])):
				if search_item_array[k][0] == Doc_title_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Doc_abstract_array[i])):
				if search_item_array[k][0] == Doc_abstract_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Doc_ChemicalList_array[i])):
				if search_item_array[k][0] == Doc_ChemicalList_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Doc_meshdescriptors_array[i])):
				if search_item_array[k][0] == Doc_meshdescriptors_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Doc_meshqualifiers_array[i])):
				if search_item_array[k][0] == Doc_meshqualifiers_array[i][j]:
					word_count = word_count + 1

			word_count_array.append(word_count)
			word_weight_array.append(search_item_array[k][1])
		file_score = get_score(element_length,word_count_array,word_weight_array)
		file_score_array.append(file_score)

	for i in range(0,len(Meeting_name_array)):
		element_length = get_file_word_length1(i)
		word_count_array = []
		word_weight_array = []
		for k in range(0,len(search_item_array)):

			word_count = 0
			for j in range(0,len(Meeting_name_array[i])):
				if search_item_array[k][0] == Meeting_name_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Doc_title1_array[i])):
				if search_item_array[k][0] == Doc_title1_array[i][j]:
					word_count = word_count + 1

			for j in range(0,len(Background_array[i])):
				if search_item_array[k][0] == Background_array[i][j]:
					word_count = word_count + 1

			word_count_array.append(word_count)
			word_weight_array.append(search_item_array[k][1])
		file_score = get_score(element_length,word_count_array,word_weight_array)
		file_score_array.append(file_score)
		file_name_array.append(file_name_array1[i])

	get_array_order()




	files = glob.glob('Topic_26_Relevant/*')
	for f in files:
		os.remove(f)

	files = glob.glob('Topic_26_Irrelevant/*')
	for f in files:
		os.remove(f)
	pre_score = 0
	orderNum = 0
	for i in range(0,len(file_score_array)):
		src = "Breast_cancer/" + file_name_array[i]
		if file_score_array[i] > 0:
			dst = "Topic_26_Relevant/" + file_name_array[i]
			shutil.copyfile(src,dst)
		else:
			dst = "Topic_26_Irrelevant/" + file_name_array[i]
			shutil.copyfile(src,dst)
		temp_score = str(file_score_array[i]/100)[0:5]
		cur_score = float(temp_score)
		
		if pre_score != cur_score:
			pre_score = cur_score
			orderNum = orderNum + 1
		print("1 Q0  "+file_name_array[i].rstrip(".xml")+"  "+str(orderNum)+"  "+str(cur_score)[0:5]+" Groupe_8"+"\r\n")

	print("files are seperated successfully!")

	f= open("test.txt","w+")	
	for i in range(len(file_score_array)):
		f.write("1 Q0  "+file_name_array[i].rstrip(".xml")+"  "+str(orderNum)+"  "+str(cur_score)[0:5]+" Groupe_8"+"\r\n")
	f.close() 
	print("file is created successfully")
	
if __name__ == '__main__':
	main()