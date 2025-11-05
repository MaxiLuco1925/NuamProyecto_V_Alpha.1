document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor29");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-29</title>
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
        <h1>Factor-29</h1>
        <p>
        Este factor se aplica a montos que fueron registrados como crédito por IdPC, pero que no pueden ser utilizados para rebajar el Impuesto Global Complementario (IGC) ni el Impuesto Adicional (IA), y tampoco pueden ser devueltos. Se trata de un crédito informativo, que debe ser reportado por transparencia tributaria, pero no tiene efecto compensatorio ni reembolsable.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sin derecho a devolución” bajo Factor-29?</h2>

        <p>Según criterios del SII y validaciones del Formulario 22, se incluyen:</p>

        <ul>
          <li>Gastos rechazados del artículo 21 de la LIR, cuando no cumplen requisitos para imputación.</li>
          <li>Créditos por IdPC asociados a rentas exentas o no constitutivas de renta, que no permiten devolución.</li>
          <li>Montos informados por terceros, donde el crédito no corresponde al declarante.</li>
          <li>Partidas que no fueron efectivamente gravadas con IdPC, pero que se informan por trazabilidad.</li>
          <li>Regímenes especiales o transitorios, donde el crédito no genera efecto tributario directo.</li>
        </ul>
        <p>
        Este factor afecta porque representa créditos que deben ser informados, pero que no pueden ser usados ni devueltos. Es clave para mantener la coherencia entre registros contables y tributarios, evitar observaciones como la G33, y validar correctamente partidas informativas en el Formulario 22.
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