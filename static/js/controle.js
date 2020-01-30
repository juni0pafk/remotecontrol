let down = document.getElementById('down')
let up = document.getElementById('up')
let left = document.getElementById('left')
let right = document.getElementById('right')
let stop = document.getElementById('stop')

down.addEventListener('click',()=>fetch('/down_side'))
up.addEventListener('click',()=>fetch('/up_side'))
left.addEventListener('click',()=>fetch('/left_side'))
right.addEventListener('click',()=>fetch('/right_side'))

stop.addEventListener('click',()=>fetch('/stop'))
