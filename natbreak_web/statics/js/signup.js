document.getElementById('signup-form').onsubmit = () => false;

document.getElementById('signup-btn').onclick = function() {
    username = document.getElementById('username').value;
    password = document.getElementById('password').value;
    password2 = document.getElementById('password2').value;
    email = document.getElementById('email').value;
    phone = document.getElementById('phone').value;

    if (username == '' || password == '' || password2 == '' || email == '' || phone == '') {
        alert('注册信息不能有空项');
        return false;
    }

    if (password != password2) {
        alert('两次输入的密码不一致');
        return false;
    }

    requestContent = 'username=' + username + ';';
    requestContent += 'password=' + password + ';';
    requestContent += 'password2=' + password2 + ';';
    requestContent += 'email=' + email + ';';
    requestContent += 'phone=' + phone + ';';

    xhr = new XMLHttpRequest();
    xhr.open('POST', '/signup/', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.send(requestContent);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            responseText = xhr.responseText;
            console.log(responseText);
            alert(responseText);
            if (responseText == '注册成功') {
                window.location.href = '/login/';
            }
        }
    }
}
