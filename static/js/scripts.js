/*advanced/static/js/script.js*/

$(document).ready(function () {
    let timeout;
  
    $('.nav-item.dropdown').hover(
      function () {
        clearTimeout(timeout);
        $(this).addClass('show');
        $(this).find('.dropdown-menu').addClass('show');
      },
      function () {
        const $this = $(this);
        timeout = setTimeout(function () {
          $this.removeClass('show');
          $this.find('.dropdown-menu').removeClass('show');
        }, 200);  // ✅ 하위 메뉴로 이동할 수 있는 시간 확보
      }
    );
  });