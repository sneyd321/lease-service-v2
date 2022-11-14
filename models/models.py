from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Lease(Base):
    __tablename__ = "lease"

    id = Column(Integer(), primary_key=True)
    houseId = Column(Integer(), nullable=False, unique=True)
    documentURL = Column(String(223), nullable=True)
    documentName = Column(String(100), nullable=False)
    documentState = Column(String(20), nullable=False)
    landlordInfo = relationship("LandlordInfo", lazy="joined", backref="lease", uselist=False)
    landlordAddress = relationship("LandlordAddress", lazy="joined",backref="lease", uselist=False)
    rentalAddress = relationship("RentalAddress", lazy="joined",backref="lease", uselist=False)
    rent = relationship("Rent", backref="lease", lazy="joined",uselist=False)
    tenancyTerms = relationship("TenancyTerms", lazy="joined",backref="lease", uselist=False)
    services = relationship("Service", lazy="subquery")
    utilities = relationship("Utility", lazy="subquery",)
    rentDiscounts = relationship("RentDiscount", lazy="subquery",)
    rentDeposits = relationship("RentDeposit", lazy="subquery",)
    additionalTerms = relationship("AdditionalTerm", lazy="subquery",)


    def __init__(self, **kwargs):
        self.documentName = "2229E Residential Tenancy Agreement"
        self.documentState = "CREATED"
        self.houseId = kwargs.get("houseId")
        self.landlordInfo = LandlordInfo(**kwargs.get("landlordInfo"))
        self.landlordAddress = LandlordAddress(**kwargs.get("landlordAddress"))
        self.rentalAddress = RentalAddress(**kwargs.get("rentalAddress"))
        self.rent = Rent(**kwargs.get("rent"))
        self.tenancyTerms = TenancyTerms(**kwargs.get("tenancyTerms"))
        self.services = [Service(**json) for json in kwargs.get("services")]
        self.utilities = [Utility(**json) for json in kwargs.get("utilities")]
        self.rentDiscounts = [RentDiscount(**json) for json in kwargs.get("rentDiscounts")]
        self.rentDeposits = [RentDeposit(**json) for json in kwargs.get("rentDeposits")]
        self.additionalTerms = [AdditionalTerm(**json) for json in kwargs.get("additionalTerms")]
        
    def initialize_document(self, firebase, houseId):
        blob = firebase.create_blob_no_cache(f"OntarioLease/Lease_{houseId}.pdf")
        blob.upload_from_string(b"", content_type="application/pdf")
        self.documentURL = blob.public_url
    
    def to_dict(self):
        return {
            "houseId": self.houseId,
            "documentURL": self.documentURL,
            "documentName": self.documentName,
            "documentState": self.documentState
        } 
        
    def to_json(self):
        return {
            "id": self.id,
            "houseId": self.houseId,
            "documentURL": self.documentURL,
            "documentName": self.documentName,
            "documentState": self.documentState,
            "landlordInfo": self.landlordInfo.to_json(),
            "landlordAddress": self.landlordAddress.to_json(),
            "rentalAddress": self.rentalAddress.to_json(),
            "rent": self.rent.to_json(),
            "tenancyTerms": self.tenancyTerms.to_json(),
            "services": [service.to_json() for service in self.services],
            "utilities": [utility.to_json() for utility in self.utilities],
            "rentDiscounts": [rentDiscount.to_json() for rentDiscount in self.rentDiscounts],
            "rentDeposits": [rentDeposit.to_json() for rentDeposit in self.rentDeposits],
            "additionalTerms": [additionalTerm.to_json() for additionalTerm in self.additionalTerms],
        }

   
class LandlordAddress(Base):
    __tablename__ = "landlord_address"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    streetNumber = Column(String(10), nullable=False)
    streetName = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False )
    province = Column(String(100), nullable=False)
    postalCode = Column(String(10), nullable=False)
    unitNumber = Column(String(10), nullable=True)
    poBox = Column(String(10), nullable=True)

    def __init__(self, **kwargs):
        self.streetNumber = kwargs.get("streetNumber")
        self.streetName = kwargs.get("streetName")
        self.city = kwargs.get("city")
        self.province = kwargs.get("province")
        self.postalCode = kwargs.get("postalCode")
        self.unitNumber = kwargs.get("unitNumber")
        self.poBox = kwargs.get("poBox")

    def to_dict(self):
        return {
            "lease_id": self.lease_id,
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }


    def to_json(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }


