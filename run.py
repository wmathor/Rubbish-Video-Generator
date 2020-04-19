import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import io
import os
import subprocess
import math
from time import sleep
from moviepy.editor import *
import wave, audioop

body = '' # 定义主体
thing = '' # 定义事件
other_word = '' # 定义另一种说法
in_mp4 = 'in_sub.mp4' # 输入视频
in_mp3 = 'in.mp3' # 输入音频
idx = 0

def getText(file): # 组装台词
    with open(file) as f:
        body = f.readline().strip()
        thing = f.readline().strip()
        other_word = f.readline().strip()
    
    # 主题框架
    txt = '''{}{}是怎么回事呢？:4:0
{}相信大家都很熟悉，但是{}{}是怎么回事呢？:7:4
下面就让小编带大家一起了解吧:3:11
{}{}，其实就是{}:8:15
大家可能会很惊讶{}怎么会{}呢？:6:23
但事实就是这样，小编也感到非常惊讶:5:29
这就是关于{}{}的事情了，大家有什么想法呢？:6:34
欢迎在评论区告诉小编一起讨论哦！:5:40'''.format(body, thing, body, body, thing, body, thing, other_word, body, thing, body, thing)

    # 台词写入
    with open('text.txt', mode='w') as f:
        f.write(txt)

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "lame", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8","ent": "intp65", "sfl": 1, 'volume': 100}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

def on_message(ws, message):
    try:
        message =json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            with open('./people{}.mp3'.format(idx), 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)



# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.CommonArgs,
             "business": wsParam.BusinessArgs,
             "data": wsParam.Data,
             }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        # if os.path.exists('people.mp3'):
        #     os.remove('people.mp3')
    thread.start_new_thread(run, ())

def getVideo():
    cmd =  'ffmpeg -y -i in.mp4 -ss 00:00:00 -t 00:00:50 -acodec copy -vcodec copy -async 1 in_sub.mp4'
    subprocess.call(cmd, shell=True)

def subTitle(text_file, video_file, output='out_sub.mp4'):
    video1 = VideoFileClip(video_file)
    sentences = [] # 台词列表
    with open(text_file) as f:
        text_tmp = f.readlines()
        for i in text_tmp:
            sentences.append(i.strip().split(':'))
    print(sentences)
    
    txts = [] # 所有字幕剪辑
    with open('args.txt') as f:
        color = f.readlines()[4].strip()
        for sentence, span, start in sentences:
            txt = (TextClip(sentence, fontsize=50, align='center', color=color, font='SimHei')
                    .set_position(("center","bottom")).set_duration(int(span)).set_start(int(start)))
            txts.append(txt)

    video2 = CompositeVideoClip([video1, *txts])
    video2.write_videofile(output)
    
def getLength(video): # 获取视频时长
    cmd = 'ffprobe -v quiet -select_streams v -show_entries stream=duration -of csv="p=0" {video}'.format(video=video)
    seconds = os.popen(cmd, 'r')
    seconds = math.ceil(float(seconds.read()))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

def add_audio(video, mp3, output='out.mp4'): # 将背景音乐添加到视频中
    BGM = 'ffmpeg -i {mp3} -ss 00:00:00.0 -t {time} -acodec copy BGM.mp3'.format(mp3=mp3, time=total_time)
    subprocess.call(BGM, shell=True)

    volume = 'ffmpeg -i BGM.mp3 -vcodec copy -af "volume=-20dB" BGM_volume.mp3'
    subprocess.call(volume, shell=True)
    
    command = "ffmpeg -i {mp3} -i {video} -y {output}".format(video=video, mp3='BGM_volume.mp3', output=output)
    subprocess.call(command, shell=True)


def addPeople(mp3_file, video_file):
    my_clip = VideoFileClip(video_file)
    audio_background = AudioFileClip(mp3_file)
    final_audio = CompositeAudioClip([my_clip.audio, audio_background])
    final_clip = my_clip.set_audio(final_audio)
    final_clip.write_videofile('final.mp4')

def clean():
    os.remove('in_sub.mp4')
    os.remove('out.mp4')
    os.remove('out_sub.mp4')
    for i in range(8):
        os.remove('people{}.mp3'.format(i))
    os.remove('output0.mp3')
    os.remove('test.mp3')
    os.remove('BGM.mp3')
    os.remove('BGM_volume.mp3')

if __name__ == "__main__":
    getVideo() # 裁剪视频
    getText('args.txt') # 台词写入文本
    total_time = getLength(in_mp4) # 获取视频总时长
    add_audio(in_mp4, in_mp3) # 给视频添加背景音乐
    subTitle('text.txt', 'out.mp4') # 给视频添加字幕

    # 获取APPID、APIKey、APISecret
    APPID, APIKey, APISecret = '', '', ''
    with open('args.txt') as f:
        APPID, APIKey, APISecret = f.readlines()[3].strip().split(';')

    # 文本转人声
    audio = []
    cmd = 'ffmpeg -f lavfi -i aevalsrc=0 -t {} -q:a 9 -acodec libmp3lame output0.mp3'.format('00:00:01')
    subprocess.call(cmd, shell=True)
    with open('text.txt') as f:
        text_tmp = f.readlines()
        for i in text_tmp:
            text = i.strip().split(':')[0]
            span = int(i.strip().split(":")[1])
            start = int(i.strip().split(':')[2])

            wsParam = Ws_Param(APPID=APPID, APIKey=APIKey,
                            APISecret=APISecret,
                            Text=text)
            websocket.enableTrace(False)
            wsUrl = wsParam.create_url()
            ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
            ws.on_open = on_open
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            idx = idx + 1
    
    cmd = 'ffmpeg -i output0.mp3 -i people0.mp3 -i people1.mp3 -i people2.mp3 -i people3.mp3 -i people4.mp3 -i people5.mp3 -i people6.mp3 -i people7.mp3 -filter_complex "[1]adelay=0000|0000[del1],[2]adelay=4000|4000[del2],[3]adelay=11000|11000[del3],[4]adelay=15000|15000[del4],[5]adelay=23000|23000[del5],[6]adelay=29000|29000[del6],[7]adelay=34000|34000[del7],[8]adelay=40000|40000[del8], [0][del1][del2][del3][del4][del5][del6][del7][del8]amix=9" test.mp3'
    subprocess.call(cmd, shell=True)
    addPeople('test.mp3', 'out_sub.mp4') # 给视频添加人声
    clean() # 清除中间生成的文件
    print('Complete!')

# 1. 裁剪视频 √
# 2. 台词写入文本 √
# 3. 获取视频总时长 √
# 4. 给视频添加背景音乐 √
# 5. 给视频添加字幕 √
# 6. 文本转人声 √
# 7. 给视频添加人声 √
# 8. 清除中间生成的文件 √