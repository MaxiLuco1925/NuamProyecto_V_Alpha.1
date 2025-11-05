document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor31");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-31</title>
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
        <h1>Factor-31</h1>
        <p>
        Este factor se aplica a rentas exentas o no constitutivas de renta, que fueron informadas con crédito por IdPC, pero que no pueden ser usados ni devueltos. Se trata de un crédito que debe ser reportado por transparencia fiscal, pero que no genera impacto en el cálculo del impuesto final ni permite recuperación del excedente.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sin derecho a devolución” bajo Factor-31?</h2>

        <p>Según el SII y la Ley sobre Impuesto a la Renta (LIR), se incluyen:</p>

        <ul>
          <li>Dividendos o retiros que provienen de utilidades gravadas con IdPC, pero que no se integran al IGC o IA y no cumplen requisitos de devolución.</li>
          <li>Montos informados en DJ 1943 o 1947, que no permiten imputación ni devolución.</li>
          <li>Rentas exentas o no renta, donde el crédito por IdPC se informa solo por trazabilidad.</li>
          <li>Partidas que no generan base imponible, y cuyo crédito no puede ser usado por el contribuyente.</li>
          <li>Situaciones de pérdida tributaria, donde el crédito asociado a dividendos no puede ser aprovechado.</li>
        </ul>
        <p>
        Este factor afecta porque evita que se utilicen créditos que no corresponden, manteniendo la coherencia entre registros contables y tributarios. Es clave para evitar observaciones como la G33, que controlan el uso correcto de créditos informativos. Aunque no genera efecto tributario, su correcta declaración es obligatoria para validar la consistencia fiscal.
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