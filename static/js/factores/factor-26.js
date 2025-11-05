document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor26");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-26</title>
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
        <h1>Factor-26</h1>
        <p>
        Este factor se utiliza en el Formulario 22 para declarar créditos por IdPC sin derecho a devolución, asociados a rentas que no han sido efectivamente gravadas con dicho impuesto. Aunque el crédito puede ser usado para compensar el IGC, no puede ser devuelto si hay remanente. Es una categoría informativa y compensatoria, pero no reembolsable.        
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Sin derecho a devolución” bajo Factor-26?</h2>

        <p>Según el SII, se incluyen:</p>

        <ul>
          <li>Gastos rechazados del artículo 21 de la Ley de la Renta, especialmente en empresas individuales o sociedades de hecho.</li>
          <li>Créditos por IdPC registrados en las líneas 1 a 8 del Formulario 22, cuando no provienen de rentas efectivamente gravadas.</li>
          <li>Montos que solo permiten imputación parcial, como contra el IGC, débito fiscal o reintegros anticipados, pero no devolución.</li>
          <li>Partidas informativas que deben ser reportadas por transparencia, sin efecto reembolsable.</li>
        </ul>
        <p>
        Este factor afecta porque limita el uso del crédito tributario: permite compensar, pero no recuperar excedentes. Es clave para evitar errores en el cálculo del impuesto final, observaciones como la G139, y para validar correctamente partidas como gastos rechazados o rentas no gravadas.
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