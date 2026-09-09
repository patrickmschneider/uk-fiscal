import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs/promises';

async function chooseDate(page:import('@playwright/test').Page,label:string,date:string){
 const summary=page.locator(`summary[aria-label^="${label}: "]`);await summary.click();
 const calendar=page.getByRole('group',{name:`${label} calendar`,exact:true});
 await calendar.getByRole('combobox',{name:`${label} year`,exact:true}).selectOption(date.slice(0,4));
 await calendar.getByRole('combobox',{name:`${label} month`,exact:true}).selectOption(date.slice(0,7));
 const full=new Date(`${date}T12:00:00Z`).toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
 await calendar.getByRole('button',{name:full,exact:true}).click();
}

test('fiscal briefing, period controls, URL state and exports',async({page},testInfo)=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/?page=data&view=fiscal&period=ytd&units=bn');
  await expect(page.getByRole('heading',{name:'The UK’s fiscal position.'})).toBeVisible();
  await expect(page.locator('.metric').first()).toContainText('£56.7bn');
  await expect(page.locator('.briefing')).toContainText('£2.3bn above');
  await page.getByRole('button',{name:'Latest month',exact:true}).click();
  await expect(page.locator('.metric').first()).toContainText('£1.8bn');
  await page.reload();await expect(page.getByRole('button',{name:'Latest month',exact:true})).toHaveAttribute('aria-pressed','true');
  await page.getByText('Monthly borrowing against the OBR profile',{exact:true}).click();
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
  await page.getByRole('button',{name:'Fiscal',exact:true}).focus();await page.keyboard.press('Enter');await expect(page.getByRole('heading',{name:'The UK’s fiscal position.'})).toBeVisible();
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
 await chooseDate(page,'Observation date',latest.date);
 await chooseDate(page,'Compare with',previous.date);
 await page.getByRole('button',{name:'Show data table for RPI breakeven inflation',exact:true}).click();
 const point=latest.points.find((p:{tenor:number})=>p.tenor===10);
 await expect(page.getByRole('table',{name:'RPI breakeven inflation',exact:true})).toContainText(point.rate.toFixed(2));
 await page.getByText('RPI breakeven inflation: change in basis points',{exact:true}).click();
 const downloadPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download RPI breakeven inflation change CSV',exact:true}).click();
 const download=await downloadPromise;const file=testInfo.outputPath('breakeven-change.csv');await download.saveAs(file);
 const text=await fs.readFile(file,'utf8');expect(text).toContain('Maturity (years)');expect(text).toContain('Change (bp)');expect(text).toContain('Bank of England');expect(text).toContain('Bloomberg');expect(text).toContain('Tradeweb');
 const old=previous.points.find((p:{tenor:number})=>p.tenor===10);expect(text).toContain(String((point.rate-old.rate)*100));
 await page.setViewportSize({width:375,height:900});
 await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 const svgPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download Nominal gilt yield curve SVG',exact:true}).click();const svg=await svgPromise;const svgPath=testInfo.outputPath('pricing.svg');await svg.saveAs(svgPath);const exportedSvg=await fs.readFile(svgPath,'utf8');expect(exportedSvg).toContain('Maturity (years)');expect(exportedSvg).toContain('Bank of England');expect(exportedSvg).toContain('Tradeweb');
 const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
 await page.screenshot({path:testInfo.outputPath('pricing-mobile.png'),fullPage:true});
 await page.getByRole('button',{name:'Debt & financing',exact:true}).click();await expect(page.getByRole('heading',{name:'Nominal gilt yield curve',exact:true})).toHaveCount(0);
 await page.getByRole('button',{name:'Pricing',exact:true}).click();await expect(page).toHaveURL(new RegExp(`pricingDate=${latest.date}`));
});

test('fiscal GDP toggle changes flows, persists and exports denominators',async({page,request},testInfo)=>{
 const fiscal=await (await request.get('/data/fiscal.json')).json();const end=fiscal.asOf;
 const denominator=fiscal.gdp.observations.filter((r:{date:string})=>r.date<=end).at(-1);
 const borrowing=fiscal.observations.filter((r:{date:string})=>r.date>='2026-04').reduce((s:number,r:{borrowing:number})=>s+r.borrowing,0);
 await page.goto('/?page=data&view=fiscal&period=ytd');await page.getByRole('combobox',{name:'Flow units',exact:true}).selectOption('gdp');
 await expect(page.locator('.metric').first()).toContainText(`${(borrowing/denominator.rollingAnnualMillion*100).toFixed(2)}%`);
 await expect(page.locator('.briefing')).toContainText('pp above');
 await page.reload();await expect(page.getByRole('combobox',{name:'Flow units',exact:true})).toHaveValue('gdp');
 const csvPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Download Receipts and spending CSV',exact:true}).click();const csv=await csvPromise;const file=testInfo.outputPath('gdp.csv');await csv.saveAs(file);const text=await fs.readFile(file,'utf8');expect(text).toContain('% of GDP');expect(text).toContain('GDP denominator (£bn)');expect(text).toContain(denominator.date);
 await page.getByRole('button',{name:'Latest month',exact:true}).click();const last=fiscal.observations.at(-1);await expect(page.locator('.metric').first()).toContainText(`${(last.borrowing/denominator.rollingAnnualMillion*100).toFixed(2)}%`);
 await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
 await page.screenshot({path:testInfo.outputPath('gdp-mobile.png'),fullPage:true});
});


