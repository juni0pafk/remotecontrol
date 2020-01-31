let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')
let stop = document.getElementById('stop')
let img = document.getElementById('img')

function atualiza_imagem() {
    fetch('/get_last_image')
    .then(resp => {
        resp.arrayBuffer().then(buffer => {
            let base64Flag = 'data:image/jpeg;base64,';
            let imageStr = arrayBufferToBase64(buffer);
            img.src = base64Flag + imageStr
        })
    })
}

function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = [].slice.call(new Uint8Array(buffer));
  
    bytes.forEach((b) => binary += String.fromCharCode(b));
  
    return window.btoa(binary);
  };
  

down.addEventListener('click',() => 
    fetch('/down_side')
    .then(resp => resp.ok ? atualiza_imagem() : "" )
)


up.addEventListener('click',() => 
    fetch('/up_side')
    .then(atualiza_imagem())
)
left.addEventListener('click',() => 
    fetch('/left_side')
    .then(atualiza_imagem())
)

right.addEventListener('click',() => 
    fetch('/right_side')
    .then(atualiza_imagem())
)

stop.addEventListener('click',() => 
    fetch('/stop')
    .then(atualiza_imagem())
)
