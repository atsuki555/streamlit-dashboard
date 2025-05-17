import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ==== ✅ 日本語フォントの設定（OSに応じて） ====

# Windows or IPAexGothic font (多くの環境で使える)
jp_font = None

# 検索候補
for font_name in ["IPAexGothic", "Meiryo", "Yu Gothic", "Noto Sans CJK JP"]:
    if font_name in [f.name for f in fm.fontManager.ttflist]:
        jp_font = font_name
        break

# フォントが見つかった場合は設定
if jp_font:
    plt.rcParams["font.family"] = jp_font
else:
    st.warning("⚠️ 日本語フォントが見つかりませんでした。文字化けする可能性があります。")

# ==== ✅ Streamlit UI ====

st.set_page_config(page_title="自己資金ダッシュボード", layout="centered")
st.title("💰 自己資金ダッシュボード")

# CSVアップロード
uploaded_file = st.file_uploader("📄 残高CSVファイルをアップロードしてください", type="csv")

if uploaded_file:
    # Shift_JIS → UTF-8順で読み込み
    try:
        df = pd.read_csv(uploaded_file, encoding="shift_jis")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

    st.subheader("📋 入力された資産データ")
    st.dataframe(df)

    total = df["残高"].sum()
    st.metric("💵 自己資金総額", f"{total:,.0f} 万円")

    # 機関別グラフ
    st.subheader("🏦 金融機関ごとの残高")
    fig, ax = plt.subplots()
    ax.bar(df["機関"], df["残高"], color='skyblue')
    ax.set_xlabel("金融機関")
    ax.set_ylabel("金額（万円）")
    ax.set_title("機関別残高")
    plt.xticks(rotation=15)
    st.pyplot(fig)

    # 種別別円グラフ
    st.subheader("📊 種別別の割合（銀行 / 証券など）")
    by_type = df.groupby("種別")["残高"].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(by_type, labels=by_type.index, autopct="%1.1f%%", startangle=90)
    ax2.set_title("種別別割合")
    ax2.axis("equal")
    st.pyplot(fig2)

else:
    st.info("上記からCSVファイルをアップロードしてください。")
