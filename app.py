import requests
import streamlit as st
from streamlit_lottie import st_lottie
from bs4 import BeautifulSoup

movieNames = {}
def fetchLottieJson(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Movie Scrapper", page_icon=":movie_camera:")




def fetchMovies(kw):
    import json
    url = "https://kids-in-mind.com/search-desktop.htm?fwp_keyword="+kw
    html = requests.get(url)
    bs = BeautifulSoup(html.content,'html.parser')
    movies = bs.find_all(class_='search-result')
    
    for movie in movies:
        movieInfo = evalChunks(movie.text)
        title = movieInfo['Movie']

        # now fetch from OpenMovieDataBaseAPi
        murl = "http://www.omdbapi.com/?t="+title+"&apikey=1785ad28"
        movieJson = requests.get(murl)
        movieJsonData = json.loads(movieJson.content)
        try:
            with st.container():
                leftCol , rightCol = st.columns([1,3])
                with leftCol:
                    st.markdown("![Alt Text]("+movieJsonData['Poster']+")")
                with rightCol:
                    ratings = movieJsonData['Ratings'][0]['Value'] if movieJsonData['Ratings'][0]['Value'] else 'N/a'

                    st.subheader(movieJsonData['Title']+' - '+movieJsonData['Year'])
                    st.write(movieJsonData['Genre']+", Rated:"+movieJsonData['Rated'])
                    st.write("IMDB Rating: "+ratings)
                    st.write("Starring: "+movieJsonData['Actors'])
                    st.caption("Plot: "+movieJsonData['Plot'])
        except:
            print("")


def fetchImdbInfo(movie):
    return 



def evalChunks(txt):
    import re
    infoList = {}
    m = re.search(r"\[([0-9]+)\]", txt)
    if not m:
        year = 'N/a'
    else:
        year = m.group(1)
    bm = re.search(r'\d+.\d+.\d+', txt)
    if not bm:
        bm = 'N/a'
    else:
        bm = bm.group()

    # movie name
    movie = txt.replace('['+year+']','').replace('-','').replace(bm,'')
    rating = re.search(r"\[(.*?)\]", movie)
    if not rating:
        rating = 'N/a'
    else:
        rating = rating.group(1)
    movie = movie.replace('['+rating+']','')
    if not bm == 'N/a':
        bm = bm.split('.')
        infoList['Vulgarity'] = bm[0]
        infoList['Violence'] = bm[1]
        infoList['Profanity'] = bm[2]        
    else:
        infoList['Vulgarity'] = ''
        infoList['Violence'] = ''
        infoList['Profanity'] = ''    
    infoList['Movie'] = movie.strip(' ')
    infoList['Year'] = year
    infoList['Rating'] = rating

    return infoList



animation = fetchLottieJson("https://assets8.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
load_css("styles/style.css")


with st.container():
    leftCol , rightCol = st.columns(2)
    with leftCol:
        st.subheader("A Python tool by Zeeshan")
        st.title("Movie Scrapper")
        st.write("Use below form to enter the keywords and hit the Search button.")
        kw = st.text_input('', '', placeholder='Movie Name or Keyword')
        button = st.button('Search')
    with rightCol:
        st_lottie(animation, height=300,key="coding")
    if button:
        if kw != '':
            st.write(f"""Searching for {kw}....""")
            fetchMovies(kw)
        else:
            st.write("ERROR: Please enter some Movie Name or Keyword!")