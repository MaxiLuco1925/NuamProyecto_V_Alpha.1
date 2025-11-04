document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnFactor13");

  btn.addEventListener("click", () => {
    const nuevaVentana = window.open("", "_blank", "width=1980,height=1080");

    if (nuevaVentana) {
      nuevaVentana.document.write(`
        <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Factor-13</title>
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
        <h1>Factor-13</h1>
        <p>
          Este factor se aplica a rentas que sí se integran al GI, permitiendo usar el crédito por IdPC para compensar el impuesto personal, pero sin derecho a devolución si el crédito es mayor al impuesto determinado. Es común en regímenes semi-integrados, donde el crédito por IdPC está sujeto a restitución parcial.
        </p>

        <h2>¿Qué tipo de ingresos se consideran “Afectos a GI con derecho a compensación sin devolución”?</h2>

        <p>Según el artículo 14 A de la Ley sobre Impuesto a la Renta (LIR) y observaciones como la G139 del SII se incluyen : </p>

        <ul>
          <li>Utilidades retiradas o distribuidas desde empresas acogidas al régimen semi-integrado.</li>
          <li>Dividendos percibidos por personas naturales residentes, con crédito por IdPC sujeto a restitución del 35%.</li>
          <li>Montos que generan crédito por IdPC, pero que no pueden ser devueltos si el impuesto personal es menor.</li>
          <li>Ingresos que se integran al GI, pero cuyo crédito está limitado por norma legal.</li>
        </ul>
        <p>
          Este factor afecta porque permite compensar el IdPC pagado contra el GI, pero no genera devolución si hay excedente. Requiere aplicar la restitución del 35% del crédito por IdPC en regímenes semi-integrados. Impacta directamente en el cálculo del impuesto final en el Formulario 22 (códigos 608, 610, 1592). Es clave para evitar observaciones como la G139, que controlan el uso correcto del crédito.
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