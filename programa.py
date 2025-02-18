import pandas as pd
import streamlit as st
import base64
import csv
from fractions import Fraction

st.session_state.diametro=0
codvalde = ""
codlimits= ""
codilimits = ""
codcilde = ""
codicil = ""
convertido = float
valor = ""
st.session_state.min = 0
st.session_state.max = 0
st.session_state.cil = 0 
codposi = ""
st.session_state.presion = float
st.session_state.diam = float
v = 1
codigocil = ""
cuaddosvias = ""
dosvias = ""
flag = 0
check = False
codicilde = ""
codicilse = ""


def cargar_base_datos(ruta):
    datos = []
    with open(ruta, newline='', encoding='Latin-1') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter= ";")  
        for fila in lector:
            datos.append(fila)  
    return datos

lista_base_de_datos = cargar_base_datos("basedatos.csv")
esferica_tres = cargar_base_datos("3vias.csv")
cilindros = cargar_base_datos("codigoscilindros2.csv")
limit = cargar_base_datos("limits.csv")
posicionadores = cargar_base_datos("posicionadores1.csv")
esferica_dos = cargar_base_datos("bola1.csv")
bobinas = cargar_base_datos("bobinas.csv")
simpleefecto = cargar_base_datos("simpleefecto.csv")

st.set_page_config(page_title="Automatización de Válvulas")

def fondo_de_pantalla():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{get_image_as_base64('fondo.jpg')}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_image_as_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

fondo_de_pantalla()
    
