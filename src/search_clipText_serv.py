from docarray import DocumentArray, Document
from jina import Flow


def main():

    
    flow = (
        Flow(port=3234)
        .add(
            uses="jinahub+docker://CLIPTextEncoder",
            install_requirements=True,
            name="clipEncoder2",
        )
        .add(
            uses="jinahub://SimpleIndexer/latest",
            install_requirements=True,
            name="indexer",
            uses_metas={'workspace': 'wspace2_ClipTexxt_all6'},
            uses_with={"traversal_right": "@c", 'traversal_left': '@r','table_name': 'encoded_chunks'},
        )
    )

    with flow as f:
       f.block()


main()