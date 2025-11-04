document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor16");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-16</title>
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
        <h1>Factor-16</h1>
        <p>
        Este factor se aplica a montos que fueron acogidos a un régimen tributario especial o transitorio, pero que la ley clasifica como no constitutivos de renta. Aunque no generan obligación de pago de impuestos personales, deben ser registrados y declarados correctamente para evitar observaciones o inconsistencias.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “No Constitutivos de Renta acogidos a impuesto”?</h2>

        <p>Según el artículo 17 de la LIR y disposiciones del SII, se incluyen:</p>

        <ul>
          <li>Devoluciones de capital que fueron acogidas a tributación en etapas anteriores.</li>
          <li>Aportes de capital registrados como ingresos en ciertos regímenes, pero que no constituyen renta.</li>
          <li>Indemnizaciones o beneficios previsionales que fueron informados como renta, pero luego reclasificados.</li>
          <li>Distribuciones de utilidades que ya tributaron en el régimen atribuido o semi-integrado, y que no deben volver a hacerlo.</li>
          <li>Montos acogidos a regímenes especiales, como el artículo 14 ter, que luego se reclasifican como no renta.</li>
        </ul>
        <p>
        Este factor afecta porque permite declarar correctamente ingresos que no deben tributar, pero que fueron acogidos a un régimen impositivo. Evita duplicidad en la carga tributaria, mejora la trazabilidad fiscal y asegura la correcta clasificación en el Formulario 22 y en declaraciones juradas como la 1947 o 1939. Es clave para evitar observaciones como la G33 y para mantener la coherencia entre registros contables y tributarios.
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