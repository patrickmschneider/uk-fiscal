import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('published app loads its data, navigation and charts beneath the project path',async({page,request})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 const response=await request.get('data/fiscal.json');expect(response.ok()).toBe(true);const fiscal=await response.json();
 await page.goto('./?page=fiscal');await expect(page.getByRole('heading',{name:'The UK’s fiscal position.'})).toBeVisible();
 await page.getByRole('combobox',{name:'Flow units',exact:true}).selectOption('gdp');
 await page.getByRole('button',{name:'Debt & financing',exact:true}).click();await expect(page.getByRole('heading',{name:'The stock. The cost. The calendar.'})).toBeVisible();
 await page.getByRole('button',{name:'Pricing',exact:true}).click();await expect(page.getByRole('heading',{name:'Yields and inflation pricing.'})).toBeVisible();
 const curve=await (await request.get('data/curve.json')).json();
 for(const id of ['yield-curve','real-curve','breakeven'])await expect(page.locator(`[aria-labelledby="${id}-title"] .recharts-line-curve`).first()).toBeVisible();
 await expect(page.getByRole('link',{name:'Bank of England · Gilt yield curves',exact:true}).first()).toBeVisible();
 await page.reload();await expect(page.getByRole('heading',{name:'RPI breakeven inflation',exact:true})).toBeVisible();
 expect(curve.breakevenCurves.length).toBeGreaterThan(0);expect(fiscal.observations.at(-1).date).toBe(fiscal.asOf);
 await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 const accessibility=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(accessibility.violations).toEqual([]);
 await page.locator('.brand').click();await expect(page.getByRole('heading',{name:'The UK’s fiscal position.'})).toBeVisible();
 expect(errors).toEqual([]);
});
