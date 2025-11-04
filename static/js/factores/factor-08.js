document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor08");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-08</title>
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
        <h1>Factor-08</h1>
        <p>
          El Factor-08 representa la proporción del monto total de dividendos, retiros o remesas que corresponde a ingresos que no se consideran renta para efectos tributarios, según la Ley sobre Impuesto a la Renta (LIR). Es decir, son montos que no generan obligación de pagar impuestos ni se suman a la base imponible del contribuyente.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “No Constitutivos de Renta”?</h2>

        <p>Según el artículo 17 de la LIR y otras disposiciones del SII, estos incluyen:</p>

        <ul>
          <li>Devoluciones de capital (por disminución de patrimonio, no por utilidad).</li>
          <li>Aportes de capital realizados por socios o accionistas.</li>
          <li>Indemnizaciones por seguros que no generan ganancia.</li>
          <li>Donaciones recibidas en ciertos regímenes.</li>
          <li>Distribuciones que no provienen de rentas acumuladas.</li>
          <li>Montos que ya tributaron en etapas anteriores y no deben volver a hacerlo.</li>
        </ul>

        <p>
          Este factor afecta, porque define qué parte del monto no tributa, limita la asignación de otros factores, y modifica el resultado final de la calificación tributaria. Es un componente esencial para que el sistema sea legalmente válido y fiscalmente correcto.
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