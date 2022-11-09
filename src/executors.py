from jina import Executor, requests
import numpy as np
from docarray import DocumentArray, Document
import openai
# from numpy import ndarray
import numpy as np


class ImageNormalizer(Executor):
    @requests(on="/index")
    def normalize_chunks(self, docs, **kwargs):
        for doc in docs:
            for chunk in doc.chunks[...]:
                if chunk.blob:
                    chunk.convert_blob_to_image_tensor()

                if hasattr(chunk, "tensor"):
                    if chunk.tensor is not None:
                        chunk.convert_image_tensor_to_uri()
                        chunk.tags["image_datauri"] = chunk.uri
                        chunk.tensor = chunk.tensor.astype(np.uint8)
                        chunk.set_image_tensor_shape((64, 64))
                        chunk.set_image_tensor_normalization()


class ChunkMerger(Executor):
    @requests(on="/index")
    def merge_chunks(self, docs, **kwargs):
        for doc in docs:  # level 0 document
            for chunk in doc.chunks:
                if doc.text:
                    # this logic does not seem right.  docs does not have chuck.id as its array element
                    docs.pop(chunk.id)
                    # The original level 1 chunks - paras and pages, are not getting deleted due to this.
                    # ChunkMerger2 is created to address this.
            doc.chunks = doc.chunks[...]


class ChunkMerger2(Executor):
    @requests(on="/index")
    def merge_chunks(self, docs, **kwargs):
        for doc in docs:  # level 0 document
            popList = []
            for chunk in doc.chunks:
                if chunk.text:
                    popList.append(chunk.id)
            doc.chunks = doc.chunks[...]
            for chunkId in popList:
                doc.chunks.pop(chunkId)


EMB_DIM = 512


class EmbeddingChecker(Executor):
    @requests(on='/index')
    def check(self, docs, **kwargs):
       # filtered_docs = DocumentArray()
        for doc in docs:
            delChunks = []
            for chunk in doc.chunks:
                if chunk.embedding is None:
                    # del doc.chunks[chunk.id]
                    delChunks.append(chunk.id)
                    print('deleted - no embedding')
                    continue
                """
                if chunk.embedding.shape[0] != EMB_DIM:
                    # del doc.chunks[chunk.id]
                    delChunks.append(chunk.id)
                    print('deleted - dim is not 512')
                    continue
                """
            for delId in delChunks:
                del doc.chunks[delId]
        return docs


class TextChecker(Executor):
    @requests(on='/index')
    def checkText(self, docs, **kwargs):
        print("entering TextChecker")
       # filtered_docs = DocumentArray()
        for doc in docs:
            delChunks = []
            for chunk in doc.chunks:
                if chunk.text is None:
                    # del doc.chunks[chunk.id]
                    delChunks.append(chunk.id)
                    print('deleted - no text')
                    continue
                if chunk.text == '':
                    # del doc.chunks[chunk.id]
                    delChunks.append(chunk.id)
                    print('deleted - text is empty')
                    continue
                """
                if chunk.embedding.shape[0] != EMB_DIM:
                    # del doc.chunks[chunk.id]
                    delChunks.append(chunk.id)
                    print('deleted - dim is not 512')
                    continue
                """
            for delId in delChunks:
                del doc.chunks[delId]
        return docs


class Gpt3Encoder_o1(Executor):
    @requests(on='/index')
    def encodeGpt3(self, docs, **kwargs):
        print("entering Gpt3Encoder")
        docTextArray = []
        MODEL = "text-search-babbage-doc-001"

        """
        print("Docs summary at the beginning")
        docs.summary()
        print("Docs[0] summary at the beginning")
        docs[0].summary()
        print("Docs[0].chunks summary at the beginning")
        docs[0].chunks.summary()
        print("Docs[0].chunks[0] summary at the beginning")
        docs[0].chunks[0].summary()
        """

        for doc in docs:
            for chunk in doc.chunks:
                docTextArray.append(chunk.text)

        print("docTextArray length")
        print(len(docTextArray))
        # encode the text array
        res = openai.Embedding.create(
            input=docTextArray, engine=MODEL)
        # print("res is:")
        # print(res)
        # extract embeddings to a list
        embeds = [record['embedding'] for record in res['data']]
        # print("embeds:")
        # print(embeds)

        # update the embedding in docs
        counter = 0
        for doc in docs:
            for chunk in doc.chunks:
                chunk.embedding = np.array(embeds[counter])
                counter += 1

        """
        print("docs summary  & docs.chunks[0] at the end:")
        print(docs.summary())
        print("Docs[0] summary at the end")
        docs[0].summary()
        print("Docs[0].chunks summary at the end")
        docs[0].chunks.summary()
        print("Docs[0].chunks[0] summary at the end")
        docs[0].chunks[0].summary()

        print("counter = ", counter)
        """


class Gpt3Encoder(Executor):
    @requests(on='/index')
    def encodeGpt3(self, docs, **kwargs):
        print("entering Gpt3Encoder")
        docTextArray = []
        # MODEL = "text-search-babbage-doc-001"
        MODEL = "text-search-davinci-doc-001"

        for doc in docs:
            for chunk in doc.chunks:
                docTextArray.append(chunk.text)

            print("docTextArray length")
            print(len(docTextArray))
            # encode the text array
            res = openai.Embedding.create(
                input=docTextArray, engine=MODEL)

            embeds = [record['embedding'] for record in res['data']]

            # update the embedding in docs
            counter = 0
            for chunk in doc.chunks:
                chunk.embedding = np.array(embeds[counter])
                counter += 1

            # clear the docTextArray for next iteration
            docTextArray = []


class Gpt3Encoder_search(Executor):
    @requests(on='/search')
    def encodeGpt3_search(self, docs, **kwargs):
        print("entering Gpt3Encoder_search")

        # MODEL = "text-search-davinci-query-001"
        MODEL = "text-search-babbage-query-001"

        print("Docs summary at the beginning")
        docs.summary()
        docs[0].summary()

        for doc in docs:
            print("doc.text: ", doc.text)

        # encode the text array
        res = openai.Embedding.create(
            input=docs[0].text, engine=MODEL)

        # extract embeddings from res
        # embeds = [record['embedding'] for record in res['data']]
        embed = res['data'][0]['embedding']
        # print("embed is:", embed)
        docs[0].embedding = np.array(embed)


CHUNK_SIZE_LIMIT = 1000  # number of  chars in the chunk


class MergeChunks(Executor):
    @requests(on='/index')
    def mergeChunks(self, docs, **kwargs):
        for doc in docs:
            chunks_size = len(doc.chunks)
            mask = [False] * chunks_size
            i = 0
            while (i < chunks_size):
                j = i
                mask[i] = False
                while (len(doc.chunks[j].text) < CHUNK_SIZE_LIMIT):
                    i += 1
                    if (i < chunks_size):
                        doc.chunks[j].text += doc.chunks[i].text
                        mask[i] = True
                    else:
                        break
                i += 1
            del doc.chunks[mask]
                