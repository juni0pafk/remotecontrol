let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')
let stop = document.getElementById('stop')
let save = document.getElementById('save')
let img = document.getElementById('img')
let msg = document.getElementById('msg')
let auto = document.getElementById('auto')
let manual = document.getElementById('manual')

function atualiza_imagem(resp) {
    img.src = '/camera/'+resp    
}

down.addEventListener('click',() => 
    fetch('/down_side')
    .then(resp =>  resp.text().then(text => atualiza_imagem(text)))
)


up.addEventListener('click',() => 
    fetch('/up_side')
    .then(resp =>  resp.text().then(text => atualiza_imagem(text)))
)
left.addEventListener('click',() => 
    fetch('/left_side')
    .then(resp =>  resp.text().then(text => atualiza_imagem(text)))
)

right.addEventListener('click',() => 
    fetch('/right_side')
    .then(resp =>  resp.text().then(text => atualiza_imagem(text)))
)

stop.addEventListener('click',() => 
    fetch('/stop')
    .then(resp =>  resp.text().then(text => atualiza_imagem(text)))
)

save.addEventListener('click', () => {
    fetch('/save')
    .then(resp => resp.text())
    .then(text => {
        msg.innerHTML = "Dados salvos no arquivo "+text
    })
})

auto.addEventListener('click', () => {
    fetch('/autonomous_mode')
    .then(resp => {
        if(resp.ok){
            msg.innerHTML = "Modo autônomo iniciado!"
        }
    })
})

manual.addEventListener('click',()=>{
    fetch('/stop_autonomous')
    .then(resp => {
        if(resp.ok){
            msg.innerHTML = "Modo autônome desligado!"
        }
    })
})
