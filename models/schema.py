from typing import Set, Union, List
from pydantic import BaseModel


class EmailSchema(BaseModel):
    email: str

class ContactInfoSchema(BaseModel):
    contact: str

class LandlordInfoSchema(BaseModel):
    fullName: str
    receiveDocumentsByEmail: bool
    emails: Union[List[EmailSchema], None]
    contactInfo: bool
    contacts: Union[List[ContactInfoSchema], None]



class ParkingDescriptionSchema(BaseModel):
    description: str


class RentalAddressSchema(BaseModel):
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitName: str
    isCondo: bool
    parkingDescriptions: List[ParkingDescriptionSchema]



class RentServiceSchema(BaseModel):
    name: str
    amount: str

class PaymentOptionSchema(BaseModel):
    name: str

class RentSchema(BaseModel):
    baseRent: str
    rentMadePayableTo: str
    rentServices: Union[List[RentServiceSchema], None]
    paymentOptions: Union[List[PaymentOptionSchema], None]



class RentalPeriodSchema(BaseModel):
    rentalPeriod: str
    endDate: str

class PartialPeriodSchema(BaseModel):
    amount: str
    dueDate: str
    startDate: str
    endDate: str
    isEnabled: bool

class TenancyTermsSchema(BaseModel):
    rentalPeriod: Union[RentalPeriodSchema, None] = None
    startDate: str
    rentDueDate: str
    paymentPeriod: str
    partialPeriod: Union[PartialPeriodSchema, None] = None


class DetailSchema(BaseModel):
    detail: str

class ServiceSchema(BaseModel):
    name: str
    isIncludedInRent: bool
    isPayPerUse: bool = None
    details: Union[List[DetailSchema], None]




class UtilitySchema(BaseModel):
    name: str
    responsibility: str
    details: Union[List[DetailSchema], None]

class RentDiscoutSchema(BaseModel):
    name: str
    amount: str
    details: Union[List[DetailSchema], None]

class RentDepositSchema(BaseModel):
    name: str
    amount: str
    details: Union[List[DetailSchema], None]

class AdditionalTermSchema(BaseModel):
    name: str 
    details: Union[List[DetailSchema], None]
    
class TenantNameSchema(BaseModel):
    name: str

class LeaseSchema(BaseModel):
    houseId: int
    landlordInfo: Union[LandlordInfoSchema, None]
    rentalAddress: Union[RentalAddressSchema, None]
    rent: Union[RentSchema, None]
    tenancyTerms: Union[TenancyTermsSchema, None]
    services: Union[List[ServiceSchema], None]
    utilities: Union[List[UtilitySchema], None] 
    rentDeposits: Union[List[RentDepositSchema], None] 
    rentDiscounts: Union[List[RentDiscoutSchema], None] 
    additionalTerms: Union[List[AdditionalTermSchema], None] 

