from models.db import DB
from models.repository import Repository
from models.models import Lease, LandlordAddress
from models.Firebase import Firebase
import asyncio, pytest, json

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

user = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASS", "root")
host = os.environ.get("DB_HOST", "host.docker.internal")
db = DB(user, password, host, database)
repository = Repository(db)

@pytest.mark.asyncio
async def test_Lease_Service_returns_error_when_data_does_not_exist():
    with open(r"./tests/landlord_address_test.json", mode="r") as landlord_address_test:
        landlordAddressData = json.load(landlord_address_test)
    landlordAddress = LandlordAddress(**landlordAddressData)
    landlordAddress.lease_id = 0
    monad = await repository.update_landlord_address(landlordAddress)
    assert monad.error_status == {"status": 404, "reason": "No data in repository monad"}

@pytest.mark.asyncio
async def test_Lease_Service_returns_empty_list_when_retieving_multiple_lease_by_house_id():
    monad = await repository.get_lease(["0"])
    assert monad.get_param_at(0) == []