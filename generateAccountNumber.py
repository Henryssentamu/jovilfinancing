import secrets
import hashlib

class GenerateAccountNumber:
    def __init__(self, existingAccounts) -> None:
        self.existingAccounts = existingAccounts
    def generateNumber(self):
        number  = secrets.randbelow(10**3)
        account_number = str(number).zfill(3)
        checksum = hashlib.sha256(account_number.encode()).hexdigest()[:2]
        full_account_number = f"{account_number}{checksum}"
        if full_account_number not in self.existingAccounts:
            return full_account_number
        else:
            return self.generateNumber()



