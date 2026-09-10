import {it,expect} from 'vitest';
import {forecastLabelPosition} from './chartPlacement';
it('puts labels opposite high or low forecast data',()=>{
 expect(forecastLabelPosition([{v:20,status:'Outturn'},{v:95,status:'Forecast'}],['v'])).toBe('insideBottom');
 expect(forecastLabelPosition([{v:95,status:'Outturn'},{v:20,status:'Forecast'}],['v'])).toBe('insideTop');
});
it('accounts for both ends of signed stacks and avoids a crowded plot',()=>{
 const rows=[{a:8,b:-2,total:6,status:'Forecast'}];
 expect(forecastLabelPosition(rows,['a','b'],true,'total',[-3,9])).toBe('top');
 expect(forecastLabelPosition(rows,['a','b'],true,'total',[-3,20])).toBe('insideTop');
});
