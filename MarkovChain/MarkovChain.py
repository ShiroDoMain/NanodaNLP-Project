import random
import sys
from typing import Dict, List
import re


class Markov:
    rank: int = 3
    state: str = ""
    content: Dict[str,List[str]] = None

    def __init__(
        self,
        rank: int = rank,
        state: str = state,
        content = content
        ) -> None:
        self.rank = rank
        self.state = state
        self.content = content or {"##START##":[]}

    def append(self,text:str) -> None:
        text = re.sub("\s|\n|\t|“|”|【|】|（|）|「|」","",text.strip())
        for word1,word2 in self.process(text):
            if word1 not in self.content.keys():
                self.content[word1] = []
            self.content[word1].append(word2)

    def process(self,text:str):
        if len(text) < self.rank+1:return
        start = text[:self.rank]
        self.content["##START##"].append(start)
        for i in range(self.rank,len(text)):
            if i == self.rank:
                yield (start,text[i])
            elif i == len(text) - 1:
                yield text[i],"##END##"
                return
            else:
                yield text[i],text[i+1]

    def gen(self,text:str,max=100) -> str:
        # if len(text) < self.rank+1:
        #     return
        text = text or random.choice(self.content.get("##START##"))
        start = text[0:self.rank]
        result = start
        for i in range(max):
            arr = self.content.get(start)
            if arr is None:
                arr = self.content.get(start[0])
                start = start[0]
                if arr is None:
                    return
            suffix = random.choice(arr)#arr[random.randrange(len(arr))]
            if suffix == "##END##":
                break
            result += suffix
            start = suffix
        return result if result.endswith("。") else result+"。"

        


def fileGenerator(fileName:str):
    with open(fileName,"r") as f:
        while 1:
            yield f.readline()      

if __name__=="__main__":
    file = sys.argv[1]
    fg = fileGenerator(fileName=file)
    mk = Markov()
    for line in fg:
        mk.append(line)
    print(mk.gen())


