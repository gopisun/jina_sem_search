from docarray import DocumentArray, Document
from jina import Flow
from executors import ChunkMerger2, ImageNormalizer, EmbeddingChecker


#docs = DocumentArray.from_files("data/*.pdf", recursive=True)
docs = DocumentArray.from_files("../data/contracts/*.pdf", recursive=True)

for docu in docs:
    docu.load_uri_to_blob()

flow = (Flow()
        .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="pdfSegmenter")
        .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="chunkSpaceSentencizer")
        .add(uses=ChunkMerger2, install_requirements=True, name="chuckMerger2")
        .add(uses=ImageNormalizer, install_requirements=True, name="imageMormalizer")
        .add(
            uses='jinahub+docker://TransformerTorchEncoderCU113/latest',  # default: sentence-transformers/all-mpnet-base-v2
            install_requirements=True,
            name="cu113Encoder",
            uses_with={
                "traversal_paths": "@c", 
             #   "pretrained_model_name_or_path": "bert-base-uncased"},  # non default used instead of defaul mpnet
                "pretrained_model_name_or_path": "nlpaueb/bert-base-uncased-contracts"},  # non default used instead of defaul mpnet
)
    .add(uses=EmbeddingChecker, install_requirements=True, name="embeddingChecker")
    .add(
    # +docker is not working with SimpleIndexer.  Not sure why ?  may be created inside the container
        uses="jinahub://SimpleIndexer/latest",
        install_requirements=True,
        name="indexer",
        workspace="wspace_cu113_contract_bertLegal",
        #uses_metas={'workspace': 'wspace_cu113_contract_bert'},
        uses_with={"traversal_right": "@c",
                   'table_name': 'encoded_chunks'}
)
)


with flow:
    indexed_docs = flow.index(docs)

indexed_docs.summary()
for doc in indexed_docs:
    # doc.summary()
    doc.chunks.summary()
    print('---------------------------')
print('---------------------------end of Indexed docs')


print("-------------")
for doc in indexed_docs:
    for chunk in doc.chunks:
        print(chunk.text)
        if (chunk.embedding is not None):
            print(chunk.embedding.shape[0])
            print(type(chunk.embedding))
        else:
            print('embedding is None - not good. Should have been identified in EmbeddingChecker')
        print("-----End of chunk")
    print("-------------end of doc")

print("-------------end of all docs ")
