"""
https://help.monarchmoney.com/hc/en-us/articles/4409682789908-How-do-I-import-data-in-CSV-format-


TODO: Define a configuration file that lets you import ignore statements and
      categorization statements so that we don't have to hard code all of these
      values. That's if I want to upload this to github generally.
TODO: Rather then just set the category we instead want to be able to set multiple
      values like category, note, and merchant
"""
import csv
from datetime import datetime
from decimal import getcontext, Decimal
from dataclasses import dataclass, asdict

import typer


@dataclass
class BECUTransaction:
    date: datetime
    number: str
    description: str
    debit: Decimal
    credit: Decimal

@dataclass
class MonarchTransaction:
    date: datetime
    merchant: str
    category: str
    account: str
    original_statement: str
    notes: str
    amount: Decimal

DATE_INDEX: int = 0
NUMBER_INDEX: int = 1
DESCRIPTION_INDEX: int = 2
DEBIT_INDEX: int = 3
CREDIT_INDEX: int = 4

# NOTE: This is not used for categorization but instead used for statements
#       that we don't want to show up in Monarch for whatever reason.
IGNORE_STATEMENTS: tuple[str] = (
    "ENDING CASH BACK BALANCE", # No new information
    "CASH BACK EARNED THIS CYCLE", # No new information
    "CASH BACK EARNED THIS CYCLE", # No new information
    "CASH BACK REDEEMED THIS CYCLE", # No new information
    "BEGINNING CASH BACK BALANCE", # No new information
    "Interest Charge on Purchases", # Maybe should include
    "Interest Charge on Cash Advances", # Maybe should include
    "BALANCE TRANSFER FOR ACCT", # I don't know if I should include?
    "TOTAL *FINANCE CHARGE*  BILLED IN", # Maybe Should Keep, never been charged interest.
    )

CHARITY_STATEMENTS: tuple[str] = (
    "MALARIACONSORTIUM US",
    "STRONGTOWNS.ORG",
    "STRONG TOWNS MEMBER",
    "WWW.EFF.ORG",
    "PLANNED PARENTHOOD",
    "PAYPAL *OPPORTUNITY",
    "DISCOVERYOURNORTHWEST",
)

NON_REIMBURSABLE_DONATIONS: tuple[str] = (
    "Patreon",
)

RESTAURANT_STATEMENTS: tuple[str] = (
    "ROMIOSPIZZAPAST",
    "QBRC LOUNGE",
    "FUJI TERIYAKI",
    "TACOS DON RIKY",
    "SEATTLE SAMOSA LLC",
    "KATSU BURGER",
    "SALT & STRAW ICE CREA",
    "EXIT 5 KOREAN BBQ",
    "DIN TAI FUNG RESTAURANT",
    "Dough Zone -",
    "THE BIRCH DOOR CAFE",
    "NAAN N CURRY",
    "BREAKERS                 PACIFICA",
    "MIKES AT THE CROSSROADS  COTATI",
    "MOJITO",
    "IKEA SEATLE REST",
    "MASHIKO JAPANESE RESTAUR SEATTLE",
    "LARSENS BAKERY SEATTLE WA",
    "CAFE TURKO",
    "ARASHI RAMEN",
    "Five Sisters Thai Cuis",
    "FIVE SISTERS THAI",
    "ARASHI RAM",
    "TOCK ATCANLIS CANLIS",
    "UNEEDA BUR",
    "POSTMATES 32B83 KIZUKI",
    "BAMBU TACOMA",
    "BUDDHA BRUDDAH LLC",
    "FOREST FAIRY BAKERY",
    "DOOFERS BAR AND GRILL",
    "DELAURENTI FOOD AND WINE",
    "EZELLS FAMOUS CHICKEN",
    "OSCARS MEAT PIE",
    "THE STONE HOUSE CAFE",
    "UMI CAFE",
    "TOCK ATEXIT 5 KOREAN",
    "NAVY STRENGTH",
    "FERAL CARE",
    "SKY LOUNGE RESTAURANT",
    "VENMO",
    "SEA BEECHERS",
)

SHOPPING_STATEMENTS: tuple[str] = (
    "Amazon.com*",
    "AMZN Mktp US*",
    "AMZN MKTP US*"
    "AMAZON.COM",
    "AMZN MKTP US",
    "AMAZON.COM",
    "Amazon Prime",
    "BEST BUY",
    "CAITLINS CUTLERY",
    "EB WASHINGTON MIDSUMM",
    "SMITH'S WOLF DE",
)


