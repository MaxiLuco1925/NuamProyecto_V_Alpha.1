document.addEventListener('DOMContentLoaded', function(){
    const FACTOR_CALC_START = 8;
    const FACTOR_CALC_END = 37;
    

    const switchMontos = document.getElementById('ingresoPorMontos');
    const seccionMontos = document.getElementById('seccionMontos');
    const factorInputs = document.querySelectorAll('.factor-input');
    const montoInputs = document.querySelectorAll('.monto-input');
    const btnCalcular = document.getElementById('btnCalcular');


    function toggleMontosSection(){
        if(switchMontos.checked) {
            seccionMontos.style.display = 'block';
            factorInputs.forEach(input => {
                input.setAttribute('readonly', 'readonly');
                input.classList.add('bg-light');
                input.value = '0.00'; 
            });
        } else {
            seccionMontos.style.display = 'none';
            factorInputs.forEach(input => {
                input.removeAttribute('readonly');
                input.classList.remove('bg-light');
            });
        }
    }


    if(btnCalcular){
        btnCalcular.addEventListener('click', function(){
            let totalMontos = 0;
            let sumaFactoresFinal = 0;
            
            const valoresMontos = {}; 

            montoInputs.forEach(input => {
                const id = input.id.split('_')[1];
                const value = parseFloat(input.value) || 0;
                valoresMontos[id] = value;
                totalMontos += value;
            });
            
            if(totalMontos === 0){
                alert("Error: El total de los Montos ingresados es igual a 0. ¡No se puede calcular!");
                return;
            }
            
            for (let n = FACTOR_CALC_START; n <= FACTOR_CALC_END; n++) {
                const input = document.getElementById(`id_factor_${n}`);
                if (!input) continue;

                let calculo = 0;
            
                if (n >= 8 && n <= 19) {
                    const montoIndex = n - 7; 
                    
                    const montoAsociado = valoresMontos[montoIndex.toString()] || 0;
                    
                    if (montoAsociado > 0) {
                        calculo = montoAsociado / totalMontos;
                    }

                } else {
        
                    calculo = 0;
                }
                
                input.value = calculo.toFixed(6);
                sumaFactoresFinal += calculo;
            }
            
            if (Math.round(sumaFactoresFinal * 1000000) > 1000000) {
                alert(` Advertencia: La suma de los factores (${sumaFactoresFinal.toFixed(6)}) excede el límite de 1.00. Revise los montos ingresados.`);
            } else {
                alert(" El Monto de los factores ha sido calculado de forma exitosa y la suma es válida.");
            }
        });
    }


    toggleMontosSection(); 
    switchMontos.addEventListener('change', toggleMontosSection);
});