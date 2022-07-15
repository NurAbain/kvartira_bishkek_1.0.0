import parser_kvartiry
import  skaner_adds_lalafo
import parser_hash_images
import bot_images_find
from threading import Thread

if __name__ == "__main__":
    Thread(target=parser_kvartiry.Starter_check_lalafo_kg, args=()).start()
    Thread(target=skaner_adds_lalafo.Starter_skaner_kvartir_lalafo, args=()).start()
    Thread(target=parser_hash_images.Starter_parser_lalafo, args=()).start()
    Thread(target=bot_images_find.Starter_botmen, args=()).start()







