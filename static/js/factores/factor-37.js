document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor37");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-37</title>
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
        <h1>Factor-37</h1>
        <p>
        Este factor se aplica cuando una empresa realiza una devolución de capital a sus socios o accionistas. Según el artículo 17 N°7 de la LIR, no constituye renta si la devolución se realiza sobre el capital social efectivamente aportado y reajustado. Sin embargo, si se imputa a utilidades acumuladas no tributadas, se considera renta y se grava con Impuesto de Primera Categoría (IdPC) y luego con IGC o IA, según corresponda.
        </p>

        <h2>¿Qué tipo de devoluciones se consideran bajo Factor-37?</h2>

        <p>Según el SII y doctrina tributaria vigente, se incluyen:</p>

        <ul>
          <li>Reembolsos de aportes de capital realizados por socios o accionistas, debidamente reajustados.</li>
          <li>Disminuciones de capital social, siempre que no afecten utilidades tributables.</li>
          <li>Distribuciones que no excedan el monto del capital aportado, según registros contables.</li>
          <li>Montos informados en DJ 1938, que acreditan la devolución de capital.</li>
          <li>Operaciones que cumplen el orden de imputación legal: primero a utilidades, luego a capital.</li>
        </ul>
        <p>
        Evita que se califiquen como renta operaciones que son meramente patrimoniales, como la devolución de aportes. Sin embargo, si se imputa a utilidades, se genera carga tributaria. Este factor es clave para validar correctamente la DJ 1938, evitar observaciones como la G139, y asegurar la coherencia entre registros contables y tributarios.
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