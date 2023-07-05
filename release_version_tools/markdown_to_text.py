from bs4 import BeautifulSoup
from markdown import markdown
import re

def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text

def parse_markdown_to_text(file_name:str) -> str:
    with open(file_name) as changelog_file:
        change_log_text = ""
        for line in changelog_file:
            if line == "":
                break
            change_log_text += "\n"
            change_log_text += markdown_to_text(line)
    print(change_log_text)

if __name__=="__main__":

    with open('CHANGELOG.md') as changelog_file:
        change_log_text = ""
        for line in changelog_file:
            if line is None:
                break
            change_log_text += "\n"
            change_log_text += markdown_to_text(line)
    print(change_log_text)
