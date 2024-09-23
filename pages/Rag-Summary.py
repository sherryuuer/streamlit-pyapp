import streamlit as st
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


# 处理 PDF
def process_pdf(pdf_path, api_key):
    CHUNK_SIZE = 700
    CHUNK_OVERLAP = 100

    pdf_loader = PyPDFLoader(pdf_path)
    split_pdf_document = pdf_loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    context = "\n\n".join(str(p.page_content) for p in split_pdf_document)
    texts = text_splitter.split_text(context)

    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/embedding-001',
        google_api_key=api_key
    )

    vector_index = Chroma.from_texts(texts, embeddings)
    retriever = vector_index.as_retriever(search_kwargs={"k": 5})

    return retriever


# 处理 VTT 文件
def process_vtt_file(vtt_content):
    lines = vtt_content.splitlines()
    filtered_lines = [line for line in lines if line.startswith('<v')]
    return '\n'.join(filtered_lines)


# 根据 PDF 内容总结 VTT 文件
def summarize_vtt(vtt_content, retriever, api_key):
    gemini_model = ChatGoogleGenerativeAI(
        model='gemini-pro',
        google_api_key=api_key,
        temperature=0.8
    )

    qa_chain = RetrievalQA.from_chain_type(
        gemini_model,
        retriever=retriever,
        return_source_documents=True
    )

    # 使用 PDF 生成的 embedding 提问
    question = f"""
        Summarize the VTT file based on the PDF content:\n\n{vtt_content}
        """
    result = qa_chain.invoke({"query": question})

    return result["result"]


# Streamlit 应用程序
def main():
    st.title("PDF & VTT File Processor")

    # 用户输入 API 密钥
    api_key = st.text_input("Enter your Google API key", type="password")

    if api_key:
        # 上传 PDF 文件
        uploaded_pdf = st.file_uploader("Upload your PDF file", type="pdf")

        # 上传 VTT 文件
        uploaded_vtt = st.file_uploader("Upload your VTT file", type="vtt")

        if uploaded_pdf and uploaded_vtt:
            with st.spinner("Processing PDF..."):
                pdf_path = uploaded_pdf.name
                retriever = process_pdf(pdf_path, api_key)

            vtt_content = uploaded_vtt.read().decode('utf-8')
            processed_vtt = process_vtt_file(vtt_content)

            with st.spinner("Summarizing VTT based on PDF..."):
                summary = summarize_vtt(processed_vtt, retriever, api_key)
                st.text_area("VTT Summary", value=summary, height=300)


if __name__ == "__main__":
    main()
