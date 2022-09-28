"""
Unir la info de Paises join places

"""

from curses import echo
from os import pread


class Software:
    def __init__(self) -> None:
        self.host_country_ids = {}
        self.all_countries_info = {}
        self.all_places_peru = []
        self.all_places_chile = []
        self.all_places_colombia = []
        self.all_places_ecuador = []
        self.all_places_españa = []
        self.all_places_mexico = []
        self.all_places_otros = {}
        self.all_places_otros_metadata = [] # Save a name of country
        self.all_places_otros_metadata_control = {} # The program save a places_otros in final data?
        self.all_countries_metadata_control = {}
        self.general_reg_counter = 0
        self.headers = ""
        self.nullable_data = "NULL|NULL|NULL|NULL|NULL|NULL|NULL|NULL|NULL|NULL|NULL|"
        self.outputDATA = [] # Save the final data
        self.chargeHeaders()
        self.chargeCountriesHostInfo()
        self.chargeAllDestinations()
        self.exportData()
        

    def chargeHeaders(self):
        try:
            f = open('DATA/headers.txt', 'r', encoding="UTF-8")
            
            for i in f.read().split("\n"):
                if str(i).strip() != "":
                    self.headers = self.headers + i + "|"
            f.close()
            print("Cargado... los headers")
        except:
            print("Error cargando los headers")


    def chargeCountriesHostInfo(self):
        try:
            f = open('DATA/paises_host.txt', 'r', encoding="UTF-8")
            for i in f.read().split("\n"):
                if str(i).strip() != "":
                    data = i.split("|")
                    id_host = data[1]
                    name_host = str(data[3]).lower()
                    self.host_country_ids[id_host] = name_host

            f.close()

            print("Cargado los host id de los paises")
            #print(self.host_country_ids)
        except:
            print("Error al optener la infor de countries host")

    def chargeAllDestinations(self):
        try:
            f = open('DATA/todosLosPaisesAPI.txt', 'r', encoding="UTF-8")
            for i in f.read().split("\n"):
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    #id_data = data.split("|")[0]
                    name = data.split("|")[-2]
                    self.all_countries_info[name] = data
                    self.all_countries_metadata_control[name] = 0

             #for i in self.all_countries_info:
            #    print(self.all_countries_info[i])


            print("Se cargo toda la info de paises")
        except:
            print("Error La data de todos los paises")

        try:
            f = open('DATA/places_peru.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    self.all_places_peru.append(data)
                    
            print("En Peru se cargaron: ", len(self.all_places_peru), " Sitios. ")
        except:
            print("Error cargando el informe... peru")

        try:
            f = open('DATA/places_chile.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    self.all_places_chile.append(data)
                    
            print("En chile se cargaron: ", len(self.all_places_chile), " Sitios. ")
        except:
            print("Error cargando el informe... Chile")

        try:
            f = open('DATA/places_colombia.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    self.all_places_colombia.append(data)
                    
            print("En colombia se cargaron: ", len(self.all_places_colombia), " Sitios. ")
        except:
            print("Error cargando el informe... colombia")

        try:
            f = open('DATA/places_ecuador.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    self.all_places_ecuador.append(data)
                    
            print("En ecuador se cargando: ", len(self.all_places_ecuador), " Sitios. ")
        except:
            print("Error cargando el informe... ecuador")

        try:
            f = open('DATA/places_españa.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    self.all_places_españa.append(data)
                    
            print("En españa se cargando: ", len(self.all_places_españa), " Sitios. ")
        except:
            print("Error cargando el informe... España")


        try:
            f = open('DATA/places_mexico.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    self.all_places_mexico.append(data)
                    
            print("En mexico se cargando: ", len(self.all_places_mexico), " Sitios. ")
        except:
            print("Error cargando el informe... Mexico")

        try:
            f = open('DATA/places_otros.csv', 'r', encoding="UTF-8")
            for i in f.read().split("\n")[1:-1]:
                if str(i).strip() != "":
                    data = self.trimLINE(i)
                    # Get country
                    country_host_id = data.split("|")[-3]
                    name_country = self.host_country_ids[country_host_id]

                    if name_country not in self.all_places_otros_metadata:
                        self.all_places_otros_metadata.append(name_country)
                        self.all_places_otros_metadata_control[name_country] = 0

                    try:
                        if not name_country in self.all_places_otros.keys():
                            self.all_places_otros[name_country] = []

                        self.all_places_otros[name_country].append(data)
                    except:
                        print("Error Fatal creando el registro...")
                        print(data)
                    
                
            for i in self.all_places_otros:
                print("En ", i, " se han cargado ", len(self.all_places_otros[i]), " Sitios ")
            
        except:
            print("Error cargando el informe... Otros")


    def exportData(self):
        print("Exportando el Excel...")

        for i in self.all_countries_info:

            if str(i).lower() == 'perú':
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_peru:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                    

                print("Creando info de peru... TOTAL INSETR: ", str(contador))


            if str(i).lower() == 'chile':
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_chile:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                    

                print("Creando info de chile... TOTAL INSETR: ", str(contador))


            if str(i).lower() == 'colombia':
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_colombia:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                    

                print("Creando info de colombia... TOTAL INSETR: ", str(contador))
            
            if str(i).lower() == 'ecuador':
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_ecuador:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                    

                print("Creando info de ecuador... TOTAL INSETR: ", str(contador))

            if str(i).lower() == 'españa':
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_españa:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                    

                print("Creando info de españa... TOTAL INSETR: ", str(contador))


            if str(i).lower() == 'mexico':
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_mexico:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                

                print("Creando info de mexico... TOTAL INSETR: ", str(contador))


            if str(i).lower() in self.all_places_otros_metadata: 
                self.all_places_otros_metadata_control[str(i).lower()] = 1
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_otros[str(i).lower()]:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1
                    

                print("Creando info de " + str(i).lower() + "... TOTAL INSETR: ", str(contador))

            if str(i).lower() == 'sudáfrica':
                self.all_places_otros_metadata_control['sudafrica'] = 1
                self.all_countries_metadata_control[i] = 1
                contador = 0
                for j in self.all_places_otros['sudafrica']:
                    self.outputDATA.append(self.all_countries_info[i]+j)
                    contador = contador + 1
                    self.general_reg_counter = self.general_reg_counter  +  1

                print("Creando info de " + str(i).lower() + "... TOTAL INSETR: ", str(contador))
                

            if self.all_countries_metadata_control[i] == 0:
                self.all_countries_metadata_control[i] = 1
                self.general_reg_counter = self.general_reg_counter  +  1
                self.outputDATA.append(self.all_countries_info[i]+self.nullable_data)


        self.generateEXCEL()
        print("Fin del programa... ")
        print("Total de registros insertados..", self.general_reg_counter)
        print("Estado general de insertado por pais")
        for i in self.all_countries_metadata_control:
            print(i, " Status:  "+str(self.all_countries_metadata_control[i]))
        print("Estado de la estructura de control server otros paises: ")
        print(self.all_places_otros_metadata_control)
        

    def generateEXCEL(self):
        try:
            txt = ""
            for i in self.outputDATA:
                txt = txt + str(i) + "\n"
            f = open('OUTPUT/destinos_turismoi.csv', 'w', encoding="UTF-8")
            f.write(self.headers+"\n"+txt)
            f.close()
        except:
            print("Error creando el Excel......")


    def trimLINE(self, x):
        data = x.split("|")
        clean_data = "" 
        for i in data:
            clean_data = clean_data + str(i).rstrip().lstrip() + "|"

        return clean_data


s = Software()
