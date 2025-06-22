import streamlit as st
import csv

# ゲームデータの読み込み
@st.cache_data
def load_games(file_path="games.csv"):
    games = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            game = {
                "title": row["title"],
                "tags": row["tags"].split(";"),
                "play_time": row["play_time"],
                "difficulty": row["difficulty"],
                "platform": row["platform"].split(";")
            }
            games.append(game)
    return games

# アプリ本体
def main():
    st.title("🎮 ゲームおすすめアプリ")

    games = load_games()

    # 全タグ・時間・プラットフォームを動的取得
    all_tags = sorted({tag for game in games for tag in game["tags"]})
    all_play_times = sorted({game["play_time"] for game in games})
    all_platforms = sorted({plat for game in games for plat in game["platform"]})

    # ユーザー入力
    selected_tags = st.multiselect("✅ 好きなジャンルを選んでください", all_tags)
    selected_time = st.radio("🕒 希望プレイ時間を選んでください", all_play_times)
    selected_platforms = st.multiselect("🖥️ 所持プラットフォームを選んでください", all_platforms)

    if st.button("🎯 おすすめを表示"):
        if not selected_tags or not selected_time or not selected_platforms:
            st.warning("ジャンル・プレイ時間・プラットフォームをすべて選んでください。")
        else:
            results = []
            for game in games:
                if (
                    any(tag in game["tags"] for tag in selected_tags) and
                    game["play_time"] == selected_time and
                    any(plat in game["platform"] for plat in selected_platforms)
                ):
                    results.append(game)

            if results:
                st.success(f"{len(results)} 件のおすすめゲームが見つかりました！")
                for g in results:
                    st.markdown(f"### 🎮 {g['title']}")
                    st.write(f"- ジャンル：{', '.join(g['tags'])}")
                    st.write(f"- プレイ時間：{g['play_time']}")
                    st.write(f"- プラットフォーム：{', '.join(g['platform'])}")
                    st.write("---")
            else:
                st.info("条件に一致するゲームが見つかりませんでした。")

if __name__ == "__main__":
    main()
