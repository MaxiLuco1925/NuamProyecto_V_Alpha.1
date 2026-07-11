document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor18");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-18</title>
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
        <h1>Factor-18</h1>
        <p>
        Este factor se aplica a ingresos que, por disposición legal, están exentos de los impuestos finales que gravan a las personas naturales (IGC) o a los no residentes (IA). Aunque pueden formar parte de la renta bruta global para ciertos efectos, no generan carga tributaria directa.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Exentos de IGC y/o IA”?</h2>

        <p>Según el artículo 17 y otros de la LIR, además de instrucciones del SII, se incluyen:</p>

        <ul>
          <li>Rentas provenientes de beneficios previsionales, como pensiones o jubilaciones exentas.</li>
          <li>Ingresos por Ley de Bosques, acogidos al Decreto Supremo N°4363 de 1931.</li>
          <li>Donaciones recibidas, en ciertos regímenes y bajo condiciones específicas.</li>
          <li>Indemnizaciones por seguros, que no generan ganancia ni utilidad.</li>
          <li>Intereses o rentas de instrumentos exentos, como ciertos depósitos a plazo o bonos estatales.</li>
          <li>Rentas percibidas por personas naturales o jurídicas no residentes, cuando están exentas del IA por convenios de doble tributación.</li>
        </ul>
        <p>
        Este factor afecta porque permite declarar correctamente rentas que no deben tributar bajo el IGC o IA. Evita que se integren erróneamente a la base imponible, mejora la precisión del Formulario 22 y de las declaraciones juradas como la 1926 o 1943. Es clave para evitar observaciones como la G33 y para validar beneficios tributarios otorgados por ley.
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