class RentalAddress(Base):
    __tablename__ = "rental_address"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    streetNumber = Column(String(10), nullable=False)
    streetName = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    postalCode = Column(String(10), nullable=False)
    unitName = Column(String(100), nullable=False)
    isCondo = Column(Boolean(), nullable=False)
    parkingDescriptions = relationship("ParkingDescription", lazy="subquery")



    def __init__(self, **kwargs):
        self.streetNumber = kwargs.get("streetNumber")
        self.streetName = kwargs.get("streetName")
        self.city = kwargs.get("city")
        self.province = kwargs.get("province")
        self.postalCode = kwargs.get("postalCode")
        self.unitName = kwargs.get("unitName")
        self.isCondo = kwargs.get("isCondo")
        self.parkingDescriptions = [ParkingDescription(**json) for json in kwargs.get("parkingDescriptions", [])]

    def to_dict(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitName": self.unitName,
            "isCondo": self.isCondo,
        }

    def to_json(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitName": self.unitName,
            "isCondo": self.isCondo,
            "parkingDescriptions": [parkingDescription.to_json() for parkingDescription in self.parkingDescriptions]
        }



class Rent(Base):
    __tablename__ = "rent"
    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    baseRent = Column(String(16))
    rentMadePayableTo = Column(String(200))
    rentServices = relationship("RentService", lazy="subquery")
    paymentOptions = relationship("PaymentOption", lazy="subquery")

    def __init__(self, **kwargs):
        self.baseRent = kwargs.get("baseRent")
        self.rentMadePayableTo = kwargs.get("rentMadePayableTo")
        self.rentServices = [RentService(**json) for json in kwargs.get("rentServices")]
        self.paymentOptions = [PaymentOption(**json) for json in kwargs.get("paymentOptions")]

    def to_dict(self):
        return {
            "baseRent": self.baseRent,
            "rentMadePayableTo": self.rentMadePayableTo
        }

    def to_json(self):
        return {
            "baseRent": self.baseRent,
            "rentMadePayableTo": self.rentMadePayableTo,
            "rentServices": [rentService.to_json() for rentService in self.rentServices],
            "paymentOptions": [paymentOption.to_json() for paymentOption in self.paymentOptions]
        }



class RentService(Base):
    __tablename__ = "rent_service"
    id = Column(Integer(), primary_key=True)
    rent_id = Column(Integer(), ForeignKey("rent.id"))
    name = Column(String(200), nullable=False)
    amount = Column(String(16), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount
        }


class PaymentOption(Base):
    __tablename__ = "payment_option"
    id = Column(Integer(), primary_key=True)
    rent_id = Column(Integer(), ForeignKey("rent.id"))
    name = Column(String(200), nullable=False)
   
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")

    def to_json(self):
        return {
            "name": self.name
        }


class TenancyTerms(Base):
    __tablename__ = "tenancy_terms"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    startDate = Column(String(20), nullable=False)
    rentDueDate = Column(String(20), nullable=False)
    paymentPeriod = Column(String(20), nullable=False)
    rentalPeriod = relationship("RentalPeriod", lazy="joined", backref="tenancy_terms", uselist=False)
    partialPeriod = relationship("PartialPeriod", lazy="joined", backref="tenancy_terms", uselist=False)

    def __init__(self, **kwargs):
        self.startDate = kwargs.get("startDate")
        self.rentDueDate = kwargs.get("rentDueDate")
        self.paymentPeriod = kwargs.get("paymentPeriod")
        self.rentalPeriod = RentalPeriod(**kwargs.get("rentalPeriod"))
        self.partialPeriod = PartialPeriod(**kwargs.get("partialPeriod"))


    def to_dict(self):
        return {
            "startDate": self.startDate,
            "rentDueDate": self.rentDueDate,
            "paymentPeriod": self.paymentPeriod
        }

    def to_json(self):
        return {
            "startDate": self.startDate,
            "rentDueDate": self.rentDueDate,
            "paymentPeriod": self.paymentPeriod,
            "rentalPeriod": self.rentalPeriod.to_json(),
            "partialPeriod": self.partialPeriod.to_json()
        }

