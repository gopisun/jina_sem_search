from docarray import DocumentArray, Document
from jina import Flow
from executors import  Gpt3Encoder_search
import openai

# connect to openai
openai.api_key = "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"


flow = (
     Flow(port=5234)
     .add(uses=Gpt3Encoder_search, install_requirements=True, name="gpt3Encoder")
     .add(
          uses="jinahub://SimpleIndexer/latest",
          install_requirements=True,
          name="indexer",
          uses_metas={'workspace': 'wspace_gpt3_babbage_all6'},
          uses_with={"traversal_right": "@c",
                      'traversal_left': '@r', 'table_name': 'encoded_chunks'},
          )
     )


with flow:
    flow.block()
   
