let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')
let stop = document.getElementById('stop')
let img = document.getElementById('img')

function atualiza_imagem(resp) {
    img.src = '/camera/'+resp    
}

down.addEventListener('click',() => 
    fetch('/down_side')
    .then(resp =>  resp.text().then(atualiza_imagem(text)))
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
