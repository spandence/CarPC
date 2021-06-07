import sys
import os
import json
from pathlib import Path
import time
import subprocess

def loadConfigs(subConfig):
    with open(sys.argv[1]) as json_file:
        config = json.load(json_file)
        return config[subConfig]

def genFilePath():
    OutputFolder = f"{GlobalConfigs['persistant_storage']}CameraCache/"
    Path(OutputFolder).mkdir(parents=True, exist_ok=True)
    TimeString = time.strftime("%Y%m%d%H%M%S")
    FileName = f'Camera_{TimeString}'
    return f'{OutputFolder}{FileName}.mp4'

def recordCamera():
    Device = CameraConfigs['cameraDevice']
    FrameRate = CameraConfigs['frameRate']
    VideoSize = CameraConfigs['videoSize']
    Duration = 60 * CameraConfigs['duration_mins']
    FilePath = genFilePath()
    cmd = f'ffmpeg -f v4l2 -framerate {FrameRate} -video_size {VideoSize} -t {Duration} -i {Device} {FilePath}'
    subprocess.call(cmd, shell=True)
    return FilePath

def directorySize(path):
    size = subprocess.check_output(['du','-sm', path]).split()[0].decode('utf-8')
    return size

def oversize(MaxSize):
    DirSize = float(directorySize(f"{GlobalConfigs['persistant_storage']}CameraCache/"))
    if DirSize > MaxSize:
        return True
    else:
        return False

def clearFiles():
    DirectoryPath = f"{GlobalConfigs['persistant_storage']}CameraCache/"
    files = os.listdir(DirectoryPath)
    sorted_files =  sorted(files, reverse=True)
    MaxSize = CameraConfigs['keep_size_utilization'] * CameraConfigs['keep_size_G'] * 1024
    count = -1
    while oversize(MaxSize):
        os.remove(f"{DirectoryPath}{sorted_files[count]}")
        count -= 1

CameraConfigs = loadConfigs('camera')
GlobalConfigs = loadConfigs('global')

while True:
    clearFiles()
    recordCamera()