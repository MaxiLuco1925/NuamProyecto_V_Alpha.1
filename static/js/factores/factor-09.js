document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor09");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-09</title>
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
        <h1>Factor-09</h1>
        <p>
            El "factor-09" se refiere a un coeficiente usado para calcular el crédito por Impuesto de Primera Categoría (IdPC) en Chile, cuando este afecta el Global Complementario (GI) y puede ser objeto de devolución.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Afectos a GI con derecho a crédito y devolución”?</h2>

        <p>Según el artículo 56 y otros del LIR, estos incluyen:</p>

        <ul>
          <li>Utilidades retiradas o distribuidas desde empresas que ya pagaron IdPC.</li>
          <li>Dividendos percibidos por personas naturales residentes en Chile.</li>
          <li>Rentas que provienen de actividades comerciales, industriales, mineras, agrícolas o de servicios.</li>
          <li>Montos que se integran al Global Complementario y permiten usar el crédito por IdPC.</li>
          <li>Rentas que no están exentas ni acogidas a regímenes especiales de no tributación.</li>
        </ul>

        <p>
        Este factor afecta, porque:	Define qué parte del monto tributa en el Global Complementario permite imputar el crédito por IdPC contra el impuesto personal Puede generar devolución si el crédito excede el impuesto determinado Modifica la carga tributaria final del contribuyente Es clave para la correcta aplicación del sistema semi-integrado o atribuido, según el régimen vigente.
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