MEDICAL_STATEMENTS: tuple[str] = (
    "UW MEDICINE",
    "POLYCLINIC",
    "CHAKABOX THERAPEUTIC",
    "RITE AID",
    "HARBORVIEW MEDICAL",
    "WALGREENS",
)

COFFEE_SHOP_STATEMENTS: tuple[str] = (
    "STARBUCKS STORE",
    "IN *THERE YA GO ESPRESSO MAPLE VALLEY",
    "THIRD CULTURE COFFEE",
    "OASIS TEA ZONE",
    "BOON BOONA COFFEE",
    "COFFEE MILL              LYNNWOOD",
    "PHILZ COFFEE",
    "BENSON ESPRESSO",
)

GROCERIES_STATEMENTS: tuple[str] = (
    "SAFEWAY",
    "FRED-MEYER",
    "HAYTON FARMS",
    "SPOONER FARMS INC",
    "KING'S MOZZARELLA",
    "BROTHERS FARMS",
    "UWAJIMAYA",
    "TRADER JOE'S ",
    "FRED MEYER",
    "COSTCO WHSE",
    "FRED-MEYER",
    "CASCADE VALLEY FARM",
    "AGUILARS FARM SUNNYSIDE WA",
    "JEWEL-OSCO",
    "OCEAN SHORES IGA",
)

PETS_STATEMENTS: tuple[str] = (
    "SIERRA FISH & PETS",
    "MUD BAY",
    "VALUE PET CLINIC KENT",
    "WELLHAVEN - RENTON WEST",
    "CHEWY.COM",
    "FERAL CARE",
)

VIDEO_GAMES_STATEMENTS: tuple[str] = (
    "STEAMGAMES.COM",
    "Steam Purchase",
)

SOFTWARE_SUBSCRIPTIONS_STATEMENTS: tuple[str] = (
    "MIDJOURNEY INC.",
)

BOOKS_STATEMENTS: tuple[str] = (
    "Audible",
    "Kindle Svcs",
    "HALF PRICE BOOKS",
)

GAS_STATEMENTS: tuple[str] = (
    "ARCO",
    "FRED M FUEL",
    "CHEVRON",
    "SHELL OIL",
    "EXXONMOBIL",
)

SEWER_STATEMENTS: tuple[str] = (
    "SOOS CREEK WATER & SEW",

)

DECORATIONS_AND_ART_STATEMENTS: tuple[str] = (
    "PFAFF'S U-CUT CHRISTMAS",
    "SP PHILIPROBERTSART",
)

PARKING_STATEMENTS: tuple[str] = (
    "THE POLYCLINIC PARKING GA SEATTLE WA",
)


CRAFTING_STATEMENTS: tuple[str] = (
    "SP * TANDY LEATHER",
    "JOANN STORES",
    "SignoftheGray",
    "Etsy.com - Multiple Shops",
    "FABRICS STORE.COM",
    "WWW.REDBUBBLE.COM",
)

ALCOHOL_STATEMENTS: tuple[str] = (
    "TOTAL WINE AND MORE",
    "BEVERAGES & MORE",
)

GYM_STATEMENTS: tuple[str] = (
    "LA FITNESS",
    "LA FIT",
)

TEA_AND_COFEE_STATEMENTS: tuple[str] = (
    "ADAGIO TEAS ELMWOOD PARK NJ",
)

CLOTHING_STATEMENTS: tuple[str] = (
    "WWW.HOTTOPIC.COM",
    "JCPENNEY.COM",
    "ARDA WIGS USA HTTPSARDAWIGS",
    "PeachtreeWeddi",
    "FlagsUK",
    "EveenStudios",
    "HistoricTrade",
    "TARGET",
    "VALUE VILLAGE",
    "KOHL'S",
    "ROSS STORES",
    "MEUNDIES INC.",
    "MARSHALLS",
)


MOVING_EXPENSES_STATEMENTS: tuple[str] = (
    "U HAUL STORE",
)

LICENSING_AND_TABS_STATEMENTS: tuple[str] = (
    "WA VEHICLE LICENSING",
)

