#某ハッカソンで作ったものの改修版API  リクエストで動画を合成してS3にアップロードし、URLを返す

from flask import Flask, jsonify, request
import os
import json
import subprocess
import random
import librosa
import boto3

app = Flask(__name__)

def danceCreaterMain():
    #main関数、曲を取得しそれをdanceMaker()に投げ、URLを返す(また作り直したい)
    bgm = ['music/128_1.mp3', 'music/128_2.mp3']
    filename = str(bgm[random.randint(0, 1)])
    #今回はランダムで曲を作成

    bpm = 128
    time = 32
    #時間があればbpm及び動画時間を以下で取得する
    # bpm, time = bpmTimeGetter(filename)

    danceMaker(filename, time, bpm)

    return "https://s3.amazonaws.com/rechack-dance/output.mp4"

def bpmTimeGetter(filename):
    # bpm、およびTime(音楽の時間)をlibrosaを用いて計測、返り値は[bpm,time]
    # 時間短縮のため現在は使ってない
    y, sr = librosa.load(filename)
    bpm, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = int(bpm)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return (bpm, int(beat_times[-1]))


def danceMaker(filename, time, bpm):
    #曲の時間に合うようにダンス動画を組み合わせる
    num = 1
    limit = int(time / 4 - 2)

    #ffmpegで使う用の文字列の初期 最初はa1.mp4を使う
    combo = 'movie/a1.mp4 -i '

    #ランダムで動画を取得する
    for i in range(limit):
        num += 1
        combo += 'movie/a' + str(random.randint(2, 7)) + '.mp4 -i '

    #最後にa8.mp4を合成
    combo += 'movie/a8.mp4 '
    num += 1

    #ffmpegで動画を結合
    cmd = 'ffmpeg -y -i ' + combo + '-strict ' + str(num) + ' -filter_complex "concat=n=' + str(
        num) + ':v=1:a=1 " convideo.mp4'
    res1 = subprocess.call(cmd, shell=True)
    #print(res1)

    #作成した動画に音声を合成し、output.mp4を作成
    cmd2 = 'ffmpeg -y -i convideo.mp4 -i ' + filename + ' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 /tmp/output.mp4'
    res2 = subprocess.call(cmd2, shell=True)
    # print(res2)

    #s3にアップロード
    bucket_name = "rechack-dance"

    s3 = boto3.client('s3', 'ap-northeast-1', aws_access_key_id="", aws_secret_access_key="")

    s3.upload_file('/tmp/output.mp4', bucket_name, 'output.mp4', ExtraArgs={"ContentType": "mp4", 'ACL':'public-read'})


@app.route('/api/test', methods=['POST'])
def api_test():
    print("api")
    deta = request.get_json()
    level = deta["level"]
    genre = deta["genre"]
    name = deta["name"]
    #res = {"url": music(level, genre, bpm=100)}
    #return jsonify(res)
    url = danceCreaterMain()


    data = {"url":url}
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
