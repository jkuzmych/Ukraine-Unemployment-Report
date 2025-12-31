// @ts-nocheck
import { useState } from 'react';
import { CartesianGrid, Legend, Line, LineChart, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { RechartsDevtools } from '@recharts/devtools';
import useData from '../hooks/useUnrateByRegion';
import './UnemploymentChart.css'

export default function UnrateByRegion() {
    const data = useData();
    const [hiddenLines, setHiddenLines] = useState(new Set());
    
    return (
        <> 
        </>
    );
}