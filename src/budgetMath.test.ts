import {describe,it,expect} from 'vitest';
import {annualBudgets,budgetValue} from './budgetMath';
import type {Fiscal} from './data';
const fixture=()=>({schemaVersion:1,asOf:'2020-03',releaseDate:'2026-08-21',nextRelease:'',scope:'test',basis:'test',sources:[],series:{},notes:[],observations:Array.from({length:12},(_,i)=>({date:i<9?`2019-${String(i+4).padStart(2,'0')}`:`2020-${String(i-8).padStart(2,'0')}`,spending:100,receipts:90,goodsServices:40,benefits:20,interest:5,netInvestment:10,depreciation:5,incomeTax:30,nic:20,vat:20,corporationTax:10,councilTax:5})),gdp:{basis:'test',sources:[],observations:[{date:'2020-03',rollingAnnualMillion:2400}]}} as Fiscal);
describe('annual budget decomposition',()=>{
 it('uses full financial years and preserves the expenditure identity',()=>{const [year]=annualBudgets(fixture(),'economic');expect(year.year).toBe('2019-20');expect(year.totalPctGdp).toBe(50);expect(year.items.reduce((s,x)=>s+x.value,0)).toBe(year.total);expect(year.items.at(-1)?.value).toBe(240);});
 it('does not turn a partial year or missing category into a full annual budget',()=>{const fiscal=fixture();fiscal.observations.splice(3,1);expect(annualBudgets(fiscal,'economic')).toEqual([]);const other=fixture();other.observations[0].benefits=null;expect(annualBudgets(other,'economic')).toEqual([]);});
 it('reconciles revenue without mislabelling the residual as only non-tax income',()=>{const [year]=annualBudgets(fixture(),'receipts');expect(year.items.at(-1)?.name).toBe('Other receipts & accounting differences');expect(year.items.reduce((s,x)=>s+x.value,0)).toBe(1080);});
 it('distinguishes GDP shares from shares of spending and handles missing GDP',()=>{expect(budgetValue(100,4,400,'gdp')).toBe(4);expect(budgetValue(100,4,400,'share')).toBe(25);expect(budgetValue(100,null,400,'gdp')).toBeNull();});
});
