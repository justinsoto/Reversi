import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import ReversiApp from './ReversiApp.jsx'

document.title = "Reversi";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ReversiApp />
  </React.StrictMode>,
)
