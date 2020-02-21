import time

class World:
    """make a class that will represent the world.
    should have variables for: name
    tags
    export state
    created date
    last used date

    tag values should be include things like:
    local
    imported
    adventure
    creative
    pvp
    ask marcus for types of worlds he plays"""
    def __init__(self, name, created=None, modified=None):
        self.name = name
        self.dir = ''
        self.tags = []
        self.exported = False
        self.created_seconds = created
        self.modified = modified
        self.created = time.asctime(time.gmtime(created))
        self.last_used = time.asctime(time.gmtime(modified))


    def add_tags(self,tag_list):
        """takes a list of user slected tags and adds to the world"""
        for tag in tag_list:
            self.tags.append(tag)
    #
    def __lt__(self, other):
        return (self.name.lower() < other.name.lower())


