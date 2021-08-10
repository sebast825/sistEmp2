const btn = document.querySelectorAll('.btn-danger');


if(btn){
    const btnArray = Array.from(btn);
    btnArray.forEach((btn)=>{
        btn.addEventListener('click',(e)=>{
            if(!confirm('Delete Contact?')){
                e.preventDefault()
            };
        });
    });   
};
