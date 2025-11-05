document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor34");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-34</title>
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
        <h1>Factor-34</h1>
        <p>
        Este factor se utiliza en el Formulario 22 para declarar el crédito por Impuesto Único (IU) del 40% pagado sobre gastos rechazados, según lo establece el artículo 21 de la LIR. Estos gastos corresponden a desembolsos que no cumplen los requisitos del artículo 31 para ser deducibles, y que se consideran realizados en beneficio del contribuyente o terceros relacionados.
        </p>

        <h2>¿Qué tipo de partidas generan crédito bajo Factor-34?</h2>

        <p>Según el SII y la Circular N°71 de 2015, se incluyen:</p>

        <ul>
          <li>Gastos rechazados que no cumplen requisitos de necesidad, proporcionalidad o documentación.</li>
          <li>Remuneraciones, beneficios o pagos realizados a socios, accionistas o relacionados, sin respaldo válido.</li>
          <li>Partidas que fueron gravadas con IU del 40%, conforme al artículo 21 inciso primero.</li>
          <li>Montos informados en la línea 62 del Formulario 22, que generan crédito por IU pagado.</li>
          <li>Contribuyentes con contabilidad completa, que declaran rentas efectivas en Primera Categoría.</li>
        </ul>
        <p>
        Este factor afecta porque permite compensar el IU pagado, pero limita la recuperación del crédito. Es clave para validar correctamente partidas rechazadas, evitar observaciones como la G139, y asegurar el uso correcto del crédito tributario en contextos de fiscalización.
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