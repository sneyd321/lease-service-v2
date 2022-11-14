import uvicorn, os
from fastapi import FastAPI, HTTPException
from typing import List
from models.schema import *
from models.db import DB
from models.repository import Repository
from models.models import *
from models.Firebase import Firebase


user = os.environ.get("DB_USER", "test")
password = os.environ.get("DB_PASS", "homeowner")
host = os.environ.get("DB_HOST", "host.docker.internal")
database = "roomr"

db = DB(user, password, host, database)
repository = Repository(db)

app = FastAPI()

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()


@app.get("/Health")
async def health_check():
    return {"status": 200}


@app.post("/Lease")
async def create_lease(leaseSchema: LeaseSchema):
    lease = Lease(**leaseSchema.dict())
    lease.initialize_document(firebase, lease.houseId)
    monad = await repository.insert(lease)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return lease.to_json()

@app.get("/Lease/{houseId}")
async def get_lease(houseId: int):
    monad = await repository.get_lease(houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()


@app.put("/Lease/{houseId}/LandlordInfo")
async def update_landlord_info(houseId: int, landlordInfo: LandlordInfoSchema):
    landlordInfo = LandlordInfo(**landlordInfo.dict())
    monad = await repository.update_landlord_info(landlordInfo, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()
        

@app.put("/Lease/{houseId}/LandlordAddress")
async def update_landlord_address(houseId: int, landlordAddressSchema: LandlordAddressSchema):
    landlordAddress = LandlordAddress(**landlordAddressSchema.dict())
    monad = await repository.update_landlord_address(landlordAddress, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()
    
@app.put("/Lease/{houseId}/RentalAddress")
async def update_rental_address(houseId: int, rentalAddressSchema: RentalAddressSchema):
    rentalAddress = RentalAddress(**rentalAddressSchema.dict())
    monad = await repository.update_rental_address(rentalAddress, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()
    
@app.put("/Lease/{houseId}/Rent")
async def update_rent(houseId: int, RentSchema: RentSchema):
    rent = Rent(**RentSchema.dict())
    monad = await repository.update_rent(rent, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()

@app.put("/Lease/{houseId}/TenancyTerms")
async def update_tenancy_terms(houseId: int, tenancyTermsSchema: TenancyTermsSchema):
    tenancyTerms = TenancyTerms(**tenancyTermsSchema.dict())
    monad = await repository.update_tenancy_terms(tenancyTerms, houseId)    
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()


@app.put("/Lease/{houseId}/Services")
async def update_services(houseId: int, serviceSchema: List[ServiceSchema]):
    services = [Service(**schema.dict()) for schema in serviceSchema]
    monad = await repository.update_services(services, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [service.to_json() for service in services]
    
@app.put("/Lease/{houseId}/Utilities")
async def update_utilities(houseId: int, utilitesSchema: List[UtilitySchema]):
    utilities = [Utility(**schema.dict()) for schema in utilitesSchema]
    monad = await repository.update_utilities(utilities, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [utility.to_json() for utility in utilities]


@app.put("/Lease/{houseId}/RentDiscounts")
async def update_rent_discounts(houseId: int, rentDiscoutSchema: List[RentDiscoutSchema]):
    rentDiscounts = [RentDiscount(**schema.dict()) for schema in rentDiscoutSchema]
    monad = await repository.update_rent_discounts(rentDiscounts, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [rentDiscount.to_json() for rentDiscount in rentDiscounts]

@app.put("/Lease/{houseId}/RentDeposits")
async def update_rent_discounts(houseId: int, rentDepositSchema: List[RentDepositSchema]):
    rentDeposits = [RentDeposit(**schema.dict()) for schema in rentDepositSchema]
    monad = await repository.update_rent_deposits(rentDeposits, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [rentDeposit.to_json() for rentDeposit in rentDeposits]

@app.put("/Lease/{houseId}/AdditionalTerms")
async def update_additional_terms(houseId: int, additionalTermSchema: List[AdditionalTermSchema]):
    additionalTerms = [AdditionalTerm(**schema.dict()) for schema in additionalTermSchema]
    monad = await repository.update_additional_terms(additionalTerms, houseId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [additionalTerm.to_json() for additionalTerm in additionalTerms]
   
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)