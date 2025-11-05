document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor23");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-23</title>
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
        <h1>Factor-23</h1>
        <p>
        Este factor se aplica a rentas que han sido efectivamente gravadas con IdPC, pero que provienen de regímenes especiales, como el artículo 14 ter o rentas acumuladas en registros históricos (SAC), y que mantienen el derecho a devolución del crédito por IdPC. Es similar al Factor-21, pero se usa para clasificar rentas que no encajan en los factores estándar del régimen general.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Con derecho a devolución” bajo Factor-23?</h2>

        <p>Según las instrucciones del Formulario 22 y validaciones del SII, se incluyen:</p>

        <ul>
          <li>Rentas acogidas a regímenes especiales, como el artículo 14 ter letra A o B.</li>
          <li>Dividendos o retiros que provienen de registros SAC con créditos acumulados antes del 01.01.2017.</li>
          <li>Montos informados en DJ 1947 o 1948, que cumplen con los requisitos de devolución.</li>
          <li>Ingresos que no están sujetos a restitución del 35%, pero que no se clasifican bajo Factor-21.</li>
          <li>Utilidades distribuidas por empresas que ya pagaron IdPC, bajo regímenes antiguos o transitorios.</li>
        </ul>
        <p>
        Este factor afecta porque permite compensar el IdPC pagado contra el IGC o IA, y además genera devolución si hay excedente. Se aplica a rentas que no encajan en los factores tradicionales, pero que cumplen con los requisitos de devolución. Impacta directamente en el cálculo del impuesto final en el Formulario 22 y en la validación de las Declaraciones Juradas 1947 y 1948. Es clave para evitar observaciones como la G139 y para asegurar el uso correcto del crédito tributario.
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