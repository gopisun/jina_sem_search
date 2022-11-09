from docarray import DocumentArray, Document
from jina import Flow


def main():

    flow = (
        Flow(port=2234)
        .add(
            uses="jinahub+docker://CLIPEncoder",
            install_requirements=True,
            name="clipEncoder2",
        )
        .add(
            uses="jinahub://SimpleIndexer/latest",
            install_requirements=True,
            name="indexer",
            uses_metas={'workspace': 'wspace_CLIPEncoder_all6'},
            uses_with={"traversal_right": "@c", 'traversal_left': '@r','table_name': 'encoded_chunks'},
        )
    )

    

    with flow as f:
       f.block()
       
    print("End -- should never be reached")
        
       
    

def main1():

    search_string = "kitten"
    flow = (
        Flow()
        .add(
            uses="jinahub+docker://CLIPEncoder",
            install_requirements=True,
            name="clipEncoder2",
        )
        .add(
            uses="jinahub://SimpleIndexer/latest",
            install_requirements=True,
            name="indexer",
            ## uses_metas={'workspace': 'workspace'},
            uses_with={"traversal_right": "@c", 'traversal_left': '@r','table_name': 'encoded_chunks'},
        )
    )

    search_doc = Document(text=search_string)

    with flow:
        output = flow.search(search_doc)
       
    print("Output Summary:")    
    output.summary()
    print("Matches Summary:")   
    output[0].matches.summary()
    print("Match doc Summary:")   
    output[0].matches[0].summary()

    print(output)
    matches = output[0].matches
    
    for doc in matches:
            print(doc.content)
            print(doc.scores)
            print(doc.tags)
            print("-" * 10)

main()