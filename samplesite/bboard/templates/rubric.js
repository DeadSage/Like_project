const domain = 'http://localhost:';

let list = document.getElementById('list');
let listLoader = new XMLHttpRequest();

listLoader.addEventListener('readystatechange', () => {
    if (listLoader.readyState == 4) {
        if (listLoader.status == 200) {
            let data = JSON.parce(listLoader.responseText);
            let s = '<url>', d;
            for (let i = 0; i < data.length; i ++) {
                d = data[i];
                s += '<li>' + d.name + '</li>';
                }
                s += '</ul>';
                list.innerHTML = s;
            } else
                window.alert(listLoader.statusText);
                }
                });
function listLoader(){
    listLoader.open('GET', domain + 'bboard/api/rubrics/', true);
    listLoader.send();
}

listLoader();