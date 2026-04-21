チュートリアル：https://docs.djangoproject.com/ja/6.0/intro/tutorial01/
モデル参考：https://qiita.com/kotayanagi/items/3cfadae951c407ac044a
vue+Django参考：：https://qiita.com/ryo-keima/items/aaa3f65524241a418fc9
API設計書：https://hackmd.io/@rLRaaRcwSX-7C_ch87eUvA

デザイン：https://www.figma.com/make/u6NuPNF76PRqfinYNA9Yy0/Adult-Video-Genre-Search-UI?t=zQchJOo5QmWKjeWM-0

## DMM API
- フロアAPI：https://api.dmm.com/affiliate/v3/FloorList?api_id=B4gzyyeG7yB3gDWX4uCS&affiliate_id=okd0405-990&output=json
- メーカー検索：https://api.dmm.com/affiliate/v3/MakerSearch?api_id=B4gzyyeG7yB3gDWX4uCS&affiliate_id=okd0405-990&floor_id=43&output=json
- シリーズ検索：https://api.dmm.com/affiliate/v3/SeriesSearch?api_id=B4gzyyeG7yB3gDWX4uCS&affiliate_id=okd0405-990&floor_id=43&output=json
- ジャンル検索：https://api.dmm.com/affiliate/v3/GenreSearch?api_id=B4gzyyeG7yB3gDWX4uCS&affiliate_id=okd0405-990&floor_id=43&output=json
- 作品取得：https://api.dmm.com/affiliate/v3/ItemList?api_id=B4gzyyeG7yB3gDWX4uCS&affiliate_id=okd0405-990&floor_id=43&output=json

## マスターデータ
### シーダー手順
- カテゴリ：python manage.py seeder_categories
- 大ジャンル：python manage.py seeder_major_janre
- 中ジャンル：python manage.py seeder_midium_genre

### バッチ処理
- DMMデータ取得
    - 作品データ
        - JSON、CSV出力
            - 全て取得：python manage.py import_dmm_initial
            - 年指定で取得：python manage.py import_dmm_initial --only-year 2024
            - 年月指定で取得：python manage.py import_dmm_initial --only-year 2024 --only-month 2
    - 女優取得
        - python manage.py import_dmm_actress --initial そ　// イニシャルははマストで指定
    - メーカー情報取得
        - python manage.py import_dmm_maker
    - シリーズ取得
        - python manage.py import_dmm_series
    - ジャンル情報取得
        - python manage.py import_dmm_genre
    - 作品情報取得
        - python manage.py import_dmm_works --only-year 2025 --dry-run


## テーブル情報更新手順
1. モデルを更新
2. ' python manage.py makemigrations adaken '
    ⇨自動でモデルの差分からマイグレーションファイルを作成
3. python manage.py migrate

ローカルadmin
user：admin
password：password

アドミンユーザー作成

''
python manage.py createsuperuser
''

リスト
- DB関係
    - modelファイル作成
    - マイグレーションファイル作成
    - seederファイル作成

- BE

- batch
    - 初期設定
        - 女優情報取得
        - メーカー、レーベル情報取得
        - 作品情報取得
    - 作品情報取得
    - 投稿データ集約


### デザインシステム

```
src/
├─ assets/
│  └─ styles/
│     ├─ tokens/
│     │  ├─ _theme.scss          # CSS変数（色/角丸/影などのテーマ定義）
│     │  ├─ _scale.scss          # SCSS変数（余白/文字サイズなどのスケール）
│     │  ├─ _breakpoints.scss    # ブレイクポイント
│     │  └─ _index.scss          # tokens の集約（@forward）
│     ├─ tools/
│     │  ├─ _media.scss          # レスポンシブmixin
│     │  ├─ _mixins.scss         # 汎用mixin（focus-ring等）
│     │  └─ _index.scss          # tools の集約（@forward）
│     ├─ base/
│     │  ├─ _reset.scss          # reset（最小）
│     │  ├─ _base.scss           # body等の全体スタイル
│     │  └─ _index.scss          # base の集約（@forward）
│     └─ main.scss               # アプリ全体で一回だけ読み込む
│
├─ components/
│  └─ base/
│     ├─ BaseButton.vue          # 共通ボタン（chip/primary等）
│     ├─ BaseCard.vue            # 共通カード
│     ├─ BaseFab.vue             # 右上/中央に出る丸いアクションボタン
│     └─ BaseDivider.vue         # 区切り線（必要なら）
│
├─ pages/
│  └─ Top/
│     ├─ TopPage.vue             # 添付画像のトップページ
│     └─ TopPage.scss            # ページ固有（レイアウト中心）
│
├─ router/
│  └─ index.js                   # Vue Router ルーティング
│
├─ App.vue                       # ルートコンポーネント（<router-view/>）
└─ main.js                       # createApp + router + main.scss 読み込み
```


バッチ処理
- マスターシーダー
    - カテゴリーテーブル：python manage.py categories_seeder

- DMMデータ取得
    - 作品データ
        - JSON、CSV出力
            - 全て取得：python manage.py import_dmm_initial
            - 年指定で取得：python manage.py import_dmm_initial --only-year 2024
            - 年月指定で取得：python manage.py import_dmm_initial --only-year 2024 --only-month 2
    - 女優取得
        - python manage.py import_dmm_actress_initial --out actresses.jsonl --initials あいうえお
    - メーカー情報取得
        - python manage.py import_dmm_maker
    - ジャンル情報取得
        - python manage.py import_dmm_genre


テーブル情報更新次
1. モデルを更新
2. ' python manage.py makemigrations adaken '
    ⇨自動でモデルの差分からマイグレーションファイルを作成
3. python manage.py migrate

### API実装箇所
例）work
- URL追加：app/adaken/urls.py
- シリアライザー追加：app/adaken/serializers/work_serializers.py
    - 初期追加時のみ
- views追加：app/adaken/views/work_views.py
    - 検索条件の追加等はここで行う