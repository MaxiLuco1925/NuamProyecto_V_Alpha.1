document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor33");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-33</title>
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
        <h1>Factor-33</h1>
        <p>
        Este factor se utiliza en el Formulario 22 para declarar el crédito por impuestos efectivamente pagados en el extranjero, cuando un contribuyente chileno obtiene rentas fuera del país. Su objetivo es evitar la doble tributación internacional, permitiendo imputar el IPE contra el impuesto chileno que afecta esas rentas.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sujetos a crédito por IPE”?</h2>

        <p>Según el artículo 41 A de la LIR y las Circulares N°31/2021 y N°73/2020 del SII, se incluyen:</p>

        <ul>
          <li>Dividendos, intereses, regalías o ganancias de capital obtenidas en el extranjero.</li>
          <li>Rentas de fuente extranjera percibidas por personas naturales o jurídicas domiciliadas en Chile.</li>
          <li>Impuestos efectivamente pagados en el país de origen, acreditados mediante documentación válida.</li>
          <li>Ingresos que se integran al IGC o IA, y que cumplen con los requisitos de control y registro exigidos por el SII.</li>
          <li>Contribuyentes con derecho al crédito IPE, según convenios bilaterales o normas unilaterales.</li>
        </ul>
        <p>
        Este factor afecta porque permite reducir la carga tributaria total del contribuyente, evitando pagar dos veces por la misma renta. Es clave para validar correctamente operaciones internacionales, evitar observaciones como la G139, y asegurar el uso correcto del crédito en contextos de inversión o actividad fuera de Chile.
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