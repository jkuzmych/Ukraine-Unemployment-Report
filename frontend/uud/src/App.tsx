import { useState, useMemo } from 'react'
import './App.css'
import Header from './components/Header'
import unemployment_by_region from '../public/data/unemployment_by_region.json' 
import unemployment_by_social_group from '../public/data/unemployment_by_social_group.json'
import unrate_by_social_group from '../public/data/unrate_by_social_group.json'
import unemployment_real_registered from '../public/data/unemployment_real_registered.json'
import Chart from './components/Chart'
import { parseChartJSON } from './components/ParseChartJSON'
import { Unemployment_by_category_Notes, Unemployment_real_registered_Notes, UnemploymentByRegionNotes } from './components/Notes'

function App() {
  const [view, setView] = useState('unrate-by-social-group')

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
          <h2>Unemployment rate</h2>
          <Chart chartData={unrateBySocialGroupData}/>
          <h2>Unemployment, in thousands</h2>
          <Chart chartData={unemploymentBySocialGroupData}/>
          <Unemployment_by_category_Notes />
        </div>
      ) : view === 'real-registered-unemployment' ? (
        <>
          <h2>Unemployment, in thousands</h2>
          <Chart chartData={unemploymentRealRegisteredData}/>
          <Unemployment_real_registered_Notes />
        </>
      ) : (
        <>
          <Chart chartData={unemploymentByRegionData}/>
          <UnemploymentByRegionNotes />
        </>
      )}
    </>
  )
}

export default App
