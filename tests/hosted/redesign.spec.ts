import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
test('the briefing introduces the story and every investigation route works',async({page},info)=>{
 test.setTimeout(90000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('./');await expect(page).toHaveTitle('The Fiscal Space');
 await expect(page.getByRole('heading',{name:'The UK’s fiscal position, explained.'})).toBeVisible();
 await expect(page.locator('.headline-strip .metric')).toHaveCount(4);
 await expect(page.getByRole('heading',{name:'The Budget isn’t the whole story'})).toBeVisible();
 for(const name of ['Briefing','Outlook','Fiscal Rules','Tax Reliefs','Data'])await expect(page.getByRole('navigation').getByRole('button',{name,exact:true})).toBeVisible();
 await page.screenshot({path:info.outputPath('briefing-desktop.png')});
 for(const route of ['briefing','outlook','rules','reliefs','data&view=methodology']){
  await page.goto(`./?page=${route}`);await expect(page.locator('h1').first()).toBeVisible();
  await page.setViewportSize({width:375,height:900});
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
  await page.screenshot({path:info.outputPath(`${route.split('&')[0]}-mobile.png`)});
 }
 expect(errors).toEqual([]);
});
test('tax relief filters, source statuses, detail links and ISA history are usable',async({page})=>{
 await page.goto('./?page=reliefs');await expect(page.getByRole('heading',{name:'Tax reliefs.',exact:true})).toBeVisible();
 await expect(page.getByRole('heading',{name:'Tax relief cost ≠ revenue available'})).toBeVisible();
 await expect(page.locator('.relief-ranking li')).toHaveCount(20);
 await page.locator('.relief-ranking button').first().click();await expect(page.getByRole('region',{name:'Selected tax relief'})).toBeVisible();
 await expect(page).toHaveURL(/relief=/);await page.reload();await expect(page.getByRole('region',{name:'Selected tax relief'})).toBeVisible();
 await page.getByRole('combobox',{name:'Relief units',exact:true}).selectOption('gdp');
 await expect(page.locator('[aria-labelledby="reliefs-evolution-title"] .recharts-line-curve').first()).toBeVisible();
 await expect(page.getByRole('heading',{name:'Estimated cost of ISA tax relief',exact:true})).toBeVisible();
 await page.getByRole('combobox',{name:'Tax group',exact:true}).selectOption('VAT');
 await expect(page.locator('.relief-ranking')).toContainText('VAT');
});
test('series explorer exposes coherent transforms and exports',async({page})=>{
 await page.goto('./?page=data&view=series');await page.getByRole('combobox',{name:'Series',exact:true}).selectOption('vat');
 await page.getByRole('combobox',{name:'Transformation',exact:true}).selectOption('cumulative');
 await expect(page.locator('[aria-labelledby="series-explorer-title"]')).toContainText('counter resets');
 const download=page.waitForEvent('download');await page.getByRole('button',{name:/Download .* CSV/}).first().click();await download;
 await page.getByRole('combobox',{name:'Series',exact:true}).selectOption('debtBillion');
 await expect(page.getByRole('combobox',{name:'Transformation',exact:true}).locator('option[value=cumulative]')).toHaveCount(0);
});
test('outlook vintages and formal headroom remain distinct',async({page})=>{
 await page.goto('./?page=outlook');
 const choice=page.getByRole('combobox',{name:'Forecast vintage',exact:true});await expect(choice.locator('option')).toHaveCount(2);
 await choice.selectOption('2025-11');await expect(page.locator('[aria-labelledby="outlook-borrowing-title"]')).toContainText('reconstructed');
 await expect(page.locator('[aria-labelledby="stance-balance-title"] .recharts-line-dot').first()).toBeVisible();
 await page.getByRole('navigation').getByRole('button',{name:'Fiscal Rules',exact:true}).click();
 await expect(page.locator('.rule-row').first()).toContainText('21.7');
 await expect(page.locator('.coverage-note').filter({hasText:'March forecast update'})).toContainText('23.6');
 await expect(page.getByRole('table',{name:'Official OBR borrowing sensitivities'})).toBeVisible();
});