FURNATURE_AND_HOUSEWARES_STATEMENTS: tuple[str] = (
    "IKEA",
)

MAINTENANCE_STATEMENTS: tuple[str] = (
    "YOUNKER NISSAN",
    "BROWN BEAR CAR WASH",
)

AIRPLANE_TICKETS_STATEMENTS: tuple[str] = (
    "ALASKA AIR",
)


HOTEL_TICKETS_STATEMENTS: tuple[str] = (
    "AIRBNB",
)


ENTERTAINMENT_STATEMENTS: tuple[str] = (
    "AMC ONLINE",
    "THELONGESTJOHN",
    "ANGEL DEMONIA",
    "CHAOTICA INTO THE",
    "EB CHAOTICA ALL HEAUX",
    "MOULIN ROUGE TOURI",
    "RECREATION.GOV",
    "MONTANASTATEPARKS"
    "FINE ARTS MUSEUMS",
    "MUIR WOODS"
)


NEWS_STATEMENTS: tuple[str] = (
    "WWW.VICE.COM",
)

PLANTS_STATEMENTS: tuple[str] = (
    "KENT EAST HILL NURSERY",
    "BEAMIS HIC",
)


TAXI_STATEMENTS: tuple[str] = (
    "LYFT",
)

CLEANING_SUPPLIES_STATEMENTS: tuple[str] = (
    "SP MW SOAPWORKS LLC"
)

# TODO: It's waaaay more efficient computationally to make a single set that
#       you  can do an contains check on that returns the category then to iterate
#       on a list of sets like this data structure enforces. But I'm being lazy
#       for now since I'm not sure the size of the statements is big enough to
#       matter for this script currently.
CATEGORY_TO_SEARCH_SPACES: dict[str, tuple[str]] = {
    "Charity": CHARITY_STATEMENTS,
    "Coffee Shops": COFFEE_SHOP_STATEMENTS,
    "Restaurants": RESTAURANT_STATEMENTS,
    "Groceries": GROCERIES_STATEMENTS,
    "Pets": PETS_STATEMENTS,
    "Video Games": VIDEO_GAMES_STATEMENTS,
    "Books + Audio Books": BOOKS_STATEMENTS,
    "Software Subscriptions": SOFTWARE_SUBSCRIPTIONS_STATEMENTS,
    "Medical": MEDICAL_STATEMENTS,
    "Gas": GAS_STATEMENTS,
    "Sewer": SEWER_STATEMENTS,
    "Shopping": SHOPPING_STATEMENTS,
    "Decorations And Art": DECORATIONS_AND_ART_STATEMENTS,
    "Parking": PARKING_STATEMENTS,
    "Crafting": CRAFTING_STATEMENTS,
    "Alcohol": ALCOHOL_STATEMENTS,
    "Gym": GYM_STATEMENTS,
    "Tea And Coffee": TEA_AND_COFEE_STATEMENTS,
    "Clothing": CLOTHING_STATEMENTS,
    "Moving Expenses": MOVING_EXPENSES_STATEMENTS,
    "Licensing And Tabs": LICENSING_AND_TABS_STATEMENTS,
    "Furniture & Housewares": FURNATURE_AND_HOUSEWARES_STATEMENTS,
    "Car Maintenance": MAINTENANCE_STATEMENTS,
    "Airplane Tickets": AIRPLANE_TICKETS_STATEMENTS,
    "Non-Reimbursable Donations": NON_REIMBURSABLE_DONATIONS,
    "Hotel": HOTEL_TICKETS_STATEMENTS,
    "Entertainment & Recreation": ENTERTAINMENT_STATEMENTS,
    "News Subscription": NEWS_STATEMENTS,
    "Plants": PLANTS_STATEMENTS,
    "Taxi & Ride Sharing": TAXI_STATEMENTS,
    "Cleaning Supplies": CLEANING_SUPPLIES_STATEMENTS,
}


# TODO: Lock the return str down to an enum or list of strings
def find_category(description: str) -> str:
    category: str = ""
    for potential_category, search_space in CATEGORY_TO_SEARCH_SPACES.items():
        if any(
                search_statement
                in description
                for search_statement
                in search_space):
            category = potential_category
            break
    return category


def to_decimal(value: str) -> Decimal:
    try:
        output = Decimal(value)
    except:
        output = Decimal(0.00)
    return output

