import {total,type Fiscal,type Source} from './data';
export type BudgetItem={name:string;value:number;pctGdp:number|null};
export type BudgetYear={year:string;total:number;totalPctGdp:number|null;items:BudgetItem[];tme?:number;tmePctGdp?:number;accountingAdjustments?:number;accountingAdjustmentsPctGdp?:number;debtInterest?:number;debtInterestPctGdp?:number};
export type FunctionalHistory={years:BudgetYear[];basis:string;notes:string[];sources:Source[]};
export function exactAnnualGdp(fiscal:Fiscal,endpoint:string):number|null{
 const value=fiscal.gdp?.observations.find(r=>r.date===endpoint)?.rollingAnnualMillion;
 return endpoint.endsWith('-03')&&typeof value==='number'&&Number.isFinite(value)&&value>0?value:null;
}
export function annualBudgets(fiscal:Fiscal,view:'economic'|'receipts'):BudgetYear[]{
 const result:BudgetYear[]=[];
 for(const row of fiscal.observations.filter(r=>r.date.endsWith('-03'))){
  const endpoint=row.date;const amount=(key:string)=>total(fiscal.observations,key,endpoint,'ytd');
  const denominator=exactAnnualGdp(fiscal,endpoint);
  const pct=(v:number)=>denominator?v/denominator*100:null;
  const parts=view==='economic'?[['Goods & services','goodsServices'],['Net social benefits (including pensions)','benefits'],['Interest & dividends paid','interest'],['Net investment','netInvestment'],['Depreciation','depreciation']]:[['Income tax & capital gains tax','incomeTax'],['Compulsory social contributions','nic'],['VAT','vat'],['Corporation tax (gross of credits)','corporationTax'],['Council tax','councilTax']];
  const totalValue=amount(view==='economic'?'spending':'receipts');if(totalValue==null)continue;
  const items:BudgetItem[]=[];let incomplete=false;
  for(const [name,key] of parts){const value=amount(key);if(value==null){incomplete=true;break;}items.push({name,value,pctGdp:pct(value)});}
  if(incomplete)continue;
  const residual=totalValue-items.reduce((sum,x)=>sum+x.value,0);
  items.push({name:view==='economic'?'Other spending & accounting residual':'Other receipts & accounting differences',value:residual,pctGdp:pct(residual)});
  result.push({year:`${Number(endpoint.slice(0,4))-1}-${endpoint.slice(2,4)}`,total:totalValue,totalPctGdp:pct(totalValue),items});
 }
 return result;
}
export function budgetValue(value:number,pct:number|null,totalValue:number,units:string){return units==='gdp'?pct:units==='share'?(totalValue?value/totalValue*100:null):value/1000;}

/** Differences are accounting contributions. Missing categories never imply zero. */
export function budgetComparison(first:BudgetYear,last:BudgetYear,units:string){
 const names=[...new Set([...first.items,...last.items].map(i=>i.name))];
 const rows=names.map(name=>{
  const a=first.items.find(i=>i.name===name),b=last.items.find(i=>i.name===name);
  const start=a?budgetValue(a.value,a.pctGdp,first.total,units):null;
  const end=b?budgetValue(b.value,b.pctGdp,last.total,units):null;
  return {name,start,end,change:start!=null&&end!=null?end-start:null};
 }).sort((a,b)=>Math.abs(b.change??0)-Math.abs(a.change??0));
 const start=budgetValue(first.total,first.totalPctGdp,first.total,units),end=budgetValue(last.total,last.totalPctGdp,last.total,units);
 const change=start!=null&&end!=null?end-start:null;
 const complete=rows.every(r=>r.change!=null);
 const residual=complete&&change!=null?change-rows.reduce((s,r)=>s+r.change!,0):null;
 return {rows,start,end,change,residual};
}
