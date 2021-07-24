const btn = document.querySelectorAll('.btn-danger');


if(btn){
    const btnArray = Array.from(btn);
    btnArray.forEach((btn)=>{
        btn.addEventListener('click',(e)=>{
            if(!confirm('Eliminar contacto?')){
                e.preventDefault()
            };
        });
    });   
};
