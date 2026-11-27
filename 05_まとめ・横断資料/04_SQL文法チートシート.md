# SQL文法チートシート

> 科目A（旧午前）では毎回 **1〜2問** が SQL の結果や空欄を問う問題です。科目B（旧午後）の問6（データベース）では、直近8回のうち7回で SQL の空欄補充が出ています。
> 重要度：★★★（SELECT・結合・GROUP BY・副問合せ・NULL の扱い）／★★（集合演算・CASE・ウィンドウ関数・WITH）／★（DDL・DCL の細部）
> この資料は **構文の型 → 1行の例 → ひっかけ** を一覧にしたものです。例の結果はすべて SQLite で検算済みです。
> じっくり理解したいときは [データベース 5章 SQL](../01_テクノロジ系/06_データベース.md#5-sql) を、過去問の出方は [科目B 問6 データベース](../08_過去問解説/科目B/問06_データベース.md) を見てください。

## 目次

1. [例で使う表](#1-例で使う表)
2. [SELECT 文の型と実行順](#2-select-文の型と実行順)
3. [条件式（WHERE / HAVING）](#3-条件式where--having)
4. [結合（JOIN）](#4-結合join)
5. [集約関数と GROUP BY / HAVING](#5-集約関数と-group-by--having)
6. [副問合せ・EXISTS](#6-副問合せexists)
7. [集合演算（UNION / INTERSECT / EXCEPT）](#7-集合演算union--intersect--except)
8. [CASE・COALESCE などの式と関数](#8-casecoalesce-などの式と関数)
9. [ウィンドウ関数（OVER）](#9-ウィンドウ関数over)
10. [WITH（共通表式）と再帰問合せ](#10-with共通表式と再帰問合せ)
11. [データ更新（INSERT / UPDATE / DELETE）](#11-データ更新insert--update--delete)
12. [DDL（表・制約・ビュー・索引）](#12-ddl表制約ビュー索引)
13. [DCL・トランザクション制御](#13-dclトランザクション制御)
14. [NULL と3値論理のまとめ](#14-null-と3値論理のまとめ)
15. [科目B の空欄補充：要件 → 構文の早見表](#15-科目b-の空欄補充要件--構文の早見表)

---

## 1. 例で使う表

[データベース 5.0節](../01_テクノロジ系/06_データベース.md#50-この節で使うテーブル) と同じ表に、**上司番号** の列を足したものです。**山本さんは部門コードが NULL**、**企画部（D4）には社員がいない** 点が、ほとんどのひっかけの元になります。

**部門**

| <ins>部門コード</ins> | 部門名 |
|---|---|
| D1 | 営業部 |
| D2 | 開発部 |
| D3 | 総務部 |
| D4 | 企画部 |

**社員**（給与の単位は千円）

| <ins>社員番号</ins> | 氏名 | 部門コード | 給与 | 上司番号 |
|---|---|---|---|---|
| E01 | 佐藤 | D1 | 300 | NULL |
| E02 | 鈴木 | D1 | 250 | E01 |
| E03 | 高橋 | D2 | 400 | NULL |
| E04 | 田中 | D2 | 350 | E03 |
| E05 | 伊藤 | D2 | 280 | E04 |
| E06 | 渡辺 | D3 | 220 | NULL |
| E07 | 山本 | NULL | 200 | E03 |

---

## 2. SELECT 文の型と実行順

```sql
SELECT   [DISTINCT] 列や式 [AS 別名], …    -- ⑤ 列を選ぶ
  FROM   表 [相関名] [JOIN 表 ON 結合条件] -- ① 表を決める
 WHERE   行の条件                          -- ② 行を絞る（集約関数は使えない）
 GROUP BY 列, …                            -- ③ グループにまとめる
HAVING   グループの条件                    -- ④ グループを絞る（集約関数を使う）
 ORDER BY 列 [ASC | DESC], …               -- ⑥ 並べ替え（既定は ASC＝昇順）
```

| 覚えること | 内容 |
|---|---|
| 実行順 | **FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY** |
| 別名の使える場所 | SELECT で付けた別名は **ORDER BY では使える**が、WHERE では使えない（WHERE のほうが先に実行されるため） |
| `SELECT *` | すべての列 |
| `DISTINCT` | 結果の重複行を1行にまとめる |
| 先頭 n 行だけ | 標準 SQL は `FETCH FIRST 3 ROWS ONLY`、MySQL・PostgreSQL などは `LIMIT 3` |

⚠️ ORDER BY を書かないと、結果の並び順は **保証されません**。

---

## 3. 条件式（WHERE / HAVING）

| 書き方 | 意味 | 例の結果 |
|---|---|---|
| `=` `<>` `<` `<=` `>` `>=` | 比較（「等しくない」は `<>`。`!=` も使える製品が多い） | `部門コード <> 'D2'` → 3行（山本は入らない） |
| `AND` `OR` `NOT` | 論理演算。優先順位は **NOT ＞ AND ＞ OR** | |
| `BETWEEN a AND b` | a 以上 b 以下（**両端を含む**） | |
| `IN (値, …)` / `IN (副問合せ)` | どれかに一致 | |
| `LIKE 'パターン'` | `%` は0文字以上、`_` はちょうど1文字 | `氏名 LIKE '_藤'` → 佐藤、伊藤 |
| `IS NULL` / `IS NOT NULL` | NULL の判定 | `部門コード = NULL` は **0行**（`IS NULL` と書く） |
| `> ALL (副問合せ)` | すべての値より大きい（＝最大値より大きい） | `給与 > ALL (D1の給与)` → 高橋、田中 |
| `> ANY (副問合せ)` | どれか1つより大きい（＝最小値より大きい）。`SOME` も同じ意味 | |
| `EXISTS (副問合せ)` | 副問合せが1行以上返せば真 | [6章](#6-副問合せexists) |

💡 `x IN (a, b)` は `x = a OR x = b`、`x NOT IN (a, b)` は `x <> a AND x <> b` と同じです。NOT IN の落とし穴は [6章](#6-副問合せexists) を見てください。
💡 `%` や `_` という文字そのものを探すときは、`LIKE '10\%' ESCAPE '\'` のようにエスケープ文字を指定します。

---

## 4. 結合（JOIN）

```sql
SELECT S.氏名, B.部門名
  FROM 社員 S
  [INNER | LEFT OUTER | RIGHT OUTER | FULL OUTER] JOIN 部門 B
    ON S.部門コード = B.部門コード;

-- 古い書き方（内部結合と同じ結果）
SELECT S.氏名, B.部門名 FROM 社員 S, 部門 B WHERE S.部門コード = B.部門コード;
```

| 結合 | 残る行 | 例（社員 × 部門）の行数 |
|---|---|---|
| `INNER JOIN` | 両方に一致する行だけ | 6行（山本と企画部が消える） |
| `LEFT OUTER JOIN` | 左表の全行 ＋ 一致した右表（なければ NULL） | 部門 LEFT JOIN 社員 → 7行（企画部は社員が NULL） |
| `RIGHT OUTER JOIN` | 右表の全行 ＋ 一致した左表 | |
| `FULL OUTER JOIN` | 両方の全行 | 8行（山本と企画部の両方が残る） |
| `CROSS JOIN` | すべての組合せ（直積） | 4 × 7 ＝ 28行 |
| **自己結合** | 同じ表に別の相関名を付けて結合 | `社員 部下 LEFT JOIN 社員 上司 ON 部下.上司番号 = 上司.社員番号` |

- `OUTER` は省略でき、`LEFT JOIN` と書いても同じです。`INNER` も省略でき、`JOIN` だけなら内部結合です。
- `NATURAL JOIN`（同じ名前の列で自動的に結合する）や `JOIN … USING (部門コード)` という書き方もあります。

⚠️ 外部結合で、相手側の表の条件を **WHERE** に書くと、NULL の行が落ちて内部結合と同じ結果になります。相手側の絞込みは **ON の中**に書きます。

```sql
-- 「全部門と、その部門の給与300以上の社員」→ 条件は ON に書く
SELECT B.部門名, S.氏名
  FROM 部門 B LEFT JOIN 社員 S
    ON B.部門コード = S.部門コード AND S.給与 >= 300;
```

---

## 5. 集約関数と GROUP BY / HAVING

| 関数 | 意味 | NULL の扱い | 0行のとき |
|---|---|---|---|
| `COUNT(*)` | 行数 | NULL の行も数える | 0 |
| `COUNT(列)` | NULL でない値の個数 | 除く | 0 |
| `COUNT(DISTINCT 列)` | 異なる値の個数 | 除く | 0 |
| `SUM(列)` / `AVG(列)` | 合計 / 平均 | 除く（AVG は NULL を分母にも入れない） | **NULL** |
| `MAX(列)` / `MIN(列)` | 最大 / 最小 | 除く | **NULL** |

例：`SELECT COUNT(*), COUNT(部門コード), COUNT(DISTINCT 部門コード) FROM 社員` → **7, 6, 3**

```sql
-- 部門ごとの人数と給与合計（社員のいない部門も 0 で出す）
SELECT B.部門名, COUNT(S.社員番号) AS 人数, COALESCE(SUM(S.給与), 0) AS 給与計
  FROM 部門 B LEFT JOIN 社員 S ON B.部門コード = S.部門コード
 GROUP BY B.部門コード, B.部門名
 ORDER BY B.部門コード;
```

| 部門名 | 人数 | 給与計 |
|---|---|---|
| 営業部 | 2 | 550 |
| 開発部 | 3 | 1030 |
| 総務部 | 1 | 220 |
| 企画部 | 0 | 0 |

⚠️ ひっかけ：
- 上の例で `COUNT(*)` と書くと、企画部は **1** になります。外部結合で作られた NULL だけの行も1行と数えるからです。社員の人数を数えるなら `COUNT(S.社員番号)` と書きます。
- GROUP BY を使うとき、SELECT に書けるのは **GROUP BY に指定した列と集約関数だけ**です。
- `WHERE AVG(給与) > 250` は書けません。集約した値での絞込みは HAVING に書きます。
- GROUP BY がなくても HAVING は書けます。そのときは表全体が1つのグループとして扱われます。
- GROUP BY では、NULL どうしは **1つのグループ**にまとまります。

---

## 6. 副問合せ・EXISTS

| 種類 | 形 | 使う場所・注意 |
|---|---|---|
| **スカラ副問合せ** | `(SELECT AVG(給与) FROM 社員)` | 結果が **1行1列** の値。比較演算子の右辺や SELECT 句に書ける。2行以上返すとエラー |
| **IN 副問合せ** | `部門コード IN (SELECT …)` | 結果が1列で複数行 |
| **相関副問合せ** | `WHERE S1.給与 > (SELECT AVG(S2.給与) FROM 社員 S2 WHERE S2.部門コード = S1.部門コード)` | 外側の1行ごとに内側を実行する。内側から外側の相関名（S1）を参照するのが目印 |
| **EXISTS** | `WHERE EXISTS (SELECT * FROM 社員 S WHERE S.部門コード = B.部門コード)` | 1行でもあれば真。SELECT の列は何でもよい（`*` が慣例） |
| **FROM 句の副問合せ** | `FROM (SELECT …) AS T` | 導出表。名前（相関名）を付ける |

**「社員が1人もいない部門」の3つの書き方**

```sql
-- ○ NOT EXISTS（NULL があっても正しい）
SELECT 部門名 FROM 部門 B
 WHERE NOT EXISTS (SELECT * FROM 社員 S WHERE S.部門コード = B.部門コード);      -- → 企画部

-- ○ 外部結合して相手が NULL の行だけ残す
SELECT B.部門名 FROM 部門 B LEFT JOIN 社員 S ON B.部門コード = S.部門コード
 WHERE S.社員番号 IS NULL;                                                         -- → 企画部

-- × NOT IN（副問合せの結果に NULL が混ざると0行になる）
SELECT 部門名 FROM 部門
 WHERE 部門コード NOT IN (SELECT 部門コード FROM 社員);                            -- → 0行！
```

⚠️ 最後の NOT IN が0行になるのは、山本さんの NULL が副問合せの結果に入るからです。`'D4' <> NULL` が UNKNOWN になるので、どの行も真になりません。副問合せの中に `WHERE 部門コード IS NOT NULL` を足せば企画部が返ります。

💡 「すべての〜を満たす」（関係代数の **商**）は「満たさないものが存在しない」と言い換えて、**NOT EXISTS を二重**にして書きます。

---

## 7. 集合演算（UNION / INTERSECT / EXCEPT）

```sql
SELECT 部門コード FROM 部門
EXCEPT                       -- UNION / UNION ALL / INTERSECT / EXCEPT
SELECT 部門コード FROM 社員;  -- → D4
```

| 演算子 | 意味 | 例（部門の部門コード と 社員の部門コード） |
|---|---|---|
| `UNION` | 和集合。**重複を除く** | NULL, D1, D2, D3, D4 の5行 |
| `UNION ALL` | 和集合。**重複を残す**（そのまま縦に積む） | 4 ＋ 7 ＝ 11行 |
| `INTERSECT` | 積集合（両方にある行） | D1, D2, D3 |
| `EXCEPT` | 差集合（左にあって右にない行）。Oracle では `MINUS` | D4 |

- 左右の SELECT は、**列の数と型をそろえます**。結果の列名は左側の SELECT の名前になります。
- ORDER BY は最後に1回だけ書き、結果全体を並べ替えます。
- 集合演算では NULL どうしを同じ値として扱います（上の UNION で NULL が1行にまとまるのはそのためです）。

💡 JOIN は表を「横につなぐ」、UNION は「縦に積む」操作です。横持ちの表（第1期売上・第2期売上…の列）を縦持ちにするには、列ごとの SELECT を UNION ALL で積み重ねます。
💡 UNION は重複を除くために並べ替えなどの処理が増えます。重複が起きないと分かっていれば UNION ALL のほうが速いです。

---

## 8. CASE・COALESCE などの式と関数

| 式・関数 | 意味 | 例 |
|---|---|---|
| `CASE WHEN 条件 THEN 値 … ELSE 値 END` | 条件で値を切り替える（検索 CASE） | `CASE WHEN 給与 >= 300 THEN 'A' WHEN 給与 >= 250 THEN 'B' ELSE 'C' END` |
| `CASE 列 WHEN 値 THEN … END` | 値で切り替える（単純 CASE） | `CASE 部門コード WHEN 'D1' THEN '営業' … END` |
| `COALESCE(a, b, …)` | 最初の **NULL でない** 値を返す | `COALESCE(SUM(給与), 0)` → NULL なら 0 |
| `NULLIF(a, b)` | a ＝ b なら NULL、違えば a | `x / NULLIF(y, 0)`：0 で割るのを防ぐ |
| `CAST(式 AS 型)` | 型の変換 | `CAST(給与 AS DECIMAL(7,1))` |
| `文字列1 \|\| 文字列2` | 文字列の連結（標準 SQL。製品によっては `CONCAT()` や `+`） | `氏名 \|\| 'さん'` |
| `SUBSTRING(s FROM 開始 FOR 長さ)` | 部分文字列 | |
| `CURRENT_DATE` / `CURRENT_TIMESTAMP` | 現在の日付 / 日時 | |
| `EXTRACT(YEAR FROM 日付)` | 日付から年・月・日などを取り出す | |

**CASE を集約関数の中に入れて「条件つきで数える」**

```sql
SELECT SUM(CASE WHEN 給与 >= 300 THEN 1 ELSE 0 END) AS 高給与人数   -- → 3
  FROM 社員;
-- COUNT(CASE WHEN 給与 >= 300 THEN 1 END) でも 3（ELSE を省くと NULL になり、COUNT が数えない）
```

⚠️ CASE で ELSE を省略すると、どの WHEN にも当てはまらない行は **NULL** になります。

---

## 9. ウィンドウ関数（OVER）

集約しても **行を減らさずに**、各行に集計値や順位を付けます。GROUP BY との違いはここです。

```sql
関数名() OVER ( [PARTITION BY 区切る列]   -- グループ分け（省略すると全体で1つ）
                [ORDER BY 並べる列]       -- グループ内の順序
                [ROWS BETWEEN … AND …] )  -- 集計する範囲（ウィンドウ枠）
```

| 関数 | 意味 |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 … の連番（同じ値でも別の番号） |
| `RANK()` | 同順位があると次を飛ばす：1, 2, 2, **4** |
| `DENSE_RANK()` | 同順位があっても飛ばさない：1, 2, 2, **3** |
| `SUM()` `AVG()` `COUNT()` `MAX()` `MIN()` ＋ `OVER` | グループ内の合計・平均など（各行に付く） |
| `LAG(列, n)` / `LEAD(列, n)` | n 行前 / n 行後の値（n を省くと1） |

**例：部門内の給与順位と部門合計**

```sql
SELECT 氏名, 部門コード, 給与,
       SUM(給与) OVER (PARTITION BY 部門コード)                 AS 部門計,
       RANK()    OVER (PARTITION BY 部門コード ORDER BY 給与 DESC) AS 部門内順位
  FROM 社員;
```

| 氏名 | 部門コード | 給与 | 部門計 | 部門内順位 |
|---|---|---|---|---|
| 佐藤 | D1 | 300 | 550 | 1 |
| 鈴木 | D1 | 250 | 550 | 2 |
| 高橋 | D2 | 400 | 1030 | 1 |
| 田中 | D2 | 350 | 1030 | 2 |
| 伊藤 | D2 | 280 | 1030 | 3 |
| 渡辺 | D3 | 220 | 220 | 1 |
| 山本 | NULL | 200 | 200 | 1 |

→ 7行すべてが残ります（GROUP BY なら4行になります）。

**ウィンドウ枠（累計・移動平均）**

| 書き方 | 範囲 |
|---|---|
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | 先頭から現在の行まで（**累計**） |
| `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` | 6行前から現在の行までの7行（日次データなら **直近7日間の移動平均**） |
| `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` | 前後1行ずつを含む3行 |

- 例：`SUM(給与) OVER (ORDER BY 社員番号)` の結果は 300, 550, 950, 1300, 1580, 1800, 2000 です。
- ORDER BY だけを書いて枠を省略すると、既定は「先頭から現在の行まで」なので累計になります（正確には `RANGE` 指定なので、並べる値が同じ行はまとめて含まれます）。
- 同じウィンドウ指定を何度も使うときは、`WINDOW w AS (PARTITION BY … ORDER BY …)` と名前を付け、`RANK() OVER w` のように参照できます。

⚠️ ウィンドウ関数は SELECT 句（と ORDER BY）でしか使えません。WHERE で「順位が3位以内」と絞るには、副問合せか WITH で一度結果を作り、その外側で絞ります。

---

## 10. WITH（共通表式）と再帰問合せ

**WITH（共通表式、CTE）**：問合せの中だけで使う一時的な表に名前を付けます。長い副問合せを読みやすく分けられます。

```sql
WITH 部門平均 AS (
  SELECT 部門コード, AVG(給与) AS 平均 FROM 社員 GROUP BY 部門コード
)
SELECT S.氏名
  FROM 社員 S JOIN 部門平均 A ON S.部門コード = A.部門コード
 WHERE S.給与 > A.平均;          -- → 佐藤、高橋、田中
```

**WITH RECURSIVE（再帰問合せ）**：階層構造（組織、部品表、カテゴリの木）をたどります。

```sql
WITH RECURSIVE 部下 (社員番号, 氏名, 深さ) AS (
    SELECT 社員番号, 氏名, 0 FROM 社員 WHERE 社員番号 = 'E03'   -- ① 開始行（非再帰部）
  UNION ALL
    SELECT S.社員番号, S.氏名, 部下.深さ + 1                      -- ② 再帰部：1段下をたどる
      FROM 社員 S JOIN 部下 ON S.上司番号 = 部下.社員番号
)
SELECT * FROM 部下;
```

| 社員番号 | 氏名 | 深さ |
|---|---|---|
| E03 | 高橋 | 0 |
| E04 | 田中 | 1 |
| E07 | 山本 | 1 |
| E05 | 伊藤 | 2 |

- 再帰部が1行も返さなくなった時点で終わります。
- 開始行と再帰部をつなぐのは **UNION ALL** が定番です。
- 💡 見分け方：WITH で定義した名前（部下）を、その定義の中で自分自身として参照していたら再帰です。空欄には `WITH RECURSIVE` が入ります。

---

## 11. データ更新（INSERT / UPDATE / DELETE）

```sql
INSERT INTO 部門 (部門コード, 部門名) VALUES ('D5', '法務部');          -- 1行追加
INSERT INTO 部門 VALUES ('D6', '広報部'), ('D7', '経理部');              -- 複数行（列名を省くと全列を定義順に）
INSERT INTO 退職者 (社員番号, 氏名) SELECT 社員番号, 氏名 FROM 社員 WHERE …;  -- 問合せ結果を追加

UPDATE 社員 SET 給与 = 給与 * 1.1, 部門コード = 'D2' WHERE 社員番号 = 'E07';
UPDATE 社員 S SET 給与 = (SELECT MAX(給与) FROM 社員 WHERE 部門コード = S.部門コード)
 WHERE …;                                                                -- 相関副問合せで更新

DELETE FROM 社員 WHERE 社員番号 = 'E07';
```

| 文 | ポイント |
|---|---|
| `INSERT … SELECT` | VALUES の代わりに問合せ結果を入れる。列の数と型をそろえる |
| `UPDATE … SET` | 複数列はカンマで区切る。右辺は **更新前の値** で計算される |
| `DELETE FROM` | 行を削除する。表そのものは残る（表を消すのは `DROP TABLE`） |
| `MERGE INTO … USING … ON … WHEN MATCHED THEN UPDATE … WHEN NOT MATCHED THEN INSERT …` | あれば更新、なければ追加（製品によっては `INSERT … ON CONFLICT` など） |

⚠️ UPDATE や DELETE で WHERE を忘れると **全行** が対象になります。
⚠️ 参照制約がある場合、子の表から参照されている親の行の削除や更新は、参照動作の指定によって拒否されたり、子に波及したりします（[12章](#12-ddl表制約ビュー索引)）。

---

## 12. DDL（表・制約・ビュー・索引）

```sql
CREATE TABLE 社員 (
  社員番号   CHAR(3)     PRIMARY KEY,                 -- 列制約
  氏名       VARCHAR(20) NOT NULL,
  部門コード CHAR(2),
  給与       INTEGER     DEFAULT 0 CHECK (給与 >= 0),
  上司番号   CHAR(3),
  FOREIGN KEY (部門コード) REFERENCES 部門 (部門コード)  -- 表制約
    ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (上司番号) REFERENCES 社員 (社員番号)
);
```

**制約**

| 制約 | 意味 |
|---|---|
| `PRIMARY KEY` | 主キー。一意 ＋ NOT NULL。1表に1つ |
| `UNIQUE` | 重複不可。NULL は許す（複数の NULL も可とする製品が多い） |
| `NOT NULL` | NULL 不可 |
| `CHECK (条件)` | 条件を満たす値だけ許す。条件が UNKNOWN（NULL を含む）なら **通る** |
| `DEFAULT 値` | 値を指定しなかったときの既定値（制約ではなく列の既定値の指定） |
| `FOREIGN KEY (列) REFERENCES 表 (列)` | 外部キー（参照制約）。参照先にない値は入れられない（NULL は入れられる） |

💡 **複数列にまたがる制約**（`PRIMARY KEY (受注番号, 明細番号)` など）は、列定義とは別に書く **表制約** でしか書けません。

**参照動作**（親の行を削除・更新したときに子をどうするか）

| 指定 | 動作 |
|---|---|
| `CASCADE` | 子も一緒に削除・更新する |
| `SET NULL` | 子の外部キーを NULL にする |
| `SET DEFAULT` | 子の外部キーを既定値にする |
| `RESTRICT` / `NO ACTION` | 子が参照していれば親の操作を拒否する（指定しないときの既定は NO ACTION） |

**その他の DDL**

| 文 | 意味 |
|---|---|
| `ALTER TABLE 社員 ADD 入社日 DATE;` | 列の追加（`DROP COLUMN` で削除、`ADD CONSTRAINT` で制約の追加） |
| `DROP TABLE 社員;` | 表の削除（定義ごと消える） |
| `CREATE VIEW 開発部社員 AS SELECT … ;` | ビュー（仮想の表）の定義。集約・DISTINCT・GROUP BY・結合を含むビューは原則として更新できない |
| `CREATE INDEX 索引名 ON 社員 (部門コード);` | 索引の作成。検索は速くなるが、更新は遅くなる |
| `CREATE TRIGGER … AFTER UPDATE OF 給与 ON 社員 FOR EACH ROW …` | トリガ（更新をきっかけに自動で処理を実行） |

**データ型**：`CHAR(n)`（固定長）、`VARCHAR(n)`（可変長）、`INTEGER`・`SMALLINT`、`DECIMAL(p,s)`（全体 p 桁・小数 s 桁）、`REAL`・`FLOAT`、`DATE`・`TIME`・`TIMESTAMP`。詳しくは [データベース 5.1節](../01_テクノロジ系/06_データベース.md#51-ddlデータ定義-) にあります。

---

## 13. DCL・トランザクション制御

```sql
GRANT SELECT, UPDATE (給与) ON 社員 TO user01 [WITH GRANT OPTION];  -- 権限を与える（列単位も可）
REVOKE UPDATE ON 社員 FROM user01;                                   -- 権限を取り消す

SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;          -- 製品によっては BEGIN。省略して自動で始まる製品も多い
  UPDATE …;
  SAVEPOINT sp1;            -- 途中の時点に名前を付ける
  DELETE …;
  ROLLBACK TO SAVEPOINT sp1; -- sp1 の時点まで取り消す
COMMIT;                     -- 確定（ROLLBACK ならすべて取り消し）
```

| 権限 | 許される操作 |
|---|---|
| `SELECT` / `INSERT` / `UPDATE` / `DELETE` | 検索 / 追加 / 更新 / 削除 |
| `REFERENCES` | その表を外部キーの参照先にする |
| `ALL PRIVILEGES` | すべて |
| `WITH GRANT OPTION` | 受け取った権限を、さらに他人に与えられる |

**隔離性水準**（○＝起こり得る、×＝起こらない）

| 水準（`ISOLATION LEVEL`） | ダーティリード | ノンリピータブルリード | ファントムリード |
|---|---|---|---|
| `READ UNCOMMITTED` | ○ | ○ | ○ |
| `READ COMMITTED` | × | ○ | ○ |
| `REPEATABLE READ` | × | × | ○ |
| `SERIALIZABLE` | × | × | × |

💡 下の水準ほど安全ですが、待ちが増えて同時実行の性能は落ちます。詳しくは [データベース 6.7節](../01_テクノロジ系/06_データベース.md#67-隔離性水準-) にあります。

---

## 14. NULL と3値論理のまとめ

NULL との比較は **TRUE でも FALSE でもない UNKNOWN（不明）** になります。WHERE・ON・HAVING は **TRUE の行だけ** 残します。

| A | B | A AND B | A OR B |
|---|---|---|---|
| TRUE | UNKNOWN | UNKNOWN | **TRUE** |
| FALSE | UNKNOWN | **FALSE** | UNKNOWN |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

`NOT UNKNOWN` は UNKNOWN のままです。

| 場面 | NULL の扱い | 例の結果 |
|---|---|---|
| `列 = NULL`、`列 <> 'D2'` | UNKNOWN になり、行は残らない | `部門コード <> 'D2'` に山本は入らない |
| `IS NULL` / `IS NOT NULL` | 唯一の正しい判定方法 | |
| `NOT IN (… NULL …)` | 全体が真にならず **0行** | [6章](#6-副問合せexists) |
| 集約関数（`COUNT(*)` 以外） | NULL を無視する | AVG は NULL を除いた件数で割る |
| 0行に対する SUM / AVG / MAX / MIN | NULL を返す | `COALESCE(SUM(…), 0)` で 0 にする |
| 算術演算 | NULL を含むと結果も NULL | `給与 + NULL` → NULL |
| GROUP BY / DISTINCT / UNION | NULL どうしを同じ値として1つにまとめる | |
| CHECK 制約 | UNKNOWN なら違反にならない | `CHECK (給与 >= 0)` は給与 NULL を通す |
| ORDER BY | NULL を先頭に置くか末尾に置くかは製品による（`NULLS FIRST` / `NULLS LAST` で指定できる） | |

---

## 15. 科目B の空欄補充：要件 → 構文の早見表

問題文の要件や処理概要の言い回しから、入る構文を引きます。

| 問題文の要件・手がかり | 入りやすい構文 |
|---|---|
| 「〜が1件もない行も一覧に出す」「売上0の商品も表示」 | `LEFT OUTER JOIN` ＋ `COALESCE(…, 0)` |
| SELECT 句に `COALESCE(…, 0)` がある | 結合は外部結合を疑う |
| 「両方にあるものだけ」 | `INNER JOIN` / `INTERSECT` / `EXISTS` |
| 「〜が存在しない」「未登録の」 | `NOT EXISTS`（NULL が絡むなら NOT IN は避ける） |
| 「すべての〜を満たす」 | `NOT EXISTS` の二重 |
| 「〜ごとに集計」「〜別の件数」 | `GROUP BY` ＋ 集約関数 |
| 「合計が〜以上のグループだけ」 | `HAVING` |
| 「平均より大きい」「最大のものを」 | スカラ副問合せ `(SELECT AVG(…) …)`、`MAX` |
| 「自グループの平均より」 | 相関副問合せ |
| 「2つの結果を合わせて1つの一覧に」「縦に積む」 | `UNION ALL`（重複を除くなら `UNION`） |
| 「順位」「上位3件をグループごとに」 | `RANK()` / `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` |
| 「直近7日間の平均」「累計」 | `AVG / SUM … OVER (ORDER BY … ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` |
| 「前回との差」「前日比」 | `LAG(列) OVER (ORDER BY …)` |
| 「上位カテゴリから下位をすべてたどる」「階層」 | `WITH RECURSIVE … UNION ALL …` |
| 「条件によって表示を変える」「区分を付ける」 | `CASE WHEN … THEN … ELSE … END` |
| 「最大の連番＋1 で採番（まだなければ1）」 | `COALESCE(MAX(連番), 0) + 1` |
| 「親を削除したら子も削除」 | `ON DELETE CASCADE` |
| 「参照されている行は削除させない」 | `ON DELETE RESTRICT` / `NO ACTION` |
| 「同じ値の登録を防ぐ」 | `UNIQUE` 制約（`ALTER TABLE … ADD UNIQUE (…)`） |
| 「この利用者には参照だけ許す」 | `GRANT SELECT ON … TO …`（必要ならビューに対して） |

💡 空欄を埋めたら、例の表のように **NULL の行**と **相手のいない行**を1つずつ想定して、結果に残るか消えるかを確かめると取りこぼしが減ります。

---

## 参考

- [IPA 応用情報技術者試験（AP）](https://www.ipa.go.jp/shiken/kubun/ap.html)
- [IPA 試験要綱・シラバス](https://www.ipa.go.jp/shiken/syllabus/gaiyou.html)
- [IPA 過去問題（問題冊子・配点割合・解答例）](https://www.ipa.go.jp/shiken/mondai-kaiotu/index.html)
- [PostgreSQL 文書 SELECT（日本語）](https://www.postgresql.jp/document/current/html/sql-select.html)
- [PostgreSQL 文書 ウィンドウ関数（日本語）](https://www.postgresql.jp/document/current/html/tutorial-window.html)
- [SQLite: The WITH Clause](https://www.sqlite.org/lang_with.html)
