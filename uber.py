import requests
import json


class Comment:

	def __init__(self, res, url = None):
		self.user_id = res["userId"]
		self.username = res["user"]["displayName"]
		self.content = res["text"]
		self.replies = []
		self.url = url
		
		# Get replies
		if res["childrenTotal"] > 0 and url != None:
			try:
				replyId = res["children"][0]["commentId"]
				self.replies.append(Comment(res["children"][0]))
				for res in self.get_replies(replyId):
					self.replies.append(Comment(res))
			except IndexError:
				self.replies = []

	def get_replies(self, _id):
		url = extractCode(self.url)
		endpoint = "https://comment-cdn.9gag.com/v1/cacheable/comment-list.json"
		params = f"?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&url=http:%2F%2F9gag.com%2Fgag%2F{url}&count=1000&order=score&refCommentId={_id}&origin=https:%2F%2F9gag.com"
		res = requests.get(endpoint+params).json()["payload"]["comments"]
		return res


def get_comments(url):
	code = extractCode(url)
	endpoint = "https://comment-cdn.9gag.com/v1/cacheable/comment-list.json"
	params = f"?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&url=http:%2F%2F9gag.com%2Fgag%2F{code}&count=1000&order=score&origin=https:%2F%2F9gag.com"

	link = endpoint + params
	response = requests.get(link).json()["payload"]["comments"]

	comments = []
	for res in response:
		comment = Comment(res, url)
		comments.append(comment)
	
	return comments

def extractCode(url):
    i = len(url)-1
    code = ""
    while i != 0:
        if url[i] == '/':
            break

        code = url[i] + code
        i -= 1

    return code

if __name__ == "__main__":
	get_comments("https://9gag.com/gag/aKdE7oZ")
	pass