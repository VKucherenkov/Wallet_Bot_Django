/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Проверяем состояние боковой панели при загрузке страницы
        if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
            document.body.classList.add('sb-sidenav-toggled');
            sidebarToggle.textContent = 'Показать Меню'; // Устанавливаем текст кнопки
        } else {
            sidebarToggle.textContent = 'Скрыть Меню'; // Устанавливаем текст кнопки
        }

        // Обработчик клика на кнопку
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');

            // Меняем текст кнопки в зависимости от состояния
            if (document.body.classList.contains('sb-sidenav-toggled')) {
                sidebarToggle.textContent = 'Показать Меню';
            } else {
                sidebarToggle.textContent = 'Скрыть Меню';
            }

            // Сохраняем состояние в localStorage
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});
