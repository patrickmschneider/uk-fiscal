import {useEffect,useRef,useState} from 'react';
import {ChevronLeft,ChevronRight,CalendarDays} from 'lucide-react';
import {dateLabel,shiftMonth} from './data';

/** A calendar of published observations: never silently substitute another day. */
export function DatePicker({label,value,onChange,dates}:{label:string;value:string;onChange:(date:string)=>void;dates:string[]}){
 const root=useRef<HTMLDetailsElement>(null);
 const [month,setMonth]=useState(value.slice(0,7));
 useEffect(()=>setMonth(value.slice(0,7)),[value]);
 useEffect(()=>{const escape=(e:KeyboardEvent)=>{if(e.key==='Escape'&&root.current?.open){root.current.open=false;root.current.querySelector('summary')?.focus();}};window.addEventListener('keydown',escape);return()=>window.removeEventListener('keydown',escape);},[]);
 const available=new Set(dates);
 const years=[...new Set(dates.map(d=>d.slice(0,4)))].sort().reverse();
 const months=[...new Set(dates.map(d=>d.slice(0,7)))].sort();
 const current=month||value.slice(0,7);
 const [year,m]=current.split('-').map(Number);
 const first=new Date(Date.UTC(year,m-1,1));
 const offset=(first.getUTCDay()+6)%7;
 const days=new Date(Date.UTC(year,m,0)).getUTCDate();
 const previous=shiftMonth(current,-1),next=shiftMonth(current,1);
 function pick(date:string){onChange(date);if(root.current){root.current.open=false;root.current.querySelector('summary')?.focus();}}
 return <div className="date-field"><span className="date-field-label">{label}</span><details ref={root} className="date-picker"><summary aria-label={`${label}: ${dateLabel(value,true)}`}><CalendarDays size={16}/>{dateLabel(value,true)}</summary><div className="date-calendar" role="group" aria-label={`${label} calendar`}>
 <div className="calendar-selects"><label>Year<select aria-label={`${label} year`} value={String(year)} onChange={e=>{const target=`${e.target.value}-${String(m).padStart(2,'0')}`;setMonth(months.includes(target)?target:months.find(v=>v.startsWith(e.target.value))!);}}>{years.map(y=><option key={y}>{y}</option>)}</select></label><label>Month<select aria-label={`${label} month`} value={current} onChange={e=>setMonth(e.target.value)}>{months.filter(v=>v.startsWith(String(year))).map(v=><option key={v} value={v}>{new Date(`${v}-01T12:00:00Z`).toLocaleDateString('en-GB',{month:'long',timeZone:'UTC'})}</option>)}</select></label></div>
 <div className="calendar-month"><button aria-label={`${label}: previous month`} disabled={previous<months[0]} onClick={()=>setMonth(previous)}><ChevronLeft size={16}/></button><strong aria-live="polite">{dateLabel(current)}</strong><button aria-label={`${label}: next month`} disabled={next>months.at(-1)!} onClick={()=>setMonth(next)}><ChevronRight size={16}/></button></div>
 <div className="calendar-grid">{['Mo','Tu','We','Th','Fr','Sa','Su'].map(d=><span className="weekday" key={d}>{d}</span>)}{Array.from({length:offset},(_,i)=><span key={`blank-${i}`}/>)}{Array.from({length:days},(_,i)=>{const day=i+1,date=`${current}-${String(day).padStart(2,'0')}`;return <button key={date} disabled={!available.has(date)} aria-label={dateLabel(date)} aria-pressed={date===value} onClick={()=>pick(date)}>{day}</button>;})}</div><p>Only days with saved observations can be selected.</p>
 </div></details></div>;
}
