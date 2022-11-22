from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from models.models import Lease, LandlordInfo, Email, ContactInfo, LandlordAddress, RentalAddress, ParkingDescription, Rent, RentService, PaymentOption, TenancyTerms, RentalPeriod, PartialPeriod, Service, Utility, RentDiscount, RentDeposit, AdditionalTerm, Detail, ServiceDetailJuntion, UtilityDetailJuntion, RentDiscountDetailJunction, RentDepositDetailJunction, AdditionalTermDetailJunction

class DB:

    def __init__(self, user, password, host, database):
        self.engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{database}",  pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = Session()
        
    def get_session(self):
        return self.session



    async def get_landlord_info_by_lease_id(self, landlordInfo):
        result = await self.session.execute(select(LandlordInfo).where(LandlordInfo.lease_id == landlordInfo.lease_id))
        return result.scalars().first()

    async def get_landlord_address_by_lease_id(self, landlordAddress):
        result = await self.session.execute(select(LandlordAddress).where(LandlordAddress.lease_id == landlordAddress.lease_id))
        return result.scalars().first()

    async def get_rental_address_from_lease_id(self, rentalAddress):
        result = await self.session.execute(select(RentalAddress).where(RentalAddress.lease_id == rentalAddress.lease_id))
        return result.scalars().first()

    async def get_rent_from_lease_id(self, rent):
        result = await self.session.execute(select(Rent).where(Rent.lease_id == rent.lease_id))
        return result.scalars().first()

    async def get_tenancy_terms_from_lease_id(self, tenancyTerms):
        result = await self.session.execute(select(TenancyTerms).where(TenancyTerms.lease_id == tenancyTerms.lease_id))
        return result.scalars().first()

    async def get_rental_period_from_tenancy_terms_id(self, rentalPeriod):
        result = await self.session.execute(select(RentalPeriod).where(RentalPeriod.tenancy_terms_id == rentalPeriod.tenancy_terms_id))
        return result.scalars().first()

    async def get_partialPeriod_from_tenancy_terms_id(self, partialPeriod):
        result = await self.session.execute(select(PartialPeriod).where(PartialPeriod.tenancy_terms_id == partialPeriod.tenancy_terms_id))
        return result.scalars().first()

    async def get_lease_by_houseId(self, houseId):
        result = await self.session.execute(select(Lease).where(Lease.houseId == houseId))
        return result.scalars().first()

    async def get_all_service_detail_ids_from_lease_id(self, leaseId):
        result = await self.session.execute(select(Service.id).where(Service.lease_id == leaseId))
        serviceIds = result.scalars().all()
        result = await self.session.execute(select(ServiceDetailJuntion.detail_id).where(ServiceDetailJuntion.service_id.in_(serviceIds)))
        return result.scalars().all()

    async def get_all_utility_detail_ids_from_lease_id(self, leaseId):
        result = await self.session.execute(select(Utility.id).where(Utility.lease_id == leaseId))
        utilityIds = result.scalars().all()
        result = await self.session.execute(select(UtilityDetailJuntion.detail_id).where(UtilityDetailJuntion.utility_id.in_(utilityIds)))
        return result.scalars().all()

    async def get_all_rent_discount_detail_ids_from_lease_id(self, leaseId):
        result = await self.session.execute(select(RentDiscount.id).where(RentDiscount.lease_id == leaseId))
        rentDiscountIds = result.scalars().all()
        result = await self.session.execute(select(RentDiscountDetailJunction.detail_id).where(RentDiscountDetailJunction.rent_discount_id.in_(rentDiscountIds)))
        return result.scalars().all()

    async def get_all_rent_deposit_detail_ids_from_lease_id(self, leaseId):
        result = await self.session.execute(select(RentDeposit.id).where(RentDeposit.lease_id == leaseId))
        rentDepositIds = result.scalars().all()
        result = await self.session.execute(select(RentDepositDetailJunction.detail_id).where(RentDepositDetailJunction.rent_deposit_id.in_(rentDepositIds)))
        return result.scalars().all()

    async def get_all_additional_term_detail_ids_from_lease_id(self, leaseId):
        result = await self.session.execute(select(AdditionalTerm.id).where(AdditionalTerm.lease_id == leaseId))
        additionalTermIds = result.scalars().all()
        result = await self.session.execute(select(AdditionalTermDetailJunction.detail_id).where(AdditionalTermDetailJunction.additional_term_id.in_(additionalTermIds)))
        return result.scalars().all()

    async def update_landlord_info(self, landlordInfo):
        await self.session.execute(update(LandlordInfo).where(LandlordInfo.lease_id == landlordInfo.lease_id).values(landlordInfo.to_dict()))
             
    async def update_landlord_address(self, landlordAddress):
        await self.session.execute(update(LandlordAddress).where(LandlordAddress.lease_id == landlordAddress.lease_id).values(landlordAddress.to_dict()))

    async def update_rental_address(self, rentalAddress):
        await self.session.execute(update(RentalAddress).where(RentalAddress.lease_id == rentalAddress.lease_id).values(rentalAddress.to_dict()))

    async def update_rent(self, rent):
        await self.session.execute(update(Rent).where(Rent.lease_id == rent.lease_id).values(rent.to_dict()))

    async def update_tenancy_terms(self, tenancyTerms):
        await self.session.execute(update(TenancyTerms).where(TenancyTerms.lease_id == tenancyTerms.lease_id).values(tenancyTerms.to_dict()))

    async def update_rental_period(self, rentalPeriod):
        await self.session.execute(update(RentalPeriod).where(RentalPeriod.tenancy_terms_id == rentalPeriod.tenancy_terms_id).values(rentalPeriod.to_dict()))

    async def update_partial_period(self, partialPeriod):
        await self.session.execute(update(PartialPeriod).where(PartialPeriod.tenancy_terms_id == partialPeriod.tenancy_terms_id).values(partialPeriod.to_dict()))

    async def delete_by_column_id(self, model, column, id):
        await self.session.execute(delete(model).where(column == id))

    async def delete_by_ids(self, model, column, ids):
        await self.session.execute(delete(model).where(column.in_(ids)))

    async def insert(self, data):
        self.session.add(data)

    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()

    async def delete_lease_by_house_id(self, houseId):
        await self.session.execute(delete(Lease).where(Lease.houseId == houseId))