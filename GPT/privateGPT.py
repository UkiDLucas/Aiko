#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
from datetime import datetime
import os
import argparse
import timeit # execution timer

from python.query_private_embedings import query_private_embedings

load_dotenv() # make sure you edited .env file


# Load environment variables

# all-MiniLM-L6-v2:
# It maps sentences & paragraphs to a 384 dimensional dense vector space 
# and can be used for tasks like clustering or semantic search. 
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
persist_directory = os.environ.get('PERSIST_DIRECTORY', 'db')
model_type = os.environ.get('MODEL_TYPE', "GPT4All")
model_path = os.environ.get('MODEL_PATH', "models/ggml-gpt4all-j-v1.3-groovy.bin")
model_n_ctx = os.environ.get('MODEL_N_CTX', "4000")

from constants import CHROMA_SETTINGS

def main():
    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    retriever = db.as_retriever()
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False)
        case "GPT4All":
            llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', callbacks=callbacks, verbose=False)
        case _default:
            print(f"Model {model_type} not supported!")
            exit;
    retrievalQA = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= not args.hide_source)
    # Interactive questions and answers
    while True:
        print("============================================================")
        query = input("\nEnter keywords to be found in the private corpus: \n")
        if query == "exit":
            break
        
        start = timeit.timeit()
        now = datetime.now()
        print("\n\n> Start: ", now.strftime("%H:%M:%S") )
        # Get the answer from the chain

        text_snippet_Dict = query_private_embedings(query, retrievalQA)
        print("time elapsed: ", timeit.timeit() - start)

        res = qa(query)
        print("time elapsed: ", timeit.timeit() - start)

        for key, value in text_snippet_Dict.items():
            print("{} ({})".format(key, value))

        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        print("\n> Answer:")
        # print(answer)

        # Print the relevant sources used for the answer
        for document in docs:
            print("\n> " + document.metadata["source"] + ":")
            print(document.page_content)
        
        print("END time elapsed: ", timeit.timeit() - start)

def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()


if __name__ == "__main__":
    main()
