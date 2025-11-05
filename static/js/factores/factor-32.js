document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor32");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-32</title>
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
        <h1>Factor-32</h1>
        <p>
        Este factor se utiliza en el Formulario 22 para declarar créditos por IdPC asociados a rentas exentas o no constitutivas de renta, que fueron efectivamente gravadas con IdPC y que, pese a no formar parte de la base imponible del contribuyente, permiten solicitar devolución del impuesto pagado. Es una categoría especial que reconoce el derecho a recuperar el IdPC en contextos donde no hay integración directa.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Con derecho a devolución” bajo Factor-32?</h2>

        <p>Según el Servicio de Impuestos Internos (SII) y las validaciones de renta 2025, se incluyen:</p>

        <ul>
          <li>Dividendos o retiros que provienen de utilidades gravadas con IdPC, pero que no se integran al IGC o IA.</li>
          <li>Montos informados en Declaraciones Juradas 1943 o 1947, que cumplen con los requisitos de devolución.</li>
          <li>Rentas exentas del IGC o IA, pero con respaldo de pago efectivo de IdPC.</li>
          <li>Ingresos acogidos a regímenes especiales, como ciertos fondos de inversión o beneficios previsionales, que permiten devolución.</li>
          <li>Partidas que no generan base imponible, pero sí derecho a recuperar el impuesto pagado por la empresa.</li>
        </ul>
        <p>
        Este factor afecta porque permite recuperar el IdPC pagado, incluso si la renta no se integra al impuesto personal. Esto mejora la eficiencia tributaria del contribuyente, impacta directamente en el cálculo del impuesto final en el Formulario 22 y en la validación de la DJ 1943. Es clave para evitar observaciones como la G139, que controlan el uso correcto del crédito tributario.
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