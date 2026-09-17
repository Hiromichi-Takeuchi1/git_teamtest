from flask import Flask, render_template
from data import ORDERS

app = Flask(__name__)

menu = {
    "D01": {"name": "ブレンドコーヒー", "price": 400},
    "D02": {"name": "アイスコーヒー", "price": 450},
    "D03": {"name": "カフェオレ", "price": 500},
    "D04": {"name": "紅茶", "price": 400},
    "D05": {"name": "オレンジジュース", "price": 350},
    "F01": {"name": "ナポリタン", "price": 900},
    "F02": {"name": "ミートソース", "price": 950},
    "F03": {"name": "カレーライス", "price": 850},
    "F04": {"name": "ミックスサンド", "price": 750},
    "F05": {"name": "グラタン", "price": 900},
    "S01": {"name": "チーズケーキ", "price": 500},
    "S02": {"name": "ショートケーキ", "price": 550},
    "S03": {"name": "プリン", "price": 450},
    "S04": {"name": "バニラアイス", "price": 400},
    "S05": {"name": "パンケーキ", "price": 650},
}


@app.route("/menu")
def show_menu():
    return render_template("menu.html", menu=menu)


@app.route("/staff")
def show_staff():
    return render_template("staff.html", orders=ORDERS)


# ---- B(八木) カート・注文の窓口をつなぐ。ここは3行だけ ----
app.secret_key = "sunaba-renshu"       # カートの中身を覚えるのに必要（練習用の合言葉）
from routes_b import bp as bp_b        # noqa: E402  B の窓口は routes_b.py にある
app.register_blueprint(bp_b)


if __name__ == "__main__":
    app.run(debug=True)