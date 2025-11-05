document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor25");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-25</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background: #414152;
          color: #ffffff;
          margin: 0;
          padding: 20px;
        }

        header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          position: relative;
        }

        header img {
          width: 100px;
          height: auto;
          position: absolute;
          left: 20px;
          top: 10px;
        }

        header label {
          position: absolute;
          top: 10px;
          left: 50%;
          transform: translateX(-50%);
          color: #e37854;
          font-style: italic;
          font-weight: bold;
          font-size: 60px;
        }

        main {
          margin-top: 150px; /* deja espacio para el logo y Nuam */
          text-align: left; /* texto alineado a la izquierda */
        }

        h1 {
          color: #ffffff;
        }

        p {
          color: #ffffff;
          text-align: justify;
          max-width: 600px;
        }
      </style>
    </head>
    <body>
      <header>
        <img src="/static/image/rayo.png" alt="rayo">
        <label>Nuam</label>
      </header>

      <main>
        <h1>Factor-25</h1>
        <p>
        Este factor se aplica a créditos por Impuesto de Primera Categoría (IdPC) que sí dan derecho a devolución, y que están asociados a rentas que no se integran al Impuesto Global Complementario (IGC) ni al Impuesto Adicional (IA), pero que igualmente permiten recuperar el crédito por IdPC pagado. Es una categoría especial que reconoce el derecho a devolución sin integración tributaria directa.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Con derecho a devolución” bajo Factor-25?</h2>

        <p>Según criterios del SII y validaciones del Formulario 22, se incluyen:</p>

        <ul>
          <li>Créditos por IdPC asociados a rentas exentas del IGC o IA, pero que cumplen requisitos de devolución.</li>
          <li>Montos informados en DJ 1943 o 1947, con respaldo de pago efectivo de IdPC.</li>
          <li>Rentas que no se integran a la base imponible, pero generan devolución por exceso de crédito.</li>
          <li>Dividendos o retiros percibidos por personas naturales con beneficio de exención, pero con derecho a recuperar el IdPC.</li>
          <li>Ingresos acogidos a regímenes especiales que mantienen el derecho a devolución, como ciertos beneficios previsionales o fondos de inversión.</li>
        </ul>
        <p>
        Este factor afecta porque permite recuperar el IdPC pagado, incluso si la renta no se integra al IGC o IA. Mejora la eficiencia tributaria del contribuyente, impacta directamente en el cálculo del impuesto final en el Formulario 22 y en la validación de la Declaración Jurada 1943. Es clave para evitar observaciones como la G139 y para asegurar el uso correcto del crédito tributario en regímenes exentos con devolución.
        </p>
      </main>
    </body>
    </html>
      `);
    } else {
      alert("La ventana fue bloqueada por el navegador.");
    }
  });
});