test('reload replaces a nominal-only snapshot and change calendars select historical dates',async({page,request})=>{
 const full=await (await request.get('/data/curve.json')).json();let serveLegacy=true;
 await page.route('**/data/curve.json',async route=>{const payload={...full};if(serveLegacy){delete payload.realCurves;delete payload.breakevenCurves;}await route.fulfill({json:payload});});
 await page.goto('/?page=pricing');await expect(page.getByText('This snapshot contains nominal yields',{exact:false})).toBeVisible();
 serveLegacy=false;await page.getByRole('button',{name:'Reload saved data',exact:true}).click();
 for(const id of ['real-curve','breakeven'])await expect(page.locator(`[aria-labelledby="${id}-title"] .recharts-line-curve`).first()).toBeVisible();
 await expect(page.getByText('This snapshot contains nominal yields',{exact:false})).toHaveCount(0);
 await page.getByText('Nominal gilt yield curve: change in basis points',{exact:true}).click();
 const earlier=full.curves[20],later=full.curves[100];
 await chooseDate(page,'Nominal gilt yield curve: observation date',later.date);
 await chooseDate(page,'Nominal gilt yield curve: compare with',earlier.date);
 await expect(page).toHaveURL(new RegExp(`pricingDate=${later.date}.*pricingCompare=${earlier.date}`));
 await page.getByRole('button',{name:'Show data table for Nominal gilt yield curve change',exact:true}).click();
 const ten=(c:{points:{tenor:number;rate:number}[]})=>c.points.find(p=>p.tenor===10)!.rate;
 await expect(page.getByRole('table',{name:'Nominal gilt yield curve change',exact:true})).toContainText(((ten(later)-ten(earlier))*100).toFixed(2));
 await page.locator('summary[aria-label^="Compare with: "]').click();const calendar=page.getByRole('group',{name:'Compare with calendar',exact:true});
 await expect(calendar.locator('.calendar-grid button:disabled').first()).toBeDisabled();
 const month=calendar.getByRole('combobox',{name:'Compare with month',exact:true});const before=await month.inputValue();await calendar.getByRole('button',{name:'Compare with: next month',exact:true}).click();await expect(month).not.toHaveValue(before);
 await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
 await page.keyboard.press('Escape');await expect(calendar).not.toBeVisible();
});


test('failed curve reload preserves all last-good pricing curves',async({page})=>{
 await page.goto('/?page=pricing');await expect(page.locator('[aria-labelledby="breakeven-title"] .recharts-line-curve').first()).toBeVisible();
 await page.route('**/data/curve.json',route=>route.fulfill({status:503,body:'temporarily unavailable'}));
 await page.getByRole('button',{name:'Reload saved data',exact:true}).click();
 await expect(page.getByText('Some saved data could not be loaded.',{exact:false})).toBeVisible();
 for(const id of ['yield-curve','real-curve','breakeven'])await expect(page.locator(`[aria-labelledby="${id}-title"] .recharts-line-curve`).first()).toBeVisible();
});

