import { useState } from 'react';
import { CartesianGrid, Legend, Line, LineChart, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { RechartsDevtools } from '@recharts/devtools';
import useData from '../hooks/useData';
import './UnemploymentChart.css'
import Unemployment_by_category_Notes from './Notes'


export default function UnrateByCategories() {
  const data = useData();
  const [usePercent, setUsePercent] = useState(true);
  const [hiddenLines, setHiddenLines] = useState(
    new Set(['females_pc', 'males_pc', 'rural_pc', 'urban_pc', 'females', 'males', 'rural', 'urban'])
  );

  const seriesConfig = [
    { baseKey: 'total', name: 'Total', color: '#8884d8' },
    { baseKey: 'females', name: 'Females', color: '#ff84d8' },
    { baseKey: 'males', name: 'Males', color: '#45b5e6' },
    { baseKey: 'urban', name: 'Urban', color: '#ffd155' },
    { baseKey: 'rural', name: 'Rural', color: '#84d55a' },
  ];

  const series = seriesConfig.map(({ baseKey, ...rest }) => ({
    ...rest,
    dataKey: usePercent ? `${baseKey}_pc` : baseKey,
  }));

  // change color of the legend
  const legendPayload = series.map(item => ({
    ...item,
    color: hiddenLines.has(item.dataKey) ? '#9ca3af' : item.color,
    type: 'line',
    id: item.dataKey,
  }));

  const legendFormatter = (value, entry) => {
    const isHidden = hiddenLines.has(entry.dataKey);
    const className = `legend-text${isHidden ? ' legend-text--hidden' : ''}`;
    return <span className={className}>{value}</span>;
  };

  // toggle visibility on legend click
  const handleLegendClick = (data) => {
    const dataKey = data.dataKey;
    if (dataKey) {
      setHiddenLines(prev => {
        const newSet = new Set(prev);
        if (newSet.has(dataKey)) {
          newSet.delete(dataKey);
        } else {
          newSet.add(dataKey);
        }
        return newSet;
      });
    }
  };

  const CustomTooltip = ({ active, payload = [], label }) => {
    if (!active) return null;

    const visibleItems = payload.filter(item => !hiddenLines.has(item.dataKey));
    if (!visibleItems.length) return null;

    const suffix = usePercent ? ' %' : ' thousands';
    const formatValue = (value) => {
      if (typeof value !== 'number') return value;
      return usePercent ? value.toFixed(2) : value.toLocaleString();
    };

    return (
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.92)',
        border: '1px solid #2d72b4',
        borderRadius: '8px',
        padding: '12px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
        minWidth: '160px'
      }}>
        <p style={{ 
          margin: '0 0 6px',
          fontSize: '14px',
          color: '#111827',
          fontWeight: 600
        }}>
          {label}
        </p>
        {visibleItems.map((item) => (
          <div 
            key={item.dataKey}
            style={{ 
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              gap: '10px',
              marginBottom: '4px',
              color: '#334155',
              fontSize: '13px'
            }}
          >
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
              <span 
                style={{ 
                  width: '10px', 
                  height: '10px', 
                  borderRadius: '999px', 
                  backgroundColor: item.color || '#8884d8' 
                }} 
              />
              {item.name || item.dataKey}
            </span>
            <span style={{ fontWeight: 600 }}>
              {formatValue(item.value)}{suffix}
            </span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <>
      <div className="chart-container">
        <div className="chart-header">
          <div>
            <p className="chart-subtitle">
              Dispaly data in thousands or percentage from the labour force.
            </p>
          </div>
          <div className="chart-toggle">
            <span className={`toggle-label ${!usePercent ? 'toggle-label--active' : ''}`}>
              Thousands
            </span>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={usePercent} 
                onChange={(e) => setUsePercent(e.target.checked)} 
              />
              <span className="slider round"></span>
            </label>
            <span className={`toggle-label ${usePercent ? 'toggle-label--active' : ''}`}>
              Percent
            </span>
          </div>
        </div>

        <div className="chart-body">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart 
              data={data}
              margin={{ top: 40, right: 30, left: 0, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="period" 
                height={60}
                tick={{ fontSize: 14 }}
                angle={-35}
                textAnchor="end"
                tickMargin={12}
              />
              <YAxis 
                domain={[0, (dataMax) => Math.ceil(dataMax * 1.1)]}
                tickFormatter={(val) => usePercent ? `${val}%` : `${val}k`}
              />
              <Legend 
                onClick={handleLegendClick} 
                payload={legendPayload}
                formatter={legendFormatter}
                verticalAlign="top"
                align="center"
              />
              {series.map(({ dataKey, name, color }) => (
                <Line 
                  key={dataKey}
                  dataKey={dataKey} 
                  stroke={color} 
                  strokeWidth={2} 
                  name={name}
                  strokeOpacity={hiddenLines.has(dataKey) ? 0 : 1}
                  dot={hiddenLines.has(dataKey) ? false : true}
                  activeDot={hiddenLines.has(dataKey) ? false : true}
                />
              ))}
              
              <RechartsDevtools />
              <Tooltip content={<CustomTooltip />}/>
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      <Unemployment_by_category_Notes></Unemployment_by_category_Notes>
    </>
  );
}