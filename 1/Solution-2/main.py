import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

basepasswd = "stefano"
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]

cyphertext = b'gAAAAABgoqMJ17XcgGFW347sJ9q1cXjzd1Cl74v42sZVhmbGGer1_l1NFfZSM-FRCVpCaZ9' \
            b'-JYjy5Ut0Ycy4E1GHyUxCSEgROSw2HFsJjX43qZgk2AyMG1Vzfxx8V212x3WWwszfCV1rR2KWHvUyorQB' \
            b'-0asgI3NLcrZiLVjJSQHg2qOqqKNUyv-TQsR-EIo-GgI4FOnA1kyFymTQv2Vcjxq4zAtUO3' \
            b'-nssuxuVC_n27xefX4eRd_GrnonCvRL_0b_3KYt-pQp4iT_hcbvuEnuM--Ue-F_BjYg=='

salt = b'\xd4\x1f\xceg\xe9\xafW\xad\xb7+Y\xc3\xd9t\xe1\xc6'

i = 0
j = 0
k = 0
p = 0
while i < 8:
    while j < 8:
        while k < 10:
            while p < 26:
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                passwd = basepasswd[:i] + str(k) + basepasswd[i:]
                passwd_str = passwd[:j] + alphabet[p] + passwd[j:]
                passwd = bytes(passwd_str, 'utf-8')
                print('password = ', passwd)
                try:
                    key = base64.urlsafe_b64encode(kdf.derive(passwd))
                    print("key = ", key)
                    f = Fernet(key)
                    print('cleartext = ', f.decrypt(cyphertext))
                except Exception:
                    print("nope")
                    pass
                p = p + 1
            k = k + 1
            p = 0
        j = j + 1
        k = 0
    i = i + 1
    j = 0
