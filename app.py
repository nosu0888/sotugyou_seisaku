import os
# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import *
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'sunabakoza'

from datetime import datetime

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/result')
# def result():
#     return render_template('result.html')

# @app.route("/result")
# def result():
    
#     conn = sqlite3.connect('service.db')
#     c = conn.cursor()
#     c.execute("select * from user")
#     user_result = c.fetchall()
#     conn.close()
#     return render_template("result.html", tpl_user_result=user_result)





# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
# @app.route('/register',methods=["GET", "POST"])
# def register():
#     #  登録ページを表示させる
#     if request.method == "GET":
#         if 'user_id' in session :
#             return redirect ('/bbs')
#         else:
#             return render_template("register.html")

#     # ここからPOSTの処理
#     else:
#         # 登録ページで登録ボタンを押した時に走る処理
#         name = request.form.get("name")
#         password = request.form.get("password")
#         addrss = request.form.get("addrss")
#         age = request.form.get("age")
#         sex = request.form.get("sex")
#         hobby1 = request.form.get("hobby1")
#         hobby2 = request.form.get("hobby2")

#         conn = sqlite3.connect('service.db')
#         c = conn.cursor()
#         # 課題4の答えはここ
#         c.execute("insert into user values(null,?,?,?,?,?,?,?)", (name,password,addrss,age,sex,hobby1,hobby2))
#         conn.commit()
#         conn.close()
#         return redirect('/login')

#川満追加
@app.route("/register")
def regist_get():
    return render_template("register.html")

@app.route("/register", methods=["post"])
def register_post():

    upload = request.files['avatar']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'png,jpg,jpeg形式のファイルを選択してください'
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)

    input_name = request.form.get("name")
    input_password = request.form.get("password")
    input_address = request.form.get("address")
    input_age = request.form.get("age")
    input_sex = request.form.get("sex")
    input_hobby_1 = request.form.get("hobby_1")
    input_hobby_2 = request.form.get("hobby_2")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("insert into user values(null, ?,?,?,?,?,?,?,?)",(input_name,input_password,input_address,input_age,input_sex,input_hobby_1,input_hobby_2,filename))
    conn.commit()
    c.close()

    return redirect("/search")

@app.route("/mypage")
def mypage_get():
    return render_template("mypage.html")














# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         if 'user_id' in session :
#             return redirect("/bbs")
#         else:
#             return render_template("login.html")
#     else:
#         # ブラウザから送られてきたデータを受け取る
#         name = request.form.get("name")
#         password = request.form.get("password")

#         # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
#         # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
#         conn = sqlite3.connect('service.db')
#         c = conn.cursor()
#         c.execute("select id from user where name = ? and password = ?", (name, password) )
#         user_id = c.fetchone()
#         conn.close()
#         # DBから取得してきたuser_id、ここの時点ではタプル型
#         print(type(user_id))
#         # user_id が NULL(PythonではNone)じゃなければログイン成功
#         if user_id is None:
#             # ログイン失敗すると、ログイン画面に戻す
#             return render_template("login.html")
#         else:
#             session['user_id'] = user_id[0]
#             return redirect("/bbs")


