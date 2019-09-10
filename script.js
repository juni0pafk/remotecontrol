function Frente(){
    console.log("para frente")
    socket.emit('frente')
}

function Atras(){
    console.log("para trás")
    socket.emit('atras')
}

function Esquerda(){
    console.log("para esquerda")
    socket.emit('esquerda')
}

function Direita(){
    console.log("para direita")
    socket.emit('direita')
}