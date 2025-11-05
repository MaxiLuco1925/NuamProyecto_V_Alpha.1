document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor36");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-36</title>
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
        <h1>Factor-36</h1>
        <p>
        El TEX (Tasa Efectiva del Crédito del FUNT) se aplica cuando se distribuyen utilidades no tributables acumuladas antes del 01.01.2017, que están registradas en el FUNT. Aunque estas utilidades no forman parte de la base imponible, pueden tener crédito por IdPC asociado, el cual debe ser asignado proporcionalmente mediante esta tasa.
        </p>

        <h2>¿Qué tipo de ingresos se consideran bajo Factor-36?</h2>

        <ul>
          <li>Utilidades no tributables acumuladas al 31.12.2016, registradas en el FUNT.</li>
          <li>Retiros, remesas o dividendos que provienen de ese fondo.</li>
          <li>Créditos por IdPC asociados, que deben ser asignados proporcionalmente.</li>
          <li>Montos informados en DJ 1813, que requieren aplicación del TEX para validar el crédito.</li>
          <li>Situaciones donde el crédito no puede ser asignado directamente, sino mediante tasa efectiva.</li>
        </ul>
        <p>
        Este factor afecta porque evita la sobreasignación de crédito, asegurando que el IdPC asociado al FUNT se distribuya correctamente entre las utilidades retiradas. Es clave para validar la coherencia entre el registro FUNT, el Formulario 22 y las declaraciones juradas, y para evitar observaciones como la G139 o inconsistencias en la DJ 1813.
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