from docarray import DocumentArray, Document
import streamlit as st
import pandas as pd
import numpy as np
from jina import Client


def main():
    c1 = st.container()
    c1.title("Contracts Search")
    searchStr = c1.text_input('Search String', 'Verizon and Amdocs')
    # c1.subheader('Search String is')
    # c1.write(searchStr)

    searchEngineSel = c1.radio(
        "Select Search Engine:",
        ('Bert Base', 'Bert Base Contracts', 'Sentence-All MPnet Base'))

    # c1.write('search engine selected: ')
    # c1.text(searchEngineSel)
    host = 'grpc://0.0.0.0:1235'

    if searchEngineSel == 'Bert Base':
        host = 'grpc://0.0.0.0:1235'

    if searchEngineSel == 'Bert Base Contracts':
        host = 'grpc://0.0.0.0:1236'

    if searchEngineSel == 'Sentence-All MPnet Base':
        host = 'grpc://0.0.0.0:1237'

    resultNum = c1.slider('How many results to retrieve?', 0, 30, 20)
    # c1.write(resultNum, 'top results would be retrieved')

    if c1.button('Search'):
        c1.text('Search in progress...')
        do_search(searchStr, host)
        c1.text('Search done')
    else:
        c1.text('Goodbye')


def do_search(searchStr, host):

    search_doc = Document(text=searchStr)

    # set up the client
    client = Client(host=host)

    # send data
    output = client.post('/search', search_doc)

    print(output)
    matches = output[0].matches
   # matches[0].scores.summary()

    df = pd.DataFrame({
        'Matches': [doc.content for doc in matches],
        'Score': [doc.scores['cosine'].value for doc in matches]
    })
    with st.container():
        st.title("Search Results")
        st.table(df)


main()
