import asyncio
import random
from common import now_date, now_time, log_line

HOST = "127.0.0.1"
PORT = 9000


class Client:
    def __init__(self, client_id: int):
        self.client_id = client_id
        self.log_file = f"logs/client{client_id}.log"
        self.request_counter = 0

    async def run(self):
        reader, writer = await asyncio.open_connection(HOST, PORT)

        send_task = asyncio.create_task(self.send_loop(writer))
        recv_task = asyncio.create_task(self.receive_loop(reader))

        await asyncio.gather(send_task, recv_task)

    async def send_loop(self, writer):
        while True:
            await asyncio.sleep(random.uniform(0.3, 3.0))

            text = f"[{self.request_counter}] PING"
            send_time = now_time()
            date = now_date()

            writer.write((text + "\n").encode())
            await writer.drain()

            log_line(
                self.log_file,
                f"{date};{send_time};{text};;",
            )

            self.request_counter += 1

    async def receive_loop(self, reader):
        while True:
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=2)
            except asyncio.TimeoutError:
                date = now_date()
                time = now_time()
                log_line(self.log_file, f"{date};;;{time};(таймаут)")
                continue

            if not data:
                break

            message = data.decode().strip()
            date = now_date()
            time = now_time()

            if "keepalive" in message:
                log_line(self.log_file, f"{date};;;;{message}")
            else:
                log_line(self.log_file, f"{date};;;{time};{message}")


async def main(client_id):
    client = Client(client_id)
    await client.run()


if __name__ == "__main__":
    import sys

    cid = int(sys.argv[1])
    asyncio.run(main(cid))

