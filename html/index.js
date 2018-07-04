var move = 0

$(document).ready(() => {
    let query = window.location.search.substring(1)
    let params = query.split("&")
    for (let param of params) {
        let pair = param.split('=')
        if (pair[0].toLowerCase() === 'game') {
            let script = document.createElement('script')
            script.type = 'text/javascript'
            script.src = `../results/${pair[1]}`
            document.head.appendChild(script)
            break
        }
    }
})

let update = {
    all: () => {
        update.board()
        update.controls()
        update.move()
        update.scores()
    },
    board: () => {
        for (let space in courseOfTheGame.boardHistory[move]) {
            $(`#space-${space}`).removeClass('black')
            $(`#space-${space}`).removeClass('white')
            if (courseOfTheGame.boardHistory[move][space] === 1) {
                $(`#space-${space}`).addClass('black')
            } else if (courseOfTheGame.boardHistory[move][space] === 2) {
                $(`#space-${space}`).addClass('white')
            }
        }
    },
    controls: () => {
        $('#prev-move').removeClass('disabled')
        $('#next-move').removeClass('disabled')

        if (move === 0) {
            $('#prev-move').addClass('disabled')
        }

        if (move === courseOfTheGame.moveHistory.length) {
            $('#next-move').addClass('disabled')
        }
    },
    move: () => {
        if (move === courseOfTheGame.moveHistory.length) {
            $('#move').html('')
        } else {
            $('#move').html(`${courseOfTheGame.moveHistory[move][0].join(', ')}
            <span class="fa fa-arrow-right"></span> ${courseOfTheGame.moveHistory[move][1]}`)
        }

        $('#move').removeClass('error')

        $('#move').removeClass('black')
        $('#move').removeClass('white')
        if (move % 2 === 0) {
            $('#move').addClass(courseOfTheGame.startPlayer === 1 ? 'black' : 'white')
        } else {
            $('#move').addClass(courseOfTheGame.startPlayer === 1 ? 'white' : 'black')
        }

        if (move === courseOfTheGame.moveHistory.length) {
            if (courseOfTheGame.exitReason) {
                $('#move').append(`<br>${courseOfTheGame.exitReason}`)
                $('#move').addClass('error')
            }
            $('#move').append(`<br>Player ${courseOfTheGame.winner} won the game`)
        }
    },
    scores: () => {
        if (courseOfTheGame.scoreHistory[move]) {
            $('#left').html(courseOfTheGame.scoreHistory[move][0])
            $('#right').html(courseOfTheGame.scoreHistory[move][1])
        }
    }
}

$('#next-move').click(() => {
    if (!$('#next-move').hasClass('disabled')) {
        move++
        update.all()
    }
})

$('#prev-move').click(() => {
    if (!$('#prev-move').hasClass('disabled')) {
        move--
        update.all()
    }
})
