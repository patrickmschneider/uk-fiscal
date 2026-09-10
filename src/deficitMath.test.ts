import {it,expect} from 'vitest';
import {deficitParts,deficitHistoryRows} from './deficitMath';
import type {OutlookRow} from './policyData';
it('reconciles both deficit identities and preserves primary surpluses',()=>{
 const row={borrowingBn:50,interestBn:80,structuralBorrowingBn:40,gdpBn:2000,structuralPrimaryBalancePct:2} as OutlookRow;
 for(const unit of ['gdp','bn']){const d=deficitParts(row,unit);expect(d.primary!+d.interest!).toBeCloseTo(d.total!);expect(d.structural!+d.cyclical!).toBeCloseTo(d.total!);expect(d.primary).toBeLessThan(0);expect(d.structuralPrimary!+d.cyclicalPrimary!).toBeCloseTo(d.primary!);}
 expect(deficitParts(row,'bn').primary).toBe(-30);expect(deficitParts(row,'gdp').cyclical).toBe(.5);
});
it('does not manufacture structural estimates or GDP denominators',()=>{
 const row={borrowingBn:50,interestBn:20,gdpBn:null,structuralPrimaryBalancePct:null} as OutlookRow;
 expect(deficitParts(row,'gdp').total).toBeNull();expect(deficitParts(row,'bn').primary).toBe(30);expect(deficitParts(row,'bn').cyclical).toBeNull();expect(deficitParts(row,'bn').structuralPrimary).toBeNull();
});

it('extends totals without inventing comparable components or overwriting vintage rows',()=>{
 const historic=[{year:'1999-00',borrowingBn:1},{year:'2000-01',borrowingBn:10,interestBn:3,deficitInterestBn:5,structuralBorrowingBn:4},{year:'2024-25',borrowingBn:999}] as unknown as OutlookRow[];
 const vintage=[{year:'2024-25',borrowingBn:20,interestBn:8}] as OutlookRow[];
 const result=deficitHistoryRows(historic,vintage,'2000');
 expect(result.map(r=>r.year)).toEqual(['2000-01','2024-25']);
 expect(result[0].borrowingBn).toBe(10);expect(result[0].interestBn).toBe(5);expect(result[0].structuralBorrowingBn).toBe(4);
 expect(result[1].borrowingBn).toBe(20);expect(result[1].interestBn).toBe(8);
});

it('uses published structural primary cash rather than a rounded ratio when available',()=>{
 const row={borrowingBn:50,interestBn:20,gdpBn:2000,structuralPrimaryBalanceBn:-17,structuralPrimaryBalancePct:-.9} as OutlookRow;
 expect(deficitParts(row,'bn').structuralPrimary).toBe(17);
 expect(deficitParts(row,'gdp').structuralPrimary).toBeCloseTo(.85);
});
