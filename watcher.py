import asyncio
import os
import logging
import argparse
from bleak import BleakClient
from watchgod.main import awatch
from watchgod.watcher import Change
import base64


UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UUID_NORDIC_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


async def main(address, files, verbose, buffer_size, exec):
    logger = logging.root
    logger.info(f"Connecting to {address}...")

    def uart_data_received(sender, data):
        if verbose:
            content = data.decode()
            if not content.strip() or content == '\n':
                return

        if verbose == 1:
            logger.info(content)
        elif verbose == 2:
            logger.debug(content)

    async def send_command(command):
        c = command
        while len(c) > 0:
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(c[0:buffer_size]), True)
            c = c[buffer_size:]

    async def send_file(file):

        logger.info(f"Sending {file}...")
        with open(file, "rb") as f:
            content = f.read()
            atob = base64.b64encode(content)
            command = f'require("Storage").write("{file}",atob("{str(atob, "utf-8")}"));\n'
            await send_command(command.encode("utf-8"))

        await send_command(b'\n')
        logger.info(f"{file} sent!")

    async def send_load(exec):
        logger.info(f"Executing {exec}...")
        await send_command(f"load('{exec}');\n".encode("utf-8"))

    async with BleakClient(address) as client:
        logger.info("Connected")
        logger.info("Resetting")
        await send_command(b"reset();\n")
        logger.info("Disabling echo")
        await send_command(b"echo(0);\n")
        await asyncio.sleep(1)
        await client.start_notify(UUID_NORDIC_RX, uart_data_received)

        for file in files:
            await send_file(file)

        if exec:
            await send_load(exec)

        async for changes in awatch('.'):
            any_upload = False
            for (type, file_changed) in changes:
                if (type != Change.deleted):
                    for file in files:
                        if os.path.samefile(file_changed, file):
                            any_upload = True
                            await send_file(file)
            if exec and any_upload:
                await send_load(exec)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Bangle Watcher')

    parser.add_argument('address', help='bluetooth address to connect')
    parser.add_argument('files', metavar='file',
                        nargs='+', help='files to watch')
    parser.add_argument('--buffer_size', type=int,
                        help='buffer size (default 20)', default=20)
    parser.add_argument(
        '--exec', help='script to run (load) after each upload')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help="verbosity: -v show response from bangle, -vv show all DEBUG logs")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose == 2 else logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        asyncio.run(main(args.address, args.files, verbose=args.verbose,
                         buffer_size=args.buffer_size, exec=args.exec))
    except KeyboardInterrupt:
        logging.root.info("Interrupted. Ending watcher")
