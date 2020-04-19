# Rubbish-Video-Generator
营销号**视频**生成器~仅供娱乐

- 下载
- 如何使用
  - 示例
- 设计思路
- LICENSE

#### 下载

```shell
$ git clone https://github.com/cwjokaka/bilibili_member_crawler.git
```

#### 如何使用

1. 需准备一个时长大于50s的视频，有无背景音乐均可，命名为`in.mp4`
2. 需准备一个时长大于50s的BGM，命名为`in.mp3`
3. 提前在`args.txt`文本中定义好主体、事件、另一种说法
4. 在args.txt文本中添加讯飞语音合成（流式版）的`APPID`、`APIKey`、`APISecret`，以英文分号`;`分隔
5. 执行程序

##### 示例

![](https://s1.ax1x.com/2020/04/19/JuNRZF.png)

![](https://s1.ax1x.com/2020/04/19/JuNLZD.png)

#### 设计思路

1. 剪裁视频→`getVideo()`
2. 将台词写入文本→`getText(file)`
3. 获取视频总时长→`getLength(video)`
4. 给视频添加背景音乐→`add_audio(video, mp3, output='out.mp4')`
5. 文本转人声
6. 给视频添加人声→`add_people(mp3_file, video_file)`
7. 清除中间生成的文件→`clean()`

#### LICENSE

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br/>本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可