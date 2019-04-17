## Demo Analysis Tool for Instrumented Classroom
from functools import reduce  # f xs z
import json
import string
import argparse
import nltk
from nltk.tokenize import MWETokenizer


PUNCT = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'


parser = argparse.ArgumentParser(description="Takes in a transcript generated "\
                                   "from the instrumented classroom tool and "\
                                   "a JSON file, specifying the state machine "\
                                   "to apply to the transcript.",
                                 prog="icap.py")

parser.add_argument('transcript', help=".json transcript file")
parser.add_argument('states', help=".json state specification file")
args = parser.parse_args()


## Import states and flags from JSON object
with open(args.states, 'r') as fp_states:
    states = json.load(fp_states) 

## Import transcript
with open(args.transcript, 'r') as fp_trans:
  transcript = json.load(fp_trans)

# transcript = open(args.transcript)


flags = reduce(lambda ls, d: ls + d["flags"], states, [])
tokenizer = MWETokenizer(flags)
# transcript = transcript.splitlines() # need for text block
# print(flags)
# print(transcript)
 
## Add flags in the token representation for each state
for state in states:
    state["token_flags"] = list(map(lambda phr: '_'.join(phr), state["flags"]))


for trans in transcript:
    line = trans["transcript"]
    line_no_punct = line.translate(str.maketrans('', '', PUNCT)).lower()
    
    tokens = tokenizer.tokenize(line_no_punct.split())
    
    ls = list(map(lambda tok: reduce(lambda p_res, s: (tok, s["state"]) if (tok in s["token_flags"]) else p_res, states, None), tokens))
    
    states_found = list(filter(None, ls))

    if (states_found != []):
      timing = (trans["word_timings"][0]["start_time"], trans["word_timings"][-1]["end_time"])
      print('\n', line, '\n', states_found, timing)

    # print(line)
    # print(tokens)

# transcript.close()