class RentalPeriod(Base):
    __tablename__ = "rental_period"

    id = Column(Integer(), primary_key=True)
    tenancy_terms_id = Column(Integer(), ForeignKey("tenancy_terms.id"))
    rentalPeriod = Column(String(20), nullable=False)
    endDate = Column(String(20), nullable=True)

    def __init__(self, **kwargs):
        self.rentalPeriod = kwargs.get("rentalPeriod")
        self.endDate = kwargs.get("endDate", "")

    def to_dict(self):
        return {
            "rentalPeriod": self.rentalPeriod,
            "endDate": self.endDate
        }
    
    def to_json(self):
        return {
            "rentalPeriod": self.rentalPeriod,
            "endDate": self.endDate
        }

class PartialPeriod(Base):
    __tablename__ = "partial_period"

    id = Column(Integer(), primary_key=True)
    tenancy_terms_id = Column(Integer(), ForeignKey("tenancy_terms.id"))
    amount = Column(String(16), nullable=False)
    dueDate = Column(String(20), nullable=False)
    startDate = Column(String(20), nullable=False)
    endDate = Column(String(20), nullable=False)
    isEnabled = Column(Boolean(), nullable=False)

    def __init__(self, **kwargs):
        self.amount = kwargs.get("amount")
        self.dueDate = kwargs.get("dueDate")
        self.startDate = kwargs.get("startDate")
        self.endDate = kwargs.get("endDate")
        self.isEnabled = kwargs.get("isEnabled")

    def to_dict(self):
        return {
            "amount": self.amount,
            "dueDate": self.dueDate,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "isEnabled": self.isEnabled
        }

    def to_json(self):
        return {
            "amount": self.amount,
            "dueDate": self.dueDate,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "isEnabled": self.isEnabled
        }

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    name = Column(String(100), nullable=False)
    isIncludedInRent = Column(Boolean(), nullable=False)
    isPayPerUse = Column(Boolean(), nullable=True)
    details = relationship("Detail", secondary="service_detail_junction", lazy="subquery")

    
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.isIncludedInRent = kwargs.get("isIncludedInRent")
        self.isPayPerUse = kwargs.get("isPayPerUse", False)
        self.details = [Detail(**json) for json in kwargs.get("details")]


    def to_json(self):
        return {
            "name": self.name,
            "isIncludedInRent": self.isIncludedInRent,
            "isPayPerUse": self.isPayPerUse,
            "details": [detail.to_json() for detail in self.details]
        }

class ServiceDetailJuntion(Base):
    __tablename__ = "service_detail_junction"

    service_id = Column(Integer(), ForeignKey("service.id"), primary_key=True)
    detail_id = Column(Integer(), ForeignKey("detail.id"), primary_key=True)


class Detail(Base):
    __tablename__ = "detail"

    id = Column(Integer(), primary_key=True)
    detail = Column(String(300), nullable=False)
    
    def __init__(self, **kwargs):
        self.detail = kwargs.get("detail")

    def to_json(self):
        return {
            "detail": self.detail
        }


class UtilityDetailJuntion(Base):
    __tablename__ = "utility_detail_junction"

    utility_id = Column(Integer(), ForeignKey("utility.id"), primary_key=True)
    detail_id = Column(Integer(), ForeignKey("detail.id"), primary_key=True)

class Utility(Base):
    __tablename__ = "utility"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    name = Column(String(100), nullable=False)
    responsibility = Column(String(50), nullable=False)
    details = relationship("Detail", secondary="utility_detail_junction", lazy="subquery")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.responsibility = kwargs.get("responsibility")
        self.details = [Detail(**json) for json in kwargs.get("details")]

        
    def to_dict(self):
        return {
             "name": self.name,
            "responsibility": self.responsibility
        }

    def to_json(self):
        return {
            "name": self.name,
            "responsibility": self.responsibility,
            "details": [detail.to_json() for detail in self.details]
        }
   

class RentDiscountDetailJunction(Base):
    __tablename__ = "rent_discount_detail_junction"

    rent_discount_id = Column(Integer(), ForeignKey("rent_discount.id"), primary_key=True)
    detail_id = Column(Integer(), ForeignKey("detail.id"), primary_key=True)


