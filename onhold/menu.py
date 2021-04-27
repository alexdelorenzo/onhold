from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from os import listdir
from os.path import isfile, join
import numpy as np



def getFiles(dir):
	# Return all the files in the directory
	return np.array([f for f in listdir(dir) if isfile(join(dir, f))])

def formatFileArray(files):
	# Have to do this because numpy array doesn't allow objects
	fileList = []

	for file in files:
		fileList.append(file)
	
	for i in range(len(fileList)):
		fileList[i] = {'name': fileList[i]}

	return fileList


def menu(dir):
	style = style_from_dict({
	    Token.Separator: '#cc5454',
	    Token.QuestionMark: '#673ab7 bold',
	    Token.Selected: '#cc5454',  # default
	    Token.Pointer: '#673ab7 bold',
	    Token.Instruction: '',  # default
	    Token.Answer: '#f44336 bold',
	    Token.Question: '',
	})

	filesArray = formatFileArray(getFiles('../onhold'))

	# filter files array to only .ogg files


	separatorList = np.array([Separator('= Choose a Song: =')])

	choices = np.concatenate((separatorList, filesArray))

	questions = [
	    {
	        'type': 'checkbox',
	        'message': 'Select song',
	        'name': 'songs',
	        'choices': choices,
	        'validate': lambda answer: 'You must choose a song.' \
	            if len(answer) == 0 else True
	    }
	]

	answers = prompt(questions, style=style)
	return answers


