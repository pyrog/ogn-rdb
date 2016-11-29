#!/usr/bin/env python3

import json
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from argparse import ArgumentParser

from wikidotparser import parse_receiver_list
from wikidotcrawler import fetch_page

wiki_url = 'http://wiki.glidernet.org/ajax-module-connector.php'
receiver_list_page_ids = {'others': 22120125,
                          'france': 45174721,
                          'germany': 45177548,
                          'uk': 45177553,
                          'us': 45426379}

RECEIVERLIST_VERSION = '0.2.1'


if __name__ == "__main__":
    PARSER = ArgumentParser(description="""Fetch list-of-receivers from wiki.glidernet.org
                                           and output it into a (machine-readable) file.""")

    PARSER.add_argument("--out",
                        metavar="OUT_FILE", dest="out_file",
                        default="receivers.json",
                        help="Output file. Default:"
                             "receivers.json")
    PARSER.add_argument("--obfuscate",
                        dest="obfuscate",
                        default=False,
                        action="store_true",
                        help="Obfuscate email addresses (truncate addresses after '@').")
    PARSER.add_argument("--cache",
                        dest="cache",
                        default=False,
                        action="store_true",
                        help="Cache locally and resize images.")
    ARGS = PARSER.parse_args()

    print("Fetch and parse lists of receivers")
    receivers = []

    for country, page_id in receiver_list_page_ids.items():
        page = fetch_page(wiki_url, page_id)
        _receivers = parse_receiver_list(page)

        if country != 'others':
            for receiver in _receivers:
                receiver.update({'country': country})

        receivers += _receivers

    timestamp = datetime.utcnow().replace(microsecond=0)

    receiverdb = {'version': RECEIVERLIST_VERSION,
                  'receivers': receivers,
                  'timestamp': timestamp.isoformat()}

    if ARGS.cache:
        print("Cache photos")
        for receiver in receivers:
            i = 1
            for photo in receiver['photos']:
                try:
                    fn = "photos/"+receiver.get('callsign')+"-"+str(i)
                    print(fn+" "+photo)
                    req = requests.get(photo)
                    im = Image.open(BytesIO(req.content))
                    
                    im.resize((1024,1024), Image.HAMMING)
                    im.save(fn+".jpg", "JPEG")
                    
                    im.thumbnail((100,100))
                    im.save(fn+"-100.jpg", "JPEG")
                    
                    # Update URL in JSON datas
                    #receiver.get('photos')[i-1].update({'url': fn+".jpg"})
                    receiver.get('photos')[i-1] = fn+".jpg"

                except Exception as e:
                    print(e)
				    
                i = i+1

    if ARGS.obfuscate:
        print("Obfuscate email addresses")
        for receiver in receiverdb['receivers']:
            receiver.update({'email': ''})

    print("Save to {}".format(ARGS.out_file))
    with open(ARGS.out_file, 'w', encoding='utf-8') as f:
        json.dump(receiverdb, f, ensure_ascii=False)
