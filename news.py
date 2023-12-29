class News:
    def __init__(self, title="", date="", description="", resource=""):
        self.title = title
        self.date = date
        self.description = description
        self.resource = resource

    def __str__(self):
        return f"Source: {self.resource}\tDate: {self.date}\nTitle: {self.title}\nDescription: {self.description}"
    