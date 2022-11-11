#from docarray import DocumentArray, Document
from jina import Flow
#import streamlit as st
#import pandas as pd
#import numpy as np


def main():

    flow=(
        Flow(port=1237)
        .add(
            uses="jinahub+docker://TransformerTorchEncoderCU113/latest",
            install_requirements=True,
            name="cu113Encoder2",
        )
        .add(
            uses="jinahub://SimpleIndexer/latest",
            install_requirements=True,
            name="indexer",
            # uses_metas={'workspace': 'wspace_cu113_contract_mptext'},
            uses_metas={'workspace': 'wspace_cu113_wiki_mptext'},
            uses_with={"traversal_right": "@c",
                       'traversal_left': '@r', 'table_name': 'encoded_chunks'},
        )
    )


    with flow() as f:
       f.block()
       
    print("End -- should never be reached")

main()
