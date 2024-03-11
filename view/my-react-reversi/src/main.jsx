import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './practice/App.jsx'
import './index.css'
import CounterApp from './practice/CounterApp.jsx'
import ReversiApp from './ReversiApp.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ReversiApp />
  </React.StrictMode>,
)
