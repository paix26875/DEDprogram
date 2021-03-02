# 命名規則

Python_Labの開発ルールを書いていく。

PEP8を基に作成
[Python命名規則（PEP8より)](https://qiita.com/shiracamus/items/bc3bdfc206b39e0a75b2)

## 使用頻度低め

|用途 |命名規則|
|:-:|:-:|
|非公開、プライベート|先頭にアンダースコアを1個つける（外部からアクセスしないルール・約束事。外部からアクセスは可能）ローカル変数は元々非公開なのでつけない|
|サブクラスでの名前衝突回避|先頭にアンダースコアを2個つける（特殊なクラス名を付与して外部からアクセス可能）|
|特殊プロパティ、特殊メソッド|前後にアンダースコアを2個つける（言語仕様で用意されているので自分で新規定義しないこと）|
|予約語や組込み関数名と衝突回避|最後にアンダースコアを1個つける|
|インスタンスメソッドの第一引数|常に self|
|クラスメソッドの第一引数|常に cls|

## 使用頻度高め

|用途|命名規則|
|:-:|:-:|
|パッケージ|全て小文字の短い名前、アンダースコアは使わない|
|モジュール|全て小文字の短い名前、アンダースコアで区切ってもよい|
|クラス、例外|CapWords方式 （先頭だけ大文字の単語を繋げる、アンダースコアは使わない）|
|関数、メソッド|小文字のみ、必要に応じて単語をアンダースコアで区切る|
|定数|大文字のみ、単語をアンダースコアで区切る通常、モジュールレベル（関数の外側）に書く|
|変数、引数|小文字のみ、必要に応じて単語をアンダースコアで区切る|
|1文字変数|l (小文字のエル)、O (大文字のオー)、I(大文字のアイ) は決して使わない (フォントによって数字の1、0と見分けがつかないため)|

## リーダブルコード

- 単語は省略しない（慣例的に省略して使われている名前はOK）
- 名前に情報・意味を込める（flag, check では何のフラグか、何をチェックしたどんな値か分からない）
- 名前で情報を伝えてコメント不要にする（コメントにはwhatではなくwhyを書く）
- 1文字変数は1画面で見渡せる範囲（25行以内）で使い終わる一時変数に使う

## パッケージとモジュール

[パッケージとモジュールについて](http://www.tohoho-web.com/python/module.html)

- モジュール（module）
  - スクリプトファイル
  - モジュール内のクラスや関数、変数はモジュール名.識別子で参照可能
- パッケージ（package）
  - モジュールを複数まとめたディレクトリ
  - __init__.pyという名前のファイルを持つ
  - __init__.pyにはパッケージの初期化処理を記述する
  - なければ空で良い
- インポート（import）
  - パッケージの中からモジュールや識別子をインポートする記法

```python
# import [パッケージ.]モジュール
import mypack1.mypack2.mymod
mypack1.mypack2.mymod.myfunc()

# from パッケージ import モジュール
from mypack1.mypack2 import mymod
mymod.myfunc()

# from パッケージ import *
from mypack1.mypack2 import *                # __all__の設定が必要
mymod.myfunc()

# from [パッケージ.]モジュール import 識別子
from mypack1.mypack2.mymod import myfunc
myfunc()

# from [パッケージ.]モジュール import *
from mypack1.mypack2.mymod import *
myfunc()
```

上記の例で「from パッケージ import *」の形式を用いるには、mypack2 パッケージの __init__.py ファイルに読み込み対象のモジュールリストを __all__ に定義しておく必要があります

```python
__all__ = ["mymod"]

```

__name__ は、現在のモジュール名を示します。スクリプトとして起動されたメインモジュールの場合は __main__ という名前が設定されます。下記の例は、ファイルが python コマンドから直接起動された場合のみ実行する処理を記載しています。

```python
if __name__ == "__main__":
    test()
```

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