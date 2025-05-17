import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 📌 日本語フォント指定（Streamlit Cloud で文字化け防止）
matplotlib.rcParams['font.family'] = 'IPAGothic'

# タイトル
st.title("💰 自己資金ダッシュボード（万円単位）")

# ファイルアップロード
uploaded_file = st.file_uploader("💼 銀行・証券口座のCSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # データ表示
        st.subheader("📄 アップロードされたデータ（プレビュー）")
        st.dataframe(df)

        # 必須カラムの確認
        required_columns = {"口座名", "資産種別", "金額"}
        if not required_columns.issubset(df.columns):
            st.error("❌ データに必要な列（口座名、資産種別、金額）が含まれていません。")
        else:
            # 金額を数値に変換し、万円単位に
            df["金額"] = pd.to_numeric(df["金額"], errors="coerce") / 10000
            df.dropna(subset=["金額"], inplace=True)

            # 口座別合計
            st.subheader("🏦 口座ごとの合計（万円）")
            by_account = df.groupby("口座名")["金額"].sum()
            st.bar_chart(by_account)

            # 資産種別ごとの合計（円グラフ）
            st.subheader("📊 資産種別ごとの割合（万円）")
            by_type = df.groupby("資産種別")["金額"].sum()
            fig, ax = plt.subplots()
            by_type.plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")
            ax.set_title("資産種別割合（万円）")
            st.pyplot(fig)

            # 総資産（万円）表示
            st.subheader("🧮 自己資金総額")
            total = df["金額"].sum()
            st.success(f"💴 合計: {total:,.1f} 万円")

    except Exception as e:
        st.error(f"❌ データの読み込み中にエラーが発生しました: {e}")
else:
    st.info("📂 CSVファイルをアップロードすると、自己資金の分析が表示されます。")

# フッター
st.caption("作成者: あなたの名前 | powered by Streamlit")
