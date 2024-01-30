## Quail: A QA-First, Hallucination-Lite, Multi-LM Summarizer (COMING SOON!)
### How it works
First, we take the inputted passage, split it into individual sentences, and rank each sentence by relevance to the query using SentenceTransformers. We then take the top-n ranked sentences, combine them back into a new passage, and use FastChat-T5, a Text-To-Text Transfer Transformer Learning-based langague model to summarize the passage. FastChat-T5 is based on Google's Flan XL T5 Model.
### How to use
Paste in your passage, and query, and hit 'Go'! Depending on how busy the site is, it may take some time for you to get your summary. Using a Redis database, we queue summary jobs, and execute them one-by-one in the order that they are recieved. Each summary takes around 30 seconds. (Note, Summary Generation is still a WIP)
### Dependencies
- [SentenceTransformers](https://www.sbert.net/)
- [FastChat-T5](https://huggingface.co/lmsys/fastchat-t5-3b-v1.0)
- [Redis](https://redis.io/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Docker](https://www.docker.com/)
### Attribution
This summarization method originates from a paper submited to the iKAT Track of the 2023 Run of the Text Retreiveal Conference (TREC) entitled [Sequencing Matters: A Generate-Retrieve-Generate Model for Building Conversational Agents
](https://arxiv.org/abs/2311.09513). See the full code for that on my Github.
