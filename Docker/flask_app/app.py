#!/usr/bin/python3
from flask import Flask, render_template
import random

app = Flask(__name__)

images = [
    'https://media1.giphy.com/media/21GCae4djDWtP5soiY/giphy.webp?cid=ecf05e47s8nktvmdrlfuujq2g7mqfljdfigek0lxg7y5fhsf&rid=giphy.webp&ct=g',
    'https://media0.giphy.com/media/14rtlR7b01cjQI/200w.webp?cid=ecf05e47s8nktvmdrlfuujq2g7mqfljdfigek0lxg7y5fhsf&rid=200w.webp&ct=g',
    'https://media3.giphy.com/media/7Jplyo45Cd8Pp8A4PO/giphy.webp?cid=ecf05e47gix5a6101ny6qq8ns81opprtgle8cyzaj5m3r3ot&rid=giphy.webp&ct=g',
    'https://media2.giphy.com/media/eeUJaTwsHh3tswkaYm/giphy.webp?cid=ecf05e47gix5a6101ny6qq8ns81opprtgle8cyzaj5m3r3ot&rid=giphy.webp&ct=g',
    'https://media4.giphy.com/media/TJxrHj7AurjqljHSv2/giphy.webp?cid=ecf05e47gix5a6101ny6qq8ns81opprtgle8cyzaj5m3r3ot&rid=giphy.webp&ct=g',
    'https://media4.giphy.com/media/9fuvOqZ8tbZOU/200w.webp?cid=ecf05e47rbzdiuaws65ij7mfddhaj32axzve14bpu5i1nu6j&rid=200w.webp&ct=g',
    'https://media2.giphy.com/media/DZR39sOOQWP8A7UoVs/200w.webp?cid=ecf05e47rbzdiuaws65ij7mfddhaj32axzve14bpu5i1nu6j&rid=200w.webp&ct=g',
    'https://media3.giphy.com/media/oDK8A6xUNjD2M/giphy.webp?cid=ecf05e47mug123kf7yj2lkvdcqb2x2wsy8izq0wv6dyk2kgy&rid=giphy.webp&ct=g',
    'https://media3.giphy.com/media/x2HlgAoUgbMm6mMvlB/giphy.webp?cid=ecf05e47mug123kf7yj2lkvdcqb2x2wsy8izq0wv6dyk2kgy&rid=giphy.webp&ct=g',
    'https://media2.giphy.com/media/Y4pAQv58ETJgRwoLxj/giphy.webp?cid=ecf05e47s8nktvmdrlfuujq2g7mqfljdfigek0lxg7y5fhsf&rid=giphy.webp&ct=g'
]


@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
