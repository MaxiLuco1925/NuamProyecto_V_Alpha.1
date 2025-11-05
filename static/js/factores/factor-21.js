document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor21");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-21</title>
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
        <h1>Factor-21</h1>
        <p>
        Este factor se aplica a rentas que han sido efectivamente gravadas con IdPC, y cuyo crédito puede ser usado para compensar el impuesto personal del contribuyente. Si el monto del crédito es mayor que el impuesto determinado, el excedente puede ser devuelto por la Tesorería General de la República.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Con derecho a devolución”?</h2>

        <p>Según el artículo 20 de la LIR y criterios del SII, se incluyen:</p>

        <ul>
          <li>Utilidades retiradas o distribuidas desde empresas que ya pagaron IdPC.</li>
          <li>Dividendos percibidos por personas naturales residentes, con crédito por IdPC completo.</li>
          <li>Rentas acumuladas que se integran al sistema atribuido o semi-integrado, con derecho a devolución.</li>
          <li>Montos registrados en líneas 1 a 8 del Formulario 22, que cumplen con los requisitos de devolución.</li>
          <li>Ingresos que no están sujetos a restitución del 35%, como en el régimen atribuido.</li>
        </ul>
        <p>
        Este factor afecta porque permite compensar el IdPC pagado contra el IGC o IA, y además genera devolución si hay excedente. Mejora la eficiencia tributaria del contribuyente, impacta directamente en el cálculo del impuesto final en el Formulario 22 y en la validación de la Declaración Jurada 1947. Es clave para evitar observaciones como la G139 y para asegurar el uso correcto del crédito tributario.
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