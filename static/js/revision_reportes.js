function marcarRevisado(reporteid){
    const reporItem = document.getElementById (`report-item-${reportId}`)
    if (reporItem){
     reporItem.style.opacity = '0';
     reporItem.style.transition = 'opacity 0.3s';
     setTimeout(() => {
        reporItem.remove();
     }, 300);
    }

    const alerta = document.getElementById('alerta-dinamica');
    if(alerta){
        alerta.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                El reporte ha sido marcado como <strong>revisado</strong>. Su estado ahora es: <em>En proceso</em>.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }


}