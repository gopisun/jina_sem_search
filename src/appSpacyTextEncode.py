from docarray import DocumentArray, Document
from jina import Flow
from executors import ChunkMerger2, ImageNormalizer, EmbeddingChecker


docs = DocumentArray.from_files("data/*.pdf", recursive=True)

docs[0].load_uri_to_blob()

flow = (Flow()
            .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="pdfSegmenter")
            .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="chunkSpaceSentencizer")
            .add(uses=ChunkMerger2,install_requirements=True, name="chuckMerger2")
            .add(uses=ImageNormalizer,install_requirements=True, name="imageMormalizwe")
            .add(
                uses='jinahub+docker://SpacyTextEncoder/latest', 
                install_requirements=True, 
                name="spacyTextEncoder",
                uses_with={"traversal_paths": "@c"},
            )
            .add(uses=EmbeddingChecker, install_requirements=True, name="embeddingChecker")
            .add(
                uses="jinahub://SimpleIndexer/latest",   ## +docker is not working with SimpleIndexer.  Not sure why ?  may be created inside the container
                install_requirements=True,
                name="indexer",
                uses_metas={'workspace': 'wspace_spacyEncoder'},
                uses_with={"traversal_right": "@c", 'table_name': 'encoded_chunks'}
            )
)


with flow:
    indexed_docs=flow.index(docs)

indexed_docs.summary()
indexed_docs[0].chunks.summary()

indexed_docs.summary()
indexed_docs[0].chunks.summary()
indexed_docs[0].chunks[0].summary()
print('---------------------------end of Indexed docs')


print("-------------")
for doc in indexed_docs:
    for chunk in doc.chunks:
        print(chunk.text)
        if (chunk.embedding is not None):
            print(chunk.embedding.shape[0])
        print("-----")

    print("-------------")