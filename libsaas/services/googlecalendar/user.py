from libsaas.services import base

from .resource import ReadonlyResource
from .calendar import CalendarLists, CalendarList


class SettingResource(ReadonlyResource):
    path = 'settings'


class User(ReadonlyResource):
    path = 'users/me'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(SettingResource)
    def settings(self):
        """
        Return the resource corresponding to all the settings
        """
        return SettingResource(self)

    @base.resource(SettingResource)
    def setting(self, setting):
        """
        Return the resource corresponding to a single setting
        """
        return SettingResource(self, setting)

    @base.resource(CalendarLists)
    def calendar_lists(self):
        """
        Return the resource corresponding to all the calendar lists
        """
        return CalendarLists(self)

    @base.resource(CalendarList)
    def calendar_list(self, calendar_id):
        """
        Return the resource corresponding to a single calendar list
        """
        return CalendarList(self, calendar_id)
