# if one fails donot worry go with other , used to call api mostly


class SupportHandler:
    def __init__(self,next_handler):
        self.next_handler=next_handler
    
    def next_request(self,issue_severity):
        if self.next_handler:
            return self.next_handler.next_request(issue_severity)
        return "No request to handle"

class Assistant(SupportHandler):
    def next_request(self,issue_serverity):
        if issue_serverity <= 2:
            return "Assistant: Issue resolved."
        return super().next_request(issue_serverity)


class Manager(SupportHandler):
    def next_request(self, issue_severity):
        if issue_severity <= 5:
            return "Manager: Issue resolved."
        return super().next_request(issue_severity)


class Director(SupportHandler):
    def next_request(self, issue_severity):
        return 'Issue cannot be resolved'

a=Assistant(Manager(Director()))
print(a.next_request(1))
print(a.next_request(3))
print(a.next_request(6))


