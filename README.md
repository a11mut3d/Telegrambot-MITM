<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 TELEGRAM MITM SYSTEM - FINAL VERSION</title>
    <style>
        :root {
            --primary: #2d3436;
            --secondary: #636e72;
            --accent: #0984e3;
            --danger: #d63031;
            --success: #00b894;
            --warning: #fdcb6e;
            --dark: #1e272e;
            --light: #f5f6fa;
            --telegram: #0088cc;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--light);
            background: linear-gradient(135deg, var(--dark) 0%, #2c3e50 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(30, 39, 46, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--dark) 100%);
            padding: 40px;
            text-align: center;
            border-bottom: 3px solid var(--accent);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(9, 132, 227, 0.1) 0%, transparent 70%);
        }
        
        .header h1 {
            font-size: 3.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00b894, #0984e3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
        }
        
        .header h2 {
            font-size: 1.5rem;
            color: var(--light);
            font-weight: 300;
            position: relative;
            z-index: 1;
        }
        
        .warning-banner {
            background: linear-gradient(135deg, var(--danger) 0%, #c0392b 100%);
            padding: 25px;
            margin: 20px;
            border-radius: 15px;
            border-left: 5px solid #ff7675;
            box-shadow: 0 10px 30px rgba(214, 48, 49, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 10px 30px rgba(214, 48, 49, 0.3); }
            50% { box-shadow: 0 10px 40px rgba(214, 48, 49, 0.5); }
            100% { box-shadow: 0 10px 30px rgba(214, 48, 49, 0.3); }
        }
        
        .warning-banner h3 {
            font-size: 1.8rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .warning-banner h3::before {
            content: '⚠️';
            font-size: 2rem;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            background: rgba(45, 52, 54, 0.8);
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease;
        }
        
        .section:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }
        
        .section h3 {
            font-size: 2rem;
            margin-bottom: 20px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(9, 132, 227, 0.3);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .feature-card {
            background: rgba(30, 39, 46, 0.7);
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid var(--success);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            background: rgba(30, 39, 46, 0.9);
            transform: translateX(10px);
        }
        
        .feature-card h4 {
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: var(--light);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }
        
        .tech-badge {
            background: linear-gradient(135deg, var(--accent) 0%, #00b894 100%);
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 5px 15px rgba(9, 132, 227, 0.3);
        }
        
        .file-structure {
            background: rgba(0, 0, 0, 0.3);
            padding: 25px;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .file-item {
            padding: 8px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .file-item::before {
            content: '📄';
            font-size: 1.2rem;
        }
        
        .code-block {
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
            overflow-x: auto;
            border-left: 4px solid var(--accent);
        }
        
        .command {
            background: rgba(0, 0, 0, 0.7);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid var(--warning);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .command button {
            background: var(--accent);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .command button:hover {
            background: #0870c1;
        }
        
        .workflow {
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin: 30px 0;
        }
        
        .workflow-step {
            display: flex;
            align-items: flex-start;
            gap: 20px;
            padding: 20px;
            background: rgba(30, 39, 46, 0.7);
            border-radius: 12px;
            border-left: 4px solid var(--telegram);
        }
        
        .step-number {
            background: var(--telegram);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2rem;
            flex-shrink: 0;
        }
        
        .wallet-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .wallet-card {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .wallet-card:hover {
            transform: scale(1.05);
            background: rgba(0, 0, 0, 0.5);
        }
        
        .footer {
            background: var(--dark);
            padding: 30px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 40px;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
        }
        
        .badge.python { background: #3776ab; color: white; }
        .badge.telegram { background: var(--telegram); color: white; }
        .badge.mitm { background: var(--danger); color: white; }
        .badge.license { background: var(--success); color: white; }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5rem; }
            .section h3 { font-size: 1.6rem; }
            .features-grid { grid-template-columns: 1fr; }
            .content { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 TELEGRAM MITM SYSTEM</h1>
            <h2>FINAL VERSION - Прокси-система для перехвата и замены крипто-кошельков</h2>
        </div>

        <div class="warning-banner">
            <h3>ВНИМАНИЕ: ЗЛОЙ ПРОКСИ ДЛЯ БОТОВ</h3>
            <p><strong>⚠️ Этот проект работает ТОЛЬКО на Telegram ботах через прокси.</strong></p>
            <p><strong>⚠️ На клиентские приложения НЕ работает.</strong></p>
            <p><strong>⚠️ Предназначен ТОЛЬКО для образовательных целей и аудита безопасности.</strong></p>
            <p><strong>⚠️ Используйте только на СВОИХ собственных ботах или с явного разрешения.</strong></p>
        </div>

        <div class="content">
            <section class="section">
                <h3>🎯 Что это такое?</h3>
                <p>Это профессиональная MITM (Man-in-the-Middle) система, разработанная для перехвата трафика Telegram ботов с целью замены крипто-кошельков и чеков на ваши собственные адреса.</p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <h4>🔄 Автозамена кошельков</h4>
                        <p>Автоматически заменяет 7 типов крипто-адресов в сообщениях ботов</p>
                    </div>
                    <div class="feature-card">
                        <h4>🎫 Перехват чеков</h4>
                        <p>Обнаруживает и подменяет крипто-чеки Telegram на "фейковые"</p>
                    </div>
                    <div class="feature-card">
                        <h4>🤖 Детект ботов</h4>
                        <p>Автоматически обнаруживает новые боты по токенам в трафике</p>
                    </div>
                    <div class="feature-card">
                        <h4>📊 Админ-панель</h4>
                        <p>Полноценный Telegram бот для управления системой и статистики</p>
                    </div>
                </div>
            </section>

            <section class="section">
                <h3>🛠 Технический стек</h3>
                <div class="tech-stack">
                    <div class="tech-badge">🐍 Python 3.8+</div>
                    <div class="tech-badge">🔧 mitmproxy 10.0+</div>
                    <div class="tech-badge">🤖 aiogram 3.0+</div>
                    <div class="tech-badge">🌐 aiohttp 3.8+</div>
                    <div class="tech-badge">📡 requests 2.31+</div>
                </div>
            </section>

            <section class="section">
                <h3>📁 Структура проекта</h3>
                <div class="file-structure">
                    <div class="file-item"><strong>storage.py</strong> - Управление данными и кошельками</div>
                    <div class="file-item"><strong>patterns.py</strong> - Регулярные выражения для крипто-адресов</div>
                    <div class="file-item"><strong>mitm_interceptor.py</strong> - Основной перехватчик MITM</div>
                    <div class="file-item"><strong>admin_bot.py</strong> - Telegram бот для управления</div>
                    <div class="file-item"><strong>run.py</strong> - Главный скрипт запуска системы</div>
                    <div class="file-item"><strong>start.sh</strong> - Скрипт запуска одной командой</div>
                    <div class="file-item"><strong>install.sh</strong> - Установка зависимостей</div>
                    <div class="file-item"><strong>reset.sh</strong> - Сброс системы к начальному состоянию</div>
                </div>
            </section>

            <section class="section">
                <h3>⚡ Быстрый старт</h3>
                <div class="workflow">
                    <div class="workflow-step">
                        <div class="step-number">1</div>
                        <div>
                            <h4>Клонировать и установить</h4>
                            <div class="command">
                                <code>./install.sh</code>
                                <button onclick="copyCode('install')">Копировать</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="workflow-step">
                        <div class="step-number">2</div>
                        <div>
                            <h4>Запустить систему</h4>
                            <div class="command">
                                <code>./start.sh "YOUR_BOT_TOKEN" YOUR_ADMIN_ID</code>
                                <button onclick="copyCode('start')">Копировать</button>
                            </div>
                            <p>Где:<br>
                            • <strong>BOT_TOKEN</strong> - токен от @BotFather<br>
                            • <strong>ADMIN_ID</strong> - ваш ID из @userinfobot</p>
                        </div>
                    </div>
                    
                    <div class="workflow-step">
                        <div class="step-number">3</div>
                        <div>
                            <h4>Настроить Telegram</h4>
                            <p>В настройках Telegram установите прокси:<br>
                            • <strong>Тип:</strong> HTTP<br>
                            • <strong>Сервер:</strong> ваш_сервер_ip<br>
                            • <strong>Порт:</strong> 8082</p>
                        </div>
                    </div>
                </div>
            </section>

            <section class="section">
                <h3>💰 Поддерживаемые кошельки</h3>
                <div class="wallet-list">
                    <div class="wallet-card">
                        <h4>₿ Bitcoin</h4>
                        <p><code>bc1q...</code></p>
                    </div>
                    <div class="wallet-card">
                        <h4>⧫ Ethereum</h4>
                        <p><code>0x...</code></p>
                    </div>
                    <div class="wallet-card">
                        <h4>💵 USDT TRC20</h4>
                        <p><code>T...</code></p>
                    </div>
                    <div class="wallet-card">
                        <h4>💳 USDT ERC20</h4>
                        <p><code>0x...</code></p>
                    </div>
                    <div class="wallet-card">
                        <h4>🚀 TON</h4>
                        <p><code>UQ/EQ...</code></p>
                    </div>
                    <div class="wallet-card">
                        <h4>🌟 Solana</h4>
                        <p><code>So...</code></p>
                    </div>
                    <div class="wallet-card">
                        <h4>🔥 BNB</h4>
                        <p><code>bnb1q...</code></p>
                    </div>
                </div>
            </section>

            <section class="section">
                <h3>📊 Админ-панель</h3>
                <p>После запуска системы, Telegram бот предоставляет полный контроль:</p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <h4>🔄 Управление кошельками</h4>
                        <p>Интерактивное меню для изменения всех 7 типов адресов</p>
                    </div>
                    <div class="feature-card">
                        <h4>📈 Статистика</h4>
                        <p>Отслеживание замененных кошельков и пойманных чеков</p>
                    </div>
                    <div class="feature-card">
                        <h4>🔔 Уведомления</h4>
                        <p>Мгновенные оповещения о новых ботах и чеках</p>
                    </div>
                    <div class="feature-card">
                        <h4>📥 JSON экспорт</h4>
                        <p>Скачивание полной статистики в формате JSON</p>
                    </div>
                </div>
            </section>

            <section class="section">
                <h3>🔧 Тестирование системы</h3>
                <p>Для проверки работы системы используйте:</p>
                
                <div class="code-block">
# Тестовое сообщение для отправки через прокси
BTC: bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq
ETH: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
Check: https://t.me/test/send?start=TEST_CHECK_123
                </div>
                
                <div class="command">
                    <code>python3 test_message.py short</code>
                    <button onclick="copyCode('test')">Копировать</button>
                </div>
            </section>

            <section class="section">
                <h3>🎯 Как это работает?</h3>
                <div class="workflow">
                    <div class="workflow-step">
                        <div class="step-number">1</div>
                        <div>
                            <h4>Перехват трафика</h4>
                            <p>MITM прокси (порт 8082) перехватывает все запросы к api.telegram.org</p>
                        </div>
                    </div>
                    
                    <div class="workflow-step">
                        <div class="step-number">2</div>
                        <div>
                            <h4>Анализ сообщений</h4>
                            <p>Система ищет крипто-адреса и чеки в тексте сообщений</p>
                        </div>
                    </div>
                    
                    <div class="workflow-step">
                        <div class="step-number">3</div>
                        <div>
                            <h4>Подмена данных</h4>
                            <p>Найденные адреса заменяются на ваши из data.json</p>
                        </div>
                    </div>
                    
                    <div class="workflow-step">
                        <div class="step-number">4</div>
                        <div>
                            <h4>Отправка уведомлений</h4>
                            <p>Админ получает уведомления о перехваченных данных</p>
                        </div>
                    </div>
                </div>
            </section>

            <section class="section">
                <h3>⚙️ Команды админ-бота</h3>
                <div class="code-block">
/start - Главное меню
/stats - Скачать статистику JSON
/wallets - Управление кошельками
/setwallet COIN ADDRESS - Быстрая установка кошелька
/help - Справка по командам
                </div>
            </section>

            <section class="section">
                <h3>🚫 Ограничения</h3>
                <ul style="padding-left: 20px; margin: 15px 0;">
                    <li>⚠️ Работает ТОЛЬКО с HTTP-прокси (не SOCKS5)</li>
                    <li>⚠️ Не перехватывает зашифрованные сообщения (Secret Chats)</li>
                    <li>⚠️ Требует ручной настройки прокси в клиенте Telegram</li>
                    <li>⚠️ Не работает с веб-версией Telegram</li>
                    <li>⚠️ Только для ботов, не для пользовательских чатов</li>
                </ul>
            </section>
        </div>

        <div class="footer">
            <div class="badges">
                <span class="badge python">Python 3.8+</span>
                <span class="badge telegram">Telegram API</span>
                <span class="badge mitm">MITM Proxy</span>
                <span class="badge license">MIT License</span>
            </div>
            
            <p><strong>🤖 TELEGRAM MITM SYSTEM - FINAL VERSION</strong></p>
            <p>⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ ⚠️</p>
            <p>© 2024 | Проект для аудита безопасности Telegram ботов</p>
        </div>
    </div>

    <script>
        function copyCode(type) {
            let code = '';
            switch(type) {
                case 'install':
                    code = './install.sh';
                    break;
                case 'start':
                    code = './start.sh "YOUR_BOT_TOKEN" YOUR_ADMIN_ID';
                    break;
                case 'test':
                    code = 'python3 test_message.py short';
                    break;
            }
            
            navigator.clipboard.writeText(code).then(() => {
                alert('Команда скопирована в буфер обмена!');
            });
        }
    </script>
</body>
</html>
