document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor10");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-10</title>
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
        <h1>Factor-10</h1>
        <p>
            El Factor-10 representa partidas que están exentas de la Tasa Adicional del 10% establecida en el inciso tercero del artículo 21 de la Ley sobre Impuesto a la Renta (LIR). Estas partidas no generan obligación de pagar dicho recargo, ya sea por su naturaleza o por haber sido gravadas previamente.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Exentos de la Tasa Adicional del artículo 21”?</h2>

        <p>Según el artículo 21 de la LIR y criterios del SII, se incluyen:</p>

        <ul>
          <li>Gastos rechazados que no constituyen beneficio personal del propietario, socio o accionista.</li>
          <li>Indemnizaciones legales o pagos obligatorios que no implican retiro presunto.</li>
          <li>Ajustes contables sin efecto económico real, como correcciones de errores formales.</li>
          <li>Pagos a terceros que cumplen requisitos legales y tributarios, según el artículo 31 de la LIR.</li>
          <li>Partidas ya gravadas con el impuesto único del 40%, evitando doble tributación.</li>
          <li>Montos que no implican uso personal de activos de la empresa, como bienes arrendados o compartidos bajo contrato.</li>
        </ul>

        <p>
       Este factor afecta, porque: Permite excluir partidas del cálculo de la Tasa Adicional del 10%, evita que ciertos gastos sean considerados beneficios personales presuntos, mejora la precisión del Formulario 22 y de la Declaración Jurada 1909, reduce la carga tributaria adicional en contribuyentes del régimen semi-integrado, es clave para validar el cumplimiento tributario y evitar observaciones como la G33.

      </main>
    </body>
    </html>
      `);
    } else {
      alert("La ventana fue bloqueada por el navegador.");
    }
  });
});