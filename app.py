from flask import Flask, render_template, request, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = "airi"


@app.route('/regist')
def regist_get():
    return render_template("regist.html")

@app.route('/regist' , methods=["POST"])
def regist_post():
    input_name = request.form.get("member_name")
    input_password = request.form.get("member_password")

    # flasktest.dbに接続
    conn = sqlite3.connect("flasktest.db")
    # DBの中を操作できるようにする
    c = conn.cursor()
    # SQLを実行（DBから値を取得）
    c.execute("insert into member values(null , ? , ?)",(input_name, input_password))
    # DBの変更内容保存する
    conn.commit()
    # DBとの接続を終える
    c.close()

    return "アカウント登録完了！"

@app.errorhandler(404)
def page_not_found(error):
    return "お探しのページは見つかりませんでした"

if __name__ == "__main__":
    app.run(debug=True)
    # 開発者モードで起動！！

