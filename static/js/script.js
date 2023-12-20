
console.log('Init...');
const socket = io.connect();

socket.addEventListener("logos", (event) => {
    const data = JSON.parse(event);
    set_logos(data);
})

function set_logos(data) {
    path = "/static/logos/"
    logo_a = data['a']['logo'];
    logo_b = data['b']['logo']
    if (logo_a == 'None' || logo_b == 'None') {
        document.getElementById('team_a_logo_col').style.display = "None";
        document.getElementById('team_b_logo_col').style.display = "None";
    } else {
        document.getElementById('team_a_logo_col').style.display = "table-cell";
        document.getElementById('team_b_logo_col').style.display = "table-cell";
        img_a = document.getElementById('team_a_logo');
        img_b = document.getElementById('team_b_logo');
        img_a.src = path + encodeURI(logo_a);
        img_b.src = path + encodeURI(logo_b);
    }
}

socket.addEventListener("all", (event) => {
    const data = JSON.parse(event);
    // console.log(data);

    const current_set = data['set'];
    const team_a_name = data['a']['name'];
    const team_b_name = data['b']['name'];

    set_logos(data);
    
    
    
    if (document.getElementById('remote') != null) {        
        // print team name above control buttons
        document.getElementById('team_a_name_btns').textContent = team_a_name;
        document.getElementById('team_b_name_btns').textContent = team_b_name;
    }

    // score table
    document.getElementById('team_a_name').textContent = team_a_name;
    document.getElementById('team_a_set_1').textContent = data['a'][1];
    document.getElementById('team_a_set_2').textContent = data['a'][2];
    document.getElementById('team_a_set_3').textContent = data['a'][3];
    document.getElementById('team_a_set_4').textContent = data['a'][4];
    document.getElementById('team_a_set_5').textContent = data['a'][5];
    
    document.getElementById('team_b_name').textContent = team_b_name;
    document.getElementById('team_b_set_1').textContent = data['b'][1];
    document.getElementById('team_b_set_2').textContent = data['b'][2];
    document.getElementById('team_b_set_3').textContent = data['b'][3];
    document.getElementById('team_b_set_4').textContent = data['b'][4];
    document.getElementById('team_b_set_5').textContent = data['b'][5];

    // update columns only if set value has changed
    if (data['previous_set_value'] != data['set']){
        console.log("Set value has changed");
        for (let val = 1; val <= current_set; val++) {
        
            id_a = "set_a_" + val;
            id_b = "set_b_" + val;
            document.getElementById(id_a).style.display = "table-cell";
            document.getElementById(id_a).style.backgroundColor = "#2558a1";
            
            document.getElementById(id_b).style.display = "table-cell";
            document.getElementById(id_b).style.backgroundColor = "#2558a1";                
        }

        id_a = "set_a_" + current_set;
        id_b = "set_b_" + current_set;
        document.getElementById(id_a).style.backgroundColor = "#da2f2f";
        document.getElementById(id_b).style.backgroundColor = "#da2f2f";

        // Hide unused columns in the scoreboard
        for (let val = (current_set + 1); val < 6; val++) {
            id_a = "set_a_" + val;
            id_b = "set_b_" + val;
            document.getElementById(id_a).style.display = "none";
            document.getElementById(id_b).style.display = "none";
        }
    }

    // Highlight leading team
    for (let val = 1 ; val < 6; val++) {
        a = +data['a'][val];
        b = +data['b'][val];
        if (a > b) {
            document.getElementById("team_a_set_" + val).style.fontWeight = 1000;
            document.getElementById("team_b_set_" + val).style.fontWeight = "lighter";
        } else if (a < b) {
            document.getElementById("team_a_set_" + val).style.fontWeight = "lighter";
            document.getElementById("team_b_set_" + val).style.fontWeight = 1000;
        } else {
            document.getElementById("team_a_set_" + val).style.fontWeight = "lighter";
            document.getElementById("team_b_set_" + val).style.fontWeight = "lighter";
        }
    }
});

if (document.getElementById('remote') != null) {
    const increment_a = document.getElementById('increment_a');
    increment_a.addEventListener('click', () => {
        socket.emit('increment','a');
    });

    const decrement_a = document.getElementById('decrement_a');
    decrement_a.addEventListener('click', () => {
        socket.emit('decrement','a');
    });        

    const increment_b = document.getElementById('increment_b');
    increment_b.addEventListener('click', () => {
        socket.emit('increment','b');
    });

    const decrement_b = document.getElementById('decrement_b');
    decrement_b.addEventListener('click', () => {
        socket.emit('decrement','b');
    });

    const increment_set = document.getElementById('increment_set');
    increment_set.addEventListener('click', () => {
        socket.emit('increment_set');
    });

    const decrement_set = document.getElementById('decrement_set');
    decrement_set.addEventListener('click', () => {
        socket.emit('decrement_set');
    });

    const new_game = document.getElementById('new_game');
    new_game.addEventListener('click', () => {
        socket.emit('new_game');
    });

    const reload = document.getElementById('reload');
    reload.addEventListener('click', () => {
        socket.emit('reload');
    });
}