@app.route("/logout")
def logout():
    session.pop('user_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return render_template("index.html")


@app.route('/bbs')
def bbs():
    if 'user_id' in session :
        user_id = session['user_id']
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
        c.execute("select name,prof_img from user where id = ?", (user_id,))
        # fetchoneはタプル型
        user_info = c.fetchone()
        # user_infoの中身を確認

        # 課題1の答えはここ del_flagが0のものだけ表示する
        # 課題2の答えはここ 保存されているtimeも表示する
        c.execute("select id,comment,time from bbs where userid = ? and del_flag = 0 order by id", (user_id,))
        comment_list = []
        for row in c.fetchall():
            comment_list.append({"id": row[0], "comment": row[1], "time":row[2]})

        c.close()
        return render_template('bbs.html' , user_info = user_info , comment_list = comment_list)
    else:
        return redirect("/login")



@app.route('/add', methods=["POST"])
def add():
    user_id = session['user_id']

    # 課題2の答えはここ 現在時刻を取得
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    # POSTアクセスならDBに登録する
    # フォームから入力されたアイテム名の取得(Python2ならrequest.form.getを使う)
    comment = request.form.get("comment")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # 現在の最大ID取得(fetchoneの戻り値はタプル)

    # 課題1の答えはここ null,?,?,0の0はdel_flagのデフォルト値
    # 課題2の答えはここ timeを新たにinsert
    c.execute("insert into bbs values(null,?,?,0,?)", (user_id, comment,time))
    conn.commit()
    conn.close()
    return redirect('/bbs')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' in session :
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select comment from bbs where id = ?", (id,) )
        comment = c.fetchone()
        conn.close()

        if comment is not None:
            # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
            comment = comment[0] # "りんご" ○   ("りんご",) ☓
            # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
        else:
            return "アイテムがありません" # 指定したIDの name がなければときの対処

        item = { "id":id, "comment":comment }

        return render_template("edit.html", comment=item)
    else:
        return redirect("/login")


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@app.route("/edit")
def update_item():
    if 'user_id' in session :
        # ブラウザから送られてきたデータを取得
        item_id = request.args.get("item_id") # id
        print(item_id)
        item_id = int(item_id) # ブラウザから送られてきたのは文字列なので整数に変換する
        comment = request.args.get("comment") # 編集されたテキストを取得する

        # 既にあるデータベースのデータを送られてきたデータに更新
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
        conn.commit()
        conn.close()

        # アイテム一覧へリダイレクトさせる
        return redirect("/bbs")
    else:
        return redirect("/login")

@app.route('/del' , methods=["POST"])
def del_task():
    id = request.form.get("comment_id")
    id = int(id)
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # 指定されたitem_idを元にDBデータを削除せずにdel_flagを1にして一覧からは表示しないようにする
    # 課題1の答えはここ del_flagを1にupdateする
    c.execute("update bbs set del_flag = 1 where id=?", (id,))
    conn.commit()
    conn.close()
    # 処理終了後に一覧画面に戻す
    return redirect("/bbs")

# #課題4の答えはここ
# @app.route('/upload', methods=["POST"])
# def do_upload():
#     # bbs.tplのinputタグ name="upload" をgetしてくる
#     upload = request.files['upload']
#     # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
#     if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         return 'png,jpg,jpeg形式のファイルを選択してください'
    
#     # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
#     save_path = get_save_path()
#     # パスが取得できているか確認
#     print(save_path)
#     # ファイルネームをfilename変数に代入
#     filename = upload.filename
#     # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
#     upload.save(os.path.join(save_path,filename))
#     # ファイル名が取れることを確認、あとで使うよ
#     print(filename)
    
#     # アップロードしたユーザのIDを取得
#     user_id = session['user_id']
#     conn = sqlite3.connect('service.db')
#     c = conn.cursor()
#     # update文
#     # 上記の filename 変数ここで使うよ
#     c.execute("update user set prof_img = ? where id=?", (filename,user_id))
#     conn.commit()
#     conn.close()

#     return redirect ('/bbs')



@app.route('/search')
def search_get():

    return render_template("search.html")

@app.route("/result", methods=["POST"])
def search():
    # ブラウザから送られてきたデータを受け取る
    hobby = request.form.get("hobby")
    address = request.form.get("address")
    age = request.form.get("age")

    # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
    # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute(
        "select * from user where hobby_1 = ? or hobby_2 = ? or address = ? or age = ?", (hobby, hobby, address, age))
    user_result = c.fetchall()
    conn.close()
    # DBから取得してきたuser_id、ここの時点ではタプル型
    # print(type(user_id))

    # user_id が NULL(PythonではNone)じゃなければログイン成功
    # if user_id is None:
    #     # ログイン失敗すると、ログイン画面に戻す
    #     return render_template("login.html")
    # else:
    #     session['user_id'] = user_id[0]
    #     return redirect("/userlist")
    print(user_result)
    return render_template("result.html",tpl_user_result=user_result)

    








@app.route("/message")
def message():
    return render_template("message.html")



#画像表示にする
# @app.route('/upload',method=['POST'])
# def upload():
#     upload = request.files["upload"]
#     if not upload.filename.lower().endswith((".png",".jpg",".jpeg")):
#         return "png,jpg,jpeg形式ファイルを選択して下さい"
#     save_path = get_save_path()
#     print(save_path)

#     filename = upload.filename
#     upload.save(os.path.join(save_path,filename))
#     print(filename)

