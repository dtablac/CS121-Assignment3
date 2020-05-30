# ICSearch!

### Basic Flask app for a search engine on a discrete collection of ICS domains from UCI.

Dependencies (pip install):

    Flask
    
    BeautifulSoup
    
    Nltk

Please unzip this folder (corpus of webpages) in the same directory as src:

    https://drive.google.com/file/d/1WQVzu6Bctv4M8jKGA56hOhVJcKImxiy2/view?usp=sharing

To create the index on the collection, navigate to the src folder and run:

    python3 create_index.py
  
Run the search engine and open your web browser to http://localhost:5000

    python3 main.py
  
