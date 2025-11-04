document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor12");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-12</title>
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
        <h1>Factor-12</h1>
        <p>
          El Factor-12 representa el crédito por Impuesto de Primera Categoría (IdPC) asociado a rentas que están exentas del Impuesto Global Complementario (GI), pero que igualmente permiten compensación y devolución del IdPC pagado por la empresa.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Exentos de GI con derecho a crédito y devolución”?</h2>

        <p>Según el artículo 40 N°7 de la Ley sobre Impuesto a la Renta (LIR) y criterios del SII, se incluyen:</p>

        <ul>
          <li>Rentas exentas del GI por disposición legal, como aquellas que no superan el límite de 1.440 UTM anuales.</li>
          <li>Utilidades distribuidas a personas naturales que cumplen requisitos de exención.</li>
          <li>Dividendos o retiros que no se integran al GI por estar acogidos a regímenes especiales.</li>
          <li>Montos que ya tributaron en etapas anteriores, pero que aún generan crédito por IdPC.</li>
          <li>Ingresos percibidos por contribuyentes exentos del GI, como ciertos pensionados o rentistas.</li>
        </ul>
        <p>
          Este factor afecta, porque: Permite compensar el IdPC pagado por la empresa, incluso si el ingreso está exento del GI, puede generar devolución si el crédito excede el impuesto personal determinado, mejora la eficiencia tributaria del contribuyente, es clave para validar el uso del crédito en el Formulario 22 y en la Declaración Jurada 1943, evita la pérdida del crédito por IdPC en casos de exención legal.
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