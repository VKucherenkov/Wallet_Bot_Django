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