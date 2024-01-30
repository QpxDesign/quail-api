import redis
import json
from transformers import (
    AutoModelForSeq2SeqLM,
    T5Tokenizer,
)
from transformers import AutoTokenizer, T5ForConditionalGeneration
from sentence_transformers import SentenceTransformer, util
import sys
import time
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
start_time = time.time()
tokenizer = AutoTokenizer.from_pretrained(
    "lmsys/fastchat-t5-3b-v1.0", legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "lmsys/fastchat-t5-3b-v1.0", load_in_8bit=True)
device = "cuda"
st_model = SentenceTransformer('paraphrase-MiniLM-L6-v2',device='cuda')
print(time.time()-start_time)
print("MODELS LOADED")

while True:
    for item in r.scan_iter("job:*"):
        new_item = item
        new_item["response"] = summarize_with_fastchat(item['text'],item['question'],True)
        new_item["isComplete"] = True
        r.set("quail_queue",json.dumps
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
        print("started rs")
        passage = f"Human: Summarize this passage in 1-2 sentences {rank(passage, question)[:MAX_PASSAGE_LENGTH]} Assistant: "
        print("ranked sentances")
    encoded_input = tokenizer.encode(passage, return_tensors='pt').to(device)
    print("encoded input")
    output = model.generate(
        encoded_input, max_length=1024, temperature=0.7, top_p=1).to(device)
    print("output gen")
    decoded_output = tokenizer.decode(output[0, :], skip_special_tokens=True)
    print("decoded")
    decoded_output = decoded_output.replace('<pad> ', '')
    decoded_output = decoded_output.replace("  ", " ")
    print("GENERATED FASTCHAT SUMMARY")
    return decoded_output
#a = summarize_with_fastchat("ngenuity, nicknamed Ginny, is an autonomous NASA helicopter that operated on Mars from 2021 to 2024 as part of the Mars 2020 mission. The helicopter arrived on the planet attached to the underside of the Perseverance rover, which landed February 18, 2021.[5][6] Ingenuity made its first flight on April 19, 2021, the first powered, controlled extraterrestrial flight by any aircraft.[7][8][9][10][11] Originally intended to make five flights, the rotorcraft greatly exceeded expectations and made a total of 72 flights over a period of about 3 years until rotor damage sustained in January 2024 forced an end to the mission.[4][12] The Perseverance rover, carrying Ingenuity, was landed at Octavia E. Butler Landing near the western rim of the 45 km (28 mi) wide Jezero crater.[13][14][15] Ingenuity's flights demonstrated that flight is possible in the extremely thin atmosphere of Mars, which is only 0.6% as dense as the air on Earth. Because radio waves take between 5 and 20 minutes to travel between Earth and Mars (depending on the planets' positions), Ingenuity cannot be controlled directly.[16] Instead, Ingenuity autonomously performed maneuvers planned, scripted, and transmitted to it by its operators at the Jet Propulsion Laboratory. The helicopter was intended to perform a 30-sol technology demonstration, making five flights at altitudes ranging from 3–5 m (10–16 ft) for up to 90 seconds each.[1][17] After a brief demonstration phase to prove its airworthiness, JPL commenced a series of flights designed to show how aerial scouting could aid the exploration of Mars and other worlds.[18][19] In this operational role Ingenuity scouted areas of interest for the Perseverance rover.[20][21][1][22] The helicopter's performance and resilience in the harsh Martian environment greatly exceeded expectations. The aircraft surpassed its required altitude and flight duration specifications soon after beginning operations on Mars. This allowed Ingenuity to perform far more flights than were initially expected of the aircraft.[23] On January 18, 2024, the helicopter was damaged upon landing during its 72nd flight, and NASA announced its retirement.[4][24] Ingenuity had flown for a total of two hours, eight minutes and 48 seconds in 1,004 days, covering more than 17 kilometres (11 mi).[25] Ingenuity was designed by NASA's Jet Propulsion Laboratory (JPL) in collaboration with AeroVironment, NASA's Ames Research Center and Langley Research Center.[26] Cont", "Who Designed the copter?",True)
#print(a)
