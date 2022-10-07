import uvicorn, os
from fastapi import FastAPI, HTTPException
from typing import List
from Models.schema import *
from Models.db import DB
from Models.repository import Repository
from Models.models import *
from fastapi_responses import custom_openapi
import csv


user = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASS", "root")
host = os.environ.get("DB_HOST", "host.docker.internal")
database = "roomr"

db = DB(user, password, host, database)
repository = Repository(db)

app = FastAPI()
#Converts HTTP Exception in swagger documentation
app.openapi = custom_openapi(app)

@app.on_event("startup")
async def startup_event():
    try:
        await repository.create_all()
    except OperationalError:
        SystemExit()
   

@app.get("/Health")
async def health_check():
    return {"status": 200}


@app.post("/House/{houseId}/Lease")
async def create_lease(houseId: int, leaseSchema: LeaseSchema):
    lease = Lease(houseId=houseId, **leaseSchema.dict())
    monad = await repository.insert_lease(lease)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return lease.to_json()

@app.get("/Lease")
async def get_lease(houses: str):
    try:
        houseIds = [int(houseId) for houseId in houses.split(",")]
    except ValueError:
        return HTTPException(400, detail=f"Invalid query parameter. Must be in format 1,2 not {houses}")
    print(houseIds)
    houseId = 71
    leases = await repository.get_lease(houseIds)
   
    return [lease.to_json() for lease in leases]


@app.put("/Lease/{leaseId}/LandlordInfo")
async def update_landlord_info(leaseId: int, landlordInfo: LandlordInfoSchema):
    landlordInfo = LandlordInfo(**landlordInfo.dict())
    monad = await repository.update_landlord_info(landlordInfo, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return landlordInfo.to_json()
        

@app.put("/Lease/{leaseId}/LandlordAddress")
async def update_landlord_address(leaseId: int, landlordAddressSchema: LandlordAddressSchema):
    landlordAddress = LandlordAddress(**landlordAddressSchema.dict())
    landlordAddress.lease_id = leaseId
    monad = await repository.update_landlord_address(landlordAddress, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return landlordAddress.to_json()
    
@app.put("/Lease/{leaseId}/RentalAddress")
async def update_rental_address(leaseId: int, rentalAddressSchema: RentalAddressSchema):
    rentalAddress = RentalAddress(**rentalAddressSchema.dict())
    monad = await repository.update_rental_address(rentalAddress, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return rentalAddress.to_json()
    
@app.put("/Lease/{leaseId}/Rent")
async def update_rent(leaseId: int, RentSchema: RentSchema):
    rent = Rent(**RentSchema.dict())
    monad = await repository.update_rent(rent, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return rent.to_json()

@app.put("/Lease/{leaseId}/TenancyTerms")
async def update_tenancy_terms(leaseId: int, tenancyTermsSchema: TenancyTermsSchema):
    tenancyTerms = TenancyTerms(**tenancyTermsSchema.dict())
    monad = await repository.update_tenancy_terms(tenancyTerms, leaseId)    
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return tenancyTerms.to_json()


@app.put("/Lease/{leaseId}/Services")
async def update_services(leaseId: int, serviceSchema: List[ServiceSchema]):

    services = [Service(**schema.dict()) for schema in serviceSchema]
    print([service.to_json() for service in services])
    monad = await repository.update_services(services, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [service.to_json() for service in services]
    


@app.put("/Lease/{leaseId}/Utilities")
async def update_utilities(leaseId: int, utilitesSchema: List[UtilitySchema]):
    utilities = [Utility(**schema.dict()) for schema in utilitesSchema]
    monad = await repository.update_utilities(utilities, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [utility.to_json() for utility in utilities]


@app.put("/Lease/{leaseId}/RentDiscounts")
async def update_rent_discounts(leaseId: int, rentDiscoutSchema: List[RentDiscoutSchema]):
    rentDiscounts = [RentDiscount(**schema.dict()) for schema in rentDiscoutSchema]
    monad = await repository.update_rent_discounts(rentDiscounts, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [rentDiscount.to_json() for rentDiscount in rentDiscounts]

@app.put("/Lease/{leaseId}/RentDeposits")
async def update_rent_discounts(leaseId: int, rentDepositSchema: List[RentDepositSchema]):
    rentDeposits = [RentDeposit(**schema.dict()) for schema in rentDepositSchema]
    monad = await repository.update_rent_deposits(rentDeposits, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [rentDeposit.to_json() for rentDeposit in rentDeposits]

@app.put("/Lease/{leaseId}/AdditionalTerms")
async def update_additional_terms(leaseId: int, additionalTermSchema: List[AdditionalTermSchema]):
    additionalTerms = [AdditionalTerm(**schema.dict()) for schema in additionalTermSchema]
    monad = await repository.update_additional_terms(additionalTerms, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [additionalTerm.to_json() for additionalTerm in additionalTerms]
   
@app.put("/Lease/{leaseId}/TenantNames")
async def update_tenant_names(leaseId: int, tenantNamesSchema: List[TenantNameSchema]):
    tenantNames = [TenantName(**schema.dict()) for schema in tenantNamesSchema]
    monad = await repository.update_tenant_names(tenantNames, leaseId)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [tenantName.to_json() for tenantName in tenantNames]
   


if __name__ == "__main__":
    uvicorn.run(app)#, host="0.0.0.0", port=8000)