import streamlit as st
import requests

# Function URL
url = "https://6dskoikdkrqfq3kbi5455uzp2y0wkrfl.lambda-url.ap-northeast-1.on.aws/"

# Retrieve the password from Streamlit's secrets management
SECRET_PASSWORD = st.secrets["password"]


def process_vtt_file(vtt_content):
    lines = vtt_content.splitlines()
    filtered_lines = [line for line in lines if line.startswith('<v')]
    return '\n'.join(filtered_lines)


def main():
    st.title("VTT File Processor")

    # Password authentication
    password = st.text_input(
        "Enter password to access the application", type="password")
    submit_password = st.button("Submit Password")

    if submit_password:
        if password == SECRET_PASSWORD:
            st.success("Password is correct")
            st.session_state.authenticated = True
        else:
            st.error("Invalid password")
            st.session_state.authenticated = False

    if st.session_state.get("authenticated", False):
        uploaded_file = st.file_uploader("Upload your VTT file", type="vtt")

        if uploaded_file is not None:
            vtt_content = uploaded_file.read().decode('utf-8')
            processed_content = process_vtt_file(vtt_content)

            st.text_area(
                "Processed VTT Content",
                value=processed_content,
                height=200,
                max_chars=None,
                key="processed_vtt"
            )

            if st.button("Submit to API"):
                with st.spinner("Processing request..."):
                    headers = {
                        'Content-Type': 'application/octet-stream',
                        'X-Custom-Header': st.secrets["token"]
                    }
                    response = requests.post(
                        url,
                        data=processed_content.encode('utf-8'),
                        headers=headers
                    )

                    if response.status_code == 200:
                        st.success("POST successful")
                        st.markdown("### API Response")
                        st.markdown(
                            "```text\n" +
                            response.text.encode('utf-8').decode('unicode_escape') +
                            "\n```"
                        )
                    else:
                        st.error(
                            f"Failed with status code: {response.status_code}"
                        )
                        st.markdown("### API Response")
                        st.markdown(f"```text\n{response.text}\n```")


if __name__ == "__main__":
    main()
