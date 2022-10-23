from models.db import DB
from models.repository import Repository
from models.models import Lease
from models.Firebase import Firebase
import asyncio, pytest, json

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

@pytest.mark.asyncio
async def test_Lease_Service_returns_error_during_database_outage():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open(r"./tests/lease_test.json", mode="r") as lease_test:
        leaseData = json.load(lease_test)
    monad = await repository.insert(Lease(1, firebase, **leaseData))
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to database"}


