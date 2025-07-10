import os, sys, shutil, re
from typing import List
from pathlib import Path
import uuid

from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
#from langchain_community.llms import OpenAI
#from langchain_community.vectorstores import Chroma
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition, MatchValue
from langchain_core.vectorstores import VectorStore
from datetime import datetime

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

os.environ["OPENAI_API_KEY"] = ""

class ChatGPT:
    db = None
    client = None
    llm = None
    chain = None
    chat_history = None
    # Enable to save to disk & reuse the model (for repeated queries on the same data)
    DATA_PATH = "data"
    PERSIST_FOLDER = "chroma"

    RAG_ADD = 1
    RAG_UPDATE = 2
    RAG_DELETE = 3

    #    DEFAULT_SET="**/[!.]*"
    DEFAULT_SET = [
        "*.csv",
        "*.doc",
        "*.docx",
        "*.epub",
        "*.pdf",
        "*.txt",
        "*.md",
        "*.msg",
        "*.odt",
        "*.org",
        "*.ppt",
        "*.pptx",
        "*.rtf",
        "*.rst",
        "*.tsv",
        "*.xlsx",
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.bmp",
        "*.tiff",
        "*.tif"
    ]

    def __init__(self):
        # Initialize the conversation index and chain
        self.init_system()
        self.chat_history = []

    def init_system(self):
        self.db = self.init_index()
        self.client = self.init_llm()
        return self.chain

    def init_index(self, data_path=DATA_PATH):
        print("Connect to Qdrant database ...")
        embeddings = OpenAIEmbeddings()
        qdrant_client = QdrantClient(host="qdrant", port=6333)
        
        # Check if collection exists, create if not
        collections = qdrant_client.get_collections().collections
        if not any(c.name == "datia_k12" for c in collections):
            qdrant_client.create_collection(
                collection_name="datia_k12",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )

        self.db = QdrantVectorStore(
            client=qdrant_client,
            collection_name="datia_k12",
            embedding=embeddings
        )
        return self.db
 
    def init_llm(self):
        # Define your prompt template
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        # Initialize OpenAI client with the API key
        self.client = OpenAI(api_key=openai_api_key)
        return self.client

    def extract_chapter_title(self, text: str) -> str:
        """
        Attempt to extract chapter/section titles using common patterns.
        Modify this based on the book's structure.
        """
        patterns = [
            r"^Chapter\s+\d+\s*[:\-]?\s*(.+)",     # "Chapter 1: Intro"
            r"^CHAPTER\s+[A-Z]+\s*[:\-]?\s*(.+)",  # "CHAPTER ONE: BEGINNING"
            r"^第[一二三四五六七八九十百千]+章\s*(.+)"   # Japanese chapters
        ]

        lines = text.splitlines()
        for line in lines:
            for pattern in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    return match.group(0).strip()
        return "Unknown Section"

    # def split_save_documents(self, docs):
    #     splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=1000,
    #         chunk_overlap=200,
    #         separators=["\n\n", "\n", ".", " ", ""]
    #     )
    #     split_docs = []
    #     for doc in docs:
    #         raw_chunks = splitter.split_text(doc.page_content)
    #         for chunk in raw_chunks:
    #             title = self.extract_chapter_title(chunk)
    #             split_docs.append(
    #                 Document(
    #                     page_content=chunk,
    #                     metadata={
    #                         "source": doc.metadata.get("source", "  "),
    #                         "chapter": title
    #                     }
    #                 )
    #             )
    #     self.db.add_documents(split_docs)

    def split_save_documents(self, docs, file, month: str, year: str):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        print(f"docs: {docs}")
        print(f"split_save_documents file: {file}")

        split_docs = []
        for doc in docs:
            raw_chunks = splitter.split_text(doc.page_content)

            for i, chunk in enumerate(raw_chunks):
                # Generate a unique ID for each chunk
                chunk_id = str(uuid.uuid4())

                chunk_with_prefix = chunk

                # Copy existing metadata and add new fields: month, year, id
                metadata = dict(doc.metadata)
                metadata['month'] = month
                metadata['year'] = year
                metadata['id'] = chunk_id
                metadata['disabled'] = False
                split_docs.append(
                    Document(
                        page_content=chunk_with_prefix,
                        metadata=metadata
                    )
                )

        # ✅ Store into Qdrant
        self.db.add_documents(split_docs)

    # This function must called after creating Chroma DB
    def load_files(self, data_path=DATA_PATH, files=DEFAULT_SET, month: str = None, year: str = None):
        current_date = datetime.now()
        month = month or current_date.strftime("%B")
        year = year or str(current_date.year)
        print(f"files: {files}")

        loaded_files = []
        for file in files:
            loader = DirectoryLoader(data_path, glob=file)
            docs = loader.load()
            # if nothing to load
            if docs != []:
                self.split_save_documents(docs, file, month, year)
                loaded_files.append(file)

        return loaded_files

    def extract_filters_from_query(self, query: str):
        month = None
        year = None

        months = r"January|February|March|April|May|June|July|August|September|October|November|December"
        
        month_pattern = rf"\b({months})\b"
        month_match = re.search(month_pattern, query, re.IGNORECASE)
        if month_match:
            month = month_match.group(1).capitalize()

        year_pattern = r"\b(20\d{2})\b"
        year_match = re.search(year_pattern, query)
        if year_match:
            year = year_match.group(1)

        return month, year

    def update_disabled_status(self, identifier: str, disabled: bool, by_id: bool = False):
        """
        Update the disabled status of documents by id or source.
        :param identifier: The id or source filename to identify documents.
        :param disabled: The new disabled status (True/False).
        :param by_id: If True, identifier is treated as an id; otherwise, as a source filename.
        """
        key = "id" if by_id else "source"
        docs = self.db.client.search(
            collection_name="datia_k12",
            query_vector=[0] * 1536,  # Dummy vector for filtering
            query_filter=Filter(must=[FieldCondition(key=key, match=MatchValue(value=identifier))]),
            limit=1000
        )
        if not docs:
            return {"success": False, "message": f"No documents found with {key}: {identifier}"}

        # Update metadata for each document
        for doc in docs:
            self.db.client.set_payload(
                collection_name="datia_k12",
                payload={"disabled": disabled},
                points=[doc.id]
            )
        
        return {"success": True, "message": f"Updated disabled status to {disabled} for {len(docs)} documents with {key}: {identifier}"}

    # Save chat history for next query, this will help to keep chat context.
    def query_ai(self, query, month=None, year=None):
        print(f"query: {query}, month: {month}, year: {year}")   

        if not month or not year:
            extracted_month, extracted_year = self.extract_filters_from_query(query)
            month = month or extracted_month
            year = year or extracted_year

        filters = []
        if month:
            filters.append(FieldCondition(key="month", match=MatchValue(value=month)))
        if year:
            filters.append(FieldCondition(key="year", match=MatchValue(value=year)))
        
        if filters:
            metadata_filter = Filter(must=filters)
            retriever = self.db.as_retriever(search_kwargs={"k": 3, "filter": metadata_filter})
        else:
            retriever = self.db.as_retriever(search_kwargs={"k": 3})

        print(f"retriever: {retriever}") 
        # This for HuggingFace's Retrieval-Augmented Generation (RAG) model
        # formatted_query = f"query: {query.strip()}"
        formatted_query = f"{query.strip()}"
        retrieved_data = retriever.invoke(formatted_query)
        prompt = None
        # print(retrieved_data )
        # Step 2: Prepare the prompt for ChatGPT
        if retrieved_data:
            prompt = f"Based on the following information: {retrieved_data}, please provide a summary or answer to the query: {query}"
        else:
            prompt = f"I couldn't find relevant information for your query: {query}. Can you provide more details?"        

        # Prepare the message payload
        messages = [
            {
                "role": "system",
                "content": "You are a knowledgeable assistant that summarizes and provides insights based on book content."
                #"content": "You are a versatile assistant that answers questions and provides summaries based on various types of information."

            },
            {
                "role": "user",
                "content": prompt  # Directly use the prompt
            }
        ]

        try:
            response = self.client.chat.completions.create(                
                model="gpt-4.1-mini",
#                model="o4-mini",
                messages=messages,
                max_completion_tokens=10000
            )
