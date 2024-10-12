import random
from bot.utils import night_sleep, Colors, load_data_from_json, select_random_pixel
import asyncio
import config
import os

async def painters(NotPxClient):
    print("[+] {}Auto painting started{}.".format(Colors.CYAN, Colors.END))
    while True:
        try:
            await night_sleep()  # Assuming night_sleep is a blocking function; handle this accordingly
            user_status = NotPxClient.accountStatus()
            if not user_status:
                await asyncio.sleep(5)
                continue

            charges = user_status['charges']
            balance = user_status['userBalance']
            levels_recharge = user_status['boosts']['reChargeSpeed'] + 1
            
            if charges > 0:
                if config.X3_PIXEl:
                    data = load_data_from_json(os.path.dirname(os.path.abspath(__file__)) + '/data/data.json')
                    for _ in range(charges):
                        color, pixelid = select_random_pixel(data)
                        pixelstatus = NotPxClient.pixelStatus(pixelid)
                        pixelcolor = pixelstatus['pixel']['color']
                        
                        if pixelcolor != color:
                            balance = NotPxClient.paintPixel(pixelid, color)
                            print("[+] {}Pixel painted{} successfully. User new balance: {}{}{}".format(
                                Colors.GREEN, Colors.END,
                                Colors.GREEN, balance, Colors.END
                            ))
                        else:
                            print("[+] {}Pixel already correct{}. Trying new pixel! User balance: {}{}{}".format(
                                Colors.RED, Colors.END,
                                Colors.GREEN, balance, Colors.END
                            ))
                        t = random.randint(1, 10)
                        print("[!] Anti-detect: Sleeping for {} seconds...".format(t))
                        await asyncio.sleep(t)
                else:
                    for _ in range(charges):
                        balance = NotPxClient.autoPaintPixel()
                        print("[+] Pixel painted successfully. User new balance: {}{}{}".format(
                            Colors.GREEN, balance, Colors.END
                        ))
                        t = random.randint(1, 10)
                        print("[!] Anti-detect: Sleeping for {} seconds...".format(t))
                        await asyncio.sleep(t)
            else:
                recharge_speed = user_status['reChargeSpeed'] / 1000
                random_recharge_speed = random.randint(10, 60)
                print("[!] No charge available. Sleeping for {} minutes...".format(
                    round(((recharge_speed + random_recharge_speed) / 60), 2)
                ))
                await asyncio.sleep(recharge_speed + random_recharge_speed)
        except Exception as e:
            print(f"[!] {Colors.RED}Error{Colors.END}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

