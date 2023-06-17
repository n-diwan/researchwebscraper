import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_arxiv():
    url = 'https://arxiv.org/list/quant-ph/new'  # ArXiv URL for the new quantum physics papers
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    papers = []
    results = soup.find_all('div', class_='meta')

    for result in results:
        paper = {}

        title = result.find('div', class_='list-title mathjax').text.strip()
        authors = result.find('div', class_='list-authors').text.strip()
        status = result.find('div', class_='list-subjects').text.strip()
        description_element = result.find('p', class_='mathjax')

        if description_element:
            description = description_element.text.strip()
        else:
            description = 'No description available'

        paper['Title'] = title
        paper['Authors'] = authors
        paper['Publication Status'] = 'Journal' if 'journal' in status.lower() else 'Non-Journal'
        paper['Description'] = description

        papers.append(paper)

    return papers

def filter_papers(papers, topics):
    filtered_papers = []
    for paper in papers:
        description = paper['Description'].lower()
        paper_topics = []
        for topic in topics:
            if topic.lower() in description:
                paper_topics.append(topic)
        paper['Topics'] = ', '.join(paper_topics)
        if paper_topics:
            filtered_papers.append(paper)
    return filtered_papers

def main():
    papers = scrape_arxiv()

    if papers:
        # Specify the topics to filter
        topics = [
            'quantum mechanics',
            'quantum computation',
            'quantum information theory',
            'quantum algorithms',
            'quantum entanglement',
            'quantum optics',
            'quantum simulations',
            'quantum cryptography',
            'quantum error correction',
            'quantum machine learning'
        ]

        filtered_papers = filter_papers(papers, topics)

        if filtered_papers:
            df = pd.DataFrame(filtered_papers)
            df.to_excel('arxiv_papers_filtered.xlsx', index=False)
            print("Filtered data saved successfully to 'arxiv_papers_filtered.xlsx'.")
        else:
            print("No papers found for the specified topics.")
    else:
        print("No papers found.")

if __name__ == '__main__':
    main()