#     user_id = session["user_id"][0]
#     conn = sqlite3.connect("service.db")
#     c = conn.cursor()

#     c.execute("update user set prof_img =? where id = ?",(filename,user_id))
#     conn.commit()
#     c.close()
    # return redirect('/bbs')







    

#課題4の答えはここも
def get_save_path():
    path_dir = "./static/img"
    return path_dir


# ---------ここからchat機能---------

@app.route("/")
def jump():
    # ここにチャットルーム一覧をDBからとって、表示するプログラム
    return redirect("/login")


@app.route("/chatroom")
def chatroom_get():
    my_id = session["user_id"]
    # ここにチャットルーム一覧をDBからとって、表示するプログラム
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute(
        "select id, room from chat where user_id1 = ? or user_id2 = ?", (my_id, my_id))
    chat_list = c.fetchall()

    return render_template("/chatroom.html", tpl_chat_list=chat_list)


@app.route("/chatroom/<int:other_id>", methods=["POST"])
def chatroom_post(other_id):

    # まずはチャットルームがあるかchatidをとってくる
    my_id = session["user_id"]
    print(my_id)
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute(
        "select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
    chat_id = c.fetchone()

    print(chat_id)
    # なければ作成、あればスルー
    if chat_id == None:

        c.execute("select name from user where id = ?", (my_id,))
        myname = c.fetchone()[0]
        c.execute("select name from user where id = ?", (other_id,))
        othername = c.fetchone()[0]
        room = myname + "と" + othername + "のチャット"

        c.execute("insert into chat values(null,?,?,?)",
                  (my_id, other_id, room))
        conn.commit()
        c.execute(
            "select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
        chat_id = c.fetchone()
    conn.close()
    print(chat_id)
    return redirect("/chat/{}".format(chat_id[0]))


@app.route("/chat/<int:chatid>")
def chat_get(chatid):
    # ここにチャットをDBからとって、表示するプログラム
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute(
        "select chatmess.to_user, chatmess.from_user, chatmess.message, user.name from chatmess inner join user on chatmess.from_user = user.id where chat_id = ?", (chatid,))
    chat_fetch = c.fetchall()
    chat_info = []
    for chat in chat_fetch:
        chat_info.append(
            {"to": chat[0], "from": chat[1], "message": chat[2], "fromname": chat[3]})
    c.execute("select room from chat where id = ?", (chatid,))
    room_name = c.fetchone()[0]
    c.close()
    return render_template("chat.html", chat_list=chat_info, link_chatid=chatid, tpl_room_name=room_name)


@app.route("/chat/<int:chatid>", methods=["POST"])
def chat_post(chatid):
    # ここにチャットの送信ボタンが押されたときにDBに格納するプログラム
    my_id = session["user_id"]
    chat_message = request.form.get("input_message")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute(
        "select user_id1, user_id2 from chat where id = ?", (chatid,))
    chat_user = c.fetchone()
    print(chat_user)
    if my_id != chat_user[0]:
        to_id = chat_user[0]
    else:
        to_id = chat_user[1]
    print(to_id)
    c.execute("insert into chatmess values(null,?,?,?,?)",
              (chatid, to_id, my_id, chat_message))
    conn.commit()
    c.close()

    return redirect("/chat/{}".format(chatid))


@app.route("/userlist")
def chat():
    if "user_id" in session:
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select id, name from user")
        user_info = c.fetchall()
        conn.close()
        return render_template("userlist.html", tpl_user_info=user_info)
    else:
        redirect("/login")


@app.route("/login")
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # ブラウザから送られてきたデータを受け取る
    name = request.form.get("name")
    password = request.form.get("password")

    # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
    # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute(
        "select id from user where name = ? and password = ?", (name, password))
    user_id = c.fetchone()
    conn.close()
    # DBから取得してきたuser_id、ここの時点ではタプル型
    print(type(user_id))
    # user_id が NULL(PythonではNone)じゃなければログイン成功
    if user_id is None:
        # ログイン失敗すると、ログイン画面に戻す
        return redirect("/")
    else:
        session['user_id'] = user_id[0]
        return redirect("/search")


# ---------ここまでchat機能---------


@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'



@app.errorhandler(404)
def notfound(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run( host='0.0.0.0', port=80 , debug=True )

