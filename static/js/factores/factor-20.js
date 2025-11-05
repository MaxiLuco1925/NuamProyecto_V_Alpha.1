document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor20");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-20</title>
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
        <h1>Factor-20</h1>
        <p>
        Este factor se aplica a rentas que generan crédito por IdPC, pero que no han sido efectivamente gravadas con dicho impuesto, o que provienen de partidas especiales como gastos rechazados. Por lo tanto, el crédito solo puede ser usado para compensar, sin que el remanente pueda ser devuelto al contribuyente.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Con crédito sin derecho a devolución”?</h2>

        <p>Según la Línea 25 del Formulario 22 y el artículo 21 de la LIR, se incluyen:</p>

        <ul>
          <li>Gastos rechazados que generan crédito por IdPC, pero no permiten devolución.</li>
          <li>Partidas que no fueron gravadas con IdPC, pero que se informan como crédito compensable.</li>
          <li>Montos registrados en líneas 1 a 8 del F22, que solo permiten imputación parcial.</li>
          <li>Rentas que no cumplen con los requisitos de devolución, como aquellas sin respaldo de pago efectivo de IdPC.</li>
        </ul>
        <p>
        Este factor afecta porque permite imputar el crédito por IdPC contra el IGC o IA, pero no genera devolución si hay excedente. Se aplica a partidas como gastos rechazados del artículo 21, afectando directamente el cálculo en el Formulario 22 (línea 25). Es clave para evitar errores en la imputación de créditos y observaciones como la G139, que controlan el uso correcto del crédito.
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