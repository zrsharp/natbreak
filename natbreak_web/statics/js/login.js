document.getElementById('login-form').onsubmit = () => false;

document.getElementById('login-btn').onclick = function() {
    username = document.getElementById('username').value;
    password = document.getElementById('password').value;
    if (username == '' || password == '') {
        alert('用户名或者密码不能为空');
        return false;
    }

    requestContent = 'username=' + username + ';';
    requestContent += 'password=' + password + ';'

    xhr = new XMLHttpRequest();
    xhr.open('POST', '/login/', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.send(requestContent);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            responseText = xhr.responseText;
            console.log(responseText);
            alert(responseText);
        }
    }
}
