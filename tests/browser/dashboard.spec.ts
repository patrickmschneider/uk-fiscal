import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs/promises';

test('fiscal briefing, period controls, URL state and exports',async({page},testInfo)=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/?page=fiscal');
  await expect(page.getByRole('heading',{name:'The UK’s fiscal position.'})).toBeVisible();
  await expect(page.locator('.metric').first()).toContainText('£56.7bn');
  await expect(page.locator('.briefing')).toContainText('£2.3bn above');
  await page.getByRole('button',{name:'Latest month',exact:true}).click();
  await expect(page.locator('.metric').first()).toContainText('£1.8bn');
  await page.reload();await expect(page.getByRole('button',{name:'Latest month',exact:true})).toHaveAttribute('aria-pressed','true');
  await page.getByRole('button',{name:'Show data table for Borrowing against the forecast',exact:true}).click();
  await expect(page.getByRole('table',{name:'Borrowing against the forecast',exact:true})).toContainText('56.70');
  const csvPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download Borrowing against the forecast CSV',exact:true}).click();const csv=await csvPromise;
  const csvPath=testInfo.outputPath('borrowing.csv');await csv.saveAs(csvPath);const text=await fs.readFile(csvPath,'utf8');expect(text).toContain('OBR');expect(text).toContain('56.696');
  await page.getByRole('button',{name:'Show chart for Borrowing against the forecast',exact:true}).click();
  await page.setViewportSize({width:375,height:900});
  const svgPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download Borrowing against the forecast SVG',exact:true}).click();const svg=await svgPromise;const svgPath=testInfo.outputPath('borrowing.svg');await svg.saveAs(svgPath);const image=await fs.readFile(svgPath,'utf8');expect(image).toContain('width="960"');expect(image).toContain('stroke-dasharray="6 5"');expect(image).toContain('ONS');
  await page.getByText('Explore receipts',{exact:true}).click();await page.getByRole('combobox',{name:'Receipt series',exact:true}).selectOption('vat');await expect(page.getByRole('heading',{name:'VAT',exact:true})).toBeVisible();
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
  await page.screenshot({path:testInfo.outputPath('fiscal-mobile.png'),fullPage:true});expect(errors).toEqual([]);
});

test('debt windows, filtering, keyboard and mobile access',async({page},testInfo)=>{
  await page.clock.setFixedTime(new Date('2026-09-09T12:00:00Z'));
  await page.goto('/?page=debt');await expect(page.getByRole('heading',{name:'The stock. The cost. The calendar.'})).toBeVisible();
  await expect(page.locator('.next-operation')).toContainText('Week commencing');
  await page.getByText('Redemptions in the next 12 months',{exact:true}).click();await expect(page.getByRole('table',{name:'Upcoming gilt redemptions'})).toBeVisible();
  await page.getByText('Explore the gilt stock',{exact:true}).click();await page.getByLabel('Find a gilt').fill('GB00BNNGP668');await expect(page.getByRole('table',{name:'Gilts outstanding'}).locator('tbody tr')).toHaveCount(1);
  await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.getByRole('button',{name:'Fiscal position',exact:true}).focus();await page.keyboard.press('Enter');await expect(page.getByRole('heading',{name:'The UK’s fiscal position.'})).toBeVisible();
  await page.getByRole('button',{name:'Debt & financing',exact:true}).click();
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
  await page.screenshot({path:testInfo.outputPath('debt-mobile.png'),fullPage:true});
});

test('Pricing compares matched curves and exports maturity-labelled changes',async({page,request},testInfo)=>{
 const curve=await (await request.get('/data/curve.json')).json();
 const latest=curve.breakevenCurves.at(-1),previous=curve.breakevenCurves.at(-2);
 await page.goto('/?page=pricing');
 await expect(page.getByRole('heading',{name:'Yields and inflation pricing.'})).toBeVisible();
 await expect(page.getByRole('heading',{name:'RPI breakeven inflation',exact:true})).toBeVisible();
 await expect(page.locator('text.recharts-label:visible').filter({hasText:'Maturity (years)'})).toHaveCount(3);
 await page.getByRole('combobox',{name:'Observation date',exact:true}).selectOption(latest.date);
 await page.getByRole('combobox',{name:'Compare with',exact:true}).selectOption(previous.date);
 await page.getByRole('button',{name:'Show data table for RPI breakeven inflation',exact:true}).click();
 const point=latest.points.find((p:{tenor:number})=>p.tenor===10);
 await expect(page.getByRole('table',{name:'RPI breakeven inflation',exact:true})).toContainText(point.rate.toFixed(2));
 await page.getByText('RPI breakeven inflation: change in basis points',{exact:true}).click();
 const downloadPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download RPI breakeven inflation change CSV',exact:true}).click();
 const download=await downloadPromise;const file=testInfo.outputPath('breakeven-change.csv');await download.saveAs(file);
 const text=await fs.readFile(file,'utf8');expect(text).toContain('Maturity (years)');expect(text).toContain('Change (bp)');
 const old=previous.points.find((p:{tenor:number})=>p.tenor===10);expect(text).toContain(String((point.rate-old.rate)*100));
 await page.setViewportSize({width:375,height:900});
 await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 const svgPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download Nominal gilt yield curve SVG',exact:true}).click();const svg=await svgPromise;const svgPath=testInfo.outputPath('pricing.svg');await svg.saveAs(svgPath);expect(await fs.readFile(svgPath,'utf8')).toContain('Maturity (years)');
 const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
 await page.screenshot({path:testInfo.outputPath('pricing-mobile.png'),fullPage:true});
 await page.getByRole('button',{name:'Debt & financing',exact:true}).click();await expect(page.getByRole('heading',{name:'Nominal gilt yield curve',exact:true})).toHaveCount(0);
 await page.getByRole('button',{name:'Pricing',exact:true}).click();await expect(page.getByRole('combobox',{name:'Observation date',exact:true})).toHaveValue(latest.date);
});

test('fiscal GDP toggle changes flows, persists and exports denominators',async({page,request},testInfo)=>{
 const fiscal=await (await request.get('/data/fiscal.json')).json();const end=fiscal.asOf;
 const denominator=fiscal.gdp.observations.filter((r:{date:string})=>r.date<=end).at(-1);
 const borrowing=fiscal.observations.filter((r:{date:string})=>r.date>='2026-04').reduce((s:number,r:{borrowing:number})=>s+r.borrowing,0);
 await page.goto('/?page=fiscal');await page.getByRole('combobox',{name:'Flow units',exact:true}).selectOption('gdp');
 await expect(page.locator('.metric').first()).toContainText(`${(borrowing/denominator.rollingAnnualMillion*100).toFixed(2)}%`);
 await expect(page.locator('.briefing')).toContainText('pp above');
 await page.reload();await expect(page.getByRole('combobox',{name:'Flow units',exact:true})).toHaveValue('gdp');
 const csvPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download Receipts and spending CSV',exact:true}).click();const csv=await csvPromise;const file=testInfo.outputPath('gdp.csv');await csv.saveAs(file);const text=await fs.readFile(file,'utf8');expect(text).toContain('% of GDP');expect(text).toContain('GDP denominator (£bn)');expect(text).toContain(denominator.date);
 await page.getByRole('button',{name:'Latest month',exact:true}).click();const last=fiscal.observations.at(-1);await expect(page.locator('.metric').first()).toContainText(`${(last.borrowing/denominator.rollingAnnualMillion*100).toFixed(2)}%`);
 await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
 await page.screenshot({path:testInfo.outputPath('gdp-mobile.png'),fullPage:true});
});
