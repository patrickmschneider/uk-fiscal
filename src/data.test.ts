import {describe,it,expect} from 'vitest';
import {fiscalStart,periodsFor,total,cumulative,csvText,calendarAnniversary,operationEnd,isOverdue,type Observation} from './data';
describe('fiscal accounting boundaries',()=>{
 it('uses April financial years',()=>{expect(fiscalStart('2026-03')).toBe(2025);expect(fiscalStart('2026-04')).toBe(2026);expect(periodsFor('2026-03','ytd')).toHaveLength(12);expect(periodsFor('2026-04','ytd')).toEqual(['2026-04']);});
 it('requires every month, including explicit nulls',()=>{const rows:Observation[]=[{date:'2026-04',borrowing:4},{date:'2026-06',borrowing:3}];expect(total(rows,'borrowing','2026-06','ytd')).toBeNull();expect(total(rows,'borrowing','2026-04','rolling')).toBeNull();expect(total([{date:'2026-04',borrowing:null}],'borrowing','2026-04','month')).toBeNull();});
 it('retains surplus signs and leaves future cumulative values missing',()=>{const rows=[{date:'2026-04',borrowing:4},{date:'2026-05',borrowing:-6}];expect(cumulative(rows,2026).slice(0,3)).toEqual([4,-2,null]);});
 it('quotes CSV and neutralises text formulas without corrupting negative numbers',()=>{const result=csvText(['name','value'],[['=BAD',-3],['a,"b',null]]);expect(result).toContain("\"'=BAD\",\"-3\"");expect(result).toContain('"a,""b"');});
 it('uses a calendar anniversary including leap day',()=>{expect(calendarAnniversary('2026-09-06')).toBe('2027-09-06');expect(calendarAnniversary('2024-02-29')).toBe('2025-02-28');});
 it('keeps a syndication window open during its week',()=>{expect(operationEnd({date:'2026-09-07',datePrecision:'week',type:'syndication',name:'test',amountMillion:null,status:'planned',sourceUrl:''})).toBe('2026-09-13');});
 it('flags an old curve even on a current build',()=>{expect(isOverdue('curve','2026-08-01',new Date('2026-09-06'))).toBe(true);expect(isOverdue('curve','2026-09-04',new Date('2026-09-06'))).toBe(false);});
});
