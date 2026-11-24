import pandas as pd


def 정제(df):
    # 원본을 직접 수정하지 않고 복사본으로 작업한다.
    df = df.copy()
    print("시작       ", len(df))

    # 점수가 비어 있는 행을 삭제한다.
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거 ", len(df))

    # 완전히 같은 행의 중복을 제거한다.
    df = df.drop_duplicates()
    print("중복 제거  ", len(df))

    # 반과 과목의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()

    # 점수가 허용 범위를 벗어난 행을 삭제한다.
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거", len(df))
    return df


def 반별평균(df):
    평균 = df.groupby("반")["점수"].mean()
    return 평균.round(2).to_dict()


def 반별통계(df):
    통계 = df.groupby("반")["점수"].agg(
        개수="count",
        평균="mean",
        중앙값="median",
        최댓값="max",
    )
    통계["평균"] = 통계["평균"].round(2)
    통계["중앙값"] = 통계["중앙값"].round(2)
    return 통계


if __name__ == "__main__":
    본 = 정제(pd.read_csv("scores_2026.csv"))
    미니 = 정제(pd.read_csv("mini.csv"))

    수학 = 본[본["과목"] == "수학"]
    print("수학 행 수", len(수학))
    print("반별 평균")
    print(본.groupby("반")["점수"].mean().round(2))
    print("과목 × 반 평균")
    print(본.groupby(["과목", "반"])["점수"].mean().round(2))
    print("반별 통계")
    print(반별통계(본))
    print("점수 합계 일치", 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum())
    print("개수 합계 일치", 본.groupby("반")["점수"].count().sum() == len(본))
    print("mini 반별 평균", 반별평균(미니))
