import {it,expect} from 'vitest';
import {deficitParts} from './deficitMath';
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
