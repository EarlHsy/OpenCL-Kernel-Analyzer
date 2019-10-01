#!/usr/bin/python3
# -*- coding: UTF-8 -*-


# Build by Hsy  8/24/2019
# Base on clang & libclc



import os
import sys
import threading

version = '1.0'
work_dir = 'OpenCL_Kernel_Analyzer_build'
kernels_temp_dir = work_dir + '/kernels'
sources_path = ''
string_key_head = 'STRING('
string_key_end = ')'

clang_version = ''
compile_option = '-cl-std=CL1.1 -Wno-everything -include include/clc/clc.h -c '
# compile_option = '-Dcl_clang_storage_class_specifiers -isystem $LIBCLC/generic/include -include include/clc/clc.h -x'
opencl_extension = ['cl_khr_fp16']

list_fileThreads = []

class fileThread(threading.Thread):
    targetF = ''
    # def __init__(self, threadID, name, counter):
    #     threading.Thread.__init__(self)
    #     self.threadID = threadID
    #     self.name = name
    #     self.counter = counter

    def __init__(self, targetF):
        threading.Thread.__init__(self)
        self.targetF = targetF
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter
    def run(self):
        checkFile(self.targetF)
        compileFile(self.targetF)

def show_usage():
    print('OpenCL kernel checker, version ' + version)
    print('Dependence: clang-5.0+ libclc-dev')
    print('Usage:')
    print('python OpenCL_Kernel_Analyzer.py {$dir_of_your_kernels}')

def create_work_dir():

    if not os.path.exists(sources_path):
        print(sources_path + ' is not exists')
        exit(-2)
    if os.path.exists(work_dir):
        os.system('rm -R ' + work_dir + '/')
    kernels_dir = work_dir + '/'+ os.path.basename(sources_path)
    # os.makedirs(work_dir)
    os.makedirs(kernels_dir)
    print('created work dir.')


def checkFile(targetF):
    f = open(targetF, 'r')
    line = f.readline()
    line_all = []
    # Append opencl extensions
    for str in opencl_extension:
        line_all.append('#pragma OPENCL EXTENSION ' + str + ' : enable')
    while line:
        index = line.find(string_key_head)
        if index == 0:
            line = line.replace(string_key_head, '/*' + string_key_head + '*/')
        index = line.find(string_key_end)
        if index == 0:
            line = line.replace(string_key_end, '/*' + string_key_end + '*/')
        line_all.append(line)
        line = f.readline()
    f.close()
    f = open(targetF, 'w')
    for line in line_all:
        f.write(line)
    f.close()

def compileFile(targetF):
    # command = 'clang++'
    command = './clangSpirV'
    if clang_version:
        command += '-'
        command += clang_version
    command += ' '
    command += compile_option
    command += targetF
    # command += ' -o '
    # command += targetF
    # command += '.o'
    print('\033[32m' + targetF)
    os.system(command)
    

def copyFiles(sourceDir, targetDir):
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            # copyFileCounts += 1
            if sourceF.split('.')[1] == 'cl':
                open(targetF, 'wb').write(open(sourceF, 'rb').read())
        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)

def process(targetDir):
    for f in os.listdir(targetDir):
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(targetF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            # copyFileCounts += 1
            if targetF.split('.')[1] == 'cl':
                # newFileThread = fileThread(targetF)
                # newFileThread.start()
                # list_fileThreads.append(newFileThread)
                checkFile(targetF)
                compileFile(targetF)
		
        if os.path.isdir(targetF):
            process(targetF)



if __name__ == '__main__':
    if len(sys.argv) < 2 :
        show_usage()
        exit(-1)
    os.system('./clangSpirV -v')
    sources_path = sys.argv[1].strip()  #arg[0] is path of opencl kernels dir
    # sources_path = '/home/hsy/PhoneBit/OpenCL-Android/app/src/main/cppcode/src/kernels'  #arg[0] is path of opencl kernels dir
    create_work_dir()
    copyFiles(sources_path, kernels_temp_dir)
    print('\033[33mcompile options: ' + compile_option)
    process(kernels_temp_dir)
    # for fileThread in list_fileThreads:
    #     fileThread.join()
    os.system('rm *.o')
    # os.system('rm *.tmp')




