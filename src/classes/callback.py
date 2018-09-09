import asyncio
import functools
from .dummy_logger import DummyLogger

class Callback(object):

    callbackList    = []
    name            = ""
    objectType      = None
    eventLoop       = None
    logger          = None

    def __init__(self, name="", objectType=None, logger=None):
        self.callbackList   = []
        self.name           = name
        self.objectType     = objectType
        self.eventLoop      = asyncio.get_event_loop()
        self.logger         = logger if logger != None else DummyLogger()

    def addCallback(self, *anotherCallbacks):
        for anotherCallback in anotherCallbacks:
            if not isinstance(anotherCallback, Callback):
                raise Exception("Callback: %s is not inherited from Callback Class" % anotherCallback)
            # if not callable(anotherCallback):
            #     raise Exception("Provided callback = %s is not a function!")
            self.callbackList += [ anotherCallback ]

    async def callback(self, obj):
        self.logger.debug("calling callback for object %s" % self.name)

        self.checkCallback(obj)
        obj = await self.processCallback(obj)
        await self.sendCallback(obj)

    async def sendCallback(self, obj):
        tasks = [ asyncio.ensure_future(cb.callback(obj)) for cb in self.callbackList ]
        # tasks = [
        #     self.eventLoop.run_in_executor(None, functools.partial(
        #         cb.callback, obj
        #     )) for cb in self.callbackList
        # ]
        if len(tasks) != 0:
            await asyncio.wait(tasks)

    def checkCallback(self, obj):
        if type(obj) != self.objectType and not self.objectType == None:
            raise Exception("[%s] check failed for object %s! Expected %s" % ( self.name, obj, self.objectType ))

    async def processCallback(self, obj):
        raise NotImplementedError("Not Implemented, LOL! Please kill me!")
