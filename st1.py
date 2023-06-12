import pandas as pd
import streamlit as st

df = pd.DataFrame({'id':[1,2,3],'name':['Zeeshan','Ahmed','Hashmi']})

st.write("First StreamLit App.")
st.write(df)



#x = st.slider("Select a value")
#st.write(x, "squared is", x * x)

