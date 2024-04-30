import subprocess
import tempfile
import os

def open_in_browser(html_content: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        temp_file.write(html_content.encode('utf-8'))
        temp_file_path = temp_file.name
    subprocess.run(["firefox", temp_file_path])
