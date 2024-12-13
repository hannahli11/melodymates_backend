import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# In-memory storage for users and messages
users = set()  # Store registered users dynamically as a set
messages = {}  # Store messages by chat key

class ChatHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == "/users":
            self._set_headers()
            self.wfile.write(json.dumps(list(users)).encode("utf-8"))
        elif self.path.startswith("/messages"):
            self._set_headers()
            chat_key = self.path.split("/")[-1]
            self.wfile.write(json.dumps(messages.get(chat_key, [])).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        if self.path == "/register":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = json.loads(self.rfile.read(content_length))

            username = post_data.get("username")
            if username and username not in users:
                users.add(username)
                self._set_headers()
                self.wfile.write(json.dumps({"status": "User registered", "username": username}).encode("utf-8"))
            else:
                self.send_error(400, "Invalid or duplicate username")

        elif self.path == "/send":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = json.loads(self.rfile.read(content_length))

            sender = post_data.get("sender")
            receiver = post_data.get("receiver")
            message = post_data.get("message")

            if sender and receiver and message:
                if sender not in users or receiver not in users:
                    self.send_error(400, "Sender or receiver not registered")
                    return

                chat_key = "-".join(sorted([sender, receiver]))

                # Censor bad words
                bad_words = ["fuck", "shit", "bitch", "asshole", "ass"]
                for word in bad_words:
                    message = message.replace(word, "****")

                if chat_key not in messages:
                    messages[chat_key] = []
                messages[chat_key].append(f"{sender}: {message}")

                self._set_headers()
                self.wfile.write(json.dumps({"status": "Message sent", "chatKey": chat_key}).encode("utf-8"))
            else:
                self.send_error(400, "Invalid message data")

        else:
            self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, ChatHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
