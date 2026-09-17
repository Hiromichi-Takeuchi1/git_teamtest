# 動かし方（全員共通）

## 最初の1回だけ

```bash
python3 -m venv .venv
.venv/bin/pip install flask
```
Windows は `.venv\Scripts\pip install flask`。

## 毎回

```bash
.venv/bin/python app.py
```
Windows は `.venv\Scripts\python app.py`。

ブラウザで開く:
- http://127.0.0.1:5000/menu … メニュー（A）
- http://127.0.0.1:5000/cart … カート（B）
- http://127.0.0.1:5000/api/orders … 注文の一覧（C が使う）

止めるときは黒い画面で Ctrl + C。赤いエラーが出たら、そのままコピーして貼ってください。
