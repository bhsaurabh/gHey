from event import Event
__author__ = 'Saurabh Bhatia'

class MessageEvent(Event):
    """
    When subclassing Event class the only thing you must do is to define
    a list of class level constants which defines the event types and the
    string associated to them
    """
    messageTyped = "messageTyped"