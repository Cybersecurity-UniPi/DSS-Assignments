import logging
import base64
import threading
from cryptography.fernet import Fernet, InvalidToken
from string import ascii_uppercase
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

cyphertext = b'gAAAAABgoqMJ17XcgGFW347sJ9q1cXjzd1Cl74v42sZVhmbGGer1_l1NFfZSM-FRCVpCaZ9' \
             b'-JYjy5Ut0Ycy4E1GHyUxCSEgROSw2HFsJjX43qZgk2AyMG1Vzfxx8V212x3WWwszfCV1rR2KWHvUyorQB' \
             b'-0asgI3NLcrZiLVjJSQHg2qOqqKNUyv-TQsR-EIo-GgI4FOnA1kyFymTQv2Vcjxq4zAtUO3' \
             b'-nssuxuVC_n27xefX4eRd_GrnonCvRL_0b_3KYt-pQp4iT_hcbvuEnuM--Ue-F_BjYg=='

salt = b'\xd4\x1f\xceg\xe9\xafW\xad\xb7+Y\xc3\xd9t\xe1\xc6'
keyword = "stefano"


def search_with_letter(letter: str):
    for num in numbers:
        for i in range(0, len(keyword)):
            for j in range(0, len(keyword)):
                passwd = keyword[:i] + str(num) + keyword[i:]
                passwd_str = passwd[:j] + letter + passwd[j:]
                passwd = bytes(passwd_str, 'utf-8')

                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                try:
                    key = base64.urlsafe_b64encode(kdf.derive(passwd))
                    f = Fernet(key)
                    logging.info(f.decrypt(cyphertext))
                    logging.info(passwd)
                    print("Done")
                    quit()
                except InvalidToken as e:
                    pass


if __name__ == '__main__.py':
    logging.basicConfig(filename="/home/jackson/Desktop/prova_cybersec.txt",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    letters = ascii_uppercase
    numbers = range(0, 9)
    logging.info("============BEG============")
    threads = []
    try:
        for c in letters:
            logging.info(str.format("Started with letter {0}", c))
            x = threading.Thread(daemon=True, target=search_with_letter, args=c)
            threads.append(x)
            x.start()

        for x in threads:
            x.join()
    except ConnectionRefusedError as e:
        # Non throwable exception, didn't want to create my own
        quit()
    finally:
        logging.info("============END============")
