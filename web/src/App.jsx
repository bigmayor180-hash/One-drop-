import { useState, useEffect } from 'react'
import './App.css'
import Status from './components/Status'
import Observe from './components/Observe'

export default function App() {
  return (
    <div className="app">
      <header>
        <h1>💧 OceanicOS Drop</h1>
        <p>One Drop. Infinite Reflections.</p>
      </header>
      <main>
        <Status />
        <Observe />
      </main>
    </div>
  )
}
