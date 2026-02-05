import asyncio
import random
from common import now_date, now_time, log_line

HOST = "127.0.0.1"
PORT = 9000
LOG_FILE = "logs/server.log"

clients = {}
client_counter = 0
response_counter = 0


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global client_counter, response_counter

    client_counter += 1
    client_id = client_counter
    clients[client_id] = writer

    addr = writer.get_extra_info("peername")
    print(f"Client {client_id} connected from {addr}")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            request_text = data.decode().strip()
            recv_time = now_time()
            date = now_date()

            # 10% chance ignore
            if random.random() < 0.1:
                log_line(
                    LOG_FILE,
                    f"{date};{recv_time};{request_text};(проигнорировано);(проигнорировано)",
                )
                continue

            await asyncio.sleep(random.uniform(0.1, 1.0))

            response_counter += 1
            answer = f"[{response_counter}/{request_text.strip('[]').split()[0]}] PONG ({client_id})"
            send_time = now_time()

            writer.write((answer + "\n").encode())
            await writer.drain()

            log_line(
                LOG_FILE,
                f"{date};{recv_time};{request_text};{send_time};{answer}",
            )

    finally:
        print(f"Client {client_id} disconnected")
        clients.pop(client_id, None)
        writer.close()
        await writer.wait_closed()


async def keepalive_sender():
    global response_counter

    while True:
        await asyncio.sleep(5)

        for writer in list(clients.values()):
            response_counter += 1
            msg = f"[{response_counter}] keepalive\n"
            writer.write(msg.encode())
            await writer.drain()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Server started on {HOST}:{PORT}")

    async with server:
        await asyncio.gather(server.serve_forever(), keepalive_sender())


if __name__ == "__main__":
    asyncio.run(main())

