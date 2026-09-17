# B(八木) の窓口: カート画面と注文。
# カートの中身はブラウザごとの「session」に覚えさせる。形は {"D01": 2, "F03": 1} のように 商品ID → 数。
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from data import ORDERS, next_order_id

bp = Blueprint("b", __name__)


def get_menu():
    """app.py にある商品表(menu)を借りる。読み込み順の都合で関数の中で import する"""
    from app import menu
    return menu


def get_cart():
    """session からカートを取り出す。無ければ空"""
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart


def cart_rows(cart):
    """カート {"D01": 2} を、画面に出しやすい行の一覧に直す"""
    menu = get_menu()
    rows = []
    for item_id, qty in cart.items():
        item = menu.get(item_id)
        if item is None:
            continue
        rows.append({"id": item_id, "name": item["name"], "price": item["price"],
                     "qty": qty, "subtotal": item["price"] * qty})
    return rows


@bp.route("/cart")
def cart():
    """カート画面"""
    rows = cart_rows(get_cart())
    total = sum(r["subtotal"] for r in rows)
    return render_template("cart.html", rows=rows, total=total, menu=get_menu(),
                           message=request.args.get("message"))


@bp.route("/cart/add", methods=["POST"])
def cart_add():
    """カートに入れる。A のメニュー画面のボタンからも、これを呼べばよい。
    フォームで送る: id=D01（qty は省略すると1）"""
    item_id = request.form.get("id")
    qty = int(request.form.get("qty", 1))
    if item_id in get_menu() and qty > 0:
        cart = get_cart()
        cart[item_id] = cart.get(item_id, 0) + qty
        save_cart(cart)
    return redirect(url_for("b.cart"))


@bp.route("/cart/change", methods=["POST"])
def cart_change():
    """数を 1 増やす／減らす。0 になったら消える。フォームで送る: id=D01, delta=1 または -1"""
    item_id = request.form.get("id")
    delta = int(request.form.get("delta", 0))
    cart = get_cart()
    if item_id in cart:
        cart[item_id] += delta
        if cart[item_id] <= 0:
            del cart[item_id]
        save_cart(cart)
    return redirect(url_for("b.cart"))


@bp.route("/cart/remove", methods=["POST"])
def cart_remove():
    """1品まるごと消す。フォームで送る: id=D01"""
    cart = get_cart()
    cart.pop(request.form.get("id"), None)
    save_cart(cart)
    return redirect(url_for("b.cart"))


@bp.route("/order", methods=["POST"])
def order():
    """「注文する」。カートの中身を伝票(ORDERS)に積んで、カートを空にする"""
    rows = cart_rows(get_cart())
    if not rows:
        return redirect(url_for("b.cart", message="カートが空です"))
    order = {
        "orderId": next_order_id(),
        "items": [{"id": r["id"], "name": r["name"], "price": r["price"], "qty": r["qty"]} for r in rows],
        "total": sum(r["subtotal"] for r in rows),
        "createdAt": datetime.now().strftime("%H:%M"),
        "status": "受付",
    }
    ORDERS.append(order)
    save_cart({})
    return redirect(url_for("b.cart", message=f"注文しました（注文番号 {order['orderId']}）"))


@bp.route("/api/orders")
def api_orders():
    """注文の一覧を JSON で返す。C の店員画面が使える（画面で直接 ORDERS を import してもよい）"""
    return jsonify(ORDERS)
