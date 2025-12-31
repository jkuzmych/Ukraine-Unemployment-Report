import { TooltipProps } from 'recharts';

interface CustomTooltipProps extends TooltipProps<number, string> {
  fieldVisibility: Record<string, boolean>;
  unit?: string;
  payload?: Array<{
    dataKey?: string;
    value?: number;
    color?: string;
    name?: string;
  }>;
  active?: boolean;
  label?: string;
}

export function CustomTooltip({ active, payload = [], label, fieldVisibility, unit }: CustomTooltipProps) {
  if (!active) return null;

  const visibleItems = payload.filter(item => fieldVisibility[item.dataKey]);
  if (!visibleItems.length) return null;

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
            {item.value}{unit ? ` ${unit}` : ''}
          </span>
        </div>
      ))}
    </div>
  );
}