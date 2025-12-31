// @ts-nocheck
import { useState } from 'react';
import { CartesianGrid, Legend, Line, LineChart, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { RechartsDevtools } from '@recharts/devtools';
import useData from '../hooks/useUnemployment_2000_2021';
import './UnemploymentChart.css'
import { Unemployment_real_registered_Notes } from './Notes'

export default function UnemploymentRealRegistered() {
  const data = useData();
  const [hiddenLines, setHiddenLines] = useState(new Set());

  const series = [
    { dataKey: 'unemployed', name: 'Unemployed', color: '#8884d8' },
    { dataKey: 'registered_unemployed', name: 'Registered unemployed', color: '#45b5e6' },
  ];

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

  const handleLegendClick = (data) => {
    const dataKey = data.dataKey;
    if (dataKey) {
      setHiddenLines(prev => {
        const next = new Set(prev);
        next.has(dataKey) ? next.delete(dataKey) : next.add(dataKey);
        return next;
      });
    }
  };

  const CustomTooltip = ({ active, payload = [], label }) => {
    if (!active) return null;

    const visibleItems = payload.filter(item => !hiddenLines.has(item.dataKey));
    if (!visibleItems.length) return null;

    const suffix = ' thousands';
    const formatValue = (value) => {
      if (typeof value !== 'number') return value;
      return value.toLocaleString();
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
        <p className="chart-subtitle">
              Data is displayed in thousands of people.
            </p>
        </div >
        <div className="chart-body">
        <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={{ top: 40, right: 30, left: 0, bottom: 50 }}
          >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="year"
            height={60}
            tick={{ fontSize: 14 }}
            angle={-35}
            textAnchor="end"
            tickMargin={12}
          />

        <YAxis 
          domain={[0, (dataMax) => Math.ceil(dataMax * 1.1)]}
          tickFormatter={(val) => `${val}k`}
        /> 
        <Tooltip content={<CustomTooltip />} />
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
            type="monotone"
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
      </LineChart>
        </ResponsiveContainer>
        </div>
        </div>
        <Unemployment_real_registered_Notes />
      </>
  );
}