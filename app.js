let tg = window.Telegram.WebApp

if (tg) {
    tg.expand()
}

let user = tg.initDataUnsafe.user

let coins = 0

const tapButton = document.getElementById('tapButton')
const coinText = document.getElementById('coinText')


function saveCoins(){

    fetch('/save', {
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            user_id:user.id,
            coins:coins
        })
    })

}


function createAnimation(x, y){

    let plus = document.createElement('div')

    plus.innerHTML = '+1'

    plus.classList.add('plus-one')

    plus.style.left = x + 'px'
    plus.style.top = y + 'px'

    document.body.appendChild(plus)

    setTimeout(()=>{
        plus.remove()
    },700)

}


function tapEffect(){

    coins += 1

    coinText.innerHTML = coins

    saveCoins()

}


tapButton.addEventListener('click', (e)=>{

    tapEffect()

    createAnimation(
        e.pageX,
        e.pageY
    )

})