class RentDiscount(Base):
    __tablename__ = "rent_discount"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    name = Column(String(100), nullable=False)
    amount = Column(String(16), nullable=False)
    details = relationship("Detail", secondary="rent_discount_detail_junction", lazy="subquery")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")
        self.details = [Detail(**json) for json in kwargs.get("details")]

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount
        }

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "details": [detail.to_json() for detail in self.details]
        }
    
class RentDepositDetailJunction(Base):
    __tablename__ = "rent_deposit_detail_junction"

    rent_deposit_id = Column(Integer(), ForeignKey("rent_deposit.id"), primary_key=True)
    detail_id = Column(Integer(), ForeignKey("detail.id"), primary_key=True)



class RentDeposit(Base):
    __tablename__ = "rent_deposit"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    name = Column(String(100), nullable=False)
    amount = Column(String(16), nullable=False)
    details = relationship("Detail", secondary="rent_deposit_detail_junction", lazy="subquery")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")
        self.details = [Detail(**json) for json in kwargs.get("details")]

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount
        }

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "details": [detail.to_json() for detail in self.details]
        }

class AdditionalTermDetailJunction(Base):
    __tablename__ = "additional_term_detail_junction"

    additional_term_id = Column(Integer(), ForeignKey("additional_term.id"), primary_key=True)
    detail_id = Column(Integer(), ForeignKey("detail.id"), primary_key=True)

class AdditionalTerm(Base):
    __tablename__ = "additional_term"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    name = Column(String(100), nullable=False)
    details = relationship("Detail", secondary="additional_term_detail_junction", lazy="subquery")


    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.details = [Detail(**json) for json in kwargs.get("details")]

    def to_dict(self):
        return {
            "name": self.name
        }

    def to_json(self):
        return {
            "name": self.name,
            "details": [detail.to_json() for detail in self.details]
        }

class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer(), primary_key=True)
    landlord_info_id = Column(Integer(), ForeignKey("landlord_info.id"))
    contact = Column(String(255), nullable=False)

    def __init__(self, **kwargs):
        self.contact = kwargs.get("contact")

    def to_dict(self):
        return  {
            "contact": self.contact
        }
    
    def to_json(self): 
        return  {
            "contact": self.contact
        }


class Email(Base):
    __tablename__ = "email"

    id = Column(Integer(), primary_key=True)
    landlord_info_id = Column(Integer(), ForeignKey("landlord_info.id"))
    email = Column(String(255), nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get("email")

    def to_dict(self):
        return  {
            "email": self.email
        }
    
    def to_json(self): 
        return  {
            "email": self.email
        }

class LandlordInfo(Base):
    __tablename__ = "landlord_info"

    id = Column(Integer(), primary_key=True)
    lease_id = Column(Integer(), ForeignKey("lease.id"))
    fullName = Column(String(200), nullable=False)
    receiveDocumentsByEmail = Column(Boolean(), nullable=False)
    contactInfo = Column(Boolean(), nullable=False)
    contacts = relationship("ContactInfo", lazy="subquery")
    emails = relationship("Email", lazy="subquery")

    def __init__(self, **kwargs):
        self.fullName = kwargs.get("fullName")
        self.receiveDocumentsByEmail = kwargs.get("receiveDocumentsByEmail")
        self.contactInfo = kwargs.get("contactInfo")
        self.contacts = [ContactInfo(**json) for json in kwargs.get("contacts")]
        self.emails = [Email(**json) for json in kwargs.get("emails")]

    def to_dict(self):
        return  {
            "fullName": self.fullName,
            "contactInfo": self.contactInfo,
            "receiveDocumentsByEmail": self.receiveDocumentsByEmail
        }
    
    def to_json(self): 
        return  {
            "fullName": self.fullName,
            "contactInfo": self.contactInfo,
            "receiveDocumentsByEmail": self.receiveDocumentsByEmail,
            "contacts": [contact.to_json() for contact in self.contacts],
            "emails": [email.to_json() for email in self.emails]
        }


class ParkingDescription(Base):
    __tablename__ = "parking_description"

    id = Column(Integer(), primary_key=True)
    rental_address_id = Column(Integer(), ForeignKey("rental_address.id"))
    location = Column(String(100), nullable=False)

    def __init__(self, **kwargs):
        self.location = kwargs.get("description")

    def to_dict(self):
        return {
            "description": self.location
        }

    def to_json(self): 
        return {
            "description": self.location
        }