document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor24");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-24</title>
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
        <h1>Factor-24</h1>
        <p>
        Este factor se aplica a créditos por Impuesto de Primera Categoría (IdPC) que no dan derecho a devolución, pero que sí pueden ser imputados directamente por el contribuyente en su declaración personal. Se diferencia del Factor-22 porque sí tiene efecto tributario compensable, aunque no reembolsable.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Con crédito sin derecho a devolución” bajo Factor-24?</h2>

        <p>Según criterios del SII y validaciones del Formulario 22, se incluyen:</p>

        <ul>
          <li>Créditos por IdPC asociados a utilidades retiradas o distribuidas desde empresas acogidas a regímenes sin devolución.</li>
          <li>Dividendos percibidos por personas naturales residentes, con crédito sujeto a restitución del 35%.</li>
          <li>Rentas que se integran al Impuesto Global Complementario (IGC), pero no cumplen requisitos de devolución.</li>
          <li>Montos registrados en líneas compensables del F22, sin excedente reembolsable.</li>
          <li>Ingresos que provienen de regímenes semi-integrados o especiales con restricción de devolución.</li>
        </ul>
        <p>
        Este factor afecta porque permite compensar el IdPC pagado contra el IGC o IA, pero no genera devolución si hay excedente. Tiene efecto directo en el cálculo del impuesto final en el Formulario 22 y en la validación de la Declaración Jurada 1947. Es clave para evitar observaciones como la G139 y para asegurar el uso correcto del crédito tributario en regímenes sin devolución.
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