import tkinter as tk
from tkinter import messagebox
import random

class RuletaBiblicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎡 Ruleta Bíblica 🎡")
        
        # Iniciar en pantalla completa
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.confirmar_salida)

        self.color_fondo = "#0f172a" 
        self.root.config(bg=self.color_fondo)

        self.ancho_pantalla = self.root.winfo_screenwidth()
        self.alto_pantalla = self.root.winfo_screenheight()

        self.crear_fondo_animado()

        self.colores_base = ["#FF0040", "#FF8000", "#FFD700", "#80FF00", "#00FF40", 
                             "#00FFC0", "#00BFFF", "#0040FF", "#8000FF", "#FF00BF"]
        
        self.preparar_preguntas()
        
        self.angulo_actual = 0
        self.girando = False
        
        # Variables para el confeti
        self.confetis = []
        self.animando_confeti = False

        self.crear_interfaz()
        self.dibujar_ruleta()
        self.actualizar_contadores() # Inicializar el conteo visual

    def confirmar_salida(self, event=None):
        respuesta = messagebox.askyesno("Confirmar Salida", "¿De verdad quieres salir del juego?")
        if respuesta:
            self.root.destroy()

    def crear_fondo_animado(self):
        self.bg_canvas = tk.Canvas(self.root, width=self.ancho_pantalla, height=self.alto_pantalla, 
                                   bg=self.color_fondo, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.particulas = []
        colores_particulas = ["#38bdf8", "#818cf8", "#c084fc", "#ffffff"]

        for _ in range(60):
            x = random.randint(0, self.ancho_pantalla)
            y = random.randint(0, self.alto_pantalla)
            tamano = random.randint(2, 6)
            velocidad = random.uniform(0.5, 2.0)
            color = random.choice(colores_particulas)
            
            id_particula = self.bg_canvas.create_oval(x, y, x+tamano, y+tamano, fill=color, outline="")
            self.particulas.append({"id": id_particula, "velocidad": velocidad, "x": x})
            
        self.animar_fondo()

    def animar_fondo(self):
        for p in self.particulas:
            self.bg_canvas.move(p["id"], 0, -p["velocidad"])
            coords = self.bg_canvas.coords(p["id"])
            if len(coords) > 0 and coords[3] < 0:
                nueva_x = random.randint(0, self.ancho_pantalla)
                ancho_p = coords[2] - coords[0]
                self.bg_canvas.coords(p["id"], nueva_x, self.alto_pantalla, nueva_x + ancho_p, self.alto_pantalla + ancho_p)

        self.root.after(30, self.animar_fondo)

    # --- NUEVO: SISTEMA DE CONFETI ---
    def lanzar_confeti(self):
        colores_confeti = ["#FF0040", "#FFD700", "#00FF40", "#00BFFF", "#8000FF", "#FFFFFF"]
        
        # Crear 150 papelitos de confeti
        for _ in range(150):
            x = random.randint(0, self.ancho_pantalla)
            y = random.randint(-150, -10) # Empiezan arriba fuera de la pantalla
            tamano = random.randint(6, 14)
            color = random.choice(colores_confeti)
            
            id_confeti = self.bg_canvas.create_rectangle(x, y, x+tamano, y+tamano, fill=color, outline="")
            
            self.confetis.append({
                "id": id_confeti,
                "dx": random.uniform(-3, 3), # Movimiento horizontal (viento)
                "dy": random.uniform(2, 10)  # Velocidad de caída
            })
            
        if not self.animando_confeti:
            self.animando_confeti = True
            self.animar_confeti()

    def animar_confeti(self):
        activos = []
        for c in self.confetis:
            self.bg_canvas.move(c["id"], c["dx"], c["dy"])
            c["dy"] += 0.2 # Gravedad (aceleración hacia abajo)
            
            coords = self.bg_canvas.coords(c["id"])
            # Si el confeti no ha tocado el fondo de la pantalla, sigue activo
            if coords and coords[1] < self.alto_pantalla:
                activos.append(c)
            else:
                self.bg_canvas.delete(c["id"]) # Eliminar para no consumir memoria
                
        self.confetis = activos
        
        if self.confetis:
            self.root.after(30, self.animar_confeti)
        else:
            self.animando_confeti = False

    def preparar_preguntas(self):
        todas_las_preguntas = [
            ("¿Quién fue el primer hombre creado por Dios?", "Adán (Génesis 2:7)."),
            ("¿Quién construyó el arca para salvarse del diluvio?", "Noé (Génesis 6:13-14)."),
            ("¿A quién se le conoce como el 'Padre de la Fe'?", "Abraham (Génesis 17:5)."),
            ("¿Cómo se llamaba la esposa de Abraham que tuvo un hijo a los 90 años?", "Sara (Génesis 17:17)."),
            ("¿Quién fue vendido por sus hermanos como esclavo a Egipto?", "José (Génesis 37:28)."),
            ("¿Qué personaje bíblico fue rescatado de las aguas del Nilo por la hija del Faraón?", "Moisés (Éxodo 2:5-10)."),
            ("¿A través de qué objeto le habló Dios a Moisés por primera vez?", "Una zarza ardiente (Éxodo 3:2)."),
            ("¿Cuántas plagas envió Dios sobre Egipto?", "Diez (Éxodo 7-12)."),
            ("¿Qué mar dividió Dios para que el pueblo de Israel cruzara?", "El Mar Rojo (Éxodo 14:21)."),
            ("¿Dónde recibió Moisés los Diez Mandamientos?", "En el Monte Sinaí (Éxodo 19:20)."),
            ("¿Qué alimento envió Dios del cielo al pueblo en el desierto?", "Maná (Éxodo 16:14-15)."),
            ("¿Quién sucedió a Moisés como líder de Israel?", "Josué (Josué 1:1-2)."),
            ("¿Qué ciudad cayó después de que el pueblo de Israel marchara alrededor de ella siete días?", "Jericó (Josué 6:20)."),
            ("¿Quién fue el hombre más fuerte de la Biblia cuya fuerza residía en su cabello?", "Sansón (Jueces 16:17)."),
            ("¿Qué mujer fue una famosa jueza y profetisa en Israel?", "Débora (Jueces 4:4)."),
            ("¿Quién fue la joven moabita que decidió seguir al Dios de su suegra Noemí?", "Rut (Rut 1:16)."),
            ("¿Quién fue el primer rey de Israel?", "Saúl (1 Samuel 10:1)."),
            ("¿Con qué arma mató David al gigante Goliat?", "Con una honda y una piedra (1 Samuel 17:50)."),
            ("¿Qué instrumento tocaba David para calmar al rey Saúl?", "El arpa (1 Samuel 16:23)."),
            ("¿Quién pidió a Dios sabiduría en lugar de riquezas o larga vida?", "Salomón (1 Reyes 3:9)."),
            ("¿Quién construyó el primer Templo en Jerusalén?", "Salomón (1 Reyes 6:1)."),
            ("¿Qué profeta fue llevado al cielo en un torbellino y un carro de fuego?", "Elías (2 Reyes 2:11)."),
            ("¿Quién fue el profeta que desafió a los 450 profetas de Baal en el Monte Carmelo?", "Elías (1 Reyes 18:21)."),
            ("¿Quién fue arrojado al foso de los leones por orar a Dios?", "Daniel (Daniel 6:16)."),
            ("¿Cómo se llamaban los tres amigos de Daniel que sobrevivieron al horno de fuego?", "Sadrac, Mesac y Abed-nego (Daniel 3:12)."),
            ("¿Qué profeta fue tragado por un gran pez por desobedecer a Dios?", "Jonás (Jonás 1:17)."),
            ("¿Quién perdió todo lo que tenía pero nunca negó a Dios?", "Job (Job 1:21-22)."),
            ("¿Qué reina judía arriesgó su vida para salvar a su pueblo de un decreto de muerte?", "Ester (Ester 4:16)."),
            ("¿Quién dirigió la reconstrucción de los muros de Jerusalén?", "Nehemías (Nehemías 2:17-18)."),
            ("¿Cuál es el libro más largo de la Biblia?", "Salmos (150 capítulos)."),
            ("¿En qué ciudad nació Jesús?", "Belén (Mateo 2:1)."),
            ("¿Quiénes fueron los primeros en visitar a Jesús recién nacido?", "Los pastores (Lucas 2:8-16)."),
            ("¿Quién bautizó a Jesús en el río Jordán?", "Juan el Bautista (Mateo 3:13)."),
            ("¿Cuántos días ayunó Jesús en el desierto antes de ser tentado?", "40 días y 40 noches (Mateo 4:2)."),
            ("¿Cuál fue el primer milagro de Jesús?", "Convertir el agua en vino en las bodas de Caná (Juan 2:1-11)."),
            ("¿Cuántos discípulos eligió Jesús originalmente?", "Doce (Mateo 10:1)."),
            ("¿Quién era el recaudador de impuestos que se subió a un árbol de sicómoro para ver a Jesús?", "Zaqueo (Lucas 19:1-4)."),
            ("¿Cómo se llamaba el amigo de Jesús que fue resucitado después de cuatro días de muerto?", "Lázaro (Juan 11:43-44)."),
            ("¿Qué apóstol caminó sobre las aguas hacia Jesús?", "Pedro (Mateo 14:29)."),
            ("¿Cuántas personas alimentó Jesús con cinco panes y dos peces?", "Cinco mil hombres (Mateo 14:21)."),
            ("¿Qué discípulo negó a Jesús tres veces antes de que el gallo cantara?", "Pedro (Mateo 26:74-75)."),
            ("¿Quién traicionó a Jesús por 30 piezas de plata?", "Judas Iscariote (Mateo 26:14-15)."),
            ("¿En qué monte oró Jesús antes de ser arrestado?", "En el Monte de los Olivos o Getsemaní (Mateo 26:36)."),
            ("¿Quién era el gobernador romano que sentenció a Jesús a muerte?", "Poncio Pilato (Mateo 27:24-26)."),
            ("¿En qué lugar fue crucificado Jesús?", "En el Gólgota o Lugar de la Calavera (Mateo 27:33)."),
            ("¿Qué inscripción pusieron sobre la cruz de Jesús?", "Este es Jesús, el Rey de los Judíos (Mateo 27:37)."),
            ("¿Quién prestó su tumba nueva para el cuerpo de Jesús?", "José de Arimatea (Mateo 27:57-60)."),
            ("¿Al cuántos días resucitó Jesús?", "Al tercer día (Mateo 28:1-6)."),
            ("¿Quién fue la primera persona en ver a Jesús resucitado?", "María Magdalena (Juan 20:14-16)."),
            ("¿Cuál es el mandamiento más importante según Jesús?", "Amar a Dios con todo el corazón, alma y mente (Mateo 22:37-38).")
        ]

        random.shuffle(todas_las_preguntas)

        self.secciones = []
        for i in range(10):
            nombre = f"Sección {i+1}"
            preguntas = todas_las_preguntas[i*5 : (i+1)*5]
            color = self.colores_base[i]
            self.secciones.append({"nombre": nombre, "preguntas": preguntas, "color": color})

    def crear_interfaz(self):
        # --- NUEVO: Panel lateral izquierdo para los contadores ---
        self.frame_contadores = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_contadores.place(relx=0.05, rely=0.5, anchor=tk.W)

        tk.Label(self.frame_contadores, text="📊 PREGUNTAS", font=("Arial", 16, "bold"), bg=self.color_fondo, fg="#FFFFFF").pack(pady=(0, 15))
        
        self.etiquetas_secciones = {}
        for i in range(10):
            nombre_sec = f"Sección {i+1}"
            lbl = tk.Label(self.frame_contadores, text="", font=("Arial", 14, "bold"), bg=self.color_fondo, fg=self.colores_base[i])
            lbl.pack(anchor="w", pady=5)
            self.etiquetas_secciones[nombre_sec] = {"label": lbl, "color_original": self.colores_base[i]}

        # Panel central para el juego
        self.frame_principal = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.lbl_salir = tk.Label(self.root, text="Presiona 'ESC' para salir", font=("Arial", 10), bg=self.color_fondo, fg="#64748b")
        self.lbl_salir.place(x=10, y=10)

        self.canvas = tk.Canvas(self.frame_principal, width=400, height=400, bg=self.color_fondo, highlightthickness=0)
        self.canvas.pack(pady=10)

        self.lbl_seccion = tk.Label(self.frame_principal, text="¡Haz clic en Girar!", font=("Arial", 18, "bold"), bg=self.color_fondo, fg="#ffffff")
        self.lbl_seccion.pack(pady=10)

        self.lbl_pregunta = tk.Label(self.frame_principal, text="", font=("Arial", 18, "bold"), bg=self.color_fondo, fg="#FFD700", wraplength=800, justify="center")
        self.lbl_pregunta.pack(pady=15)

        self.lbl_temporizador = tk.Label(self.frame_principal, text="", font=("Arial", 30, "bold"), bg=self.color_fondo, fg="#FF0040")
        self.lbl_temporizador.pack(pady=10)

        self.lbl_respuesta = tk.Label(self.frame_principal, text="", font=("Arial", 20, "bold"), bg=self.color_fondo, fg="#00FF40", wraplength=800, justify="center")
        self.lbl_respuesta.pack(pady=15)

        self.btn_girar = tk.Button(self.frame_principal, text="🎲 GIRAR RULETA 🎲", font=("Arial", 16, "bold"), bg="#0284c7", fg="white", command=self.iniciar_giro, relief="raised", bd=5, padx=20, pady=10)
        self.btn_girar.pack(pady=20)

    # --- NUEVO: Función que actualiza el conteo en pantalla ---
    def actualizar_contadores(self):
        # Diccionario rápido de cuántas preguntas le quedan a cada sección activa
        conteo_actual = {sec["nombre"]: len(sec["preguntas"]) for sec in self.secciones}

        for i in range(10):
            nombre_sec = f"Sección {i+1}"
            datos_lbl = self.etiquetas_secciones[nombre_sec]
            
            if nombre_sec in conteo_actual:
                restantes = conteo_actual[nombre_sec]
                datos_lbl["label"].config(text=f"{nombre_sec}: {restantes}/5", fg=datos_lbl["color_original"])
            else:
                # Si ya no está en la lista activa, se agotó
                datos_lbl["label"].config(text=f"{nombre_sec}: AGOTADA", fg="#475569") # Gris oscuro

    def dibujar_ruleta(self):
        self.canvas.delete("ruleta") 
        
        if not self.secciones:
            return

        num_secciones = len(self.secciones)
        grados_por_seccion = 360 / num_secciones

        for i, seccion in enumerate(self.secciones):
            start = self.angulo_actual + (i * grados_por_seccion)
            self.canvas.create_arc(20, 20, 380, 380, start=start, extent=grados_por_seccion, 
                                   fill=seccion["color"], outline="white", width=2, tags="ruleta")
            
        self.canvas.create_polygon(190, 10, 210, 10, 200, 40, fill="white", outline="black", width=2, tags="ruleta")
        self.canvas.create_oval(180, 180, 220, 220, fill="white", outline="gray", width=3, tags="ruleta") 

    def iniciar_giro(self):
        if not self.secciones:
            messagebox.showinfo("Fin del Juego", "¡Se han respondido todas las preguntas!")
            return

        self.btn_girar.config(state=tk.DISABLED)
        self.lbl_pregunta.config(text="")
        self.lbl_respuesta.config(text="")
        self.lbl_temporizador.config(text="")
        
        self.velocidad = random.uniform(15, 25)
        self.friccion = random.uniform(0.1, 0.3)
        self.girando = True
        
        self.animar_ruleta()

    def animar_ruleta(self):
        if self.velocidad > 0.1:
            self.angulo_actual = (self.angulo_actual + self.velocidad) % 360
            self.velocidad -= self.friccion
            
            self.dibujar_ruleta()
            self.root.after(20, self.animar_ruleta)
        else:
            self.girando = False
            self.procesar_resultado()

    def procesar_resultado(self):
        num_secciones = len(self.secciones)
        grados_por_seccion = 360 / num_secciones
        
        offset = (90 - self.angulo_actual) % 360
        indice_ganador = int(offset // grados_por_seccion)
        
        seccion_ganadora = self.secciones[indice_ganador]
        pregunta, respuesta = seccion_ganadora["preguntas"].pop(0)

        # Actualizamos la lista lateral al sacar la pregunta
        self.actualizar_contadores()

        self.lbl_seccion.config(text=f"🌀 Cayó en la {seccion_ganadora['nombre']} 🌀", fg=seccion_ganadora["color"])
        self.lbl_pregunta.config(text=f"❓ {pregunta}")

        self.respuesta_actual = respuesta
        self.seccion_actual_obj = seccion_ganadora
        
        self.tiempo_restante = 15
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        if self.tiempo_restante > 0:
            self.lbl_temporizador.config(text=f"⏳ {self.tiempo_restante}")
            self.tiempo_restante -= 1
            self.root.after(1000, self.actualizar_temporizador)
        else:
            self.lbl_temporizador.config(text="¡Tiempo!")
            self.lbl_respuesta.config(text=f"💡 Respuesta:\n{self.respuesta_actual}")
            self.btn_girar.config(state=tk.NORMAL)
            
            # ¡Disparamos el confeti al revelar la respuesta!
            self.lanzar_confeti()

            if len(self.seccion_actual_obj["preguntas"]) == 0:
                self.secciones.remove(self.seccion_actual_obj)
                self.actualizar_contadores() # Asegurar que aparezca como AGOTADA
                messagebox.showinfo("Sección completada", f"La {self.seccion_actual_obj['nombre']} se ha quedado sin preguntas. ¡El tablero se ajustará!")
                self.dibujar_ruleta() 

if __name__ == "__main__":
    ventana = tk.Tk()
    app = RuletaBiblicaApp(ventana)
    ventana.mainloop()