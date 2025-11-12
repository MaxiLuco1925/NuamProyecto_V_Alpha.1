document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnEjemplo");

    btn.addEventListener("click", () => {
    const imagenUrl = new URL(btn.dataset.imagenUrl, window.location.origin).href;
    const nuevaVentana = window.open("", "_blank", "width=2000,height=1120");
        
    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="UTF-8">
          <title>Factor-08</title>
          <style>
          body {
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f8fafc;
            color: #333;
            display: flex;
            height: 100vh;
          }

          .izquierda {
            flex: 1;
            background-color: #1e293b;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 10px;
          }

          .izquierda img {
            width: 95%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
          }

          .derecha {
            flex: 1;
            background-color: #ffffff;
            padding: 40px;
            overflow-y: auto;
          }

          h1 {
            color: #0d6efd;
            font-size: 24px;
            margin-bottom: 20px;
          }

          h2 {
            color: #2563eb;
            margin-top: 25px;
            font-size: 18px;
          }

          p, li {
            line-height: 1.6;
            font-size: 15px;
          }

          .emoji {
            font-weight: bold;
            margin-right: 5px;
          }

          ul {
            padding-left: 20px;
          }

          .section {
            margin-bottom: 20px;
            background: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #0d6efd;
          }
        </style>
        </head>
        <body>
          <div class="izquierda">
          <img src="${imagenUrl}" alt="Ejemplo del formulario">
          </div>
          <div class="derecha">
          <h1>🧾 Guía para llenar el formulario</h1>

          <div class="section"><h2>🟦 1. Descripción</h2>
          <p>📄 Qué es: Un texto breve que identifique el evento o ingreso que estás calificando.</p>
          <p>✍️ Ejemplo:<br>“Pago de dividendo acción A”<br>“Renta percibida por instrumento extranjero”<br>“Distribución de utilidades 2024”</p>
          <p>👉 Debe ser claro y representativo del movimiento o ingreso.</p></div>

          <div class="section"><h2>📅 2. Fecha de pago</h2>
          <p>📄 Qué es: Fecha en que efectivamente se realizó el pago o se percibió el ingreso.</p>
          <p>⏰ Formato: dd/mm/aaaa</p>
          <p>✍️ Ejemplo:<br>25/04/2024<br>10/01/2025</p>
          <p>👉 Debe coincidir con la fecha del comprobante o documento de respaldo.</p></div>

          <div class="section"><h2>🔢 3. Secuencia del evento</h2>
          <p>📄 Qué es: Un número interno o correlativo que identifique la operación.</p>
          <p>✍️ Ejemplo:<br>1 (si es el primer dividendo del año)<br>2024-05 (si usas formato tipo año-secuencia)</p>
          <p>👉 Sirve para organizar varias calificaciones dentro de un mismo instrumento.</p></div>

          <div class="section"><h2>💰 4. Dividendo</h2>
          <p>📄 Qué es: El monto bruto del dividendo o utilidad pagada, sin descontar impuestos.</p>
          <p>✍️ Ejemplo:<br>125000<br>567890.50</p>
          <p>👉 Debe ser numérico, en pesos o en la moneda base definida por el sistema.</p></div>

          <div class="section"><h2>💵 5. Valor histórico</h2>
          <p>📄 Qué es: El monto original al momento del pago, antes de aplicar reajustes o factores de actualización.</p>
          <p>✍️ Ejemplo:<br>125000<br>85000</p>
          <p>👉 Sirve para comparar el valor nominal con el valor actualizado (Factor de Actualización).</p></div>

          <div class="section"><h2>📆 6. Año tributario</h2>
          <p>📄 Qué es: El año al que corresponde la declaración tributaria.</p>
          <p>✍️ Ejemplo:<br>2024 → (si corresponde a ingresos de 2023)<br>2025 → (si corresponde a ingresos de 2024)</p>
          <p>👉 Recuerda que el “año tributario” es el año en que se declara, no el año del pago.</p></div>

          <div class="section"><h2>🧾 7. ISFUT</h2>
          <p>📄 Qué es: Indica si el dividendo o utilidad está afecto a Impuesto Sustitutivo al Fondo de Utilidades Tributables (ISFUT).</p>
          <p>🔘 Valores posibles:<br>“Sí” → Si el ingreso proviene de utilidades sujetas a ISFUT.<br>“No” → Si no aplica.</p>
          <p>👉 Si no estás seguro, normalmente es “No”.</p></div>

          <div class="section">
            <h2>🌍 8. Mercado</h2>
            <p>📄 Qué es: El tipo de mercado o ámbito económico donde se genera el ingreso o pertenece el instrumento.</p>
            <p>🔽 Ejemplo de opciones:<br>
            “Acciones”<br>
            “Bonos”<br>
            “Criptomonedas”<br>
            “Instrumentos financieros”<br>
            “Exportaciones”<br>
            “Importaciones”<br>
            “Servicios”<br>
            “Renta mobiliaria”<br>
            “Comercio”<br>
            “Agroindustria”</p>
            <p>👉 Elige según la naturaleza o el sector económico del ingreso o inversión.</p>
            </div>

          <div class="section"><h2>📊 9. Instrumento</h2>
          <p>📄 Qué es: El tipo de título, acción o inversión de la cual proviene el ingreso.</p>
          <p>🔽 Ejemplo:<br>“Acción”<br>“Fondo de Inversión”<br>“Bonos”<br>“ETF”</p>
          <p>👉 Debe estar registrado previamente en la tabla de instrumentos del sistema.</p></div>

          <div class="section"><h2>📈 10. Factor de Actualización</h2>
          <p>📄 Qué es: Un número que reajusta valores históricos a valores actualizados según IPC o normativa (por ejemplo, el Factor-08 del SII).</p>
          <p>✍️ Ejemplo:<br>1.0834<br>0.9975</p>
          <p>👉 El sistema puede calcularlo automáticamente o ingresarse manualmente según el período.</p></div>
        </div>
      </body>
      </html>
    `);
    } else {
      alert("Por favor, permite las ventanas emergentes para ver el ejemplo.");
    }
    });
});