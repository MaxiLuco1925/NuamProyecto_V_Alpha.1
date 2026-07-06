document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor17");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-17</title>
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
        <h1>Factor-17</h1>
        <p>
        Este factor se aplica cuando una empresa realiza una disminución de capital y devuelve parte del aporte original a sus socios o accionistas. Según el artículo 17 N°7 de la LIR, esta devolución no constituye renta, siempre que se impute correctamente al capital social reajustado y no a utilidades acumuladas.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Devolución de capital no constitutiva de renta”?</h2>

        <p>Según el artículo 17 N°7 de la LIR y criterios del SII, se incluyen:</p>

        <ul>
          <li>Montos devueltos por disminución de capital social, imputados al capital aportado reajustado.</li>
          <li>Transferencias de activos que representan devolución de aportes, no distribución de utilidades.</li>
          <li>Reembolsos de capital que no provienen de rentas acumuladas ni de utilidades pendientes de tributación.</li>
          <li>Operaciones autorizadas por el SII, que acreditan que la devolución no implica retiro presunto.</li>
        </ul>
        <p>
        Este factor afecta porque permite declarar correctamente la devolución de capital como ingreso no constitutivo de renta, evitando que se grave como retiro o utilidad. Requiere imputación ordenada: primero a utilidades tributables, luego al capital social. Es clave para evitar observaciones como la G33 y para validar la disminución de capital en el Formulario 22 y en la Declaración Jurada 1939.
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