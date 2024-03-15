
async function getUserData(){
    const response = await fetch('/api/users');
    return response.json();
}

function loadTable(users){
    const table = document.querySelector('#result');
    for(let user of users){
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
        </tr>`;
    }
}

async function main(){
    const users = await getUserData();
    loadTable(users);
}

function openNav(){
    document.getElementById("mySidepanel").style.width = "20vw";
}
  
function closeNav(){
    document.getElementById("mySidepanel").style.width = "0";
}

main();