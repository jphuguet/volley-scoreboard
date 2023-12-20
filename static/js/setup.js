console.log('Init index...');
const socket = io.connect();

const team_a_logo = document.getElementById('team_a_logo');
const team_b_logo = document.getElementById('team_b_logo');

// Add logos to dropdown list
socket.addEventListener("setup", (event) => {
    const files = JSON.parse(event)['files'];
    let i = 0;

    while (i < files.length) {
        f = files[i];
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = f;
        team_a_logo.appendChild(opt);
        
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = f;
        team_b_logo.appendChild(opt);    
        i++;
    }  
})

socket.addEventListener("all", (event) => {
    const data = JSON.parse(event);

    document.getElementById('team_a_name_input').value = data['a']['name'];
    document.getElementById('team_b_name_input').value = data['b']['name'];

});

team_a_logo.addEventListener("change", () => {
    const index = team_a_logo.selectedIndex;
    file = team_a_logo.options[index].innerHTML;
    set_logo('a', file)
});

team_b_logo.addEventListener("change", () => {
    const index = team_b_logo.selectedIndex;
    file = team_b_logo.options[index].innerHTML;
    set_logo('b', file)
});

function set_logo(team, file) {
    var data = {}
    data[team] = file
    socket.emit('team_logos',data);
}

function set_team_names()
{
    team_a_name = document.getElementById('team_a_name_input').value;
    team_b_name = document.getElementById('team_b_name_input').value;
    var names={  
        a : team_a_name,
        b : team_b_name
        };
    socket.emit('team_names',names);
}

function set_team_colors()
{
    const team_a_color = document.getElementById('team_a_color').value;
    const team_b_color = document.getElementById('team_b_color').value;
    var colors={  
        a : team_a_color,
        b : team_b_color
        };
    socket.emit('team_colors',colors);
}

const new_game = document.getElementById('new_game');
new_game.addEventListener('click', () => {
    socket.emit('new_game');
});

const team_a_name_input = document.getElementById('team_a_name_input');
team_a_name_input.addEventListener("blur", () => {
    set_team_names();
});

const team_b_name_input = document.getElementById('team_b_name_input');
team_b_name_input.addEventListener("blur", () => {
    set_team_names();
});

const team_a_color = document.getElementById('team_a_color');
team_a_color.addEventListener("change", () => {
    set_team_colors();
});

const team_b_color = document.getElementById('team_b_color');
team_b_color.addEventListener("change", () => {
    set_team_colors();
});
