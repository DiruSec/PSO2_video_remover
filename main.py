#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib.request
import re
import sys
import os
import shutil
import locale
from datetime import datetime as dt

validLang = ["en","cn","ja"]
currentLang = locale.getdefaultlocale()[0].lower()
for lang in validLang:
    try:
        currentLang.index(lang)
        currentLang = lang
    except:
        pass
if (len(currentLang)>2):
    currentLang = 'en'

langString = {
    "en": {
        "checkVer": "Checking game version ...",
        "failLoadPatchList": "Cannot load patchlist file.",
        "checkCache": "Checking cache ...",
        "useCache": "Vaild cache detected. Use cache instead of re-downloading? (Y/n)",
        "parseList": "Parsing patchlist file ...",
        "readDict": "Reading game dictionary ...",
        "manualPath": "Cannot recongize gamefile dictionary. Input dictionary path manually? (y/N)",
        "manualPath2": "Input game root dictionary which contains 'pso2_bin' folder.\nLike 'D:\\PHANTASYSTARONLINE2'",
        "downloadList": "Downloading patchlist file ...",
        "readCache": "Loading patchlist file from cache ...",
        "movingFile": "Moving %s, size: %s KiB",
        "removeFile": "Removing %s ...",
        "moveResult": "Moved %s files.",
        "sizeResult": "Total size: %s KiB.",
        "deleteConfirm": "Delete these files now？(y/N)",
        "listNotEnough": "Patchlist seems corrupted. Try re-download patchlist.\nIf still dosen't work, it might be a bug.",
        "notDetected": "Did not detected any dummy file.",
        "checkMDayDiff": "How many days that files created before should not be deleted? (Default: 30）\n※If you don't know the meaning, press Enter. ",
        "pressContinue": "Press Enter to continue ..."
    },
    "ja": {
        "checkVer": "ゲームバージョンをチェックしています…",
        "failLoadPatchList": "Patchlist の読み込みが失敗しました。",
        "checkCache": "キャッシュをチェックしています…",
        "useCache": "有効なキャッシュが存在しています。キャッシュを使用しますか？ (Y/n)",
        "parseList": "Patchlist を分析しています…",
        "readDict": "データフォルダーをチェックしています…",
        "manualPath": "データフォルダーを認識できません。手動でゲームのインストール先を入力しますか？ (y/N)",
        "manualPath2": "ゲームのインストール先を入力してください。インストール先は 'pso2_bin' というフォルダーを含まれています。\n例：'D:\\PHANTASYSTARONLINE2'",
        "downloadList": "Patchlist をダウンロードしています…",
        "readCache": "キャッシュから patchlist を読み込みしています。",
        "movingFile": "ファイル：%s、サイズ： %s KiB",
        "removeFile": "%s を削除しています…",
        "moveResult": "%s 件のファイルを検出しました。",
        "sizeResult": "合計サイズ： %s KiB.",
        "deleteConfirm": "検出したファイルを削除しますか？(y/N)",
        "listNotEnough": "Patchlist が破損してるようです。再ダウンロードを試してください。\n相変わらずダメの場合は、バグが起きてるかもしれません。",
        "notDetected": "動画ファイルを検出してませんでした。",
        "checkMDayDiff": "日数を入力してください。期間中にダウンロードしたファイルは削除されません。(デフォルト: 30）\n※意味がわからないの場合は、Enter を押してください。 ",
        "pressContinue": "続行するには Enter キーを押してください…"
    },
    "cn": {
        "checkVer": "正在检测游戏版本…",
        "failLoadPatchList": "读取 patchlist 文件失败。",
        "checkCache": "正在确认缓存…",
        "useCache": "检测到有效缓存。要使用缓存吗？ (Y/n)",
        "parseList": "正在处理 patchlist 文件…",
        "readDict": "正在读取游戏数据文件夹…",
        "manualPath": "未检测到游戏数据文件夹。要手动输入文件夹地址吗？ (y/N)",
        "manualPath2": "请输入游戏根目录地址（内有 'pso2_bin' 文件夹）。\n形如 'D:\\PHANTASYSTARONLINE2'。可以从资源管理器的地址栏中复制并粘贴到此处。",
        "downloadList": "正在下载 patchlist 文件…",
        "readCache": "正在从缓存读取 patchlist 文件…",
        "movingFile": "检测到 %s，大小：%s KiB",
        "removeFile": "正在删除 %s …",
        "moveResult": "共检测到 %s 个文件。",
        "sizeResult": "总大小 %s KiB。",
        "deleteConfirm": "立即删除上述文件吗？(y/N)",
        "listNotEnough": "Patchlist 文件似乎损坏了。请尝试重新下载。\n若仍然不行，可能是出现了一个 Bug。",
        "notDetected": "没有检测到任何无用文件。",
        "checkMDayDiff": "请输入一个天数。距现在一定天数内的文件不会被删除。（默认：30）\n※如果你不知道这有什么用，请直接回车。 ",
        "pressContinue": "按回车键继续…"
    }
}
print (langString[currentLang]["checkVer"])
try:
    req = urllib.request.urlopen(
        urllib.request.Request(
        url="http://patch01.pso2gs.net/patch_prod/patches/management_beta.txt",
        data=None,
        headers={
            'User-Agent': 'AQUA_HTTP'
        }
    ))
    MFile = req.read().decode("UTF-8")
    regexp = re.compile(r"PatchURL=(.*)(?:\r)")
    patchlist = re.findall(regexp, MFile)[0] + "patchlist.txt"
