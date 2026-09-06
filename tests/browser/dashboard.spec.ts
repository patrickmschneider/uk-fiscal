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
