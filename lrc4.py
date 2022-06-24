from music_dl.source import MusicSource
from music_dl import config,source
import re
import logging
from music_dl.exceptions import *
from pydub import AudioSegment
#通过酷狗音乐下载mp3和lrc
def get_mp3_lrc(keyword,soure,ourdir,number):
   # 初始化全局变量
   config.init()
   config.set("keyword", keyword)
   config.set("url", '')
   config.set("playlist", '')
   if source:
      config.set("source", source)
   config.set("number", number)
   config.set("outdir", ourdir)
   config.set("verbose", 'verbose')
   config.set("lyrics", '')
   config.set("cover", '')
   config.set("nomerge", '')
   # if proxy:
   #    proxies = {"http": proxy, "https": proxy}
   #    config.set("proxies", proxies)
   ms = MusicSource()
   songs_list = ms.search(config.get("keyword"),config.get("source"))

   for i in range(0,number+1):
      songs_list[i].download_lyrics()
      lrc = songs_list[i].lyrics_text
      if read_lrc(lrc,keyword)==404 or len(lrc)==0 :
         continue
      else:
         song = songs_list[i].download()
         fullname = songs_list[i]._fullname
         break
   return fullname,read_lrc(lrc,keyword)
#音频切片
def cut_mp3(out_file,filepath,start,end):
    """
    # 程序流程
    1. 读取一个mp3文件,指定文件路径即可
    2. 根据用户选择设置截取片段，使用切片, 单位为ms
    3. 导出文件并保存, 指定导出文件名以及路径，最后指定导出的格式
    （其他编码格式，参考ffmpeg上的专业知识）

    :param filepath: 音乐文件路径, path
    :out_file: 导出文件夹路径
    :start:切片开始时间
    :end：切片结束时间
    :return: None
    """
    music = AudioSegment.from_mp3(file=filepath)
    AudioSegment.from_raw
    sound_time = music.duration_seconds
    print(f"music duration time: {sound_time}")

    # 使用切片截取, 单位毫秒， 1s -> 1000ms
    out_music = music[start: end]

    # 导出
    out_music.export(out_f=f"{out_file}/cut.mp3", format='mp3')   # 可以指定bitrate为64k比特率 None为源文件

    print('done')
    pass
#根据歌词关键字查找片段的开始时间和结束时间
def read_lrc(data,keyword):
   data = data.splitlines()
   lrc_url = list(reversed(data))
   geci_num=0
   for num,str in enumerate(lrc_url):
      # print(str)
      if num >6:
         pattern = '.*' + ']' + keyword + '.*'
         obj = re.findall(pattern, str)
         if len(obj) > 0:
            geci_num = num
            # print(geci_num)
            break
         # print(lrc_ur[geci_num-2])
   def make_time(nf_str):
      print(nf_str)
      nf_str = re.findall(r"""[\[\s\S]*?\]""",nf_str)
      nf_str = nf_str[-1].replace('[','').replace(']','').replace('\r\n','')
      # print(nf_str)
      ts = int(nf_str[0:2])*60*1000+int(nf_str[3:5])*1000+int(nf_str[6:8])*10
      return ts
   print(geci_num)
   if geci_num==0:
      return 404
   else:
      start_time = make_time(lrc_url[geci_num])-1000
      end_time = make_time(lrc_url[geci_num-1])+1000
      # print(start_time,end_time)
      return start_time,end_time
if __name__ == "__main__":
   keyword = '日子再忙也有人一起吃'#请输入关键词
   source = ['kugou','netease']
   ourdir = '/home/fangjiyuan/github_file/LRC/'#需要自定义
   number = 20 #一次查询返回的条数
   # try:
   song = get_mp3_lrc(keyword,source,ourdir,number)
   file_url =song[0]+'.mp3'
   start = song[1][0]
   end = song[1][1]
   cut_mp3(ourdir,file_url,start,end)
   # except:
      # print('没有找到可用的歌曲')