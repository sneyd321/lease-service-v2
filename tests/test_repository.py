from models.db import DB
from models.repository import Repository
from models.models import Lease, LandlordAddress
from models.Firebase import Firebase
import asyncio, pytest, json, os

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()
host = os.environ.get("DB_HOST", "localhost")



async def test_Lease_Service_returns_error_when_data_does_not_exist():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/landlord_address_test.json", mode="r") as landlord_address_test:
        landlordAddressData = json.load(landlord_address_test)
    landlordAddress = LandlordAddress(**landlordAddressData)
    landlordAddress.lease_id = 0
    monad = await repository.update_landlord_address(landlordAddress)
    assert monad.error_status == {"status": 404, "reason": "No data in repository monad"}


async def test_Lease_Service_returns_error_when_duplicate_house_id_is_entered():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/lease_test.json", mode="r") as lease_test:
        leaseData = json.load(lease_test)
    lease = Lease(houseId=4, firebase=firebase, **leaseData)
    
    monad = await repository.insert(lease)
    monad = await repository.insert(lease)
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database"}