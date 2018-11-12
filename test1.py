#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import subprocess
import os
import time
import sys
import platform
import difflib


def get_path():
    currentpath = os.path.abspath('.')
    return currentpath


def get_input(currentpath, inputfile_number):
    testCasePath = currentpath + "/test/input/input" + str(inputfile_number) + ".txt"
    if (os.path.exists(testCasePath)):
        with open(testCasePath, 'r') as inputf:
            testCase = inputf.read().strip()
            return testCase
    else:
        return "error:this file:" + testCasePath + " does not exist."


def get_inputfile_number(currentpath):
    inputPath = currentpath + "/test/input/"
    fileslist = os.listdir(inputPath)
    n = 0
    for i in range(len(fileslist)):
        path = os.path.join(inputPath, fileslist[i])
        if (os.path.isfile(path)):
            n += 1
    return n


def get_expect(currentpath, expectfile_number):
    expectFilePath = currentpath + "/test/expect/expect" + str(expectfile_number) + ".txt"
    if (os.path.exists(expectFilePath)):
        with open(expectFilePath, 'rb') as expect:
            expectCaseB = expect.read().strip()
            expectCase = str(expectCaseB,encoding = "UTF-8")
            #print(expectCase)
            return expectCase
    else:
        return "error:this file:" + expectFilePath + " does not exist."


def get_compile(currentpath):
    FilePath = currentpath + "/test/compile.txt"
    if (os.path.exists(FilePath)):
        with open(FilePath, 'r') as File:
            compileName = File.read().strip()
            return compileName
    else:
        return "error:this file:" + FilePath + " does not exist."


def get_command(currentpath):
    FilePath = currentpath + "/test/command.txt"
    if (os.path.exists(FilePath)):
        with open(FilePath, 'r') as File:
            commandName = File.read().strip()
            return commandName
    else:
        return "error:this file:" + FilePath + " does not exist."


def Compared(currentpath, expectCase, outputCase):
    if (expectCase == outputCase):
        print("PASSED:")
        return 0
    else:
        print("FAILURE:The output result is different from the expected result.")
    #d = difflib.HtmlDiff()
    # print(d.make_file(expectCase.splitlines(),outputCase.splitlines()))
    #with open(currentpath + "/test/result/index.html", 'w+') as fo:
    #    fo.write(d.make_file(expectCase.splitlines(), outputCase.splitlines()).replace('utf-8', 'gbk'))
    #    fo.close()


    # if(expectCase==outputCase):
    #   print("success:")
    #   return 0
    # else:
    #   print ("error:The input result is different from the expected result.")
    #   return 1

def FileOutput(outputCase, currentpath, outputfile_number):
    outputFilePath = currentpath + "/test/output/ontput" + str(outputfile_number) + ".txt"
    with open(outputFilePath, 'w+') as File:
        File.write(outputCase)
        File.close()

def compileFile(inputCase, currentpath, compileName, commandName, timeout):
    # 两个待传入的参数：filepath、timeout、input
    filePath = currentpath + "/" + compileName
    # timeout = "5"
    # filePath="${filePath}"
    # timeout = "${timeout}"
    #
    deadline = time.time() + float(timeout)
    #

    # print(index)
    execPath = currentpath + "/" + commandName
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
    print(out)

    _system = platform.system()
    if (_system == "Windows"):
        execPath += ".exe"

    chlid = subprocess.Popen(execPath, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    chlid.stdin.write(bytes(inputCase, encoding="UTF-8"))
    # chlid.stdin.write(b"10")
    # print (chlid.stdout.read())
    '''poll_seconds = .250
    # 进程是否终止标志
    flag = False
    # .poll()检查是否结束，设置返回值
    # .terminate()方法 终止进程
    while time.time() < deadline and chlid.poll() == None:
        time.sleep(poll_seconds)
    if chlid.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            chlid.terminate()
            flag = True'''

    res = chlid.communicate()
    # res[0] = open("C:\\Users\Administrator\\Desktop\\2018 10.txt",'r');
    # print (res[0])

    out = str(res[0], encoding="utf-8")
    err = str(res[1], encoding="utf-8")
    os.remove(execPath)
    if err != "":
        for line in err.split():
            print(line)

    #if flag:
        #print("forced out of")

    print (out)
    return (out.strip())


def function(output_list,expect_list,currentpath, inputfiles_number, compileName, commandName):
    for i in range(1, inputfiles_number+1):
        inputCase = get_input(currentpath, i)
        print(inputCase)
        outputCase = compileFile(inputCase, currentpath, compileName, commandName, "5")
        FileOutput(outputCase, currentpath, i)
        #print(outputCase)
        output_list.append(outputCase)
        # list_ = []
        # list_.append(outputCase)
        # print(list_)
        expectCase = get_expect(currentpath, i)
        #print(expectCase)
        expect_list.append(expectCase)
        Compared(currentpath,expectCase,outputCase)


def create_html_block(inputfiles_number,output_list,expect_list):
        html_block = r'<h3>%s</h3><div class="container"><div class="row"><div class="col-sm-6"><div class="panel panel-default"><div class="panel-heading"><form class="form-inline"><div class="row"><div class="col-xs-6"><button type="button" class="btn btn-default">实际输出：</button></div></div></form></div><textarea class="form-control">%s</textarea></div></div><div class="col-sm-6"><div class="panel panel-default"><div class="panel-heading"><form class="form-inline"><div class="row"><div class="col-xs-6"><button type="button"  class="btn btn-default">期望输出：</button></div></div></form></div><textarea class="form-control">%s</textarea></div></div></div></div>'
        block_i =''
        for i in range(0, inputfiles_number):
            block_i += html_block%("Test Case"+str(i+1),output_list[i],expect_list[i])
        html_add = r'<html lang="en"><head><meta charset="utf-8"><title>result</title><link rel="stylesheet" href="./jquery-ui.min.css"><script src="./jquery-1.10.2.js"></script><script src="./jquery-ui.min.js"></script><link rel="stylesheet" href="./bootstrap.min.css"><script src="./bootstrap.min.js"></script><script>$(function() {$( "#accordion" ).accordion();});</script><style>.container {width:100%;}</style></head><body><div id="accordion">'+block_i+'</div></body></html>'
        return(html_add)

def main():
    currentpath = get_path()
    inputfiles_number = get_inputfile_number(currentpath)
    # print(inputfiles_number)
    compileName = get_compile(currentpath)
    commandName = get_command(currentpath)
    output_list = []
    expect_list = []
    function(output_list,expect_list,currentpath, inputfiles_number, compileName, commandName)
    html = create_html_block(inputfiles_number, output_list, expect_list)
    with open(currentpath + "/test/result/index.html", 'w+',encoding = 'UTF-8') as fo:
        fo.write(html)
        fo.close()
    #print(type(output_list[0]))
    #print(expect_list)


if __name__ == '__main__':
    main()