test('annual composition changes reconcile, switch units and preserve comparisons',async({page,request},info)=>{
 const composition=await (await request.get('/data/composition.json')).json();
 await page.goto('/?page=fiscal&section=composition&bhMode=change');
 await expect(page.getByRole('table',{name:'Budget change contributions'})).toContainText('Net social benefits (including pensions)');
 await page.getByText('Accounting boundaries and supporting measures',{exact:true}).click();
 await expect(page.getByRole('table',{name:'Interest and dividend bridge'})).toContainText('1.45');
 await page.getByRole('combobox',{name:'Budget breakdown',exact:true}).selectOption('functional');
 await page.getByRole('combobox',{name:'Budget comparison start',exact:true}).selectOption('2019-20');
 await page.getByRole('combobox',{name:'Budget comparison end',exact:true}).selectOption('2025-26');
 const first=composition.history.years.find((y:{year:string})=>y.year==='2019-20'),last=composition.history.years.find((y:{year:string})=>y.year==='2025-26');
 const health=(y:{items:{name:string;pctGdp:number}[]})=>y.items.find(i=>i.name==='Health')!.pctGdp;
 const table=page.getByRole('table',{name:'Budget change contributions',exact:true});await expect(table.getByRole('row').filter({hasText:'Health'})).toContainText((health(last)-health(first)).toFixed(2));
 await page.getByRole('combobox',{name:'Budget history units',exact:true}).selectOption('bn');
 const amount=(y:{items:{name:string;value:number}[]})=>y.items.find(i=>i.name==='Health')!.value;
 await expect(table.getByRole('row').filter({hasText:'Health'})).toContainText(((amount(last)-amount(first))/1000).toFixed(2));
 await page.reload();await expect(page.getByRole('combobox',{name:'Budget history units',exact:true})).toHaveValue('bn');
 await page.getByRole('combobox',{name:'Budget history units',exact:true}).selectOption('share');
 await expect(table.getByRole('row').filter({hasText:'Health'})).toContainText((amount(last)/last.total*100-amount(first)/first.total*100).toFixed(2));
 const csv=page.waitForEvent('download');await page.getByRole('button',{name:'Download comparison CSV',exact:true}).click();const file=info.outputPath('contributions.csv');await (await csv).saveAs(file);expect(await fs.readFile(file,'utf8')).toContain('percentage points of expenditure on services');
 await page.getByRole('button',{name:'Over time',exact:true}).click();await expect(page.locator('#budget-history-title')).toBeVisible();
 await expect(page.locator('[aria-labelledby="budget-history-title"] .recharts-label').filter({hasText:'Financial year'})).toBeVisible();
 await page.getByRole('combobox',{name:'Budget breakdown',exact:true}).selectOption('receipts');await expect(page.getByRole('heading',{name:'Tax take versus total receipts',exact:true})).toBeVisible();
 await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 expect((await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze()).violations).toEqual([]);
});

test('RPI chart exposes its comparison calendar and updates the plotted comparison',async({page,request})=>{
 const data=await (await request.get('/data/curve.json')).json();const old=data.breakevenCurves[30];
 await page.goto('/?page=pricing');
 const panel=page.locator('[aria-labelledby="breakeven-title"]');
 await expect(panel.locator('summary[aria-label^="RPI breakeven: compare with: "]')).toBeVisible();
 await chooseDate(page,'RPI breakeven: compare with',old.date);
 await page.getByRole('button',{name:'Show data table for RPI breakeven inflation',exact:true}).click();
 await expect(panel.getByRole('table')).toContainText(old.points.find((p:{tenor:number})=>p.tenor===10).rate.toFixed(2));
 await expect(page).toHaveURL(new RegExp(`pricingCompare=${old.date}`));
});

test('detailed composition keeps precise amounts and matched-year GDP denominators',async({page,request},info)=>{
 const fiscal=await (await request.get('/data/fiscal.json')).json(),composition=await (await request.get('/data/composition.json')).json();
 const annual=composition.years.at(-1),health=annual.items.find((x:{name:string})=>x.name==='Health');
 const end=`${Number(annual.year.slice(0,4))+1}-03`,gdp=fiscal.gdp.observations.find((x:{date:string})=>x.date===end).rollingAnnualMillion;
 await page.goto('/?page=fiscal&section=composition&bhDataset=detailed');
 const healthRow=page.locator('.bar-list li').filter({hasText:'Health'});
 await expect(healthRow).toContainText(`${(health.value/gdp*100).toFixed(2)} % of GDP`);
 await page.getByRole('combobox',{name:'Budget history units',exact:true}).selectOption('share');
 await expect(healthRow).toContainText((health.value/annual.total*100).toFixed(2));
 await page.getByRole('combobox',{name:'Budget history units',exact:true}).selectOption('bn');
 await expect(healthRow).toContainText((health.value/1000).toFixed(2));
 const pending=page.waitForEvent('download');await page.getByRole('button',{name:'Download composition CSV',exact:true}).click();const file=info.outputPath('composition.csv');await(await pending).saveAs(file);expect(await fs.readFile(file,'utf8')).toContain('Health');
 await page.reload();await expect(page.getByRole('combobox',{name:'Budget history units',exact:true})).toHaveValue('bn');
 await page.getByRole('combobox',{name:'Composition financial year',exact:true}).selectOption(composition.years[0].year);
 await expect(healthRow).toContainText((composition.years[0].items.find((x:{name:string})=>x.name==='Health').value/1000).toFixed(2));
 await page.setViewportSize({width:375,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 expect((await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze()).violations).toEqual([]);
});
