import redis
import json
from transformers import (
    AutoModelForSeq2SeqLM,
    T5Tokenizer,
)
from transformers import AutoTokenizer, T5ForConditionalGeneration
from sentence_transformers import SentenceTransformer, util
import sys

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

tokenizer = AutoTokenizer.from_pretrained(
    "lmsys/fastchat-t5-3b-v1.0", legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "lmsys/fastchat-t5-3b-v1.0", load_in_8bit=True)
device = "cuda"
st_model = SentenceTransformer('paraphrase-MiniLM-L6-v2',device='cuda')

while True:
    queue = r.get("quail_queue")
    try:
        queue = json.loads(queue)
    except:
        queue = []
    for item in queue:
        new_item = item
        new_item["response"] = summarize_with_fastchat(item['text'],item['question'],True)
        new_item["isComplete"]

def rank(passage, question):
    def merge_sentances_into_paragraph(sentances):
        ans = ""
        for s in sentances:
            ans += f"{s[0]}. "
        return ans

    sentances = passage.split('.')
    question_embedding = st_model.encode(question, convert_to_tensor=True)

    statement_embeddings = st_model.encode(sentances, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(question_embedding, statement_embeddings)

    ranked_statements = sorted(
        zip(sentances, cosine_scores.tolist()[0]), key=lambda x: x[1], reverse=True
    )
    return merge_sentances_into_paragraph(ranked_statements)

def summarize_with_fastchat(passage, question, rankSentances=True):
    MAX_PASSAGE_LENGTH = 512  # char
    if rankSentances == False:
        passage = f"Human: Summarize this passage in 1-2 sentences {passage} Assistant: "
    else:
        passage = f"Human: Summarize this passage in 1-2 sentences {rank(passage, question)[:MAX_PASSAGE_LENGTH]} Assistant: "
    encoded_input = tokenizer.encode(passage, return_tensors='pt').to(device)
    output = model.generate(
        encoded_input, max_length=1024, temperature=0.7, top_p=1)
    decoded_output = tokenizer.decode(output[0, :], skip_special_tokens=True)
    decoded_output = decoded_output.replace('<pad> ', '')
    decoded_output = decoded_output.replace("  ", " ")
    print("GENERATED FASTCHAT SUMMARY")
    return decoded_output
