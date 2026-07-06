document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor11");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-11</title>
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
        <h1>Factor-11</h1>
        <p>
            El Factor-11 representa el coeficiente de incremento aplicado a utilidades afectas al Impuesto de Primera Categoría (IdPC), con el fin de calcular el crédito tributario que puede ser imputado por el contribuyente. Este factor permite reconstituir la renta líquida imponible antes de impuestos, según la tasa efectiva de IdPC que haya gravado dicha utilidad.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sujetos a Incremento por IdPC”?</h2>

        <p>Según los artículos 38 bis, 54 N°1 y 62 de la Ley sobre Impuesto a la Renta (LIR), se incluyen:</p>

        <ul>
          <li>Utilidades retiradas, distribuidas o percibidas desde empresas que tributan con IdPC.</li>
          <li>Dividendos que provienen de rentas afectas a distintas tasas históricas de IdPC.</li>
          <li>Rentas acumuladas que se integran al sistema semi-integrado o atribuido.</li>
          <li>Montos que generan derecho a crédito por IdPC, pero requieren ser incrementados para reflejar la renta bruta.</li>
        </ul>

        <p>
           Este factor afecta, porque: Permite calcular correctamente el crédito por IdPC que se puede imputar contra el impuesto personal, ajusta la utilidad neta para reflejar su valor antes de impuestos, varía según la tasa de IdPC aplicada en el año en que se generó la renta.
        </p>
        <ul>
          <li>Tasa IdPC | Factor de Incremento</li>
          <li>10% | 0,11111</li>
          <li>15% | 0,17647</li>
          <li>17% | 0,204819</li>
          <li>20% | 0,25</li>
          <li>25% | 0,333333</li>
          <li>27% | 0,369863</li>
        </ul>
      </main>
    </body>
    </html>
      `);
    } else {
      alert("La ventana fue bloqueada por el navegador.");
    }
  });
});