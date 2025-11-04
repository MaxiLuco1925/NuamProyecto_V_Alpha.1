document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor14");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-14</title>
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
        <h1>Factor-14</h1>
        <p>
          El Factor-14 representa el crédito por Impuesto de Primera Categoría (IdPC) asociado a rentas que están exentas del Impuesto Global Complementario (GI), pero cuya compensación no permite devolución del IdPC si el crédito excede el impuesto personal. Es decir, el crédito se puede usar hasta el monto del impuesto determinado, pero no se devuelve el excedente.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Exentos de GI con derecho a compensación sin devolución”?</h2>

        <p>Según el artículo 40 de la Ley sobre Impuesto a la Renta (LIR) y criterios del SII, se incluyen:</p>

        <ul>
          <li>Utilidades retiradas o distribuidas desde empresas acogidas al régimen semi-integrado.</li>
          <li>Utilidades distribuidas a personas naturales que cumplen requisitos de exención, pero están acogidas a regímenes sin devolución.</li>
          <li>Dividendos o retiros que no se integran al GI por estar exentos, pero que generan crédito por IdPC limitado.</li>
          <li>Ingresos percibidos por contribuyentes exentos del GI, como ciertos pensionados o rentistas, sin derecho a devolución.</li>
          <li>Montos que ya tributaron en etapas anteriores, pero que no permiten devolución del crédito.</li>
        </ul>
        <p>
            Este factor afecta porque permite compensar el IdPC pagado contra el GI, pero no genera devolución si hay excedente. Limita el uso del crédito en regímenes exentos, afectando la eficiencia tributaria. Impacta directamente en el cálculo del impuesto final en el Formulario 22 y en la validación de la Declaración Jurada 1943. Es clave para evitar observaciones como la G139, que controlan el uso correcto del crédito.        </p>
      </main>
    </body>
    </html>
      `);
    } else {
      alert("La ventana fue bloqueada por el navegador.");
    }
  });
});