import asyncio
from tornado.ioloop import IOLoop

class monitor():

    def __init__(self):
        self.ioloop = IOLoop.current()

    def start(self):
        print("ioloop.time:", self.ioloop.time())
        self._startup_future = asyncio.Future()
        self.ioloop.add_callback(self._initialise)
        self.ioloop.add_timeout(self.ioloop.time() + 10, self.sanity_check)
        self.ioloop.start()
        return self._startup_future 

    async def sanity_check(self):
        print("sanity_check...", self.ioloop.time())
        self.ioloop.add_timeout(self.ioloop.time() + 10, self.sanity_check)


    async def _initialise(self):
        print("_initialise...", self.ioloop.time())
        self._startup_future.set_result(True)


async def begin():
    print("begin...")

if __name__ == '__main__':
    print("main...")
    m = monitor()
    print("monitor init...")
    m.start()
    print("start...")
    #asyncio.get_event_loop().run_until_complete(begin())
    asyncio.get_event_loop().run_forever()
