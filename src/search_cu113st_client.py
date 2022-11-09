from docarray import DocumentArray, Document
import streamlit as st
import pandas as pd
import numpy as np
from jina import Client


def main():
    c1 = st.container()
    c1.title("LLM Search")
    searchStr = c1.text_input('Search String', 'Types of Chocolate and Cake')
    # c1.subheader('Search String is')
    # c1.write(searchStr)

    searchEngineSel = c1.radio(
        "Select Search Engine:",
        ('CLIP Text & Image', 'CLIP Text', 'Spacy Text Encoder', 'GPT3-babbage', 'GPT3-davinci', 'TransformerTorch-Sentence'))

    # c1.write('search engine selected: ')
    # c1.text(searchEngineSel)
    host='grpc://0.0.0.0:1234'

    if searchEngineSel == 'TransformerTorch-Sentence':
        host='grpc://0.0.0.0:1234'

    if searchEngineSel == 'CLIP Text & Image':
        host='grpc://0.0.0.0:2234'

    if searchEngineSel == 'CLIP Text':
        host='grpc://0.0.0.0:3234'

    if searchEngineSel == 'Spacy Text Encoder':
        host='grpc://0.0.0.0:4234'

    if searchEngineSel == 'GPT3-babbage':
        host='grpc://0.0.0.0:5234'

    if searchEngineSel == 'GPT3-davinci':
        host='grpc://0.0.0.0:5234'


    resultNum=c1.slider('How many results to retrieve?', 0, 30, 20)
    # c1.write(resultNum, 'top results would be retrieved')

    if c1.button('Search'):
        c1.text('Search in progress...')
        do_search(searchStr, host)
        c1.text('Search done')
    else:
        c1.text('Goodbye')



def do_search(searchStr, host):

    search_doc=Document(text = searchStr)

    # set up the client
    client=Client(host = host)

    # send data
    output=client.post('/search', search_doc)


    print(output)
    matches=output[0].matches
   # matches[0].scores.summary()

    df=pd.DataFrame({
        'Matches': [doc.content for doc in matches],
        'Score': [doc.scores['cosine'].value for doc in matches]
    })
    with st.container():
        st.title("Search Results")
        st.table(df)

main()
