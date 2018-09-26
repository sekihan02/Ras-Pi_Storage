# coding:utf-8
'''
ラズパイで各サイトのにゅーすを読む
'''
import feedparser
import subprocess
import time

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t)
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)

'''
# parser()関数にurlを指定してパース XMLの文字列の指定もできる
d = feedparser.parse('https://techwave.jp/rsslatest.xml') # techwave

print(d.feed.title)

# 要素のタイトルの取得
# print(d.entries[0].title)
# 要素のリンクの取得
# print(d.entries[0].link)

# すべての要素について処理を繰り返す
news_text = ''
for entry in d.entries:
    print(entry.title)
    news_text += entry['title'].encode('utf-8')
# jtalk(news_text)
print()

# はてなブックマーク - 人気エントリー - テクノロジー
d = feedparser.parse('http://b.hatena.ne.jp/hotentry/it.rss') 
print(d.feed.title)

news_text = ''
for entry in d.entries:
    print(entry.title)
    news_text += entry['title'].encode('utf-8')
# jtalk(news_text)
print()
'''

# Top Stories - Google News
d = feedparser.parse('http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss')
print(d.feed.title)

news_text = ''
# すべての要素について処理を繰り返す
for entry in d.entries:
    print(entry.title)
    news_text += entry['title'].encode('utf-8')

jtalk(news_text)