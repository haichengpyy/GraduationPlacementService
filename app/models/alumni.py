from sqlalchemy import Column, String, Integer, orm
from app.models.uicer import UICer


class Alumni(UICer):

    def __init__(self, StuID, Name, Password, GPA, Email, AnonymousName, enrollment, gender):
        super(Alumni, self).__init__(StuID, Name, Password, GPA, Email, enrollment, gender)
        self.state = 1
        self.AnonymousName = AnonymousName

    # set methods

    def set_anonymous_name(self, anonymous_name):
        self.AnonymousName = anonymous_name
        return

    # update information method
    def update(self, update_information):
        print("Updating information for Alumni: ", self.get_name())
        # do something to update information
        return
