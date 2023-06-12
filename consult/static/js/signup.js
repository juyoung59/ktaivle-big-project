// 입력 오류 발생 시 스크롤 이동과 이펙트 적용
function scrollToError() {
    const firstError = document.querySelector('.error-field');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // 오류 필드에 원하는 이펙트 적용
        firstError.classList.add('error-effect');
    }
}

// 회원가입 폼 제출 시 입력 유효성 검사
function validateForm() {
    const form = document.querySelector('#signup-form');
    const inputs = form.querySelectorAll('input, select');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.checkValidity()) {
            input.classList.add('error-field');
            isValid = false;
        } else {
            input.classList.remove('error-field');
        }
    });

    if (!isValid) {
        scrollToError();
    }

    return isValid;
}