import {describe,it,expect} from 'vitest';
import {forecastHistoryRows,type Vintage,impulse,forecastBridge,reliefValue,borrowingSurprise,canCompareProfilePeriod,type OutlookRow} from './policyData';
describe('transparent fiscal calculations',()=>{
 it('a later forecast cannot create historical surprises',()=>{expect(canCompareProfilePeriod('2026-07','November 2026')).toBe(false);expect(canCompareProfilePeriod('2026-11','November 2026')).toBe(false);expect(canCompareProfilePeriod('2026-07','March 2026')).toBe(true);expect(canCompareProfilePeriod('2026-07',undefined)).toBe(false);});
 it('an improving structural primary surplus is contractionary',()=>{expect(impulse(2,1)).toBe(-1);expect(impulse(-2,-1)).toBe(1);expect(impulse(null,1)).toBeNull();});
 it('missing or withheld reliefs and unavailable GDP never become zero',()=>{expect(reliefValue({year:'2024-25',costMillion:null,status:'withheld',claimants:null},'bn',1000)).toBeNull();expect(reliefValue({year:'2024-25',costMillion:5,status:'estimate',claimants:null},'gdp',null)).toBeNull();});
 it('borrowing surprise is actual minus profile',()=>{expect(borrowingSurprise(60,55)).toBe(5);expect(borrowingSurprise(null,55)).toBeNull();});
 it('forecast bridge reconciles spending increases and receipt offsets',()=>{const a={borrowingBn:100,receiptsBn:1000,spendingBn:1100,interestBn:100,investmentBn:100} as OutlookRow;const b={borrowingBn:60,receiptsBn:1100,spendingBn:1160,interestBn:110,investmentBn:120} as OutlookRow;const parts=forecastBridge(a,b)!;expect(parts.receipts).toBe(-100);expect(parts.primaryCurrent).toBe(30);expect(parts.interest).toBe(10);expect(parts.investment).toBe(20);expect(parts.residual).toBe(0);expect(forecastBridge({...a,interestBn:null},b)).toBeNull();});
});

it('extends forecast history and joins from the selected vintage baseline without relabelling later actuals',()=>{
 const historical=[{year:'2015-16',debtPct:80},{year:'2024-25',debtPct:94},{year:'2025-26',debtPct:99}] as OutlookRow[];
 const vintage={forecastStart:'2025-26',rows:[{year:'2024-25',debtPct:93},{year:'2025-26',debtPct:95},{year:'2026-27',debtPct:null}]} as Vintage;
 const rows=forecastHistoryRows(historical,vintage,'debtPct');
 expect(rows[0]).toEqual({label:'2015-16',actual:80,forecast:null});
 expect(rows[1]).toEqual({label:'2024-25',actual:93,forecast:93});
 expect(rows[2]).toEqual({label:'2025-26',actual:null,forecast:95});
 expect(rows[3].forecast).toBeNull();
});
