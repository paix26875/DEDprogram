Python_Labの開発ルールを書いていく。

変数名はスネークケース
関数名はキャメルケース

関数のコメントはこれを参考にNumPyスタイルで書く
基本：https://qiita.com/simonritchie/items/49e0813508cad4876b5a
より詳細：https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

## 基本の書き方

関数の直下に書く
コメントは1行72文字までに収める
```
def get_fruit_price():
    """
    果物の値段を取得する。
    """

    pass
```

## 引数の書き方

1. Parametersを記載
2. Parametersの下にハイフンを追加して区切る
3. 引数名：型の形式で記載
4. 引数名の下にインデントを加えて引数の内容を記載

```python
def get_fruit_price(fruit_id):
    """
    果物の値段を取得する。

    Parameters
    ----------
    fruit_id : int
        対象の果物のマスタID。
    location_id : int
        対象地域のマスタID。
    """
    pass
```

## 返り値の書き方

引数のParametersをReturnsに変更するだけ

```python
def get_fruit_price(fruit_id, location_id):
    """
    果物の値段を取得する。

    Parameters
    ----------
    fruit_id : int
        対象の果物のマスタID。
    location_id : int
        対象地域のマスタID。

    Returns
    -------
    fruit_price : int
        対象の果物の値段。
    consumption_tax : int
        消費税値。
    """
    # ...関数内容省略。
    return fruit_price, consumption_tax
```

