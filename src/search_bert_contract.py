#from docarray import DocumentArray, Document
from jina import Flow
#import streamlit as st
#import pandas as pd
#import numpy as np


def main():

    flow=(
        Flow(port=1236)
        .add(
            uses="jinahub+docker://TransformerTorchEncoderCU113/latest",
            install_requirements=True,
            name="cu113Encoder2",
            uses_with={
              #  "traversal_paths": "@c", 
             #   "pretrained_model_name_or_path": "bert-base-uncased"},  # non default used instead of defaul mpnet
                "pretrained_model_name_or_path": "nlpaueb/bert-base-uncased-contracts"},  # non default used instead of defaul mpnet
        )
        .add(
            uses="jinahub://SimpleIndexer/latest",
            install_requirements=True,
            name="indexer",
            uses_metas={'workspace': 'wspace_cu113_contract_bertLegal'},
            uses_with={
                        "traversal_right": "@c",
                        'traversal_left': '@r', 'table_name': 'encoded_chunks'},
        )
    )


    with flow() as f:
       f.block()
       
       
       
    print("End -- should never be reached")

main()
