from docarray import DocumentArray, Document
from jina import Flow
from executors import  ChunkMerger2, Gpt3Encoder, ImageNormalizer, EmbeddingChecker, TextChecker
import openai

# connect to openai
openai.api_key = "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"

docs = DocumentArray.from_files("data/*.pdf", recursive=True)

for docu in docs:
    docu.load_uri_to_blob()

flow = (Flow()
            .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="pdfSegmenter")
            .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="ChunkSpacySentencizer")
            .add(uses=ChunkMerger2, install_requirements=True, name="chuckMerger")
            #  .add(uses=ImageNormalizer,install_requirements=True, name="imageMormalizwe")  ## not required for GPT3
            .add(uses=TextChecker, install_requirements=True, name="textChecker")
            .add(uses=Gpt3Encoder, install_requirements=True, name="gpt3Encoder")
            .add(uses=EmbeddingChecker, install_requirements=True, name="embeddingChecker")
            .add(
                # +docker is not working with SimpleIndexer.  Not sure why ?  may be created inside the container
                uses="jinahub://SimpleIndexer/latest",
                install_requirements=True,
                name="indexer",
                uses_metas={'workspace': 'wspace_gpt3_davinci_all6'},
                uses_with={"traversal_right": "@c",
                    'table_name': 'encoded_chunks'}
            )

)
"""
            .add(
                # +docker is not working with SimpleIndexer.  Not sure why ?  may be created inside the container
                uses="jinahub://SimpleIndexer/latest",
                install_requirements=True,
                name="indexer",
                uses_metas={'workspace': 'wspace_gpt3'},
                uses_with={"traversal_right": "@c",
                    'table_name': 'encoded_chunks'}
            )
            """
with flow:
    indexed_docs = flow.index(docs)

indexed_docs.summary()

for doc in indexed_docs:
    #doc.summary()
    doc.chunks.summary()
    print('---------------------------')
print('---------------------------end of Indexed docs')

print("-------------")
for doc in indexed_docs:
    for chunk in doc.chunks:
        print(chunk.text)
        if (chunk.embedding is not None):
            print(chunk.embedding.shape[0])
            #print(type(chunk.embedding))
            #print(chunk.embedding)
        else:
            print("Embedding is none - not good.  Should have been identified in EmbeddingChecker")
        print("-----End of chunk")
    print("-------------end of doc")

print("-------------end of all docs ")
