from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import jlrpy
import math
import os
import requests

# Authenticate using the username and password
c = jlrpy.Connection('agarrido@agarquitectura.es', 'Quilla2502Quilla')
v = c.vehicles[0]

class Ui(ScreenManager):
	pass

class JaguarControlRemotoApp(MDApp):
	def build (self):
		self.theme_cls.theme_style ="Dark"
		self.theme_cls.primary_palette="Teal"
		Builder.load_file("design.kv")
		return Ui()

	def change_style(self,checked,value):
		if value:
			self.theme_cls.theme_style="Dark"
		else: 
			self.theme_cls.theme_style="Light"

	def on_start(self):

		def obtener_valor_estad(estad, clave, valor_predeterminado="No puedo localizar el dato"):
			core_status = estad.get("vehicleStatus", {}).get("coreStatus", [])

			for status_entry in core_status:
				if status_entry.get("key") == clave:
					return status_entry.get("value")

			return valor_predeterminado

	
		# LEE SERVICIOS ACTIVOS DEL VEHICULO
		atributos= v.get_attributes()
		#print("Paso 1")

		# LEE ESTADO DEL VEHICULO
		estado= v.get_health_status()
		#print("Paso 2")
		
		# LEE INFORMACION DEL USUARIO
		usuario=c.get_user_info()
		print("Paso 3: ", usuario)
		
		# LEE POSICION DEL VEHICULO
		posicion = v.get_position()
		#print("Paso 4")
		
		# LEE ESTADO DEL VEHICULO
		estad = v.get_status()
		#print("Paso 5")

		
		Reserva_fuel = obtener_valor_estad(estad, "DISTANCE_TO_EMPTY_FUEL")
		self.root.ids.reserva_fuel_resp.text=str(Reserva_fuel)+" Km."

		
		KM_cambio = obtener_valor_estad(estad, "EXT_KILOMETERS_TO_SERVICE")
		self.root.ids.km_cambio_resp.text=str(KM_cambio)+" Km."

		KM_add_blue = obtener_valor_estad(estad, "EXT_EXHAUST_FLUID_DISTANCE_TO_SERVICE_KM")		
		self.root.ids.km_add_blue_resp.text=str(KM_add_blue)+" Km."

		KM_totales = obtener_valor_estad(estad, "ODOMETER_METER")		
		self.root.ids.km_totales_resp.text=str(int (KM_totales)/1000)+" Km."


		#estado_motor=v.get_status("ENGINE_BLOCK")
		estado_motor = obtener_valor_estad(estad, "ENGINE_BLOCK")		
		self.root.ids.estado_motor_resp.text=str(estado_motor)


		#voltaje_bateria=v.get_status("BATTERY_VOLTAGE")
		voltaje_bateria = obtener_valor_estad(estad, "BATTERY_VOLTAGE")		
		self.root.ids.voltaje_bateria_resp.text=str(voltaje_bateria)+" Volt"


		temp_motor = obtener_valor_estad(estad, "ENGINE_COOLANT_TEMP")	
		temp_motor = str(round((int (temp_motor)-32)*(5/9),2)) 	
		self.root.ids.temp_motor_resp.text=str(temp_motor)+" ºC"

		liquido_limpia = obtener_valor_estad(estad, "WASHER_FLUID_WARN")		
		self.root.ids.liquido_limpia_resp.text=str(liquido_limpia)+" "

		liquido_frenos = obtener_valor_estad(estad, "BRAKE_FLUID_WARN")		
		self.root.ids.liquido_frenos_resp.text=str(liquido_frenos)+" "


		#pres_rued_del_izq=v.get_status("TYRE_PRESSURE_FRONT_LEFT")
		pres_rued_del_izq = obtener_valor_estad(estad, "TYRE_PRESSURE_FRONT_LEFT")		
		self.root.ids.pres_rued_del_izq_resp.text=str(int(pres_rued_del_izq)/100)+" bar"
		#pres_rued_del_der=v.get_status("TYRE_PRESSURE_FRONT_RIGHT")
		pres_rued_del_der = obtener_valor_estad(estad, "TYRE_PRESSURE_FRONT_RIGHT")	
		self.root.ids.pres_rued_del_der_resp.text=str(int(pres_rued_del_der)/100)+" bar"
		#pres_rued_tra_izq=v.get_status("TYRE_PRESSURE_REAR_LEFT")
		pres_rued_tra_izq = obtener_valor_estad(estad, "TYRE_PRESSURE_REAR_LEFT")	
		self.root.ids.pres_rued_tra_izq_resp.text=str(int(pres_rued_tra_izq)/100)+" bar"
		#pres_rued_tra_dec=v.get_status("TYRE_PRESSURE_REAR_RIGHT")
		pres_rued_tra_dec = obtener_valor_estad(estad, "TYRE_PRESSURE_REAR_LEFT")	
		self.root.ids.pres_rued_tra_dec_resp.text=str(int(pres_rued_tra_dec)/100)+" bar"



		#est_rued_del_izq=v.get_status("TYRE_STATUS_REAR_LEFT")
		est_rued_del_izq = obtener_valor_estad(estad, "TYRE_STATUS_REAR_LEFT")	
		self.root.ids.est_rued_del_izq_resp.text=str(est_rued_del_izq)
		#est_rued_del_der=v.get_status("TYRE_STATUS_FRONT_RIGHT")
		est_rued_del_der = obtener_valor_estad(estad, "TYRE_STATUS_REAR_RIGHT")	
		self.root.ids.est_rued_del_der_resp.text=str(est_rued_del_der)
		#est_rued_tra_izq=v.get_status("TYRE_STATUS_REAR_LEFT")
		est_rued_tra_izq = obtener_valor_estad(estad, "TYRE_STATUS_REAR_LEFT")	
		self.root.ids.est_rued_tra_izq_resp.text=str(est_rued_tra_izq)
		#est_rued_tra_dec=v.get_status("TYRE_STATUS_REAR_RIGHT")
		est_rued_tra_dec = obtener_valor_estad(estad, "TYRE_STATUS_REAR_RIGHT")	
		self.root.ids.est_rued_tra_dec_resp.text=str(est_rued_tra_dec)




		#Nº matricula

		numero_matricula = atributos.get('registrationNumber',"matricula no encontrada")
		#numero_matricula = obtener_valor_atributos(atributos, "registrationNumber")
		self.root.ids.matricula_vehiculo_resp.text=str(numero_matricula)

		#MArca del coche
		fabricante_vehiculo=atributos.get("vehicleBrand","Fabricante no encontrado")
		#print ("Fabricante vehículo: ",fabricante_vehiculo)
		#Modelo del coche
		Modelo_vehiculo=atributos.get('vehicleType',"Modelo no encontrado")
		#print("Modelo del vehículo: ",Modelo_vehiculo)
		#Codigo de motor
		Codigo_motor=atributos.get('engineCode',"Codigo motor no encontrado")
		#print("Código de motor: ",Codigo_motor)
		#Combustible vehiculo
		Combustible_vehiculo=atributos.get("fuelType", "Combustible no determinado")
		#print("Combustible vehículo: ",Combustible_vehiculo)

		Designacion_vehiculo=fabricante_vehiculo+" "+Modelo_vehiculo+" "+Codigo_motor+" "+Combustible_vehiculo
		self.root.ids.designacion_vehiculo_resp.text=str(Designacion_vehiculo)
		print("Designacion vehiculo: ",Designacion_vehiculo)

		#Identificador del vehiculo
		numero_bastidor=estado.get('vehicleId',"Nº Bastidor vehiculo no encontrado")
		self.root.ids.bastidor_vehiculo_resp.text=str(numero_bastidor)
		#print ("Nº BASTIDOR VEHICULO: ",numero_bastidor)

		#Otros datos del coche

		color_ext=atributos.get("exteriorColorName", "Color no encontrado")
		self.root.ids.color_vehiculo_resp.text=str(color_ext)
		print ("COLOR VEHICULO EXT: ",color_ext)

		color_int=atributos.get("interiorColorName", "Color no encontrado")
		#self.root.ids.color_vehiculo_int_resp.text=str(color_int)
		print ("COLOR VEHICULO INT: ",color_int)

		ano_modelo=atributos.get('modelYear',"Año de construcción no encontrado")
		self.root.ids.ano_modelo_vehiculo_resp.text=str(ano_modelo)
		print ("AÑO MODELO: ",ano_modelo)


		codigo_coche=atributos.get('vehicleTypeCode',"Código vehículo no encontrado")
		self.root.ids.codigo_coche_resp.text=str(codigo_coche)


		# AQUI FALLO DE LA LIBRERIA CON EL CAMBIO DE VERSION

		#ID del usuario
		ID_usuario=usuario.get("userId","ID usuario no encontrado")
		#self.root.ids.nombre_usuario_resp.text=str(ID_usuario)
		#print ("id USUARIO: ",ID_usuario)

		#Nombre del usuario
		#Nombre_usuario=usuario["contact"]["firstName"]
		#print ("Nombre del usuario: ",Nombre_usuario)

		#Apellidos usuario
		#Apellidos_usuario=usuario["contact"]["lastName"]
		#print ("Nombre del usuario: ",Apellidos_usuario)

		#Nombre Completo usuario
		#Nombre_completo_usuario=Nombre_usuario+Apellidos_usuario
		#self.root.ids.nombre_usuario_resp.text=str(Nombre_completo_usuario)
		#print ("Nombre completo del usuario: ",Nombre_completo_usuario)

		#Correo usuario
		#Correo_usuario=usuario["contact"]["emailAddress"]
		#self.root.ids.correo_usuario_resp.text=str(Correo_usuario)
		#print("Correo del usuario: ",Correo_usuario)



		#DAtos de localización coche:
		#position = (p['position']['latitude'], p['position']['longitude'])

		latitud = (posicion['position']['latitude'])
		longitud = (posicion['position']['longitude'])
		velocidad = (posicion['position']['speed'])
		marcatiempo = (posicion['position']['timestamp'])
		heading=(posicion["position"]["heading"])
		positionQaulity=(posicion["position"]["positionQuality"])
		CalculatedPosition=(posicion["calculatedPosition"])

		#Seguridad del coche:

		#puertas_cerradas= v.get_status("DOOR_IS_ALL_DOORS_LOCKED")
		puertas_cerradas = obtener_valor_estad(estad, "DOOR_IS_ALL_DOORS_LOCKED")	
		self.root.ids.puertas_cerradas_resp.text=str(puertas_cerradas)
		
		#puerta_del_izq=v.get_status("DOOR_FRONT_LEFT_POSITION")
		puerta_del_izq = obtener_valor_estad(estad, "DOOR_FRONT_LEFT_POSITION")	
		self.root.ids.puerta_del_izq_resp.text=str(puerta_del_izq)
		#bloqueo_puert_del_izq=v.get_status("DOOR_FRONT_LEFT_LOCK_STATUS")
		bloqueo_puert_del_izq = obtener_valor_estad(estad, "DOOR_FRONT_LEFT_LOCK_STATUS")
		self.root.ids.bloqueo_puert_del_izq_resp.text=str(bloqueo_puert_del_izq)

		#puerta_del_dec=v.get_status("DOOR_FRONT_RIGHT_POSITION")
		puerta_del_dec = obtener_valor_estad(estad, "DOOR_FRONT_RIGHT_POSITION")	
		self.root.ids.puerta_del_dec_resp.text=str(puerta_del_dec)
		#bloqueo_puert_del_dec=v.get_status("DOOR_FRONT_RIGHT_LOCK_STATUS")
		bloqueo_puert_del_dec = obtener_valor_estad(estad, "DOOR_FRONT_RIGHT_LOCK_STATUS")	
		self.root.ids.bloqueo_puert_del_dec_resp.text=str(bloqueo_puert_del_dec)	

		#puerta_tra_izq=v.get_status("DOOR_REAR_LEFT_POSITION")
		puerta_tra_izq = obtener_valor_estad(estad, "DOOR_REAR_LEFT_POSITION")	
		self.root.ids.puerta_tra_izq_resp.text=str(puerta_tra_izq)
		#bloqueo_puert_tra_izq=v.get_status("DOOR_REAR_LEFT_LOCK_STATUS")
		bloqueo_puert_tra_izq = obtener_valor_estad(estad, "DOOR_REAR_LEFT_LOCK_STATUS")	
		self.root.ids.bloqueo_puert_tra_izq_resp.text=str(bloqueo_puert_tra_izq)	

		#puerta_tra_dec=v.get_status("DOOR_REAR_RIGHT_POSITION")
		puerta_tra_dec = obtener_valor_estad(estad, "DOOR_REAR_RIGHT_POSITION")
		self.root.ids.puerta_tra_dec_resp.text=str(puerta_tra_dec)
		#bloqueo_puert_tra_dec=v.get_status("DOOR_REAR_RIGHT_LOCK_STATUS")
		bloqueo_puert_tra_dec = obtener_valor_estad(estad, "DOOR_REAR_RIGHT_LOCK_STATUS")
		self.root.ids.bloqueo_puert_tra_dec_resp.text=str(bloqueo_puert_tra_dec)

		#capo=v.get_status("DOOR_ENGINE_HOOD_POSITION")
		capo = obtener_valor_estad(estad, "DOOR_ENGINE_HOOD_POSITION")
		self.root.ids.capo_resp.text=str(capo)
		#bloqueo_capo=v.get_status("DOOR_ENGINE_HOOD_LOCK_STATUS")
		bloqueo_capo = obtener_valor_estad(estad, "DOOR_ENGINE_HOOD_LOCK_STATUS")
		self.root.ids.bloqueo_capo_resp.text=str(bloqueo_capo)

	
		#maletero=v.get_status("DOOR_ENGINE_HOOD_POSITION")
		maletero = obtener_valor_estad(estad, "DOOR_BOOT_POSITION")
		self.root.ids.maletero_resp.text=str(maletero)
		#bloqueo_maletero=v.get_status("DOOR_ENGINE_HOOD_LOCK_STATUS")
		bloqueo_maletero = obtener_valor_estad(estad, "DOOR_BOOT_LOCK_STATUS")
		self.root.ids.bloqueo_maletero_resp.text=str(bloqueo_maletero)



		self.root.ids.latitud_resp.text=str(latitud)
		self.root.ids.longitud_resp.text=str(longitud)
		self.root.ids.velocidad_resp.text=str(velocidad)+" KM/h"


	def obtener_imagen_google(self):

		print("Aqui vendria lo de obtener la imagen")

		pass

		


if __name__ == '__main__':
	JaguarControlRemotoApp().run()

 