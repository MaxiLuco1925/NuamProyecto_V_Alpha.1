document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor19");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-19</title>
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
        <h1>Factor-19</h1>
        <p>
        Este factor se aplica a montos que el contribuyente percibe o genera, pero que no califican como renta según el artículo 17 de la Ley sobre Impuesto a la Renta (LIR). Aunque no se gravan, deben ser registrados en el sistema tributario, especialmente en regímenes como el 14 D 3 o en el registro REX (Rentas Exentas e Ingresos No Constitutivos de Renta).
        </p>

        <h2>¿Qué tipo de ingresos se consideran “No Constitutivos de Renta”?</h2>

        <p>Según el artículo 17 de la LIR y criterios del SII, se incluyen:</p>

        <ul>
          <li>Devoluciones de capital por disminución de patrimonio, no por utilidad.</li>
          <li>Aportes de capital realizados por socios o accionistas.</li>
          <li>Indemnizaciones por seguros que no generan ganancia.</li>
          <li>Donaciones recibidas, en ciertos regímenes y bajo condiciones específicas.</li>
          <li>Distribuciones que no provienen de rentas acumuladas ni de utilidades tributables.</li>
          <li>Montos que ya tributaron en etapas anteriores y no deben volver a hacerlo.</li>
        </ul>
        <p>
        Este factor afecta porque permite declarar correctamente ingresos que no deben tributar, asegurando la coherencia entre registros contables y tributarios. Mejora la trazabilidad fiscal, evita observaciones como la G33 y valida la clasificación en el Formulario 22 y en declaraciones juradas como la 1939 o 1947. Es clave para contribuyentes acogidos a regímenes como el 14 D 3, que deben informar ingresos no renta en el registro REX.
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