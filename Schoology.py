import requests
import json
from time import sleep
from requests_oauthlib import OAuth1Session


class SchoologyConsumer:
    """
        A simple class to easily interact with the schoology consumer api,
    consumer keys are only for accounts.
    """
    def __init__(self, consumer_key, consumer_secret):
        self.ck = consumer_key
        self.cs = consumer_secret
        self.osession = OAuth1Session(client_secret=self.cs,
                            client_key=self.ck,
                            signature_method='PLAINTEXT')
        self.userid = json.loads(self.osession.get("https://api.schoology.com/v1/users/me").content)["id"]

    def get_private_messages(self):
        """
            Return the dictionary of messages in the private inbox
        """
        a = self.osession.get("https://api.schoology.com/v1/messages/inbox").content
        return json.loads(a)

    def custom_get(self, url):
        """
            Make a get request to the specified url and return the result
        """
        a = self.osession.get(url).content
        try:
            return json.loads(a)
        except:
            return a
    def custom_post(self, url, data={}):
        """
            Make a post request to the specified url and return the result
        """
        a = self.osession.post(url, json=data).content
        try:
            return json.loads(a)
        except:
            return a

    def _parse(self, data):
        """
            internal function
        """
        try:
            return json.loads(data)
        except:
            return data

    def comment(self, comment, url_path):
        """
            Create a comment at the specifed url_path.
            Example url_path:
                    groups/1234567/discussions/123456789123/comments
                
        """
        test = {"comment": comment}

        OUT = self.osession.post("https://api.schoology.com/v1/" + url_path, json=test)
        return self._parse(OUT.content)

    def like_update(self, id, type=True):
        """
            Like an update with the specifed id
        """
        like = self.osession.custom_post(f"https://api.schoology.com/v1/like/{id}", data={"like_action": type})
        return self._parse(like)
        
    def like_comment(self, path_to_comment, type=True):
        """
            Like a comment with the specified id path
        """
        like = self.custom_post(f"https://api.schoology.com/v1/like/{path_to_comment}", data={"like_action": type})

    def mass_msg_bot(self, subj, message):
        """
            A bot that will send the subject and message to everyone whom the current user is able to send mesages to.
        """
        if input("Are you sure? (Y/N): ").upper() != "Y":
            return
        recipients = self.custom_get("https://api.schoology.com/v1/messages/recipients")
        for i in recipients["recipient"]:
            sleep(1)
            data ={
                "subject": f"{subj}",
                "message": f"{message}",
                "recipient_ids": f"{i['id']}"
            }
            self.custom_post("https://api.schoology.com/v1/messages", data=data)

    def get_updates(self):
        """
            Get the current updates from the homescreen
        """
        updates = self.custom_get("https://api.schoology.com/v1/recent")
        return updates

    def write_updates_to_file(self, file, limit=999999999999):
        updates = self.get_updates()
        trybytes = []
        cur = 0
        with open(file, "a") as e:
            for i in updates["update"]:
                if cur >= limit:
                    continue
                try:
                    e.write(i["body"] + "\n")
                except:
                    trybytes.append(i["body"] + "\n")
                cur += 1
        with open("bytes_" + file, "wb") as e:
            for i in trybytes:
                try:
                    e.write(i)
                except:
                    try:
                        e.write(i.encode())
                    except Exception as s:
                        print(f"Failed: {str(s)}")

    def like_all_updates(self, type=True, debug=True):
        """
            Like all current updates on the homescreen page.
        """
        updates = self.custom_get("https://api.schoology.com/v1/recent")

        for i in updates["update"]:
            if debug:
                print(f"Liked update with id: {i['id']}")
            #print(i)
            sleep(1)#cooldown to avoid rate limiting
            updatesd = self.custom_post(f"https://api.schoology.com/v1/like/{i['id']}", data={"like_action": type})
            if debug:
                print(updatesd)
