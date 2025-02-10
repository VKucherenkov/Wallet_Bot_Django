/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
//

// Изменение текста кнопки Показать/Скрыть меню аккардеона accordion.html
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


// Скрытие и добавления поля для ввода новой карты в add_operation_form.html
function toggleCardFields() {
            var cardChoice = document.getElementById("id_card").value;
            var newCardFields = document.getElementById("new-card-fields");
            var newCardButton = document.getElementById("add-new-card-btn");
            if (cardChoice === "" || cardChoice === "none") {
                newCardFields.style.display = "block";  // Показываем поля для добавления карты
                newCardButton.style.display = "none";
            } else {
                newCardFields.style.display = "none";   // Скрываем поля для добавления карты
            }
        }
// Скрытие и добавления поля для ввода новой категории в add_operation_form.html
function toggleCategoryFields() {
            var categoryChoice = document.getElementById("id_category").value;
            var newCategoryFields = document.getElementById("new-category-fields");
            var newCategoryButton = document.getElementById("add-new-category-btn");
            if (categoryChoice === "" || categoryChoice === "none") {
                newCategoryFields.style.display = "block";  // Показываем поля для добавления карты
                newCategoryButton.style.display = "none";
            } else {
                newCategoryFields.style.display = "none";
                newCategoryFields.removeAttribute('required');// Скрываем поля для добавления карты
            }
        }
// Скрытие и добавления поля для ввода нового получателя в add_operation_form.html
//function toggleRecipientFields() {
//            var recipientChoice = document.getElementById("id_recipient").value;
//            var newRecipientFields = document.getElementById("new-recipient-fields");
//            var newRecipientButton = document.getElementById("add-new-recipient-btn");
//            if (recipientChoice === "" || recipientChoice === "none") {
//                newRecipientFields.style.display = "block";  // Показываем поля для добавления карты
//                newRecipientButton.style.display = "none";
//            } else {
//                newRecipientFields.style.display = "none"; // Скрываем поля для добавления карты
//                newRecipientFields.removeAttribute('required');
//            }
//        }

//function toggleCardFieldsStart() {
//            var cardChoice = document.getElementById("id_card").value;
//            var newCardFields = document.getElementById("new-card-fields");
//            if (cardChoice === "") {
//                newCardFields.style.display = "none"; // Скрываем поля для добавления карты
//                newCardFields.removeAttribute('required');
//                }
//            }

//function toggleCategoryFieldsStart() {
//            var categoryChoice = document.getElementById("id_category").value;
//            var newCategoryFields = document.getElementById("new-category-fields");
//            if (categoryChoice === "") {
//                newCategoryFields.style.display = "none"; // Показываем поля для добавления категории
//                newCategoryFields.removeAttribute('required');
//                }
//            }
//
//function toggleRecipientFieldsStart() {
//            var recipientChoice = document.getElementById("id_recipient").value;
//            var newRecipientFields = document.getElementById("new-recipient-fields");
//            if (recipientChoice === "") {
//                newRecipientFields.style.display = "none"; // Показываем поля для добавления получателя
//                newRecipientFields.removeAttribute('required');
//                }
//            }

// Инициализация при загрузке страницы add_operation_form.html
//document.addEventListener("DOMContentLoaded", function() {
//    if (window.location.pathname === '/add-operation-form/') {
//        var cardChoice = document.getElementById("id_card");
//        var categoryChoice = document.getElementById("id_category");
//        var recipientChoice = document.getElementById("id_recipient");
//        if (cardChoice) {
//            cardChoice.onchange = toggleCardFields;
//            toggleCardFieldsStart(); // Вызов функции для начальной настройки
//        } else {
//            console.error("Элемент с id 'id_card' не найден.");
//        }
//        if (categoryChoice) {
//            categoryChoice.onchange = toggleCategoryFields;
//            toggleCategoryFieldsStart(); // Вызов функции для начальной настройки
//        } else {
//            console.error("Элемент с id 'id_category' не найден.");
//    }
//        if (recipientChoice) {
//                recipientChoice.onchange = toggleRecipientFields;
//                toggleRecipientFieldsStart(); // Вызов функции для начальной настройки
//            } else {
//                console.error("Элемент с id 'id_recipient' не найден.");
//    }
//    }
//});


// Дата и часы в навбаре nav_bar.html
function updateTime() {
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const formattedTime = now.toLocaleDateString('ru-RU', options);
    document.getElementById('current-time').textContent = formattedTime;
}

// Обновляем время каждую секунду
setInterval(updateTime, 1000);

// Инициализация времени при загрузке страницы
updateTime();