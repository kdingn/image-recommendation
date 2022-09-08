import streamlit as st
import pandas as pd
import datetime
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)


def get_now():
    DIFF_JST_FROM_UTC = 9
    return datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)


def filter_redundant(df, redundant):
    df = df.merge(redundant[["id", "master_id"]], how="left")
    df = df[df["master_id"].isnull()].drop("master_id", axis=1)
    return df.reset_index(drop=True)


def add_as_like(tran, ids):
    rows = pd.DataFrame({"id": [ids]})
    rows["like"] = 1
    rows["update"] = get_now()
    tran = pd.concat([tran, rows]).reset_index(drop=True)
    return tran


def add_as_not_like(tran, ids):
    rows = pd.DataFrame({"id": [ids]})
    rows["like"] = 0
    rows["update"] = get_now()
    tran = pd.concat([tran, rows]).reset_index(drop=True)
    return tran


def add_redundant(redundant, ids, master_id=-9999):
    rows = pd.DataFrame({"id": [ids]})
    rows["master_id"] = master_id
    rows["update"] = get_now()
    redundant = pd.concat([redundant, rows]).reset_index(drop=True)
    return redundant


def save_add_as_like(tran, ids):
    tran = add_as_like(tran, ids)
    tran.to_csv("label_tran.csv", index=False)


def save_add_as_not_like(tran, ids):
    tran = add_as_not_like(tran, ids)
    tran.to_csv("label_tran.csv", index=False)


def save_add_redundant(redundant, ids):
    redundant = add_redundant(redundant, ids)
    redundant.to_csv("redundant.csv", index=False)


# parameters
input_dir = "./image"
extension = config["extension"]

# dataframes
tran = pd.read_csv("label_tran.csv")  # only changed by on-change
redundant = pd.read_csv("redundant.csv")  # only changed by on-change

actl = tran.copy().sort_values(
    "update", ascending=False
).drop_duplicates(
    "id", keep="first"
).drop(
    "update", axis=1
).reset_index(drop=True)
actl = filter_redundant(actl, redundant)

pred = pd.read_csv("prediction.csv").merge(actl, on="id", how="left")
pred = filter_redundant(pred, redundant)
pred = pred.sort_values("01_like", ascending=False)

df = pred.copy()

# plots
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

nt = 10
max_page = int(len(df)/nt)
page = st.sidebar.number_input("page", min_value=1, max_value=max_page, key="sidep")

evaluation = st.sidebar.selectbox(
    "evaluation mode", ["on", "off"], index=1)

filtertt = st.sidebar.selectbox(
    "train / test", ["all", "train", "like", "not like", "test"], index=4)
if filtertt == "train":
    df = df[~df["like"].isnull()]
elif filtertt == "like":
    df = df[df["like"] == 1]
elif filtertt == "not like":
    df = df[df["like"] == 0]
elif filtertt == "test":
    df = df[df["like"].isnull()]

nw = st.sidebar.selectbox(
    "columns", [1, 2, 5, 10], index=2, key="nw")
nt = st.sidebar.selectbox(
    "show in 1 page", [1, 2, 5, 10], index=2, key="nt")
nh = int(nt/nw)

asce = st.sidebar.selectbox(
    "sort", ["ascending", "descending"], index=0
)
if asce == "descending":
    df = df.sort_values("01_like",ascending=True)

st.header(f"{filtertt} images ({page}/{max_page} page)")

for j in range(nh):
    st.write("""---""")
    cols = st.columns(nw)
    for i in range(nw):
        ij = i + nw*j + nt*(page-1)
        with cols[i]:
            index = df['id'].values[ij]
            like = df['like'].values[ij]
            pred = df["01_like"].values[ij]
            link = config["link"].format(index)

            st.markdown(f"[【{ij}】【{like}】【{pred:.2f}】]({link})")
            if evaluation == "on":
                bt1 = st.button("Like", key=f"{ij}_like")
                bt2 = st.button("Not Like", key=f"{ij}_not_like")
                bt3 = st.button("Redundant", key=f"{ij}_redundant")
                if bt1:
                    save_add_as_like(tran, index)
                    st.success(f"add {index} as like")
                    st.button("refresh")
                if bt2:
                    save_add_as_not_like(tran, index)
                    st.success(f"add {index} as not like")
                    st.button("refresh")
                if bt3:
                    save_add_redundant(redundant, index)
                    st.success(f"add {index} as redundant")
                    st.button("refresh")
            st.image(f"{input_dir}/{index}.{extension}")
st.write("""---""")
