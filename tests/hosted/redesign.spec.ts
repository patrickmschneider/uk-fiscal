import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('overview gives a concise orientation and direct analytical paths',async({page},info)=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('./');await expect(page).toHaveTitle('Fiscal Space');
 await expect(page.getByRole('heading',{name:'The fiscal position.',exact:true})).toBeVisible();
 for(const name of ['Overview','Fiscal','Pricing','Debt & financing','Explore'])await expect(page.getByRole('navigation').getByRole('button',{name,exact:true})).toBeVisible();
 await expect(page.locator('.overview .chart-panel')).toHaveCount(3);
 await expect(page.locator('.overview .metric')).toHaveCount(0);
 await expect(page.locator('.overview')).toContainText('Accounting contributions, not estimates of policy effects');
 await expect(page.locator('#overview-position-title')).toBeVisible();
 expect(await page.locator('#overview-position-title').evaluate(e=>e.getBoundingClientRect().top)).toBeLessThan(900);
 await expect(page.getByRole('link',{name:'Spending & tax composition →',exact:true})).toHaveAttribute('href',/page=fiscal&section=composition/);
 await expect(page.getByRole('link',{name:'Compare yield curves →',exact:true})).toHaveAttribute('href','?page=pricing&units=gdp');
 await expect(page.getByRole('link',{name:'Outlook, assumptions & vintages →',exact:true})).toHaveAttribute('href',/section=outlook/);
 await page.screenshot({path:info.outputPath('overview-desktop.png')});
 await page.getByRole('link',{name:'Compare yield curves →',exact:true}).click();await expect(page.locator('#yield-curve-title')).toBeVisible();
 expect(errors).toEqual([]);
});

