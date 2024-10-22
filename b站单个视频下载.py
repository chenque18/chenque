import os
from moviepy.editor import *
#安装pip install moviepy
import requests
#安装pip install requests
import re
from pprint import pprint
import json

def geturl(url):
          #设置请求头
          hander={
        "Cookie": "buvid3=B33F7C8B-3F27-82D2-9F52-39914A072F6634133infoc; b_nut=1726820634; _uuid=66C736D9-4216-310710-BDFD-D7B8F18AA23434800infoc; enable_web_push=DISABLE; home_feed_column=5; browser_resolution=1920-919; CURRENT_FNVAL=4048; rpdid=0zbfVHinoY|1OTNhDsn|1fh|3w1SRyW8; header_theme_version=CLOSE; buvid4=7056258C-C896-4A4E-34AA-4B6ECA2CC85D24412-024062310-yMoXRrpW6SYYQd6%2FsMA6qw%3D%3D; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg1NTMyNDIsImlhdCI6MTcyODI5Mzk4MiwicGx0IjotMX0.Bgtv8voqn0zpdvN4DUfphCkaBMcPV04rpNUz6PAlP8Q; bili_ticket_expires=1728553182; fingerprint=30c08cb89d1eada4e01076f6205a4763; buvid_fp_plain=undefined; buvid_fp=30c08cb89d1eada4e01076f6205a4763; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; b_lsid=C732C7810_19271160299; bp_t_offset_588833284=986280492963725312; SESSDATA=79821d3d%2C1744026919%2Cd9d12%2Aa1CjBAAF4AvXFdAioMr-5IqAFrDRhq8b06kzJwM7ZCbUCAT9FgJvRtlYneK8P4rp_1H4USVjhUdXRXVWxuN1RzWnduVmYzenhwMGFuWnpBaXp3WmpUZkdkdHVJVTRvZGNyRGFtWFg4YVFuTmUxaWlRcWh1LWd4clFUa2ZNSXBIc0ZkcVNTUkR1Vi1nIIEC; bili_jct=47cb3a332afaf5744cd3960b4cce2aec; DedeUserID=3546740399540957; DedeUserID__ckMd5=3d01ad42a36cde24; sid=mldzgup2",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        , "Referer": "https://www.bilibili.com/"}

          response=requests.get(url=url,headers=hander)
          return response

def getvideo():
    link=input('输入b站视频网址：')
    #link='https://www.bilibili.com/video/BV1xm411X72s/?spm_id_from=333.788.recommend_more_video.0&vd_source=dff476110a3b2b8d4001de1d103485d8'
    response=geturl(url=link)
    html=response.text
    #print(html)
    playinfo=re.findall('<script>window.__playinfo__=(.*?)</script>',html)[0]
    title=re.findall('<title data-vue-meta="true">(.*?)</title>',html)
    json_data=json.loads(playinfo)
    #pprint(json_data)
    audio_url=json_data['data']['dash']['audio'][0]['baseUrl']
    video_url=json_data['data']['dash']['video'][0]['baseUrl']
    print(audio_url)
    print(video_url)
    title=title[0] if title else '无标题'
    return title,audio_url,video_url

def save(title,audio_url,video_url):
    audio=geturl(url=audio_url).content
    video=geturl(url=video_url).content

    safe_title=re.sub(r'[^\w\-\. ]','_',title)
    #创造文件夹
    video_dir = r'C:\video'
    os.makedirs(video_dir,exist_ok=True)


    with open(os.path.join(video_dir,safe_title+'q.mp4'),mode='wb')as videofile:videofile.write(video)
    with open(os.path.join(video_dir,safe_title+'q.mp3'),mode='wb')as audiofile:audiofile.write(audio)
    #视音频合成
    video1=VideoFileClip(rf'C:\video\{safe_title}'+'q.mp4')
    audio1=AudioFileClip(rf'C:\video\{safe_title}'+'q.mp3')
    complete=video1.set_audio(audio1)
    complete.write_videofile(rf'C:\video\{safe_title}'+'.mp4')
    audio1.close()
    os.remove(rf'C:\video\{safe_title}'+'q.mp3')
    video1.close()
    os.remove(rf'C:\video\{safe_title}'+'q.mp4')
    complete.close()
    os.startfile(r'C:\video')



if __name__=='__main__':
    title,audio_url,video_url=getvideo()
    save(title,audio_url,video_url)





