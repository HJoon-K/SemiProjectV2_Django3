const muserid = document.querySelector('#muserid');
const mpasswd = document.querySelector('#mpasswd');
const loginbtn = document.querySelector('#loginbtn');
const logoutbtn = document.querySelector('#logoutbtn');

try {
    loginbtn.addEventListener('click', () => {
        if (muserid.value == '') alert('아이디를 입력하세요!');
        else if (mpasswd.value == '') alert('비밀번호를 입력하세요!');
        else {
            // document.loginfrm.action = '{% url 'login' %}';
            document.loginfrm.action = '/login/';
            document.loginfrm.submit();
        }
    });
} catch (e) {}

try {
    logoutbtn.addEventListener('click', () =>{
    // location.href = '{% url 'logout' %}';
    location.href = '/logout/';
});
} catch  (e) {}