test('primary analytical destinations remain accessible on mobile',async({page},info)=>{
 test.setTimeout(120000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.setViewportSize({width:375,height:900});
 for(const [name,route] of [['overview',''],['outlook','?page=fiscal&section=outlook'],['reliefs','?page=explore&view=reliefs'],['series','?page=explore&view=series'],['methods','?page=explore&view=methodology']]){
  await page.goto(`./${route}`);await expect(page.locator('main h1').first()).toBeVisible();
  await expect(page.getByRole('status').filter({hasText:'Reading the validated data snapshot'})).toHaveCount(0);
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(axe.violations).toEqual([]);
  await page.screenshot({path:info.outputPath(`${name}-mobile.png`)});
 }
 expect(errors).toEqual([]);
});

test('tax relief search, filters and selected records survive reload and browser history',async({page})=>{
 await page.goto('./?page=explore&view=reliefs');
 const search=page.getByRole('searchbox',{name:'Find a relief'});await expect(search).toBeVisible();
 const units=page.getByRole('combobox',{name:'Relief units',exact:true});await expect(units).toHaveValue('gdp');
 await expect(page.getByRole('table',{name:'HMRC tax relief explorer',exact:true})).toBeVisible();
 await expect(page.getByText('Estimated cost of ISA tax relief',{exact:true})).not.toBeVisible();
 await search.fill('Individual Savings Accounts');
 const results=page.getByRole('table',{name:'HMRC tax relief explorer',exact:true});await expect(results.getByRole('button',{name:'Individual Savings Accounts',exact:true})).toBeVisible();
 await results.getByRole('button',{name:'Individual Savings Accounts',exact:true}).click();await expect(page.getByRole('region',{name:'Selected tax relief',exact:true})).toBeVisible();
 await units.selectOption('bn');await page.getByRole('combobox',{name:'Tax year',exact:true}).selectOption('2023-24');
 const saved=page.url();await page.reload();await expect(search).toHaveValue('Individual Savings Accounts');await expect(units).toHaveValue('bn');await expect(page.getByRole('combobox',{name:'Tax year',exact:true})).toHaveValue('2023-24');
 await expect(page.getByRole('region',{name:'Selected tax relief',exact:true})).toBeVisible();await expect(page).toHaveURL(saved);
 const tax=page.getByRole('combobox',{name:'Tax group',exact:true});await tax.selectOption('VAT');await expect(results.getByRole('button')).toHaveCount(0);
 await page.goBack();await expect(tax).toHaveValue('All');await expect(results.getByRole('button',{name:'Individual Savings Accounts',exact:true})).toBeVisible();
 await page.goForward();await expect(tax).toHaveValue('VAT');
 await page.goto('./?page=explore&view=reliefs&reliefClass=all');await page.getByText('Costs by tax head',{exact:true}).click();
 await expect(page.getByText('Choose one HMRC classification to aggregate costs.',{exact:false})).toBeVisible();
});

test('series explorer persists transformations, windows and units and exports',async({page})=>{
 await page.goto('./?page=explore&view=series');
 const series=page.getByRole('combobox',{name:'Series',exact:true}),transform=page.getByRole('combobox',{name:'Transformation',exact:true}),from=page.getByRole('combobox',{name:'From year',exact:true}),units=page.getByRole('combobox',{name:'Units',exact:true});
 await expect(from).toHaveValue('all');await expect(units).toHaveValue('gdp');
 await series.selectOption('vat');await transform.selectOption('cumulative');await from.selectOption('2019');await units.selectOption('bn');
 await expect(page.locator('[aria-labelledby="series-explorer-title"]')).toContainText('counter resets');
 const saved=page.url();await page.reload();await expect(series).toHaveValue('vat');await expect(transform).toHaveValue('cumulative');await expect(from).toHaveValue('2019');await expect(units).toHaveValue('bn');await expect(page).toHaveURL(saved);
 await from.selectOption('all');await page.goBack();await expect(from).toHaveValue('2019');await page.goForward();await expect(from).toHaveValue('all');
 const download=page.waitForEvent('download');await page.locator('[aria-labelledby="series-explorer-title"]').getByRole('button',{name:/Download .* CSV/}).click();await download;
 await series.selectOption('debtBillion');await expect(transform.locator('option[value=cumulative]')).toHaveCount(0);await expect(transform).toHaveValue('level');
 await expect(page.locator('#revenue-buoyancy-title')).toHaveCount(0);
});

test('outlook vintage state survives history while reconstruction and formal headroom remain distinct',async({page})=>{
 await page.goto('./?page=fiscal&section=outlook');
 const choice=page.getByRole('combobox',{name:'Forecast vintage',exact:true});await expect(choice.locator('option')).toHaveCount(2);
 await choice.selectOption('2025-11');await expect(page.locator('[aria-labelledby="outlook-path-borrowing-title"]')).toContainText('reconstructed');
 const saved=page.url();await page.reload();await expect(choice).toHaveValue('2025-11');await expect(page).toHaveURL(saved);
 await choice.selectOption('2026-03');await page.goBack();await expect(choice).toHaveValue('2025-11');await page.goForward();await expect(choice).toHaveValue('2026-03');
 await page.getByText('Fiscal stance and real spending growth',{exact:true}).click();await expect(page.locator('[aria-labelledby="stance-balance-title"] .recharts-line-dot').first()).toBeVisible();
 await page.getByRole('link',{name:'Fiscal rules, headroom and borrowing sensitivities →',exact:true}).click();
 await expect(page.locator('.rule-row').first()).toContainText('21.7');await expect(page.locator('.rule-row').first()).toContainText('Last formal assessment');
 await expect(page.locator('.coverage-note').filter({hasText:'March forecast update'})).toContainText('23.6');
 await expect(page.getByRole('table',{name:'Official OBR borrowing sensitivities',exact:true})).toBeVisible();
 await expect(page.locator('#headroom-history-title').locator('..').locator('..').locator('..')).toContainText('not a formal assessment');
});

test('shared units change headline and official forecast stocks and follow composition links',async({page,request})=>{
 const outlook=await (await request.get('data/outlook.json')).json();const vintage=outlook.vintages.slice().sort((a:{publicationDate:string},b:{publicationDate:string})=>a.publicationDate.localeCompare(b.publicationDate)).at(-1);const end=vintage.rows.at(-1);
 await page.goto('./');await page.getByRole('button',{name:'£bn',exact:true}).click();
 await expect(page.locator('.lead-sentence')).toContainText('£');
 await expect(page.getByRole('link',{name:'Compare yield curves →',exact:true})).toHaveAttribute('href','?page=pricing&units=bn');
 const debt=page.locator('[aria-labelledby="overview-path-debt-title"]');await debt.getByRole('button',{name:'Show data table for Debt outlook',exact:true}).click();
 await expect(debt.getByRole('table')).toContainText(end.debtBn.toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2}));
 await expect(debt.getByRole('table')).toContainText('OBR forecast (£bn)');
 await page.getByRole('link',{name:'Spending & tax composition →',exact:true}).click();
 await expect(page.getByRole('combobox',{name:'Budget history units',exact:true})).toHaveValue('bn');
 await page.getByRole('combobox',{name:'Budget breakdown',exact:true}).selectOption('detailed');await expect(page.getByRole('combobox',{name:'Composition financial year',exact:true}).locator('option')).toHaveCount(5);
 await page.goto('./?page=explore&view=series&units=bn');await page.getByRole('link',{name:'Budget composition',exact:true}).click();
 await expect(page).toHaveURL(/section=composition/);await expect(page.getByRole('combobox',{name:'Budget history units',exact:true})).toHaveValue('bn');
});
