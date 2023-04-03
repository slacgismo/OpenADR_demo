import asyncio
import threading


import asyncio
import threading
import random

from aiohttp import web
import threading


async def health_handler(request):
    print("Health check")
    return web.Response(text="OK")


class HttpServer:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.add_routes([web.get('/health', health_handler)])
        self.runner = web.AppRunner(self.app)

    async def start(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

    async def stop(self):
        await self.runner.cleanup()


class SharedTime:
    __instance = None

    def __init__(self, initial_value=None):
        if SharedTime.__instance is not None:
            raise Exception(
                "Cannot create multiple instances of SharedVariable, use get_instance()")
        self._value = initial_value
        SharedTime.__instance = self

    @staticmethod
    def get_instance(initial_value=None):
        if SharedTime.__instance is None:
            SharedTime(initial_value)
        return SharedTime.__instance

    def get(self):
        return self._value

    def update(self, new_value):
        self._value = new_value


class SharedVariable:
    __instance = None

    def __init__(self, initial_value=None):
        if SharedVariable.__instance is not None:
            raise Exception(
                "Cannot create multiple instances of SharedVariable, use get_instance()")
        self._value = initial_value
        SharedVariable.__instance = self

    @staticmethod
    def get_instance(initial_value=None):
        if SharedVariable.__instance is None:
            SharedVariable(initial_value)
        return SharedVariable.__instance

    def get(self):
        return self._value

    def update(self, new_value):
        self._value = new_value


async def print_message_1(msg):
    while True:
        try:
            shared_var = SharedVariable.get_instance()
            print(msg, shared_var.get())
            shared_var.update("from message 1" +
                              str(random.randint(0, 100)))
            # SharedVariable.get_instance().value =
            await asyncio.sleep(1)
            raise Exception("test")
        except Exception as e:
            print(f"Caught exception in print_message_1: {e}")
            break


async def print_message_2(msg, delay):
    while True:
        shared_var = SharedVariable.get_instance()
        print(f"message 2 , {shared_var.get()}")
        await asyncio.sleep(delay)


# def run_asyncio_threads(funcs, args):
#     threads = []
#     num_threads = len(funcs)

#     for i in range(num_threads):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         task = loop.create_task(funcs[i](*args[i]))

#         thread = threading.Thread(target=loop.run_forever)
#         thread.start()

#         threads.append(thread)

#     for thread in threads:
#         thread.join()


# # queue = asyncio.Queue()

# funcs = [print_message_1, print_message_2]
# args = [["Message 1"], ["Message 2", 3]]

# run_asyncio_threads(funcs, args)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    loop1 = asyncio.new_event_loop()
    loop2 = asyncio.new_event_loop()
    server = HttpServer()

    t1 = threading.Thread(target=start_loop, args=(loop1,))
    t1.start()

    t2 = threading.Thread(target=start_loop, args=(loop2,))
    t2.start()

    asyncio.run_coroutine_threadsafe(print_message_1("Message 1"), loop1)
    asyncio.run_coroutine_threadsafe(print_message_2("Message 2", 2), loop2)
    asyncio.run_coroutine_threadsafe(server.start(), loop1)

    try:
        t1.join()
    finally:
        asyncio.run_coroutine_threadsafe(server.stop(), loop1)
