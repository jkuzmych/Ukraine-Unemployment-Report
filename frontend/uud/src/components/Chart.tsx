import { useState, useMemo, useCallback, useEffect } from 'react';
import { CartesianGrid, Legend, Line, LineChart, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import './UnemploymentChart.css'
import { getFieldVisibility, stringToColor } from './ParseChartJSON'
import { ChartData } from './Types';
import { CustomTooltip } from './CustomTooltip';


export default function Chart({ chartData } : { chartData: ChartData }) {
  const [fieldVisibility, setFieldVisibility] = useState(() => getFieldVisibility(chartData))

  // Update fieldVisibility when chartData changes
  useEffect(() => {
    setFieldVisibility(getFieldVisibility(chartData));
  }, [chartData]);

  const legendFormatter = useCallback((value, entry) => {
    const isVisible = fieldVisibility[entry.dataKey];
    // const className = `legend-text${!isVisible ? ' legend-text--hidden' : ''}`;
    const className = 'legend-text';
    return <span className={className} style={{ color: isVisible ? 'inherit' : '#999' }}>{value}</span>;
  }, [fieldVisibility]);

  // toggle visibility on legend click
  const handleLegendClick = useCallback((legendElementData) => {
    const dataKey = legendElementData?.dataKey;
    if (!dataKey) return;
    setFieldVisibility(prev => ({
      ...prev,
      [dataKey]: !prev[dataKey],
    }));
  }, []);

  const keyConfig = useMemo(() => 
    Object.keys(chartData.encoding.series)
      .filter((key) => key !== chartData.encoding.xKey)
      .map((key) => ({
        dataKey: key,
        color: "color" in chartData.encoding.series[key] ? chartData.encoding.series[key].color : stringToColor(key),
        name: key,
        type: 'line'
      })),
    [chartData.encoding.series, chartData.encoding.xKey]
  )

  const TooltipWrapper = useMemo(() => {
    return (props: any) => <CustomTooltip {...props} fieldVisibility={fieldVisibility} unit={chartData.encoding.unit} />;
  }, [fieldVisibility, chartData.encoding.unit]);

  return (
    <>
      <div className="chart-container">
        <div className="chart-body">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart 
              data={chartData.data}
              margin={{ top: 60, right: 30, left: 10, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey={chartData.encoding.xKey}
                height={60}
                tick={{ fontSize: 14 }}
                angle={-35}
                textAnchor="end"
                tickMargin={12}
              />
              <YAxis 
                domain={[0, (dataMax) => Math.ceil(dataMax * 1.2)]} 
                allowDataOverflow={false}
                label={{ 
                  value: chartData.axes.y.suffix || '', 
                  position: 'top',
                  offset: 25,
                  style: { textAnchor: 'middle', fontSize: 14 }
                }}
              />
              <Legend 
                onClick={handleLegendClick} 
                formatter={legendFormatter}
                verticalAlign="top"
                align="center"
                wrapperStyle={{ marginTop: -30 }}
              />
              {keyConfig.map(({ dataKey, name, color }) => (
                <Line
                  key={dataKey}
                  dataKey={dataKey} 
                  stroke={color} 
                  strokeWidth={2} 
                  name={name}
                  strokeOpacity={(fieldVisibility[dataKey] === true) ? 1 : 0}
                  dot={fieldVisibility[dataKey] ? true : false}
                  activeDot={fieldVisibility[dataKey] ? true : false}
                />
              ))}
              
              <Tooltip content={TooltipWrapper} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </>
  );
}