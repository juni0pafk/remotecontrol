let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')
let stop = document.getElementById('stop')
let img = document.getElementById('img')

function atualiza_imagem() {
    fetch('/get_last_image')
    .then(resp => resp.blob())
    .then(resp => img.src = URL.createObjectURL(resp))
}

down.addEventListener('click',() => 
    fetch('/down_side')
    .then(() => atualiza_imagem())
)


up.addEventListener('click',() => 
    fetch('/up_side')
    .then(() => atualiza_imagem())
)
left.addEventListener('click',() => 
    fetch('/left_side')
    .then(() => atualiza_imagem())
)

right.addEventListener('click',() => 
    fetch('/right_side')
    .then(() => atualiza_imagem())
)

stop.addEventListener('click',() => 
    fetch('/stop')
    .then(() => atualiza_imagem())
)
