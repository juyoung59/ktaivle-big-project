window.onload = function() {
    if (getCookie("username")) {  
        document.loginForm.username.value = getCookie("username"); 
        document.loginForm.remember.checked = true; 
    }
}

function setCookie(name, value, expiredays) { // 쿠키 저장 함수
    var todayDate = new Date();
    todayDate.setDate(todayDate.getDate() + expiredays);
    document.cookie = name + "=" + escape(value) + "; path=/; expires=" + todayDate.toGMTString() + ";"
}

function getCookie(Name) {  // 쿠키 불러오는 함수
    var search = Name + "=";
    if (document.cookie.length > 0) {  // if there are any cookies
        offset = document.cookie.indexOf(search);
        if (offset != -1) {  // if cookie exists
            offset += search.length;  // set index of beginning of value
            end = document.cookie.indexOf(";", offset);  // set index of end of cookie value
            if (end == -1)
                end = document.cookie.length;
            return unescape(document.cookie.substring(offset, end));
        }
    }
}
    
function sendit() {
    if (document.loginForm.remember.checked == true) {  
        setCookie("username", document.loginForm.username.value, 7);  
    } 
    else {  
        setCookie("username", document.loginForm.username.value, 0);  
    }

    document.loginForm.submit();  
}