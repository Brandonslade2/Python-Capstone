#HARD RESET OF DATABASE
import os
import json
import model
import server


if __name__ == "__main__":

        #Restart DB
        os.system("dropdb -U postgres jslmt")
        #Create DB
        os.system("createdb -U postgres jslmt")

        #Connect to DB
        model.connect_to_db(server.app)
        model.db.create_all()

        #Administrator Username and Password
        # username = "jslmt"
        # email = "brandonslade2@gmail.com"
        # password_hash = "032498"

        ##Load initial data##

        #Create and add first user
        # user = model.create_first_user(username, email, password_hash)
        # model.db.session.add(user)
        # model.db.session.commit()

        #homepage#
        with open("data/homepage.json") as f:
            homepage_data = json.loads(f.read())

        homepage_in_db = []
        for i in homepage_data:
            content = i["content"]
            db_homepage = model.create_homepage(content)
            homepage_in_db.append(db_homepage)


        #services#
        with open("data/services.json") as f:
            services_data = json.loads(f.read())

        services_in_db = []
        for service in services_data:
            service_name, service_description = (
                service["service_name"],
                service["service_description"],
            )

            db_service = model.create_service(service_name, service_description)
            services_in_db.append(db_service)
        
        #pricing#
        with open("data/pricing.json") as f:
            pricing_data = json.loads(f.read())

        pricing_in_db = []
        for pricing in pricing_data:
            pricing_name, pricing_location, pricing_duration, pricing_price = (
                pricing["pricing_name"],
                pricing["pricing_location"],
                pricing["pricing_duration"],
                pricing["pricing_price"],
            )

            db_pricing = model.create_pricing(pricing_name, pricing_location, pricing_duration, pricing_price)
            pricing_in_db.append(db_pricing)

        #enhancements#
        with open("data/enhancements.json") as f:
            enhancements_data = json.loads(f.read())

        enhancements_in_db = []
        for enhancement in enhancements_data:
            enhancement_name, enhancement_price, enhancement_description = (
                enhancement["enhancement_name"],
                enhancement["enhancement_price"],
                enhancement["enhancement_description"],
            )

            db_enhancement = model.create_enhancement(enhancement_name, enhancement_price, enhancement_description)
            enhancements_in_db.append(db_enhancement)

        #clients#
        with open("data/clients.json") as f:
            clients_data = json.loads(f.read())

        clients_in_db = []
        for client in clients_data:
            client_name, client_address, client_phonenumber = (
                client["client_name"],
                client["client_address"],
                client["client_phonenumber"],
            )

            db_client = model.create_client(client_name, client_address, client_phonenumber)
            clients_in_db.append(db_client)

        model.db.session.add_all(homepage_in_db)
        model.db.session.add_all(clients_in_db)
        model.db.session.add_all(enhancements_in_db)
        model.db.session.add_all(pricing_in_db)
        model.db.session.add_all(services_in_db)
        model.db.session.commit()

        #history#
        client_name = model.Client.query.filter_by(client_name="Darth Vader").first().client_name
        service_name = model.Service.query.filter_by(service_name="Deep Tissue").first().service_name
        pricing_name = model.Pricing.query.filter_by(pricing_price="90").first().pricing_name
        enhancement_name = model.Enhancement.query.filter_by(enhancement_name="Headache Treatment").first().enhancement_name
        new_history_entry = model.History(
            client_name=client_name,
            service_name=service_name,
            pricing_name=pricing_name,
            enhancement_name=enhancement_name,
            history_date="03-24-2023",
            history_total_price=105.0
        )
        model.db.session.add(new_history_entry)
        model.db.session.commit()