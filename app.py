from flask import *
import db
import os
import uuid
from werkzeug.utils import secure_filename

getdata = {}
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/")

app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True



ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
app.config['UPLOAD_FOLDER'] = './static/image/'

# 判斷格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS

@app.route("/")
def testindex():
    return render_template("index.html")

@app.route("/up_index",methods=["POST", "GET", "PATCH", "DELETE"])
def upindex():
    # print("request",request.form) #ImmutableMultiDict([('uptext', 'text')])
    # print("request",request.files) #ImmutableMultiDict([('upfile', <FileStorage: '螢幕擷圖.png' ('image/png')>)])
    text = file = None

    # 只有文字
    if len(request.files) == 0:
        text = request.form['uptext']
        print("文字訊息",text)
        db.uptords(text, file)
    else:
        # 文 + 圖
        file = request.files['upfile']
        text = request.form['uptext']

        if file and allowed_file(file.filename):
            # secure_filename方法清除中文，取後綴
            file_name_hz = secure_filename(file.filename).split('.')[-1]
            # uuid 生成唯一名稱
            first_name = str(uuid.uuid4())
            # 文件名
            file_name = first_name + '.' + file_name_hz
            # 保存路徑
            file_path = app.config['UPLOAD_FOLDER']
            # 檢查路徑
            if not os.path.exists(file_path):
	            os.makedirs(file_path)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            db.uptords(text,file_name)
    return Response(json.dumps({"message": "上傳成功"}, sort_keys=False), mimetype='application/json')


@app.route("/api/load_message")
def testindexapi():
    data = db.loadtords()
    return Response(json.dumps({"data": data}, sort_keys=False), mimetype='application/json')

app.run(port=3000, debug=True)
# app.run(host="0.0.0.0", port=3000)