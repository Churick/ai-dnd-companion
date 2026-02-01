import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl md:text-5xl font-bold text-center mb-6 text-yellow-400 font-medieval">
          🐉 AI D&D Companion
        </h1>
        
        <div className="max-w-3xl mx-auto bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-yellow-700/30">
          <h2 className="text-2xl font-bold mb-4 text-green-400">🎮 Фронтенд успешно настроен!</h2>
          
          <div className="space-y-4">
            <div className="flex items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-green-500 text-2xl mr-3">✅</span>
              <div>
                <p className="font-semibold">Tailwind CSS работает</p>
                <p className="text-gray-300 text-sm">Стили применяются корректно</p>
              </div>
            </div>
            
            <div className="flex items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-blue-500 text-2xl mr-3">⚛️</span>
              <div>
                <p className="font-semibold">React + Vite готовы</p>
                <p className="text-gray-300 text-sm">Современный стек фронтенда</p>
              </div>
            </div>
            
            <div className="flex items-center p-3 bg-gray-700/50 rounded-lg">
              <span className="text-purple-500 text-2xl mr-3">🔌</span>
              <div>
                <p className="font-semibold">API подключение</p>
                <p className="text-gray-300 text-sm">Готово к подключению к бэкенду</p>
              </div>
            </div>
          </div>
          
          <div className="mt-8 p-4 bg-gradient-to-r from-dnd-purple/20 to-dnd-red/20 rounded-lg border border-purple-700/30">
            <h3 className="text-lg font-bold mb-2">Следующие шаги:</h3>
            <ol className="list-decimal list-inside space-y-2 text-gray-300">
              <li>Создание компонентов Login/Register</li>
              <li>Настройка React Router</li>
              <li>Подключение к FastAPI бэкенду</li>
              <li>Реализация чата с AI Мастером</li>
            </ol>
          </div>
          
          <button 
            className="mt-6 w-full py-3 bg-gradient-to-r from-dnd-red to-dnd-purple text-white font-bold rounded-lg hover:opacity-90 transition-opacity"
            onClick={() => alert('В разработке!')}
          >
            Начать приключение
          </button>
        </div>
        
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Бэкенд: FastAPI + Ollama (llama3:8b) | Фронтенд: React + Tailwind</p>
        </div>
      </div>
    </div>
  )
}

export default App
