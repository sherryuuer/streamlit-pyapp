import streamlit as st
import requests

# Function URL
url = "https://6dskoikdkrqfq3kbi5455uzp2y0wkrfl.lambda-url.ap-northeast-1.on.aws/"


def process_vtt_file(vtt_content):
    lines = vtt_content.splitlines()
    filtered_lines = [line for line in lines if line.startswith('<v')]
    return '\n'.join(filtered_lines)


def main():
    st.title("VTT File Processor")

    uploaded_file = st.file_uploader("Upload your VTT file", type="vtt")

    if uploaded_file is not None:
        vtt_content = uploaded_file.read().decode('utf-8')
        processed_content = process_vtt_file(vtt_content)

        st.text_area("Processed VTT Content", processed_content, height=200)

        if st.button("Submit to API"):
            headers = {'Content-Type': 'application/octet-stream'}
            response = requests.post(
                url, data=processed_content.encode('utf-8'), headers=headers)

            if response.status_code == 200:
                st.success("POST successful")
                st.text_area("API Response", response.text.encode(
                    'utf-8').decode('unicode_escape'), height=200)
            else:
                st.error(f"Failed with status code: {response.status_code}")
                st.text_area("API Response", response.text, height=200)


if __name__ == "__main__":
    main()
