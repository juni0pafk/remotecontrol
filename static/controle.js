let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')

down.addEventListener('touchstart',()=>fetch('/down_side'))
// down.addEventListener('touchend',()=>fetch('/stop'))

up.addEventListener('touchstart',()=>fetch('/up_side'))
// up.addEventListener('touchend',()=>fetch('/stop'))

left.addEventListener('touchstart',()=>fetch('/left_side'))
// left.addEventListener('touchend',()=>fetch('/stop'))

right.addEventListener('touchstart',()=>fetch('/right_side'))
// right.addEventListener('touchend',()=>fetch('/stop'))