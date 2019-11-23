import json
import csv

if __name__ == "__main__":
	path = input("Enter path: ")
	with open(path, "r") as jf:
		with open("data.csv", "a") as cf:
			writer = csv.writer(cf)
			writer.writerow(["id", "username", "Assent Word Count", "Singular Pronoun Count", "Reply Count", "Average WordCount", "Average Assent WordCount", "Average SP WordCount"])
			for item in json.load(jf):
				writer.writerow([item["_id"], item["username"], item["assent_words"], item["singular_pronouns"], item["reply_count"], item["avg_word_count"], item["avg_assent_wordcount"], item["avg_sp_wordcount"]])

	