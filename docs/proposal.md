# 砂場珈琲 注文アプリ つなぎ方の提案（Bの八木より）

A のメニュー画面と app.py はもう main に入っているので、それに合わせる形で書きます。

## 全体の絵

```
A メニュー画面 ──「カートに入れる」──▶ B カート ──「注文する」──▶ 伝票置き場(data.py) ──▶ C 店員画面
   /menu                                /cart                         ORDERS              /staff
```

サーバー（Flask）が間にいるので、お客さんのスマホと店員さんのパソコンが別でも注文が届きます。

## ファイルの分け方（自分のファイルだけ触ればぶつからない）

| 担当 | ファイル |
|---|---|
| A | `app.py` の menu（商品の表）、`templates/menu.html` |
| B | `routes_b.py`、`data.py`、`templates/cart.html` |
| C | `routes_c.py`（これから作る）、`templates/staff.html` |

`app.py` は A のものです。B と C は「自分の窓口をつなぐ2〜3行」だけ足します。

## つなぎ目（ここだけ合わせれば別々に作れる）

**A → B: メニューに「カートに入れる」ボタンを置く**
`menu.html` の各商品の行に、このフォームを足すだけでカートに入ります。

```html
<form method="post" action="/cart/add">
    <input type="hidden" name="id" value="{{ item_code }}">
    <button>カートに入れる</button>
</form>
```

**B → C: 注文の伝票は `data.py` の `ORDERS`**
1件の形はこうです。C はこれを読んで一覧にし、`status` を変えます。

```python
{"orderId": 1, "items": [{"id": "D01", "name": "ブレンドコーヒー", "price": 400, "qty": 2}],
 "total": 800, "createdAt": "10:05", "status": "受付"}
```

- `status` は `data.py` の `STATUS_LIST` にある「受付」「作り中」「できあがり」の3つだけ
- ダミーの注文を2件入れてあるので、C は B を待たずに画面を作れます
- JSON がほしければ `/api/orders` でも同じものが取れます

**C が app.py に足す行（B と同じ形）**
```python
from routes_c import bp as bp_c
app.register_blueprint(bp_c)
```

## 進め方
1. 自分のブランチで自分のファイルを作る。少しできたら Commit → Push
2. ひと区切りで Pull request。別の人が Merge
3. 全員 Pull して、つながるか試す

## 最初の目標
「メニューでブレンドコーヒーを押す → カートで注文する → 店員画面に出る」。見た目はあとで。

## 困ったら
「ここが分からない」とそのまま書いてください。エラーの赤い文字は消さずにコピーして貼ってください。
