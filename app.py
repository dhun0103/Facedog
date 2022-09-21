from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta_1

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')
#################################################
@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title':title_receive,
        'content':content_receive,
        'file':f'{filename}.{extension}'
    }

    db.diary.insert_one(doc)

    return jsonify({'msg': '저장완료!'})

@app.route('/detail')
def detail():
    return render_template("detail.html")

@app.route('/subpage')
def subpage():
    return render_template("subpage.html")


#삭제하기 버튼
@app.route('/api/delete_word', methods=['post'])
def delete_word():
    word_receive = request.form["word_give"]
    db.words.delete_one({"word": word_receive})
    return jsonify({'result': 'success', 'msg' : '글 삭제'})



#################################################

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)