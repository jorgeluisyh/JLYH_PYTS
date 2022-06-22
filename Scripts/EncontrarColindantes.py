# -*- coding: utf-8 -*-

# Importamos librerías
import arcpy
import pandas as pd

def encontrar_colindantes(capa, field_id, field_desc):
	"""
	Funcion para encontrar los colindantes a una capa
	params:
	capa: capa sobre la cual encontraremos sus colindantes
	field_id : campo identificador
	field_desc: campo que mostrara el nombre como etiqueta
	"""

	
	# Definimos lista vacía para almacenar el distrito y sus colindantes
	lista = []
	campos = ["shape@", field_id, field_desc, "CD_DEPA"]
	query = "{} = '06'".format("CD_DEPA")

	# Usamos un cursor para recorrer información de la capa
	with arcpy.da.SearchCursor(capa,campos,query) as cursor:
		for row in cursor:
			geom_ev = row[0]
			id_ev = row[1]
			name_ev = row[2]
			with arcpy.da.SearchCursor(capa, campos, query) as cursor2:
				for i in cursor2:
					if i[1] != id_ev:
						if not i[0].disjoint(geom_ev):
							if i[0].touches(geom_ev):
								lista.append([id_ev, name_ev, i[1], i[2]])

	return lista

def lista_a_csv(lista, ruta_csv):
	"""
	Exportar lista generada de colindantes a un archivo csv
	"""
	df = pd.DataFrame(lista, columns=["ID", "NOMBRE", "ID_COLINDANTE", "NOMBRE_COLINDANTE"])
	df.to_csv(ruta_csv, encoding='utf-8-sig')



if __name__ == '__main__':
	p_capa = arcpy.GetParameterAsText(0)
	p_campo_id = arcpy.GetParameterAsText(1)
	p_campo_desc = arcpy.GetParameterAsText(2)
	p_ruta_csv = arcpy.GetParameterAsText(3)
	lista = encontrar_colindantes(p_capa, p_campo_id, p_campo_desc)
	lista_a_csv(lista, p_ruta_csv)