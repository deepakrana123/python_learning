class Subscriber:
    def update(self,video_title):
        pass

class User(Subscriber):
    def __init__(self,name):
        self.name=name
    def video_title(self,video_title):
        print(f"{video_title} is not going {self.name}")


class YouTubeChannel:
    def __init__(self,channel_name):
        self.channel_name = channel_name
        self.subscribers = []
    
    def subscribe(self,user):
        self.subscribers.append(user)
    
    def unsubscribe(self,user):
        self.subscribers.remove(user)
    
    def upload_video(self, video_title):
        print(f"📢 {self.channel_name} uploaded: {video_title}")
        self.notify_subscribers(video_title)

    def notify_subscribers(self, video_title):
        for subscriber in self.subscribers:
            subscriber.update(video_title)

channel = YouTubeChannel("Tech World")
user1 = User("Alice")
user2 = User("Bob")

channel.subscribe(user1)
channel.subscribe(user2)

channel.upload_video("Observer Pattern Explained!") 

channel.unsubscribe(user2)
channel.upload_video('New video')