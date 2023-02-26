import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

# Title :
st.title("Disease :blue[Detector] 🕵️")

# Reading CSVs :
data = pd.read_csv("files/Training.csv").drop("prognosis", axis=1)
ds = pd.read_csv("files/disease_description.csv")
pr = pd.read_csv("files/disease_precaution.csv")

# Columns (representing symptoms) :
dis= list(data.columns)

# Loading model and saved dictionary :
model = load("model.joblib")
pro = load("disease.joblib")

# Creating an array with zeros :
arr = np.zeros(135)

opt = st.multiselect(
    "Please Select Your :red[Symptoms :]",
    dis
)

# Creating a function to predict and store :
opt = list(opt)
def predictions(opt):
    idx = []
    for i in opt:
        idx.append(dis.index(i))

    for i in idx:
        arr[i] = 1
    arr[-1]= len(opt)
    pred = model.predict([arr])

    for key in pro.keys():
        if pro[key] == pred[0]:
            print(f'''Disease:{key}
                    Array:{arr}''')
            return key

# Description :
def give_des(d):
    return [ds[ds["Disease"]==d].Symptom_Description][0]

# Description :
def give_pre(d):
    return list(pr[pr["Disease"]==d].Symptom_precaution_0)[0],list(pr[pr["Disease"]==d].Symptom_precaution_1)[0],list(pr[pr["Disease"]==d].Symptom_precaution_2)[0], list(pr[pr["Disease"]==d].Symptom_precaution_3)[0]


if st.button("Detect"):
    cola, colb, colc = st.columns(3)
    prognosis = predictions(opt)

    description = give_des(prognosis)
    p1, p2, p3, p4 = give_pre(prognosis)

    with colb:
        try:
            st.header(prognosis)
            st.subheader("Description :")
            st.caption(list(description.values)[0])
            st.subheader("Precaution :")
            st.caption(f"- {p1}\n- {p2}\n- {p3}\n- {p4}")
        except:
            st.header(":red[Something Went Wrong] ⚠️")