except:
    print (langString[currentLang]["failLoadPatchList"])
    input(langString[currentLang]["pressContinue"])
    sys.exit()

def downloadList():
    global PFile
    print (langString[currentLang]["downloadList"])
    downloadReq = urllib.request.urlopen(
        urllib.request.Request(
        url=patchlist,
        data=None,
        headers={
            'User-Agent': 'AQUA_HTTP'
        }
    ))
    PFile = downloadReq.read().decode("UTF-8")

    with open("cachelist.txt",'w+') as f2:
        f2.write(PFile)
        f2.write("PatchURL="+patchlist)

def readCacheList():
    global PFile
    print (langString[currentLang]["readCache"])
    with open("cachelist.txt",'r') as f2:
        PFile = f2.read()


print (langString[currentLang]["checkCache"])
PFile = ''
try:
    with open("cachelist.txt",'r') as f:
        CFile = f.read()
        withrep = re.compile(r"PatchURL=(.*)")
        cachelist = re.findall(withrep, CFile)[0]
        if (cachelist == patchlist):
            useC = input(langString[currentLang]["useCache"]).lower()

            if (useC == 'n'):
                downloadList()
            else:
                readCacheList()
        else:
            downloadList()
except:
    downloadList()

print (langString[currentLang]["parseList"])
regexp = re.compile(r"data/win32/(.{32})\.pat")
filelist = re.findall(regexp, PFile)

# 完整性检测
if (len(filelist) < 60000):
    print (langString[currentLang]["listNotEnough"])
    input(langString[currentLang]["pressContinue"])
    sys.exit()

try:
    mdaydiff = int(input(langString[currentLang]["checkMDayDiff"]))
    if (mdaydiff <= 0):
        mdaydiff = 0
except:
    mdaydiff = 30

def definePath(inputpath):
    print (langString[currentLang]["readDict"])
    global files
    global path
    try:
        path = inputpath + "\\pso2_bin\\data\\win32"
        files = os.listdir(path)
    except:
        pathC = input(langString[currentLang]["manualPath"]).lower()
        if (pathC == 'y'):
            print (langString[currentLang]["manualPath2"])
            pathG = input()
            definePath(pathG)
        else:
            sys.exit()

definePath(os.getcwd())
# definePath('G:\PHANTASYSTARONLINE2\pso2_bin\data\win32')

totalsize = 0
deleteArray = []
dateNow = dt.now()

for index in files:
    if (index not in filelist and len(index)== 32):
        file = path+'\\'+index
        date = dt.fromtimestamp(os.stat(file).st_mtime)
        if ((dateNow - date).days >= mdaydiff):
            size = os.stat(file).st_size
            totalsize = totalsize + size
            deleteArray.append(index)
            print (langString[currentLang]["movingFile"]%(index,str(round(size/1024))))

if (len(deleteArray) == 0 or len(deleteArray) > 10000):
    print (langString[currentLang]["notDetected"])
    input(langString[currentLang]["pressContinue"])
    sys.exit()

print (langString[currentLang]["moveResult"]%len(deleteArray))
print (langString[currentLang]["sizeResult"]%str(round(totalsize/1024)))
ConfD = input(langString[currentLang]["deleteConfirm"]).lower()
if (ConfD == 'y'):
    for index in deleteArray:
        print (langString[currentLang]["removeFile"]%index)
        os.remove(path+'\\'+index)
input(langString[currentLang]["pressContinue"])