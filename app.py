from flask import Flask, render_template, request, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = "airi"


@app.route('/regist')
def regist_get():
    return render_template("regist.html")

@app.route('/regist' , methods=["POST"])
def regist_post():
    input_password = request.form.get("member_password")
    input_name = request.form.get("member_name")
    input_syumi = request.form.get("member_syumi")
    input_location = request.form.get("member_location")
    input_age = request.form.get("member_age")
    
    # flasktest.dbに接続
    conn = sqlite3.connect("airi.db")
    # DBの中を操作できるようにする
    c = conn.cursor()
    # SQLを実行（DBから値を取得）
    c.execute("insert into users values(null , ? , ? , ? , ? ,? )",(input_password, input_name ,input_syumi , input_location, input_age))
    # DBの変更内容保存する
    conn.commit()
    # DBとの接続を終える
    c.close()

    return "アカウント登録完了！"

@app.route('/login')
def login_get():
    return render_template("login.html")

@app.route('/login' , methods=["POST"])
def login_post():
    input_name = request.form.get("member_name")
    input_password = request.form.get("member_password")

    # flasktest.dbに接続
    conn = sqlite3.connect("airi.db")
    # DBの中を操作できるようにする
    c = conn.cursor()
    # SQLを実行（DBから値を取得）
    c.execute("select id from users where name = ? and password = ?",(input_name, input_password))
    # 取得した値を変数に代入
    user_id = c.fetchone()
    # DBとの接続を終える
    c.close()
    # DBから値が取れているかターミナル上で確認
    print(user_id)

    if user_id is None:
        return render_template("login.html")
    else:
        session["user_id"] = user_id[0]
        return redirect("/search")


@app.route('/result')
def result_list():
    if "user_id" in session:
        # flasktest.dbに接続
        conn = sqlite3.connect("airi.db")
        # DBの中を操作できるようにする
        c = conn.cursor()
        # SQLを実行（DBから値を取得）
        user_id_py = session["user_id"]
        c.execute("select * from users where id = ?",(user_id_py,))
        user_name = c.fetchall()

        # c.execute("select id , name from users where userid = ?", (user_id_py,))
        # 取得した値を変数に代入
        task = [] #リストとして宣言
        for item in c.fetchall(): #全てのデータを辞書型に整形
            task.append({"id" : item[0], "task" : item[1]})
        # DBとの接続を終える
        c.close()
        # DBから値が取れているかターミナル上で確認
        print(task)

        return render_template("result.html", tpl_task = task , tpl_user_name = user_name)
    else:
        return redirect("/login")


@app.errorhandler(404)
def page_not_found(error):
    return "お探しのページは見つかりませんでした"

if __name__ == "__main__":
    app.run(debug=True)
    # 開発者モードで起動！！