#            print("response: ")            
#            print(response)            
        except Exception as e:
            print(f"An error occurred: {e}")
            response = None  # Handle the error according to your application logic        

        content_data = response.choices[0].message.content
        print(content_data)
        return content_data

    def getSourcefile(self, filename):
        print(f"DATA_PATH: {self.DATA_PATH}, filename: {filename}")
        if filename is None:
            return ""
        return f"/app/{self.DATA_PATH}/{filename}"

    def getFileName(self, sourcefile):
        return os.path.basename(sourcefile)

    def deletefile(self, identifier: str, by_id: bool = False):
        key = "id" if by_id else "source"
        docs = self.db.client.search(
            collection_name="datia_k12",
            query_vector=[0] * 1536,
            query_filter=Filter(must=[FieldCondition(key=key, match=MatchValue(value=identifier))]),
            limit=1000
        )
        ids_to_delete = [doc.id for doc in docs]
        if not ids_to_delete:
            return {"success": False, "message": f"No documents found with {key}: {identifier}"}
        self.db.client.delete(
            collection_name="datia_k12",
            points_selector=ids_to_delete
        )
        return {"success": True, "message": f"Deleted {len(ids_to_delete)} documents with {key}: {identifier}"}

    def getfilelist(self):
        try:
            points = self.db.client.scroll(
                collection_name="datia_k12",
                limit=1000,
                with_payload=True
            )[0]
            unique_sources = {point.payload.get("source") for point in points if point.payload.get("source")}
            base_names = [os.path.basename(source) for source in unique_sources]
            return base_names
        except Exception as e:
            print(f"Error retrieving file list: {e}")
            return []