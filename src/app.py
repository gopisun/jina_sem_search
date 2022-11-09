from docarray import DocumentArray, Document
from jina import Flow
from executors import  ChunkMerger2, ImageNormalizer


docs = DocumentArray.from_files("data/*.pdf", recursive=True)

docs[0].load_uri_to_blob()

flow = (Flow()
            .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="segmenter")
            .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="chunkSpaceSentencizer")
            .add(uses=ChunkMerger2, install_requirements=True, name="chunkMerger2")
            .add(uses=ImageNormalizer, install_requirements=True, name="imageNormalizer")
            .add(
                uses='jinahub+docker://CLIPEncoder/latest', 
                install_requirements=True, 
                name="clipEncoder",
                uses_with={"traversal_paths": "@c"},
            )
            .add(
                uses="jinahub://SimpleIndexer/latest",   ## +docker is not working with SimpleIndexer.  Not sure why ?  may be created inside the container
                install_requirements=True,
                name="indexer",
                uses_metas={'workspace': 'wspace_CLIPEncoder_all6'},
                uses_with={"traversal_right": "@c", 'table_name': 'encoded_chunks'}
    )
)


with flow:
    indexed_docs=flow.index(docs)

indexed_docs.summary()
for doc in indexed_docs:
    doc.chunks.summary()

print("-------------")
for doc in indexed_docs:
    for chunk in doc.chunks:
        print(chunk.content)
        if (chunk.embedding is not None):
            print(chunk.embedding.shape[0])
            # print(type(chunk.embedding))
        else:
            print('embedding is None - not good. Should have been identified in EmbeddingChecker')
        print("-----End of chunk")
    print("-------------end of doc")

print("-------------end of all docs ")



