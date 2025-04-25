import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium
from streamlit_lottie import st_lottie
import requests
from modules import importer
from modules import formater
title_obj = formater.Title()
title_obj.page_config("N3DN.Tech - Home")
def load_lottie_url(url: str):
 r = requests.get(url)
 if r.status_code != 200:
 return None
 return r.json()
with st.sidebar:
 lottie_animation = 
load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_jcikwtux
.json")
 if lottie_animation:
 st_lottie(lottie_animation, height=200, key="sidebar_anim")
 else:
 st.error("Animation could not be loaded.")
if 'jobs_data' not in st.session_state:
 st.session_state.jobs_data = None
data_file = os.path.join("data", "google_jobs.csv")
if os.path.exists(data_file) and st.session_state.jobs_data is None:
 st.session_state.jobs_data = 
importer.DataImport.fetch_and_clean_data(max_rows=1000)
else:
 st.session_state.jobs_data = 
importer.DataImport.fetch_and_clean_data(max_rows=1000)
col1, col2 = st.columns([3, 1])
with col1:
Page | 10
 st.markdown('<p class="sub-header">Data-Driven Insights for 
Technology Professionals</p>', unsafe_allow_html=True)
with col2:
st.markdown(f"<h3>Data Updated: {datetime.now().year}</h3>", 
unsafe_allow_html=True)
if st.session_state.jobs_data is not None:
 if 'salary_yearly' in st.session_state.jobs_data.columns:
 salary_data = 
st.session_state.jobs_data['salary_yearly'].dropna()
 if not salary_data.empty:
 avg_salary_display = f"${int(salary_data.mean() / 1000)}K"
 elif 'salary' in st.session_state.jobs_data.columns:
 salary_data = st.session_state.jobs_data['salary'].dropna()
 if not salary_data.empty:
 avg_salary_display = f"${int(salary_data.mean() / 1000)}K"
 if 'description_tokens' in st.session_state.jobs_data.columns:
 all_skills = []
 all_skills.extend(skills)
 skill_counts = pd.Series(all_skills).value_counts()
 if not skill_counts.empty:
 top_skill_display = skill_counts.index[0]
 if 'posted_at' in st.session_state.jobs_data.columns:
 try:
 st.session_state.jobs_data['posted_date'] = 
pd.to_datetime(
 st.session_state.jobs_data['posted_at'], 
errors='coerce'
 )
recent_date = 
st.session_state.jobs_data['posted_date'].max() - pd.Timedelta(days=90)
 recent_jobs = 
st.session_state.jobs_data[st.session_state.jobs_data['posted_date'] >= 
recent_date]
 if not recent_jobs.empty and 'description_tokens' 
in recent_jobs.columns:
 recent_skills = []
 for tokens in 
recent_jobs['description_tokens'].dropna():
 if isinstance(tokens, str):
 skills = 
tokens.strip("[]").replace("'", "").split(", ")
recent_skills.extend(skills)
 recent_skill_counts = 
pd.Series(recent_skills).value_counts()
 if not recent_skill_counts.empty:
 trending_topic_d
