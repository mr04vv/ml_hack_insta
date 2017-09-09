import csv
import os
import sys
import requests
import time
from colorfullcheck import aveLab,aveLab2

argvs = sys.argv  # コマンドライン引数を格納したリストの取得
argc = len(argvs) # 引数の個数

if (argc != 2):   # 引数が足りない場合は、その旨を表示
    print("実行失敗\n保存先を引数で指定してねー")
    quit()         # プログラムの終了

def CheckIdx(images_dir):
    i = 0
    while True:
        name = images_dir + "/" + str(i) + ".jpg"
        print(name)
        if not os.path.exists(name):
            return i
        i += 1

def MakeDirectry(location):
    os.makedirs(location)

def readcsv(filename,csvdata,likedata):
    try:
        with open(filename,'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            data = [v for v in csv_reader]
            i = 0
            for row in data:
                csvdata.append([i,row[1],row[2]])
                i += 1
    except FileNotFoundError as e:
        print(e)
    except csv.Error as e:
        print(e)

def make_filename(base_dir, number, url):
    ext = os.path.splitext(url)[1] # 拡張子を取得
    filename = str(number) + ext        # 番号に拡張子をつけてファイル名にする
    print(filename)
    fullpath = os.path.join(base_dir,filename)
    return fullpath

def download_image(url, timeout = 10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content

def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)



if __name__ == "__main__":
    images_dir = argvs[1] #ここ変えれば保存先フォルダが変わります
    idx = 0
    imgdir = "./scrape/instagStb.csv" #URL読み取り先はここで変更してください
    csvdata = []
    likedata = []
    if not os.path.exists(images_dir):
        MakeDirectry(images_dir)
    #idxを定める関数（上書きしないように）
    idx = CheckIdx(images_dir)
    readcsv(imgdir,csvdata,likedata)

    list2=[]
    likeIndex = 0

    for line in csvdata[1:151]:
        url = line[1]
        print(url)
        filename = make_filename(images_dir, idx, url)
        try:
            image = download_image(url)
            save_image(filename, image)
            col = aveLab2(filename,2)
            listData = []

            listData.append(filename)

            listData.append(line[2])
            listData.append(col[0][0])
            listData.append(col[0][1])
            listData.append(col[0][2])
            listData.append(col[1][0])
            listData.append(col[1][1])
            listData.append(col[1][2])
            print("dasda")
            #listData.append(aveLab(images_dir + "/" + filename,6))
            list2.append(listData)



            with open('instagStb2.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerows(list2)
                
            likeIndex += 1

            idx += 1
        except KeyboardInterrupt:
            break;
        except Exception as err:
            break;
        time.sleep(1)