st.markdown(
    """
    <style>
   {
        color: white !important; 
    }

  
    .stTextInput, .stSelectbox, .stNumberInput, .stRadio {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



if "seleccion" not in st.session_state:
    st.session_state.seleccion = "Seleccion de válvula MiCRO"


st.session_state.seleccion = st.sidebar.radio("Automatización de procesos",("Selección de válvula MiCRO", "Automatización de válvula existente"),index=0)

if 'seleccion' not in st.session_state:
    st.session_state.seleccion = 'expanded'

if st.session_state.seleccion == "Selección de válvula MiCRO":

    st.title("Selección de válvula MiCRO")

    tab1, tab2, tab3, tab4 = st. tabs(["Instalación", "Válvula de control", "Accesorios de posición", "Equipo seleccionado"])

    with tab1: 

        actuador = st.radio("¿Qué tipo de actuador necesita en su instalación?", ["Simple efecto", "Doble efecto"])        
        control = st.radio("¿Qué tipo de control desea tener?", ["On/Off", "Proporcional"])
            
        val = st.radio("¿Qué tipo de válvula desea usar?", ["Esférica de dos vías", "Esférica de tres vías", "Mariposa"])
        if val == "Esférica de dos vías":
                tam = st.selectbox("¿De qué tamaño es la tubería de su instalación? (pulg.)" ,["1/4", "3/8", "1/2", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "4"])    
        if val == "Esférica de tres vías": 
                tam = st.selectbox("¿De qué tamaño es la tubería de su instalación? (pulg.)" , ["1/2", "3/4", "1", "1 1/4", "1 1/2", "2"] )
        if val == "Mariposa": 
                tam = st.selectbox("¿De qué tamaño es la tubería de su instalación? (pulg.)" , ["aaaaa"] )
        
        opcion = {f"{i} bar" : i for i in range(2,9)}

        seleccion_visual = st.selectbox("¿Con qué presión cuenta su instalalción?", list(opcion.keys()))

        pres = str(opcion[seleccion_visual])
            
    with tab2: 

        valvula = st.radio("¿Desea seleccionar una válvula de control?", ["Externa", "En el actuador", "No"])
        tension= st.selectbox("¿Con qué tensión alimentará dicha valvula?", ["220 V 50/60Hz", "110V 50/60Hz","48V 50/60Hz", "24V 50/60Hz", "24 Vcc", "12 Vcc"], disabled= valvula == "No")

        if val == "Esférica de dos vías": 

            if actuador == "Doble efecto": 

                for i in range(len(esferica_dos)):
                    if esferica_dos[i][1] == tam: 
                        st.session_state.torquebola =float(esferica_dos[i][2])
                        dosvias = (f"El código de la válvula esférica es {esferica_dos[i][0]}")
                        cuaddosvias = esferica_dos[i][3]
                        break
            
                for i in range (1,18):
                    if  cuaddosvias == lista_base_de_datos[i][8]:
                        st.session_state.cuad = i     
                        for i in range (1,8):     
                            if lista_base_de_datos[0][i] == pres:
                                st.session_state.presion = i 
                                for i in range(1,19):
                                    if float(lista_base_de_datos[st.session_state.cuad][st.session_state.presion]) > ((st.session_state.torquebola)*1.15): 
                                        st.session_state.diametro = lista_base_de_datos[st.session_state.cuad][0]
                                        check = True
                                        break
                            if check:
                                break
                    if check:
                        break            
                
                if check: 
                    for i in range(18): 
                        if cilindros[i][0] == st.session_state.diametro:
                            codcilde = (f"El actuador a utilizar tiene código {cilindros[i][2]}")
                            break
                else: 
                    codcilde= ("No hay actuadores que cumplan con las condiciones establecidas.")
                    

            if actuador == "Simple efecto": 

                for i in range(len(esferica_dos)):

                    if esferica_dos[i][1] == tam: 
                        st.session_state.torquebola = float(esferica_dos[i][2])
                        
                        dosvias = (f"El código de la válvula esférica es {esferica_dos[i][0]}")
                        cuaddosvias = esferica_dos[i][3]
            
                for i in range (2,19):
                    if  cuaddosvias == simpleefecto[i][12]:
                        st.session_state.cuad = i      
                        for i in range(2,19):
                                    if float(simpleefecto[st.session_state.cuad][10]) >= (st.session_state.torquebola)* 1.15: 
                                        st.session_state.diametro = simpleefecto[i][0]
                                        check = True
                                        break
                    if check:
                        break
    
                if check: 
                    for i in range(18): 
                        if cilindros[i][0] == st.session_state.diametro: 
                            codcilse = (f"El actuador a utilizar tiene código {cilindros[i][2]}")
                            break
                else: 
                    codcilse= ("No hay actuadores que cumplan con las condiciones establecidas.")
        
        if val == "Esférica de tres vías": 

            if actuador == "Doble efecto": 

                for i in range(len(esferica_tres)): 
                    if esferica_tres[i][1] == tam: 
                        st.session_state.torquetres = esferica_tres[i][2]
                        tresvias = (f"El código de la válvula es {esferica_tres[i][0]}")
                        cuadtresvias = esferica_tres[i][3]
                        
                for i in range (1,18):
                    if  cuadtresvias == lista_base_de_datos[i][8]:
                        st.session_state.cuad = i     
                    for i in range(1,8): 
                        if lista_base_de_datos[0][i] == pres: 
                            st.session_state.presio = i
                            for i in range(1,18): 
                                if float(lista_base_de_datos[st.session_state.cuad][st.session_state.presio]) >= float(st.session_state.torquetres): 
                                    st.session_state.diametro = lista_base_de_datos[i][0]
                                    check = True
                                    break
                        if check: 
                            break
                    if check: 
                        break
                    
            if check:     
                for i in range(1,18): 
                    if st.session_state.diametro == cilindros[i][0]: 
                        codigocil = (f"El actuador a utilizar tiene código {cilindros[i][2]}")
                        break 
            else: 
                    codcilse= ("No hay actuadores que cumplan con las condiciones establecidas.")


            if actuador == "Simple efecto":
                for i in range(len(esferica_tres)):

                    if esferica_tres[i][1] == tam: 
                        st.session_state.torquebola = esferica_tres[i][2]
                        tresvias = (f"El código de la válvula esférica es {esferica_tres[i][0]}")
                        cuadtresvias = esferica_tres[i][3]
            
                for i in range (2,19):
                    if  cuadtresvias == simpleefecto[i][12]:
                        st.session_state.cuad = i      
                        for i in range(2,19):
                                    if float(simpleefecto[st.session_state.cuad][10]) >= float((st.session_state.torquebola)* 1.15): 
                                        st.session_state.diametro = simpleefecto[i][0]
                                        check = True
                                        break
                    if check:
                        break
    
                if check: 
                    for i in range(18): 
                        if cilindros[i][0] == st.session_state.diametro: 
                            codcilse = (f"El actuador a utilizar tiene código {cilindros[i][1]}")
                            break
                else: 
                    codcilse= ("No hay actuadores que cumplan con las condiciones establecidas.") 

        def codigo_bobina(bobinas_l, tension):
            for i in range(len(bobinas_l)): 
                if bobinas_l[i][0] == tension: 
                    return bobinas_l[i][1]
            
        if valvula == "En el actuador" and actuador == "Doble efecto": 
 
            codvalde = (f"La válvula de control a utilizar tiene código 0.221.012.522/{codigo_bobina(bobinas, tension)}")
                           
        if valvula == "Externa" and actuador == "Doble efecto": 

            for i in range(1,19): 
                if lista_base_de_datos[i][0] == st.session_state.diametro: 
                    conexion = lista_base_de_datos[i][9]
                    break 
            
            if conexion == "1/8": 
                codval = ("0.224.002.711")
            if conexion == "1/4": 
                codval = ("0.220.002.722")
            if conexion in ("3/8", "1/2", "3/4"): 
                codval = ("0.259.002.744")

            codvalde = (f"La válvula de control a usar tiene código {codval}/{codigo_bobina(bobinas, tension)}")

        if valvula == "En el actuador " and actuador == "Simple efecto": 

            if valvula == "Externa" and actuador == "Simple efecto": 

                for i in range(1,19): 
                    if lista_base_de_datos[i][0] == st.session_state.diametro: 
                        conexion = lista_base_de_datos[i][9]
                        break 
                
                if conexion == "1/8": 
                    codval = ("0.224.002.511")
                if conexion == "1/4": 
                    codval = ("0.220.002.522")
                if conexion in ("3/8", "1/2", "3/4"): 
                    codval = ("0.259.002.544")

                codvalse = (f"La valvula de control a usar tiene código {codval}/{codigo_bobina(bobinas, tension)}")

    with tab3: 

# , disabled=st.session_state.diametro == 0 and control == "Proporcional"

        limits = st.radio("¿Desea colocar una caja Limit Switch?", ["Sí", "No"], index=1, disabled=st.session_state.diametro == 0 and control == "Proporcional")
        

        if limits == "Sí": 

            if float(st.session_state.diametro) < 125:
                
                codlimits = "0.900.009.103/210"
            if str(st.session_state.diametro) >= "140" and st.session_state.diametro <= "250": 
                codlimits = "0.900.009.103/310"
            if str(st.session_state.diametro) >= "300" and st.session_state.diametro <= "400": 
                codlimits = "0.900.009.103/310"
            
        codilimits = (f"La caja Limit Switch a utilizar tiene código {codlimits}")

#  disabled=st.session_state.diametro == 0 and control == "On/Off",

        posi = st.radio("¿Desea colocar un posicionador?", ["Sí", "No"], index=1, disabled=st.session_state.diametro == 0 and control == "On/Off")

        if posi == "Sí": 
            func = st.selectbox("¿Cómo quiere que sea el funcionamiento del posicionador?", ["Electroneumático", "Neumático"])

            for i in range(3):
                if posicionadores[i][3] == func: 
                            codposi = (f"El código del posicionador a utilizar es {posicionadores[i][1]}")
                            break
            
    
    with tab4: 

        if actuador == "Doble efecto": 
            if val == "Esférica de dos vías":  
                st.write(dosvias)
                st.write(codcilde)
            if val == "Esférica de tres vías":
                            st.write(codigocil)
                            st.write(tresvias)
        elif actuador == "Simple efecto": 
            if val == "Esférica de dos vías": 
                  st.write(dosvias)
                  st.write(codcilse)
            elif val == "Esférica de tres vías": 
                 st.write(tresvias)
                 st.write(codcilse)
            
        if valvula != "No": 
            st.write(codvalde)
        if limits == "Sí":
            st.write(codilimits)
        if posi == "Sí": 
            st.write(codposi)

elif st.session_state.seleccion == "Automatización de válvula existente":
    st.title("Automatización de válvula existente")
    tab1, tab2, tab3, tab4 = st. tabs(["Instalación", "Válvula de control", "Accesorios de posición", "Equipo seleccionado"])

    st.session_state.dicil = 0 

    with tab1:

        st.session_state.bat = st.number_input("Introduzca el torque necesario", placeholder=("2,78-13673 N"), format="%0f")
        

        actuador = st.radio("Funcionamiento del actuador", ["Simple efecto", "Doble efecto"], index=1)
        dico = 0 

        opciones = ["9mm", "11mm", "14mm", "17mm", "22mm", "27mm", "36mm", "46mm", "55mm"]

        seleccion_visual1 = st.selectbox("¿De qué tamaño es el cuadrado de su válvula?", opciones)

        cuadrado = str(seleccion_visual1.replace("mm", ""))
       
        if actuador == "Doble efecto":    
            opcion = {f"{i} bar" : i for i in range(2,9)}
            seleccion_visual = st.selectbox("¿Con qué presión cuenta su instalalción?", list(opcion.keys()), disabled= dico=="Por diámetro")
            presion = str(opcion[seleccion_visual])
        else:
            opcion = {f"{i} bar" : i for i in range(4,8)}
            seleccion_visual = st.selectbox("¿Con qué presión cuenta su instalalción?", list(opcion.keys()), disabled= dico=="Por diámetro")
            presion = str(opcion[seleccion_visual])

        # Caso donde selecciona por presión y doble efecto 

        if dico == "Por presión" and actuador == "Doble efecto":
            for i in range(8): 
                if lista_base_de_datos[0][i] == presion: 
                    st.session_state.p = i 
                    for i in range (1,18): 
                        if float(lista_base_de_datos[i][st.session_state.p]) > float(st.session_state.bat):
                            st.session_state.cil = lista_base_de_datos[i][0]
                            break

                for i in range(1,18): 
                    if cilindros[i][0] == st.session_state.cil:      
                        codcilde = (f"El actuador a utilizar tiene código {cilindros[i][2]}")
                        break
                    
        # Caso donde selecciona por diametro y doble efecto 

        elif dico == "Por diámetro" and actuador == "Doble efecto": 
            diametro_inicial = 0 
            diametro_final = 0
            
            for i in range(18): 
                if lista_base_de_datos[i][0] == diametro_inicial: 
                    st.session_state.min = i 
            for i in range (st.session_state.min,18): 
                if lista_base_de_datos[i][0] == diametro_final: 
                    st.session_state.max = i 
                    

                    ok = False
            for i in range(st.session_state.min, st.session_state.max): 
                for v in range(1,8): 
                    if float(lista_base_de_datos[i][v]) > float(st.session_state.bat):  
                        st.session_state.cil = lista_base_de_datos[i][0]
                        st.session_state.presion = lista_base_de_datos[0][v]
                        ok = True
                        break
                if ok: 
                    break

            for i in range(18): 
                if cilindros[i][0] == st.session_state.cil:
                    codicil = (f"El actuador a utilizar tiene código {cilindros[i][2]} y se deberá usar con una presión de alimentación de {lista_base_de_datos[0][v]} bar")

        # Caso por cuadrado y presión, doble efecto

        if st.session_state.bat != 0: 

            if actuador == "Doble efecto": 
                
                for i in range(1,19):
                    if cuadrado == lista_base_de_datos[i][8]: 
                                st.session_state.cuadrado = i 
                                for i in range (8):
                                    if presion == lista_base_de_datos[0][i]: 
                                        st.session_state.presion = i
                                        for i in range(1,18):
                                            if float(lista_base_de_datos[st.session_state.cuadrado][st.session_state.presion]) > float(st.session_state.bat * 1.15): 
                                                st.session_state.dicil = lista_base_de_datos[st.session_state.cuadrado][0]
                                                flag = True
                                                break 
                                if flag:
                                        break 
                    if flag: 
                        break
                                
                if flag: 
                            for i in range(1,18): 
                                if st.session_state.dicil == cilindros[i][0]:
                                    codicilde = (f"El actuador a utilizar tiene código {cilindros[i][2]}")  
                                    break 
                else: 
                            codicilde = ("No hay actuadores que cumplan con las condiciones establecidas.")

                # Caso por presión y cuadrado, simple efecto
           
            bandera = False
           
            if actuador == "Simple efecto": 
                for i in range(2,19): 
                    if cuadrado == simpleefecto[i][12]:
                        st.session_state.cuadtres = i
                        for i in range (2,19):
                            if float(simpleefecto[st.session_state.cuadtres][10]) > float(st.session_state.bat * 1.15): 
                                st.session_state.dicil = simpleefecto[st.session_state.cuadtres][0]
                                bandera = True 
                                break
                    if bandera: 
                        break 
                if bandera: 
                    for i in range(1,18): 
                        if st.session_state.dicil == (cilindros[i][0]):
                            codicilse = (f"El actuador a utilizar tiene código {cilindros[i][1]}")
                            break 
                else: 
                    codicilse = ("No hay actuadores que cumplan con las condiciones establecidas.")

    with tab2: 
        conexion = ""
        codval = ""

        valvula = st.radio("¿Desea seleccionar una válvula de control?", ["Externa", "En el actuador","No"])
        tension= st.selectbox("¿Con qué tensión alimentará dicha valvula?", ["220 V 50/60Hz", "110V 50/60Hz","48V 50/60Hz", "24V 50/60Hz", "24 Vcc", "12 Vcc"],disabled=valvula == "No")

        def codigo_bobina(bobinas_l, tension):
            for i in range(len(bobinas_l)): 
                if bobinas_l[i][0] == tension: 
                    return bobinas_l[i][1]
            
        if valvula == "En el actuador" and actuador == "Doble efecto": 
 
            codvalde = (f"La válvula a utilizar tiene código 0.221.012.522/{codigo_bobina(bobinas, tension)}")
                           
        if valvula == "Externa" and actuador == "Doble efecto": 

            for i in range(1,19): 
                if lista_base_de_datos[i][0] == st.session_state.dicil: 
                    print("entre")
                    conexion = lista_base_de_datos[i][9]
                    break 
            
            if conexion == "1/8": 
                codval = ("0.224.002.711")
            if conexion == "1/4": 
                codval = ("0.220.002.722")
            if conexion in ("3/8", "1/2", "3/4"): 
                codval = ("0.259.002.744")

            codvaldex = (f"La válvula de control a usar tiene código {codval}/{codigo_bobina(bobinas, tension)}") 
        
        if valvula == "En el actuador" and actuador == "Simple efecto": 

            codvalse = (f"La válvula a utilizar tiene un código 0.221.022.522/{codigo_bobina(bobinas, tension)}")

        if valvula == "Externa" and actuador == "Simple efecto": 

            for i in range(1,19): 
                if lista_base_de_datos[i][0] == st.session_state.dicil: 
                    conexion = lista_base_de_datos[i][9]
                    break 
            
            if conexion == "1/8": 
                codval = ("0.224.002.511")
            elif conexion == "1/4": 
                codval = ("0.220.002.522")
            elif conexion in ("3/8", "1/2", "3/4"): 
                codval = ("0.259.002.544")

            codvalsex = (f"La valvula de control a usar tiene código {codval}/{codigo_bobina(bobinas, tension)}")
        
    with tab3: 
        

        limits = st.radio("¿Desea colocar una caja Limit Switch?", ["Sí", "No"], disabled=st.session_state.dicil == 0, index=1)
        

        if limits == "Sí": 
            if str(st.session_state.diametro) < "125":
                codlimits = "0.900.009.103/210"
            elif str(st.session_state.diametro) >= "140" and st.session_state.diametro <= "250": 
                codlimits = "0.900.009.103/310"
            elif str(st.session_state.diametro) >= "300" and st.session_state.diametro <= "400": 
                codlimits = "0.900.009.103/410"
            codilimits = (f"La caja Limit Switch a utilizar tiene código {codlimits}")

        posi = st.radio("¿Desea colocar un posicionador?", ["Sí", "No"], disabled=st.session_state.dicil == 0, index=1)

        if posi == "Sí": 
            func = st.selectbox("¿Cómo quiere que sea el funcionamiento del posicionador?", ["Electroneumático", "Neumático"])

            for i in range(3):
                    if posicionadores[i][3] == func:
                        codposi = (f"El código del posicionador a utilizar es {posicionadores[i][1]}")          

    with tab4: 
          
        
        if actuador == "Doble efecto": 
            st.write(codicilde)
        else: 
            st.write(codicilse)
                  
        if actuador == "Doble efecto":
            if valvula == "En el actuador":
                st.write(codvalde)
            elif valvula == "Externa": 
                st.write(codvaldex)
    
        if actuador == "Simple efecto":
            if valvula == "En el actuador":
                st.write(codvalse)
            elif valvula == "Externa": 
                st.write(codvalsex)
        
        if limits != "No":
            st.write(codilimits)
        
        if posi != "No": 
            st.write(codposi)
 




 
