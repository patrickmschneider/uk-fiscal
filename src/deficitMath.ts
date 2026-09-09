import type {OutlookRow} from './policyData';
/** Use source cash amounts for identities; GDP conversion is applied consistently. */
export function deficitParts(row:OutlookRow,units:string){
 const scale=(value:unknown)=>typeof value==='number'&&Number.isFinite(value)?units==='bn'?value:row.gdpBn&&row.gdpBn>0?value/row.gdpBn*100:null:null;
 const total=scale(row.borrowingBn),interest=scale(row.interestBn),structural=scale(row.structuralBorrowingBn);
 const primary=total!=null&&interest!=null?total-interest:null;
 const cyclical=total!=null&&structural!=null?total-structural:null;
 const structuralPrimary=row.structuralPrimaryBalancePct==null?null:units==='bn'?(row.gdpBn?-row.structuralPrimaryBalancePct/100*row.gdpBn:null):-row.structuralPrimaryBalancePct;
 return {total,interest,primary,structural,cyclical,structuralPrimary,cyclicalPrimary:primary!=null&&structuralPrimary!=null?primary-structuralPrimary:null};
}

// Historical totals are comparable; the ONS interest/dividends proxy is not
// silently used to extend the OBR component definitions.
export function deficitHistoryRows(history:OutlookRow[],vintageRows:OutlookRow[],start:string){
 const first=vintageRows[0]?.year||'';
 return [...history.filter(r=>r.year<first).map(r=>({...r,interestBn:null,structuralBorrowingBn:null,structuralPrimaryBalancePct:null})),...vintageRows].filter(r=>r.year>=start);
}
