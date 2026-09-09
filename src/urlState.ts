import {createElement,useEffect,useState,type AnchorHTMLAttributes} from 'react';
/** Query state is the shareable view; notify sibling controls and browser history. */
export function useParam(key:string,fallback:string,mode:'push'|'replace'='push'){
 const read=()=>new URLSearchParams(location.search).get(key)??fallback;
 const [value,setValue]=useState(read);
 useEffect(()=>{const update=()=>setValue(read());update();window.addEventListener('popstate',update);return()=>window.removeEventListener('popstate',update);},[key,fallback]);
 const update=(value:string)=>{const url=new URL(location.href);url.searchParams.set(key,value);if(url.href!==location.href){history[mode==='replace'?'replaceState':'pushState']({},'',url);window.dispatchEvent(new PopStateEvent('popstate'));}setValue(value);};
 return [value,update] as const;
}

/** Render the shareable URL itself, including open-in-new-tab and copy-link actions. */
export function ViewLink(props:AnchorHTMLAttributes<HTMLAnchorElement>){
 const [units]=useParam('units','gdp');let href=props.href;
 if(href?.startsWith('?')){const url=new URL(href,location.href);if(url.searchParams.has('page')&&!url.searchParams.has('units'))url.searchParams.set('units',units);href=url.search+url.hash;}
 return createElement('a',{...props,href});
}
