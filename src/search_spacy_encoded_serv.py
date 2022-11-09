from docarray import DocumentArray, Document
from jina import Flow


def main():

    flow = (
        Flow(port=4234)
        .add(
            uses="jinahub+docker://SpacyTextEncoder/latest",
            install_requirements=True,
            name="spacyEncoder2",
        )
        .add(
            uses="jinahub://SimpleIndexer/latest",
            install_requirements=True,
            name="indexer",
            uses_metas={'workspace': 'wspace_spacyEncoder'},
            uses_with={"traversal_right": "@c", 'traversal_left': '@r','table_name': 'encoded_chunks'},
        )
    )

    

    with flow:
      flow.block()
        


main()