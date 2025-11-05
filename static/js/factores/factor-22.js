document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor22");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-22</title>
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
        <h1>Factor-22</h1>
        <p>
        Este factor se aplica a créditos por Impuesto de Primera Categoría (IdPC) que no dan derecho a devolución, y que además no pueden ser imputados directamente por el contribuyente en su declaración personal. Son créditos informativos, sin efecto tributario directo en el cálculo del impuesto final.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sin derecho a devolución ni imputación directa”?</h2>

        <p>Según criterios del SII y la estructura del Formulario 22, se incluyen:</p>

        <ul>
          <li>Créditos por IdPC asociados a rentas exentas o no constitutivas de renta, que no permiten devolución.</li>
          <li>Montos informativos que deben ser reportados por transparencia, pero que no generan compensación.</li>
          <li>Ingresos percibidos por terceros, donde el crédito no corresponde al declarante.</li>
          <li>Partidas que no cumplen requisitos formales para imputación, como falta de respaldo o documentación.</li>
        </ul>
        <p>
        Este factor afecta porque representa créditos que no pueden ser usados ni devueltos, pero deben ser informados para mantener la trazabilidad fiscal. No generan efecto en el cálculo del impuesto final, pero son clave para evitar observaciones como la G33 y para validar la coherencia entre registros contables y tributarios.
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