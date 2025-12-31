import { useState, useMemo } from 'react'
import './App.css'
import Header from './components/Header'
import unemployment_by_region from '../public/data/unemployment_by_region.json' 
import unemployment_by_social_group from '../public/data/unemployment_by_social_group.json'
import unrate_by_social_group from '../public/data/unrate_by_social_group.json'
import unemployment_real_registered from '../public/data/unemployment_real_registered.json'
import Chart from './components/Chart'
import { parseChartJSON } from './components/ParseChartJSON'

function App() {
  const [view, setView] = useState('categories')

  // Memoize parsed chart data to avoid re-parsing on every render
  const unrateBySocialGroupData = useMemo(() => parseChartJSON(unrate_by_social_group), []);
  const unemploymentBySocialGroupData = useMemo(() => parseChartJSON(unemployment_by_social_group), []);
  const unemploymentRealRegisteredData = useMemo(() => parseChartJSON(unemployment_real_registered), []);
  const unemploymentByRegionData = useMemo(() => parseChartJSON(unemployment_by_region), []);

  return (
    <>
      <h1>Unemployment data in Ukraine</h1>
      <hr></hr>
      <Header 
        value={view} 
        onChange={setView} 
      />
      {view === 'unrate-by-social-group' ? (
        <div>
          <Chart chartData={unrateBySocialGroupData}/>
          <Chart chartData={unemploymentBySocialGroupData}/>
        </div>
      ) : view === 'real-registered-unemployment' ? (
        <Chart chartData={unemploymentRealRegisteredData}/>
      ) : (
        <Chart chartData={unemploymentByRegionData}/>
      )}
    </>
  )
}

export default App
