let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')
let stop = document.getElementById('stop')

down.addEventListener('touchstart',()=>fetch('/down_side'))
up.addEventListener('touchstart',()=>fetch('/up_side'))
left.addEventListener('touchstart',()=>fetch('/left_side'))
right.addEventListener('touchstart',()=>fetch('/right_side'))

stop.addEventListener('click',()=>fetch('/stop'))
