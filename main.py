import requests
import bs4
from urllib.parse import quote as encodeurl
import time
import random
import json
import sys
import uber


from datetime import datetime
from nltk.corpus import stopwords

STOPWORD_LIST = set(stopwords.words('english'))

WORDLIST = {
    "assent": ["yes", "ok", "alright", "fine", "right", "agree", "okay", "confirm", "approve", "pass", "accept"],

    "sp": ["you", "he", "she", "it", "one", "me", "i", 
            "they", "him", "her", "my", "mine", "your", 
            "yours", "his", "her", "hers", "its",
            "who", "whom", "whose", "what", "which",
            "another", "each", "everything", "nobody", "either", "someone",
            "whose", "that", "myself", "yourself", "himself", "herself", "itself",
            "this"]
}


class User:
    

    def __init__(self, _id, username):
        self._id = _id
        self.username = username
        self.comments = []
        self.avg_word_count = 0
        self.words_used = []
        self.assent_words = 0
        self.singular_pronouns = 0
        self.reply_count = 0
        self.avg_assent_wordcount = 0
        self.avg_sp_wordcount = 0   

    def add_comment(self, comment):
        self.reply_count += 1
        self.comments.append(comment)

        new_words = self.count_words(comment)
        for token in new_words:
            if token[0] not in [word[0] for word in self.words_used]:
                self.words_used.append(token)
            else:
                for i, usedword in enumerate(self.words_used):
                    if usedword[0] == token[0]:
                        self.words_used[i][1] += token[1]

        self.words_used.sort(key = lambda token : token[1], reverse = True)

        for token in comment.split():
            if token.lower() in WORDLIST["assent"]:
                self.assent_words += 1
            elif token.lower() in WORDLIST["sp"]:
                self.singular_pronouns += 1
        
        totalLength = 0
        
        for s in self.comments:
            totalLength += len(s.split())
            

        self.avg_word_count = totalLength / len(self.comments)
        self.avg_assent_wordcount = self.assent_words / len(self.comments)
        self.avg_sp_wordcount = self.singular_pronouns / len(self.comments)



    def count_words(self, comment):
        wordlist = []
        tokens = comment.split()

        for token in tokens:

            if token in STOPWORD_LIST:
                continue

            if token in [word[0] for word in wordlist]:
                for count in wordlist:
                    if count[0] == token:
                        count[1] += 1
                        break
                continue

            wordlist.append([token, 1])
        return wordlist

def user_in_list(userid, userlist):
    if userid in [users._id for users in userlist]:
        return True
    return False

def log_user_invlovement(comments):
    userlist = []

    all_comments = []
    for comment in comments:
        all_comments.append(comment)
        for reply in comment.replies:
            all_comments.append(reply)

    progress = 0
    for comment in all_comments:
        progress += 1
        if user_in_list(comment.user_id, userlist):
            for i, user in enumerate(userlist):
                if user._id == comment.user_id:
                    userlist[i].add_comment(comment.content)
        else:
            newuser = User(comment.user_id, comment.username)
            newuser.add_comment(comment.content)
            userlist.append(newuser)

        sys.stdout.write(f"\rProgress:{progress}/{len(all_comments)}")
        sys.stdout.flush()

    print("....Done!")
    return userlist


def main():

    url = "https://9gag.com/v1/featured-posts"
    raw = requests.get(url).json()

    items = raw["data"]["items"]
    with open(f"result_{datetime.now()}.json", "w") as file:
        comments = []
        for item in items:
            url = item["url"]
            print(f"loading {url}")
            comments.extend(uber.get_comments(url))
            
        userlist = log_user_invlovement(comments)
        userlist.sort(key = lambda obj : obj.reply_count, reverse = True)
        file.write(json.dumps([item.__dict__ for item in userlist], sort_keys=True, indent=4, separators=(',', ': ')))

        print(f"Number of users: {len(userlist)}")
        print(f"Total number of posts: {len(items)}")
        

if __name__ == "__main__":
    main()
