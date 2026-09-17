# 注文の伝票置き場。B(八木) が書き込み、C が読んで状態を変える。
# ※ サーバーを止めると消える。練習用なのでこれで十分。
# ※ 商品の表(menu)は app.py にある（A の担当）。ここには置かない。

# 注文の「状態」はこの3つだけ使う
STATUS_LIST = ["受付", "作り中", "できあがり"]

# 注文 1件の形:
# {
#   "orderId": 1,                      注文番号
#   "items": [                         頼んだ商品と数
#       {"id": "D01", "name": "ブレンドコーヒー", "price": 400, "qty": 2},
#   ],
#   "total": 800,                      合計金額
#   "createdAt": "10:05",              注文した時刻
#   "status": "受付",                  状態
# }

# ダミーの注文。C の人がこれを使って店員画面を作れる。
ORDERS = [
    {
        "orderId": 1,
        "items": [
            {"id": "D01", "name": "ブレンドコーヒー", "price": 400, "qty": 2},
            {"id": "S03", "name": "プリン", "price": 450, "qty": 1},
        ],
        "total": 1250,
        "createdAt": "10:05",
        "status": "受付",
    },
    {
        "orderId": 2,
        "items": [
            {"id": "F03", "name": "カレーライス", "price": 850, "qty": 1},
        ],
        "total": 850,
        "createdAt": "10:12",
        "status": "作り中",
    },
]


def next_order_id():
    """次の注文番号（今ある最大＋1）"""
    if not ORDERS:
        return 1
    return max(o["orderId"] for o in ORDERS) + 1
