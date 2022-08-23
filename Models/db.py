from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from Models.models import *

class DB:

    def __init__(self, user, password, host, database):
        self.engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{database}", echo=True, pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = Session()
        
    def get_session(self):
        return self.session


    async def get_all_service_ids_from_lease_id(self, lease_id):
        return await self.get_ids_from_lease_id(Service, lease_id)

    async def get_all_detail_ids_from_service_junction(self, serviceIds):
        return await self.get_all_detail_ids_from_junction(ServiceDetailJuntion, ServiceDetailJuntion.service_id, serviceIds)
    
    async def get_rent_id_from_lease_id(self, lease_id):
        return await self.get_by_column_id_from_id(Rent.id, Rent.lease_id, lease_id)

    async def get_tenancy_terms_id_from_lease_id(self, lease_id):
        return await self.get_by_column_id_from_id(TenancyTerms.id, TenancyTerms.lease_id, lease_id)




    async def get_all_utility_ids_from_lease_id(self, lease_id):
        return await self.get_ids_from_lease_id(Utility, lease_id)

    async def get_all_detail_ids_from_utility_junction(self, utilityIds):
        return await self.get_all_detail_ids_from_junction(UtilityDetailJuntion, UtilityDetailJuntion.utility_id, utilityIds)
    
    async def get_all_rent_discount_ids_from_lease_id(self, lease_id):
        return await self.get_ids_from_lease_id(RentDiscount, lease_id)

    async def get_all_detail_ids_from_rent_discount_junction(self, rentDiscountIds):
        return await self.get_all_detail_ids_from_junction(RentDiscountDetailJunction, RentDiscountDetailJunction.rent_discount_id, rentDiscountIds)
    
    async def get_all_additional_term_ids_from_lease_id(self, lease_id):
        return await self.get_ids_from_lease_id(AdditionalTerm, lease_id)

    async def get_all_detail_ids_from_additional_term_junction(self, additionalTermIds):
        return await self.get_all_detail_ids_from_junction(AdditionalTermDetailJunction, AdditionalTermDetailJunction.additional_term_id, additionalTermIds)
    
    async def get_lease(self, lease_id):
        result = await self.session.execute(select(Lease).where(Lease.id == lease_id))
        return result.scalars().first()





    async def get_by_column_id_from_id(self, model, column, id):
        result = await self.session.execute(select(model).where(column == id))
        return result.scalars().first()

    async def get_all_by_column_id_from_ids(self, model, column, ids):
        result = await self.session.execute(select(model).where(column.in_(ids)))
        return result.scalars().all()

    async def get_all_detail_ids_from_junction(self, junction, junctionColumn, ids):
        return await self.get_all_by_column_id_from_ids(junction.detail_id, junctionColumn, ids)

    async def get_ids_from_lease_id(self, model, leaseId):
        result = await self.session.execute(select(model.id).where(model.lease_id == leaseId))
        return result.scalars().all()


    async def get_all_by_lease_id(self, model, leaseId):
        result = await self.session.execute(select(model).where(model.lease_id == leaseId))
        return result.scalars().all()


    async def insert(self, data):
        self.session.add(data)

    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()






    
    async def update_landlord_address(self, landlordAddress):
        await self.update_by_lease_id(LandlordAddress, landlordAddress)

    async def update_rental_address(self, rentalAddress):
        await self.update_by_lease_id(RentalAddress, rentalAddress)

    async def update_rent(self, rent):
        await self.update_by_lease_id(Rent, rent)
    
    async def update_tenancy_terms(self, tenancyTerms):
        await self.update_by_lease_id(TenancyTerms, tenancyTerms)

    async def update_rental_period(self, rentalPeriod):
        await self.update_by_tenancy_terms_id(RentalPeriod, rentalPeriod)

    async def update_partial_period(self, partialPeriod):
        await self.update_by_tenancy_terms_id(PartialPeriod, partialPeriod)

   






    async def delete_rent_services(self, rent_id):
        await self.delete_by_column_id(RentService, RentService.rent_id, rent_id)

    async def delete_payment_options(self, rent_id):
        await self.delete_by_column_id(PaymentOption, PaymentOption.rent_id, rent_id)

    async def delete_service_detail_junctions(self, serviceIds):
        await self.delete_by_ids(ServiceDetailJuntion, ServiceDetailJuntion.service_id, serviceIds)

    async def delete_details(self, detailIds):
        await self.delete_by_ids(Detail, Detail.id, detailIds)

    async def delete_services(self, lease_id):
        await self.delete_by_column_id(Service, Service.lease_id, lease_id)
    
    async def delete_utility_detail_junctions(self, utilityIds):
        await self.delete_by_ids(UtilityDetailJuntion, UtilityDetailJuntion.utility_id, utilityIds)
    
    async def delete_utilities(self, lease_id):
        await self.delete_by_column_id(Utility, Utility.lease_id, lease_id)

    async def delete_rent_discount_detail_junctions(self, rentDiscoutIds):
        await self.delete_by_ids(RentDiscountDetailJunction, RentDiscountDetailJunction.rent_discount_id, rentDiscoutIds)
    
    async def delete_rent_discounts(self, lease_id):
        await self.delete_by_column_id(RentDiscount, RentDiscount.lease_id, lease_id)

    async def delete_additional_terms_junctions(self, additionalTermIds):
        await self.delete_by_ids(AdditionalTermDetailJunction, AdditionalTermDetailJunction.additional_term_id, additionalTermIds)
    
    async def delete_additional_terms(self, lease_id):
        await self.delete_by_column_id(AdditionalTerm, AdditionalTerm.lease_id, lease_id)






    async def delete_by_ids(self, model, column, ids):
        await self.session.execute(delete(model).where(column.in_(ids)))

    async def delete_by_column_id(self, model, column, id):
        await self.session.execute(delete(model).where(column == id))
    
    async def update_by_lease_id(self, model, data):
        await self.session.execute(update(model).where(model.lease_id == data.lease_id).values(data.to_dict()))
             
    async def delete_by_rent_id(self, model, data):
        await self.session.execute(delete(model).where(model.rent_id == data.id))
                
    async def update_by_tenancy_terms_id(self, model, data):
        await self.session.execute(update(model).where(model.tenancy_terms_id == data.tenancy_terms_id).values(data.to_dict()))
             
    async def delete_by_lease_id(self, model, data):
        await self.session.execute(delete(model).where(model.lease_id == data.lease_id))

    