def extract_transactions(becu_file: typer.FileText) -> list[BECUTransaction]:
    becu_transactions: list[BECUTransaction] = []
    csv_reader = csv.reader(becu_file)
    # Skip header
    next(csv_reader, None)
    for line in csv_reader:
        # The replace is here for values like '1,319.03' where we have left
        # real people money and enter the lands of wild commas.
        credit = to_decimal(line[CREDIT_INDEX].replace(",", ""))
        debit = to_decimal(line[DEBIT_INDEX].replace(",", ""))
        description = line[DESCRIPTION_INDEX]

        if any(
                to_ignore
                in description
                for to_ignore
                in IGNORE_STATEMENTS):
            continue

        if credit == Decimal(0.00) and debit == Decimal(0.00):
            raise ValueError(f"Must have a credit or a debit statement: {line}")

        becu_transactions.append(BECUTransaction(
            datetime.strptime(line[DATE_INDEX], "%m/%d/%Y"),
            line[NUMBER_INDEX],
            description,
            debit,
            credit))
    return becu_transactions

def transform_to_monarch_format(
        becu_transactions: list[BECUTransaction],
        account_name: str)  -> list[MonarchTransaction]:
    """

    https://help.monarchmoney.com/hc/en-us/articles/4409682789908-How-do-I-import-data-in-CSV-format-

    The specific verbiage on the monarch page is:

    > ** Monarch uses positive numbers for income and negative numbers for expenses. So
    +$100 would be seen as income and -$100 would be seen as an expense. Some apps and
    banks export expenses as positive numbers which means they will show up incorrectly
    if imported directly into Monarch. You may need to play around with your CSV file to
    convert positive to negative numbers in this case.

    BECU puts credits as a negative and debits as a positive so we need to flip
    these.
    """
    monarch_transactions: list[MonarchTransaction] = []
    for becu_transaction in becu_transactions:

        description = becu_transaction.description
        category = find_category(becu_transaction.description)
        merchant = becu_transaction.description
        if "CASH BACK REDEMPTION" in becu_transaction.description:
            description = "Cash Back Redemption"
            transaction_amount = -becu_transaction.credit
            merchant = "BECU Credit Card"
            category = "Cash Back"
        elif becu_transaction.debit != Decimal(0.00):
            transaction_amount = -(becu_transaction.debit)
        elif becu_transaction.description == "PAYMENT - THANK YOU":
            transaction_amount = -(becu_transaction.credit)
            merchant = "BECU Credit Card"
            category = "Credit Card Payment"
        elif ("AMZN Mktp" in becu_transaction.description
                and becu_transaction.credit != Decimal(0.00)):
            transaction_amount = -(becu_transaction.credit)
            category = "returns"
            merchant = "Amazon"
        elif becu_transaction.credit != Decimal(0.00):
            transaction_amount = -(becu_transaction.credit)
        else:
            raise ValueError(f"{becu_transaction} is an unknown statement")

        # TODO: Make a general function that applies statements to known patterns

        monarch_transaction: MonarchTransaction = MonarchTransaction(
            date=becu_transaction.date,
            merchant=description,
            category=category,
            account=account_name,
            original_statement=description,
            notes="",
            amount=transaction_amount
            )
        monarch_transactions.append(monarch_transaction)

    return monarch_transactions



def export_to_csv(
        transactions: list[MonarchTransaction],
        output_file_name: str) -> None:
    """

    NOTE: Monarch ignores the first row in the CSV so it's expecting a headers
          row is my assumption.
    """
    transaction_writer = csv.writer(output_file_name)
    header_row = [
        "date",
        "merchant",
        "category",
        "account",
        "origin_statement",
        "notes",
        "amount"]
    transaction_writer.writerow(header_row)
    for transaction in transactions:
        values_list = list(asdict(transaction).values())
        values_list[-1] = str(values_list[-1])
        transaction_writer.writerow(values_list)


def main(
        transaction_file_name: typer.FileText = typer.Option(...),
        account_name: str = typer.Option(...),
        output_file: typer.FileTextWrite = typer.Option(default="monarch_transactions.csv")
):
    transactions = extract_transactions(transaction_file_name)
    formatted_transactions = transform_to_monarch_format(
        transactions,
        account_name)
    export_to_csv(formatted_transactions, output_file)

if __name__ == "__main__":
    typer.run(main)
