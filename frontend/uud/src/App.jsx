import { useState } from 'react'
import './App.css'
import Header from './components/Header'
import UnrateByCategories from './components/UnrateByCategories'
import UnemploymentRealRegistered from './components/UnemploymentRealRegistered'
import UnrateByRegion from './components/UnrateByRegion'

function App() {
  const [view, setView] = useState('categories')

  return (
    <>
      <h1>Unemployment data in Ukraine</h1>
      <hr></hr>
      <Header 
        value={view} 
        onChange={setView} 
      />
      {view === 'categories' ? (
        <UnrateByCategories />
      ) : view === 'regions' ? (
        <UnrateByRegion/>
      ) : (
        <UnemploymentRealRegistered />
      )}
    </>
  )
}

export default App
