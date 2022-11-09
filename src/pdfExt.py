from docarray import DocumentArray, Document
from jina import Flow
from executors import ChunkMerger2, MergeChunks

docs = DocumentArray.from_files("../data/contracts/Amdocs_SOW.pdf", recursive=True)

for docu in docs:
    docu.load_uri_to_blob()
    
flow = (Flow()
      #  .add(uses='jinahub://PDFTableExtractor/latest', install_requirements=True, name="pdfTblExt1")
        .add(uses='jinahub+docker://PDFSegmenter', install_requirements=True, name="pdfSegmenter")
        .add(uses='jinahub+docker://ChunkSpacySentencizer', install_requirements=True, name="chunkSpaceSentencizer")
        .add(uses=ChunkMerger2, install_requirements=True, name="chuckMerger2")
        .add(uses=MergeChunks, install_requirements=True, name="Merge1")
)

with flow:
   tbl_docs = flow.index(docs)
   
tbl_docs.summary()
for doc in tbl_docs:
    # doc.summary()
    doc.chunks.summary()
    print('---------------------------')
print('---------------------------end of Table docs')

print("-------------")
for doc in tbl_docs:
    for chunk in doc.chunks:
        print(chunk.text)
        print("-----End of chunk")
    print("-------------end of doc")