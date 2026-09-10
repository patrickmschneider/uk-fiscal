/** Choose clear vertical space across the forecast region, including signed stacks.
 * If neither edge has room, put the label just outside the plot instead.
 */
export function forecastLabelPosition(rows:Record<string,string|number|null>[],keys:string[],stacked=false,overlayKey?:string,domain?:[number,number]):'insideTop'|'insideBottom'|'top'{
 const bounds=(row:Record<string,string|number|null>)=>{
  const values=keys.map(k=>row[k]).filter((v):v is number=>typeof v==='number'&&Number.isFinite(v));
  const points=stacked&&values.length?[values.reduce((s,v)=>s+Math.min(0,v),0),values.reduce((s,v)=>s+Math.max(0,v),0)]:values;
  const overlay=overlayKey?row[overlayKey]:null;
  if(typeof overlay==='number'&&Number.isFinite(overlay))points.push(overlay);
  return points;
 };
 const all=rows.flatMap(bounds),forecast=rows.filter(r=>r.status==='Forecast').flatMap(bounds);
 if(!all.length||!forecast.length)return 'insideTop';
 const low=domain?.[0]??Math.min(...all),high=domain?.[1]??Math.max(...all);
 const topGap=high-Math.max(...forecast),bottomGap=Math.min(...forecast)-low;
 const clearance=(high-low)*.14;
 if(Math.max(topGap,bottomGap)<=clearance)return 'top';
 return topGap>=bottomGap?'insideTop':'insideBottom';
}
