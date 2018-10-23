#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import os
import time
import sys
import platform

def get_path():
	currentpath=os.path.abspath('.')
	return currentpath

def get_input(currentpath,inputfilename):
	testCasePath = currentpath+"/test/input/"+inputfilename
	if(os.path.exists(testCasePath) ):
		with open(testCasePath,'r') as inputf:
			testCase = inputf.read().strip()
			return testCase
	else:
		return "error:this file:"+testCasePath+" does not exist."

def get_expect(currentpath,expectfilename):
	expectFilePath = currentpath+"/test/expect/"+expectfilename
	if(os.path.exists(expectFilePath) ):
		with open(expectFilePath,'rb') as expect:
			expectCase = expect.read().strip().replace("\n\n","\r\n")
			return expectCase
	else:
		return "error:this file:"+expectFilePath+" does not exist."

def get_compile(currentpath):
	FilePath = currentpath+"/test/compile.txt"
	if(os.path.exists(FilePath) ):
		with open(FilePath,'r') as File:
			compileName = File.read().strip()
			return compileName
	else:
		return "error:this file:"+FilePath+" does not exist."


def get_command(currentpath):
	FilePath = currentpath+"/test/command.txt"
	if(os.path.exists(FilePath) ):
		with open(FilePath,'r') as File:
			commandName = File.read().strip()
			return commandName
	else:
		return "error:this file:"+FilePath+" does not exist."

def Compared(expectCase,outputCase):
	if(expectCase==outputCase):
		print("success:")
		return 0
	else:
		print ("error:The input result is different from the expected result.")
		return 1

def FileOutput(outputCase,currentpath,outputfilename):
    outputFilePath = currentpath+"/test/output/"+outputfilename
    with open(outputFilePath,'w+') as File:
    	File.write(outputCase)

def compileFile(inputCase,currentpath,compileName,commandName,timeout):
	# 两个待传入的参数：filepath、timeout、input
	filePath = currentpath+"/"+compileName
	#timeout = "5"
	# filePath="${filePath}"
	# timeout = "${timeout}"
	#
	deadline = time.time() + float(timeout)
	#
	
	# print(index)
	execPath = currentpath+"/"+commandName
	index = execPath.index(".")
	execPath = execPath[0:index]
	# print(execPath)
	# 拼接需在命令行执行的命令
	command = "g++ " + filePath + " -o " + execPath
	# 当shell=True时，表示在系统默认的shell环境中执行新的进程，此shell在windows表示为cmd.exe，在linux为/bin/sh。
	# 如果stdout设置为PIPE，此时stdout其实是个file对象，用来保存新创建的子进程的输出；如果stderr设置为PIPE，此时的stderr其实是个file对象，用来保存新创建的子进程的错误输出。
	# .communicate()输入标准输入，输出标准输出和标准出错
	chlid = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	res = chlid.communicate()
	out = str(res[0], encoding="gbk")
	err = str(res[1], encoding="gbk")
	if err != None and err != "":
		print(err)
		sys.exit(0)

	_system = platform.system()
	if (_system == "Windows"):
		execPath += ".exe"

	chlid = subprocess.Popen(execPath, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	chlid.stdin.write(bytes(inputCase, encoding="gbk"))
	# chlid.stdin.write(b"10")
	# print (chlid.stdout.read())

	poll_seconds = .250
	# 进程是否终止标志
	flag = False
	# .poll()检查是否结束，设置返回值
	# .terminate()方法 终止进程
	while time.time() < deadline and chlid.poll() == None:
		time.sleep(poll_seconds)
	if chlid.poll() == None:
		if float(sys.version[:3]) >= 2.6:
			chlid.terminate()
			flag = True
	res = chlid.communicate()
	# res[0] = open("C:\\Users\Administrator\\Desktop\\2018 10.txt",'r');
	# print (res[0])
	os.remove(execPath)
	out = str(res[0], encoding="gbk")
	err = str(res[1], encoding="gbk")
    
	if err != "":
		for line in err.split("\r\n"):
			print(line)

	if flag:
		print("forced out of")

	#print (out)
	return (out.strip())


def main():
	currentpath = get_path()
	compileName = get_compile(currentpath)
	#print(compileName)
	commandName = get_command(currentpath)
	#print(commandName)
	inputCase = get_input(currentpath,"input1.txt")
	#print(testCase)
	outputCase = compileFile(inputCase,currentpath,compileName,commandName,"5")
	FileOutput(outputCase,currentpath,"output1.txt")
	#print(outputCase)
	#list_ = []
	#list_.append(outputCase)
	#print(list_)
	expectCase = get_expect(currentpath,"expect1.txt")
	#print(expectCase.decode("gbk"))
	Compared(expectCase,outputCase)

if __name__ == '__main__':
	main()