from Rewards.models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile

def addWords():
    f = open("Rewards/animals.txt", "r")
    for row in f:
        word = row.strip().lower()
        try:
            a = AccountCodeBuilder(word=word)
            a.save()
        except:
            print(f"Duplicate: {word}")
        else:
            print(f"Added: {word}")

def run():
    addWords()