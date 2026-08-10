# Tecnología y Operación Diaria
## Papel primero, WhatsApp después, app al final

> Principio: si no funciona con cuaderno y WhatsApp en una colonia sin señal, no funciona.

---

### 1. Stack mínimo viable (semana 1)

No se necesita desarrollo. Se necesita disciplina.

| Necesidad | Herramienta | Costo | Quién opera |
|---|---|---|---|
| Vales | Talonario numerado impreso + QR generado en Google Sheets + QRCode Monkey | 800 MXN / 500 vales | Promotora + coordinadora |
| Registro | Google Sheets compartido (4 pestañas: Vales, Cirugías, Centro, Fertilizante) | 0 | Coordinadora |
| Comunicación | WhatsApp Business en celular dedicado + grupos por delegación | 0 | Promotoras |
| Tablero público | site/index.html estático (GitHub Pages) alimentado por CSV exportado de Sheets | 0 | Coordinadora (actualización diaria 10 min) |
| Fotos | Celular con cámara, carpeta Drive por fecha | 0 | Todos |
| Respaldo | Carpeta física con copias carbón + USB mensual | 0 | Coordinadora |

**Costo tecnológico mes 1-6:** <1,000 MXN/mes (impresiones + datos).

---

### 2. Flujos digitales

**A. Vale por WhatsApp (bot simple, sin IA):**

```
Usuario: Hola
Bot: ¡Hola! Soy Red de Vida San Quintín 🐾. ¿Quieres esterilizar?
     1️⃣ Perro  2️⃣ Gato
Usuario: 1
Bot: Mándame foto de tu animal + tu colonia (ej. “Flores Magón”)
Usuario: [foto] Flores Magón
Bot: Gracias. Promotora María validará en <4h. Si calificas, aquí recibirás tu vale QR.
     Mientras, ayuno 8h antes de cirugía, lleva cobija. ¿Tienes otra duda?
...
[4h después, promotora aprueba en Sheets → bot envía PDF vale]
Bot: ¡Listo! Vale #2026-0847 válido 30 días. Veterinarias cercanas: Vet SQ (612-xxx), Vet Guerrero (616-xxx) o espera quirófano 14/jun en cancha Zapata. Muestra este QR. ¿Quieres audio con instrucciones?
```

Implementación: WhatsApp Business API vía WATI o Twilio (2k MXN/mes cuando escale) o, al inicio, **respuesta manual** por promotora con plantilla guardada (suficiente para 10 vales/día).

**B. Reporte de animal extraviado/encontrado:**

Usuario envía foto + ubicación → promotora crea ficha en Sheets → script genera post para Facebook + mensaje a 5 grupos WA + ficha en tablero → actualización diaria.

**C. Tablero público:**

Archivo `data.csv` con campos: `fecha,tipo,colonia,veterinaria,estado,costo,litros_fertilizante,destino` → JavaScript en `site/index.html` lo lee y renderiza KPIs, mapa simple y tabla filtrable. Sin backend. Coordinadora exporta CSV de Sheets y arrastra a repo (o actualiza vía GitHub web).

Ejemplo fila: `2026-08-15,vale_canjeado,Flores Magón,Vet Guerrero,canjeado,1100,,`

---

### 3. Operación semanal tipo (régimen)

**Lunes:**
- Coordinadora revisa Sheets, autoriza pagos vet pendientes, actualiza tablero, agenda ruta bioliquidadora
- Promotoras visitan 2 colonias para pre-registro de jornada siguiente

**Martes-Jueves:**
- Jornadas móviles (1-2/semana) + atención CEBISQ + aquamaciones programadas
- Brigada bioliquidadora en ruta

**Viernes:**
- Cierre semanal: conteo vales, cirugías, adopciones, fertilizante; publicación en FB; preparación de reporte quincenal para Consejo

**Sábado:**
- Pasarela adopción en parque + taller duelo mensual

**Domingo:** descanso rotativo, guardia telefónica para emergencias

---

### 4. Roles y pagos

| Rol | Cantidad | Pago/mes | Perfil |
|---|---|---|---|
| Coordinadora General | 1 | 18,000 | Organización, Sheets, trato con municipio, manejo de fondo |
| Promotoras de colonia | 8 (2 por delegación grande) | 3,500 + bono 500 si meta vales | Vecinas con confianza local, hablan español + mixteco básico ideal |
| MVZ cirujana líder | 1 (por jornada) | 2,500/jornada | HQHVSN |
| Cuidadores CEBISQ | 4 | 8,000 c/u (turnos) | Experiencia animales, curso bioseguridad |
| Operador bioliquidadora | 1 | 9,000 + viático ruta | Técnico con licencia manejo, curso álcali |
| Voluntariado | 15-20 | No pago, seguro + diploma + alimento | Estudiantes, rescatistas |

Total nómina régimen: ~95k MXN/mes.

---

### 5. Manuales de 1 página (para pared)

Cada proceso tiene ficha laminada en pared del CEBISQ y en remolque:

- Cómo emitir vale (5 pasos)
- Cómo preparar animal para cirugía (ayuno, cobija)
- Cómo ingresar animal al Centro (foto en <2h)
- Cómo operar bioliquidadora (checklist pH, temp, descarga)
- Cómo diluir fertilizante (tabla dosis)

Sin manual largo. Una página, fotos, español claro.

---

### 6. Escalamiento tecnológico (mes 12+)

Cuando 300 vales/mes fluyan sin caos, entonces sí:

- PWA sencilla (React + Firebase) para registro de animales con chip, historial médico, y padrinazgo con pago Stripe/OXXO
- Lector de chip con Bluetooth que alimenta Sheets
- Sensor IoT en reactor (temp/pH a Grafana) — opcional, no crítico

Pero **nunca** obligar app para obtener vale. El papel y WhatsApp quedan como vías permanentes.

---

### 7. Métricas operativas diarias (checklist coordinadora)

- [ ] Vales emitidos / canjeados / vencidos
- [ ] Cirugías por colonia
- [ ] Animales en CEBISQ / días promedio / adopciones
- [ ] Aquamaciones (privadas/comunales)
- [ ] Litros hidrolizado / litros fertilizante / destino
- [ ] Pagos vet pendientes >72h (alerta roja)
- [ ] Quejas/sugerencias

10 minutos al día, 7 gráficos en tablero.

---

### 8. Resiliencia

- **Sin luz:** planta 5kW en CEBISQ y remolque; vales en papel.
- **Sin internet:** Sheets offline + sincroniza al volver; tablero se actualiza al día siguiente (no pasa nada).
- **Sin coordinadora (vacaciones):** promotora senior con acceso y manual.
- **Sin alcalde:** AC sigue, fondo con 3 meses reserva.

La tecnología es la parte fácil. La confianza territorial es el verdadero sistema operativo.
