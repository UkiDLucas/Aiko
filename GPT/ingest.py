#!/usr/bin/env python3
import os
import glob
import timeit # execution timer
from typing import List
from dotenv import load_dotenv
from multiprocessing import Pool
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from constants import CHROMA_SETTINGS





# adding AIKO/GPT/python/ to the system path
#import sys
#sys.path.insert(0, '/Users/uki_lucas/AIKO/GPT/python/')

load_dotenv()

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)



import time
obj = time.gmtime(0)
epoch = time.asctime(obj)
print("The epoch is:",epoch)
curr_time = round(time.time()*1000)
print("Milliseconds since epoch:",curr_time)

class MethodTimer:

    def __init__(self):
        print("Initialize MethodTimer.")
        self.start_time = time.time()
        print( "> starting timer ", self.start_time )
    
    def print_time(self, text):
        elapsed_time = time.time() - self.start_time
        print(text, ": elapsed: ", round(elapsed_time * 1000 * 1000), "s" )


timer = MethodTimer()
timer.print_time("testing")

class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"]="text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc
    





# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}



# Load environment variables
persist_directory = os.environ.get('PERSIST_DIRECTORY', 'db')
source_directory  = os.environ.get('SOURCE_DIRECTORY', 'text_corpus')

# all-MiniLM-L6-v2:
# It maps sentences & paragraphs to a 384 dimensional dense vector space 
# and can be used for tasks like clustering or semantic search.
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME', 'all-MiniLM-L6-v2')
chunk_size = 500
chunk_overlap = 50




def load_single_document(file_path: str) -> Document:
    print(file_path)
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()[0]

    raise ValueError(f"Unsupported file extension '{ext}'")


def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, doc in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.append(doc)
                pbar.update()

    return results

def split_docs(ignored_files: List[str] = []) -> List[Document]:
    """
    Load documents and split in chunks
    """
    print(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        print("No new documents to load!")
        exit(0)
    print(f"Loaded {len(documents)} new documents from {source_directory}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts

def does_vectorstore_exist(persist_directory: str) -> bool:
    """
    Checks if vectorstore exists
    """
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(persist_directory, 'chroma-embeddings.parquet')):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False

def main():
    start = timeit.timeit()

    # embeddings or (dense vector representations) 
    # used for sentences, paragraphs and images
    # capture the semantic meaning (message conveyed by words)
    # Texts are embedded in a vector space 
    # such that similar text is close, 
    # which enables applications 
    # such as semantic search, clustering, and retrieval.
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name) 
    # e.g. model_name = all-MiniLM-L6-v2
    # This is a sentence-transformers model: 
    # It maps sentences & paragraphs to 
    # a 384 dimensional dense vector space 
    # example: [[ 7.35148564e-02 -5.03818206e-02 -1.22386590e-01  2.37028450e-02 ...
    # and can be used for tasks like clustering or semantic search.

    if does_vectorstore_exist(persist_directory):
        # Update and store locally vectorstore
        print(f"Appending to existing vectorstore at {persist_directory}")
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
        collection = db.get()
        texts = split_docs([metadata['source'] for metadata in collection['metadatas']])
        print("Text corpus read in: ", timeit.timeit() - start)
        print(f"Creating embeddings. May take some minutes...")
        try:
            db.add_documents(texts)
            print(f"Added new text.")
        except Exception as e:
            print('An error occurred in db.add_documents(texts): ', e)
    else:
        # Create and store locally vectorstore
        print("Creating new vector store: ", persist_directory)
        texts = split_docs()
        print("Text corpus read in: ", timeit.timeit() - start)
        print(f"Creating embeddings db. May take some minutes...")
        db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS)
    db.persist()
    db = None

    print(f" Ingestion complete. Run python privateGPT.py ")
    end = timeit.timeit()
    print("It took: ", end - start)


if __name__ == "__main__":
    main()


