# Rubbish-Video-Generator
营销号**视频**生成器~仅供娱乐

功能：自动生成文本，自动添加字幕，自动给视频配音（人声）

- [1.1版本更新](https://github.com/wmathor/Rubbish-Video-Generator#bug11%E7%89%88%E6%9C%AC%E6%9B%B4%E6%96%B0 )
- [下载](https://github.com/wmathor/Rubbish-Video-Generator#%E4%B8%8B%E8%BD%BD)
- [如何使用](https://github.com/wmathor/Rubbish-Video-Generator#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8 )
  - [示例](https://github.com/wmathor/Rubbish-Video-Generator#%E7%A4%BA%E4%BE%8B )
- [设计思路](https://github.com/wmathor/Rubbish-Video-Generator#%E8%AE%BE%E8%AE%A1%E6%80%9D%E8%B7%AF )
- [LICENSE](https://github.com/wmathor/Rubbish-Video-Generator#license)

### :bug:1.1版本更新

- 修复了原视频带有bgm，最终生成的视频没有声音的问题
- 现在支持手动设定字体大小，在`args.txt`文件中的第五行进行设置

### 下载

```shell
$ git clone https://github.com/wmathor/Rubbish-Video-Generator.git
```

### 如何使用

moviepy == 1.0.0

python > 3.5

自行安装ImageMagick

缺少的库自行pip

如果报错'module 'websocket' has no attribute 'enableTrace''，请参考下面的解决方案

```shell
pip uninstall websocket
pip uninstall websocket-client
pip install websocket-client
```

[B站讲解](https://www.bilibili.com/video/BV1Ap4y1y7o7)

1. 需准备一个时长大于50s的视频，有无背景音乐均可，命名为`in.mp4`
2. 需准备一个时长大于50s的BGM，命名为`in.mp3`
3. 提前在`args.txt`文本中定义好主体、事件、另一种说法
4. 在`args.txt`文本中添加讯飞语音合成（流式版）的`APPID`、`APIKey`、`APISecret`，以英文分号`;`分隔
5. 执行程序

#### 示例

![](https://s1.ax1x.com/2020/04/19/Juy9QH.png)

![](https://s1.ax1x.com/2020/04/19/JuNLZD.png)

### 设计思路

1. 剪裁视频→`getVideo()`
2. 将台词写入文本→`getText(file)`
3. 获取视频总时长→`getLength(video)`
4. 给视频添加背景音乐→`add_audio(video, mp3, output='out.mp4')`
5. 给视频添加字幕→`subTitle(text_file, video_file, output='out_sub.mp4')`
6. 文本转人声→讯飞API
7. 给视频添加人声→`add_people(mp3_file, video_file)`
8. 清除中间生成的文件→`clean()`

### LICENSE

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br/>本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可