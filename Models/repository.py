
from sqlalchemy.exc import OperationalError, IntegrityError
from Models.models import *
from Models.monad import MaybeMonad




class Repository:

    def __init__(self, db):
        self.db = db

    async def check(self, monad):
        if monad.error_status:
            await self.db.rollback()
            return False
        return True

    async def create_all(self):
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await self.db.commit()

    

    async def insert_lease(self, lease):
        async with self.db.get_session():
            monad = MaybeMonad(lease)
            monad = await monad.bind(self.db.insert)
            if await self.check(monad) == False:
                return monad
            await self.db.commit()
            return monad

    async def get_lease(self, houseIds):
        async with self.db.get_session():
            return await self.db.get_all_lease_by_house_ids(houseIds)

    async def update_landlord_info(self, landlordInfo, lease_id):
        landlordInfo.lease_id = lease_id
        landlordInfoId = await self.db.get_landlord_info_id_from_lease_id(lease_id)
        if not landlordInfoId:
            return MaybeMonad(None, error_status={"status": 404, "reason": f"Landlord Info not found with lease id: {lease_id}"})
            
        landlordInfo.id = landlordInfoId
        monad = MaybeMonad(landlordInfo)
        monad = await monad.bind(self.db.update_landlord_info)
        if await self.check(monad) == False:
            return monad

        monad = MaybeMonad(landlordInfo.id)
        monad = await monad.bind(self.db.delete_emails)
        monad = await monad.bind(self.db.delete_contacts)
        if await self.check(monad) == False:
            return monad

        for email in landlordInfo.emails:
            email.landlord_info_id = landlordInfo.id
            monad = MaybeMonad(email)
            moand = await monad.bind(self.db.insert)
            if await self.check(monad) == False:
                return monad
        
        for contact in landlordInfo.contacts:
            contact.landlord_info_id = landlordInfo.id
            monad = MaybeMonad(contact)
            monad = await monad.bind(self.db.insert)
            if await self.check(monad) == False:
                return monad

        await self.db.commit()
        return monad

    async def update_landlord_address(self, landlordAddress, lease_id):
        async with self.db.get_session():
            monad = MaybeMonad(landlordAddress)
            monad = await monad.bind(self.db.update_landlord_address)
            if await self.check(monad) == False:
                return monad

            await self.db.commit()
            return monad

    async def update_rental_address(self, rentalAddress, lease_id):
        async with self.db.get_session():
            rentalAddress.lease_id = lease_id
            rentalAddressId = await self.db.get_rental_address_from_lease_id(lease_id)
            if not rentalAddressId:
                return MaybeMonad(None, error_status={"status": 404, "reason": f"Rent not found with lease id: {lease_id}"})
                
            rentalAddress.id = rentalAddressId
            monad = MaybeMonad(rentalAddress)
            monad = await monad.bind(self.db.update_rental_address)
            if await self.check(monad) == False:
                return monad

            monad = MaybeMonad(rentalAddress.id)
            monad = await monad.bind(self.db.delete_parking_descriptions)
            if await self.check(monad) == False:
                return monad
            print(rentalAddress.to_json())

            for parkingDescription in rentalAddress.parkingDescriptions:
                parkingDescription.rental_address_id = rentalAddress.id
                print(parkingDescription)
                monad = MaybeMonad(parkingDescription)
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad
            
            await self.db.commit()
            return monad

    async def update_rent(self, rent, lease_id):
        async with self.db.get_session():
            rent.lease_id = lease_id
            rentId = await self.db.get_rent_id_from_lease_id(lease_id)
            if not rentId:
                return MaybeMonad(None, error_status={"status": 404, "reason": f"Rent not found with lease id: {lease_id}"})
            
            rent.id = rentId
            monad = MaybeMonad(rent)
            monad = await monad.bind(self.db.update_rent)
            if await self.check(monad) == False:
                return monad

            monad = MaybeMonad(rent.id)
            monad = await monad.bind(self.db.delete_rent_services)
            monad = await monad.bind(self.db.delete_payment_options)
            if await self.check(monad) == False:
                return monad

            for rentService in rent.rentServices:
                rentService.rent_id = rent.id
                monad = MaybeMonad(rentService)
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad
            
            for paymentOption in rent.paymentOptions:
                paymentOption.rent_id = rent.id
                monad = MaybeMonad(paymentOption)
                monad = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad

            await self.db.commit()
            return monad
          


    async def update_tenancy_terms(self, tenancyTerms, lease_id):
        async with self.db.get_session():
            tenancyTerms.lease_id =lease_id
            tenancyTermsId = await self.db.get_tenancy_terms_id_from_lease_id(lease_id)
            if not tenancyTermsId:
                MaybeMonad(None, error_status={status: 404, "reason": f"Tenancy terms not found with lease id: {tenancyTerms.lease_id}"})
            
            tenancyTerms.id = tenancyTermsId
            monad = MaybeMonad(tenancyTerms)
            monad = await monad.bind(self.db.update_tenancy_terms)
            if await self.check(monad) == False:
                return monad
            
            tenancyTerms.rentalPeriod.tenancy_terms_id = tenancyTermsId
            monad = MaybeMonad(tenancyTerms.rentalPeriod)
            monad = await monad.bind(self.db.update_rental_period)
            if await self.check(monad) == False:
                return monad

            tenancyTerms.partialPeriod.tenancy_terms_id = tenancyTermsId
            monad = MaybeMonad(tenancyTerms.partialPeriod)
            monad = await monad.bind(self.db.update_partial_period)
            if await self.check(monad) == False:
                return monad

            await self.db.commit()
            return monad
              

    async def update_services(self, services, leaseId):
        async with self.db.session:
            serviceIds = await self.db.get_all_service_ids_from_lease_id(leaseId)
            #Get all matching detail ids for from the service detail junction table
            detailIds = await self.db.get_all_detail_ids_from_service_junction(serviceIds)
            monad = MaybeMonad(serviceIds)
            monad = await monad.bind(self.db.delete_service_detail_junctions)
            if await self.check(monad) == False:
                return monad
            monad = MaybeMonad(detailIds)
            monad = await monad.bind(self.db.delete_details)
            if await self.check(monad) == False:
                return monad
          
            monad = MaybeMonad(leaseId)
            moand = await monad.bind(self.db.delete_services)
            if await self.check(monad) == False:
               

                return monad
     
            for service in services:
                service.lease_id = leaseId
                monad = MaybeMonad(service)
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad

            await self.db.commit()
            return monad
        
            

    async def update_utilities(self, utilities, leaseId):
        async with self.db.session:
            utilityIds = await self.db.get_all_utility_ids_from_lease_id(leaseId)
            #Get all matching detail ids for from the service detail junction table
            detailIds = await self.db.get_all_detail_ids_from_utility_junction(utilityIds)

            monad = MaybeMonad(utilityIds)
            monad = await monad.bind(self.db.delete_utility_detail_junctions)
            if await self.check(monad) == False:
                return monad
        
            monad = MaybeMonad(detailIds)
            monad = await monad.bind(self.db.delete_details)
            if await self.check(monad) == False:
                return monad

            monad = MaybeMonad(leaseId)
            moand = await monad.bind(self.db.delete_utilities)
            if await self.check(monad) == False:
                return monad
     
            for utility in utilities:
                utility.lease_id = leaseId
                monad = MaybeMonad(utility)
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad

            await self.db.commit()
            return monad

    async def update_rent_discounts(self, rentDiscounts, leaseId):
        async with self.db.session:
            rentDiscountIds = await self.db.get_all_rent_discount_ids_from_lease_id(leaseId)
            #Get all matching detail ids for from the service detail junction table
            detailIds = await self.db.get_all_detail_ids_from_rent_discount_junction(rentDiscountIds)

            monad = MaybeMonad(rentDiscountIds)
            monad = await monad.bind(self.db.delete_rent_discount_detail_junctions)
            if await self.check(monad) == False:
                return monad
        
            monad = MaybeMonad(detailIds)
            monad = await monad.bind(self.db.delete_details)
            if await self.check(monad) == False:
                return monad

            monad = MaybeMonad(leaseId)
            moand = await monad.bind(self.db.delete_rent_discounts)
           
            if await self.check(monad) == False:
                return monad

            for rentDiscount in rentDiscounts:
                rentDiscount.lease_id = leaseId
                monad = MaybeMonad(rentDiscount)
                
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad

            await self.db.commit()
            return monad

    async def update_rent_deposits(self, rentDeposits, leaseId):
        async with self.db.session:
            rentDepositIds = await self.db.get_all_rent_deposit_ids_from_lease_id(leaseId)
            #Get all matching detail ids for from the service detail junction table
            detailIds = await self.db.get_all_detail_ids_from_rent_deposit_junction(rentDepositIds)

            print(rentDepositIds)
            monad = MaybeMonad(rentDepositIds)
            monad = await monad.bind(self.db.delete_rent_deposit_junctions)
            if await self.check(monad) == False:
                return monad
        
            monad = MaybeMonad(detailIds)
            monad = await monad.bind(self.db.delete_details)
            if await self.check(monad) == False:
                return monad

            monad = MaybeMonad(leaseId)
            moand = await monad.bind(self.db.delete_rent_deposits)
           
            if await self.check(monad) == False:
                return monad

            for rentDeposit in rentDeposits:
                rentDeposit.lease_id = leaseId
                monad = MaybeMonad(rentDeposit)
                
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad

            await self.db.commit()
            return monad

    async def update_additional_terms(self, additionalTerms, leaseId):
        async with self.db.session:
            additionalTermIds = await self.db.get_all_additional_term_ids_from_lease_id(leaseId)
            #Get all matching detail ids for from the service detail junction table
            detailIds = await self.db.get_all_detail_ids_from_additional_term_junction(additionalTermIds)

            monad = MaybeMonad(additionalTermIds)
            monad = await monad.bind(self.db.delete_additional_terms_junctions)
            if await self.check(monad) == False:
                return monad
        
            monad = MaybeMonad(detailIds)
            monad = await monad.bind(self.db.delete_details)
            if await self.check(monad) == False:
                return monad

            monad = MaybeMonad(leaseId)
            moand = await monad.bind(self.db.delete_additional_terms)
           
            if await self.check(monad) == False:
                return monad

            for additionalTerm in additionalTerms:
                additionalTerm.lease_id = leaseId
                monad = MaybeMonad(additionalTerm)
                
                moand = await monad.bind(self.db.insert)
                if await self.check(monad) == False:
                    return monad

            await self.db.commit()
            return monad

    async def update_tenant_names(self, tenantNames, lease_id):
        monad = MaybeMonad(lease_id)
        await monad.bind(self.db.delete_tenant_names)
        for tenantName in tenantNames:
            tenantName.lease_id = lease_id
            monad = MaybeMonad(tenantName)
            await monad.bind(self.db.insert)
            if await self.check(monad) == False:
                return monad

        await self.db.commit()
        return monad
