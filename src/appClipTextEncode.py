from docarray import DocumentArray, Document
from jina import Flow
from executors import ChunkMerger, ImageNormalizer, EmbeddingChecker, ChunkMerger2


docs = DocumentArray.from_files("data/*.pdf", recursive=True)

docs[0].load_uri_to_blob()

flow = (Flow()
        .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="pdfSegmenter")
        .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="chunkSpaceSentencizer")
        .add(uses=ChunkMerger2, install_requirements=True, name="chunkMerger")
        .add(uses=ImageNormalizer, install_requirements=True, name="imageNormalizer")
        .add(
            uses='jinahub+docker://CLIPTextEncoder/latest',
            install_requirements=True,
            name="clipTextEncoder",
            uses_with={"traversal_paths": "@c"},
        )
        .add(uses=EmbeddingChecker, install_requirements=True, name="embeddingChecker")
        .add(
            # +docker is not working with SimpleIndexer.  Not sure why ?  may be created inside the container
            uses="jinahub://SimpleIndexer/latest",
            # uses_before=EmbeddingChecker,
            install_requirements=True,
            name="simpleIndexer",
            uses_metas={'workspace': 'wspace_ClipTexxt_all6'},
            uses_with={"traversal_right": "@c", 'table_name': 'encoded_chunks'}
        )
)

flow2 = (Flow()
         .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="pdfSegmenter")
         .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="chunkSpaceSentencizer")
         .add(uses=ChunkMerger, install_requirements=True, name="chunkMerger")
         .add(uses=ImageNormalizer, install_requirements=True, name="imageNormalizer")
         .add(
                uses='jinahub+docker://CLIPTextEncoder/latest',
                install_requirements=True,
                name="clipTextEncoder",
                uses_with={"traversal_paths": "@c"},
)
)


with flow:
    indexed_docs = flow.index(docs)


# with flow2:
#  indexed_docs = flow2.index(docs)


indexed_docs.summary()
indexed_docs[0].chunks.summary()
# indexed_docs[0].chunks[0].summary()
print('---------------------------end of Indexed docs')

"""
# r = indexed_docs.post(EmbeddingChecker)
ec = EmbeddingChecker()
r = ec.check(indexed_docs)
# r2 = ec.check(r)
# print('rtojson: ', r.to_json())
r.summary()
r[0].chunks.summary()
r[0].chunks[0].summary()

print("-------------")
for doc in r:
    for chunk in doc.chunks:
        print(chunk.text)
        if(chunk.embedding is not None):
          print(chunk.embedding.shape[0])
        print("-----")

    print("-------------")

"""


print("-------------")
for doc in indexed_docs:
    for chunk in doc.chunks:
        print(chunk.text)
        if (chunk.embedding is not None):
            print(chunk.embedding.shape[0])
        print("-----")

    print("-------------")
