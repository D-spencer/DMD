import os
import streamlit as st
import numpy as np
import pickle


st.write("BASE DIR:", BASE_DIR)
st.write("FILES:", os.listdir(BASE_DIR))
st.write("MODELS:", os.listdir(os.path.join(BASE_DIR, "models")))
