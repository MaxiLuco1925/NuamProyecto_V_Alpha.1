document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor28");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-28</title>
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
        <h1>Factor-28</h1>
        <p>
        Este factor se aplica cuando un contribuyente chileno obtiene rentas de fuente extranjera que ya fueron gravadas en otro país. Para evitar la doble tributación, Chile permite imputar esos impuestos pagados en el exterior como crédito tributario, bajo condiciones específicas. El crédito por IPE puede ser unilateral o bilateral, dependiendo de si existe convenio para evitar la doble tributación.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sujetos a crédito por IPE”?</h2>

        <p>Según el artículo 41 A de la LIR y la Circular N°31 del SII, se incluyen:</p>

        <ul>
          <li>Dividendos, intereses, regalías o ganancias de capital obtenidas fuera de Chile.</li>
          <li>Rentas de fuente extranjera percibidas por personas naturales o jurídicas domiciliadas en Chile.</li>
          <li>Impuestos efectivamente pagados en el extranjero, acreditados mediante documentación válida.</li>
          <li>Ingresos que se integran al IGC o IA, y que cumplen con los requisitos de control y registro exigidos por el SII.</li>
          <li>Contribuyentes con derecho al crédito IPE, según convenios vigentes o normas unilaterales.</li>
        </ul>
        <p>
        Este factor afecta porque permite imputar contra el impuesto chileno los tributos pagados en el extranjero, evitando la doble tributación. Está sujeto a límites de proporcionalidad, topes diferenciados por tipo de renta, y requiere documentación formal. Impacta directamente en el cálculo del impuesto final en el Formulario 22 y en la validación de la Declaración Jurada 1929.
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