from models.monad import RepositoryMaybeMonad
from models.models import *




class Repository:

    def __init__(self, db):
        self.db = db

    async def insert(self, lease):
        async with self.db.get_session() as session:
            monad = await RepositoryMaybeMonad(lease) \
                .bind(self.db.insert)
            if monad.has_errors():
                return await RepositoryMaybeMonad() \
                    .bind(self.db.rollback)
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)
        


    async def get_lease(self, houseId):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(houseId) \
                .bind_data(self.db.get_lease_by_houseId)
            print(monad.error_status)
            return monad


    async def update_landlord_info(self, landlordInfo):
        monad = await RepositoryMaybeMonad(landlordInfo) \
            .bind_data(self.db.get_landlord_info_by_lease_id)
        await monad \
            .bind(self.db.update_landlord_info)
        
        await RepositoryMaybeMonad(Email, Email.landlord_info_id, monad.get_param_at(0).id) \
            .bind(self.db.delete_by_column_id)
        await RepositoryMaybeMonad(ContactInfo, ContactInfo.landlord_info_id, monad.get_param_at(0).id) \
            .bind(self.db.delete_by_column_id)

        for email in landlordInfo.emails:
            email.landlord_info_id = monad.get_param_at(0).id
            monad = await RepositoryMaybeMonad(email) \
                .bind(self.db.insert)
        
        for contact in landlordInfo.contacts:
            contact.landlord_info_id = monad.get_param_at(0).id
            monad = await RepositoryMaybeMonad(contact) \
                .bind(self.db.insert)

        return await RepositoryMaybeMonad() \
            .bind(self.db.commit)
       



    async def update_landlord_address(self, landlordAddress):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(landlordAddress) \
                .bind_data(self.db.get_landlord_address_by_lease_id)
            monad = await monad \
                .bind(self.db.update_landlord_address)
            if monad.has_errors():
                return monad 
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)




    async def update_rental_address(self, rentalAddress):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(rentalAddress) \
                .bind_data(self.db.get_rental_address_from_lease_id)
            if monad.get_param_at(0) is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Rent not found with lease id: {lease_id}"})
            await monad \
                .bind(self.db.update_rental_address)

            await RepositoryMaybeMonad(ParkingDescription, ParkingDescription.rental_address_id, monad.get_param_at(0).id) \
                .bind(self.db.delete_by_column_id)
        
            for parkingDescription in rentalAddress.parkingDescriptions:
                parkingDescription.rental_address_id = monad.get_param_at(0).id
                await RepositoryMaybeMonad(parkingDescription) \
                    .bind(self.db.insert)
               
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)
            



    async def update_rent(self, rent):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(rent) \
                .bind_data(self.db.get_rent_from_lease_id)
            if monad.get_param_at(0) is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Rent not found with lease id: {lease_id}"})
            await monad \
                .bind(self.db.update_rent)

            await RepositoryMaybeMonad(RentService, RentService.rent_id, monad.get_param_at(0).id) \
                .bind(self.db.delete_by_column_id)
            await RepositoryMaybeMonad(PaymentOption, PaymentOption.rent_id, monad.get_param_at(0).id) \
                .bind(self.db.delete_by_column_id)

            for rentService in rent.rentServices:
                rentService.rent_id = monad.get_param_at(0).id
                await RepositoryMaybeMonad(rentService) \
                    .bind(self.db.insert)
             
            for paymentOption in rent.paymentOptions:
                paymentOption.rent_id = monad.get_param_at(0).id
                await RepositoryMaybeMonad(paymentOption) \
                    .bind(self.db.insert)

            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)
          


    async def update_tenancy_terms(self, tenancyTerms):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(tenancyTerms) \
                    .bind_data(self.db.get_tenancy_terms_from_lease_id)
            if monad.get_param_at(0) is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"Tenancy terms not found with lease id: {tenancyTerms.lease_id}"})
            monad = await RepositoryMaybeMonad(tenancyTerms) \
                .bind(self.db.update_tenancy_terms)


            monad = await RepositoryMaybeMonad(tenancyTerms.rentalPeriod) \
                .bind_data(self.db.get_rental_period_from_tenancy_terms_id)
            monad = await monad \
                .bind(self.db.update_rental_period)


            monad = await RepositoryMaybeMonad(tenancyTerms.partialPeriod) \
                .bind_data(self.db.get_partialPeriod_from_tenancy_terms_id)
           
            monad = await monad \
                .bind(self.db.update_partial_period)
            
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)
              

    async def update_services(self, services, leaseId):
        async with self.db.session:
            monad = await RepositoryMaybeMonad(leaseId) \
                .bind_data(self.db.get_all_service_detail_ids_from_lease_id)
           
            await RepositoryMaybeMonad(ServiceDetailJuntion, ServiceDetailJuntion.detail_id, monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            await RepositoryMaybeMonad(Detail, Detail.id,  monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            
            await RepositoryMaybeMonad(Service, Service.lease_id, leaseId) \
                .bind(self.db.delete_by_column_id)
            
            for service in services:
                service.lease_id = leaseId
                await RepositoryMaybeMonad(service) \
                    .bind(self.db.insert)
            
            return await RepositoryMaybeMonad() \
                    .bind(self.db.commit)
   

    async def update_utilities(self, utilities, leaseId):
        async with self.db.session:
            monad = await RepositoryMaybeMonad(leaseId) \
                .bind_data(self.db.get_all_utility_detail_ids_from_lease_id)
           
            await RepositoryMaybeMonad(UtilityDetailJuntion, UtilityDetailJuntion.detail_id, monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            await RepositoryMaybeMonad(Detail, Detail.id,  monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            
            await RepositoryMaybeMonad(Utility, Utility.lease_id, leaseId) \
                .bind(self.db.delete_by_column_id)
            
            for utility in utilities:
                utility.lease_id = leaseId
                await RepositoryMaybeMonad(utility) \
                    .bind(self.db.insert)
            
            return await RepositoryMaybeMonad() \
                    .bind(self.db.commit)


    async def update_rent_discounts(self, rentDiscounts, leaseId):
        async with self.db.session:
            monad = await RepositoryMaybeMonad(leaseId) \
                .bind_data(self.db.get_all_rent_discount_detail_ids_from_lease_id)
           
            await RepositoryMaybeMonad(RentDiscountDetailJunction, RentDiscountDetailJunction.detail_id, monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            await RepositoryMaybeMonad(Detail, Detail.id,  monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            
            await RepositoryMaybeMonad(RentDiscount, RentDiscount.lease_id, leaseId) \
                .bind(self.db.delete_by_column_id)
            
            for rentDiscount in rentDiscounts:
                rentDiscount.lease_id = leaseId
                await RepositoryMaybeMonad(rentDiscount) \
                    .bind(self.db.insert)
            
            return await RepositoryMaybeMonad() \
                    .bind(self.db.commit)


    async def update_rent_deposits(self, rentDeposits, leaseId):
        async with self.db.session:
            monad = await RepositoryMaybeMonad(leaseId) \
                .bind_data(self.db.get_all_rent_deposit_detail_ids_from_lease_id)
            
            await RepositoryMaybeMonad(RentDepositDetailJunction, RentDepositDetailJunction.detail_id, monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            await RepositoryMaybeMonad(Detail, Detail.id,  monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)

            await RepositoryMaybeMonad(RentDeposit, RentDeposit.lease_id, leaseId) \
                .bind(self.db.delete_by_column_id)

            for rentDeposit in rentDeposits:
                rentDeposit.lease_id = leaseId
                await RepositoryMaybeMonad(rentDeposit) \
                    .bind(self.db.insert)

            return await RepositoryMaybeMonad() \
                    .bind(self.db.commit)



    async def update_additional_terms(self, additionalTerms, leaseId):
        async with self.db.session:
            monad = await RepositoryMaybeMonad(leaseId) \
                .bind_data(self.db.get_all_additional_term_detail_ids_from_lease_id)
            
            await RepositoryMaybeMonad(AdditionalTermDetailJunction, AdditionalTermDetailJunction.detail_id, monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)
            await RepositoryMaybeMonad(Detail, Detail.id,  monad.get_param_at(0)) \
                .bind(self.db.delete_by_ids)

            await RepositoryMaybeMonad(AdditionalTerm, AdditionalTerm.lease_id, leaseId) \
                .bind(self.db.delete_by_column_id)

            for additionalTerm in additionalTerms:
                additionalTerm.lease_id = leaseId
                await RepositoryMaybeMonad(additionalTerm) \
                    .bind(self.db.insert)
            
            return await RepositoryMaybeMonad() \
                    .bind(self.db.commit)

 