function confirmarActualizacion(idCalificacion) {
    return confirm("¿Está seguro que desea actualizar la calificacion " + idCalificacion + "?");
}

function confirmarEliminacion(idCalificacion) {
    return confirm("¿Está seguro que desea eliminar la calificacion " + idCalificacion + "?\n\nEsta acción no se puede deshacer.");
}