var move = 0

var courseOfTheGame

$.getJSON('../course_of_the_game.json', json => {
    courseOfTheGame = json
    update.all()
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
            if (courseOfTheGame.boardHistory[move][space] === 0) {
                $(`#space-${space}`).removeClass('black')
                $(`#space-${space}`).removeClass('white')
            } else if (courseOfTheGame.boardHistory[move][space] === 1) {
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

        if (move === courseOfTheGame.moveHistory.length - 1) {
            $('#next-move').addClass('disabled')
        }
    },
    move: () => {
        $('#move').html(`${courseOfTheGame.moveHistory[move][0].join(', ')}
        <span class="fa fa-arrow-right"></span> ${courseOfTheGame.moveHistory[move][1]}`)
        $('#move').removeClass('error')

        $('#move').removeClass('black')
        $('#move').removeClass('white')
        if (move % 2 === 0) {
            $('#move').addClass(courseOfTheGame.startPlayer === 1 ? 'black' : 'white')
        } else {
            $('#move').addClass(courseOfTheGame.startPlayer === 1 ? 'white' : 'black')
        }

        if (move === courseOfTheGame.moveHistory.length - 1) {
            if (courseOfTheGame.exitReason !== undefined) {
                $('#move').append(`<br>${courseOfTheGame.exitReason}`)
                $('#move').addClass('error')
            }
            $('#move').append(`<br>Player ${courseOfTheGame.winner} won the game`)
        }
    },
    scores: () => {
        $('#left').html(courseOfTheGame.scoreHistory[move][0])
        $('#right').html(courseOfTheGame.scoreHistory[move][1])
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
