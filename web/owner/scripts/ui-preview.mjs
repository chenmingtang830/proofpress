import { createServer } from 'vite';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';
import * as synthetic from './ui-preview-data.mjs';

// Optional offline receipt bundle stays outside the repository. No hosted API,
// credentials or owner session is exposed by this presentation-only server.
const supplied = process.env.PROOFPRESS_PREVIEW_DATA
  ? JSON.parse(readFileSync(process.env.PROOFPRESS_PREVIEW_DATA, 'utf8')) : null;
const { receipts, graph, context, activity, runs, policy } = supplied || synthetic;

// A loopback-only presentation server. No credentials, database, or live API.
const port = Number(process.env.PROOFPRESS_UI_PORT || 7335);
const server = await createServer({
  root:fileURLToPath(new URL('..',import.meta.url)),
  server:{host:'127.0.0.1',port,strictPort:true},
  plugins:[{name:'synthetic-ui-preview',transformIndexHtml(){return [
    {tag:'style',children:'@media(max-width:899px){.shell .workspaceLabel .workspaceContext{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.workspaceLabel strong{display:none}}',injectTo:'head'},
    ...(supplied ? [{tag:'div', attrs:{style:'position:fixed;bottom:12px;left:12px;right:12px;z-index:9999;padding:9px 16px;background:#103e46;color:white;border-radius:8px;font:13px system-ui;text-align:center;pointer-events:none'}, children:'Local reconstruction · read-only · checks executed locally · cloud workspace unchanged', injectTo:'body'}] : [])
  ];},configureServer(server){
    server.middlewares.use(async (req,res,next)=>{
      const url = new URL(req.url,'http://127.0.0.1');
      if (!url.pathname.startsWith('/owner/') && !url.pathname.startsWith('/v1/owner/')) return next();
      res.setHeader('Content-Type','application/json');
      res.setHeader('Cache-Control','no-store');
      const send=(result,status=200)=>{res.statusCode=status;res.end(JSON.stringify(result));};
      if (req.method!=='GET') return send({ok:false,error:{message:'This is a read-only local preview. No decision, setting, credential, or external request was recorded.'}},409);
      const scenario = /pp-preview-scenario=(\w+)/.exec(req.headers.cookie || '')?.[1];
      if (scenario==='slow') await new Promise(resolve=>setTimeout(resolve,1600));
      if (scenario==='error' && url.pathname==='/owner/api/context') return send({ok:false,error:{message:'Preview connection interrupted. Reload workspace to try again.'}},503);
      const empty = scenario==='empty';
      const routes = {
        '/owner/api/session':{workspace:supplied?.workspaceLabel || 'Local preview · synthetic data',csrf:'preview-not-a-credential',capabilities:{judge:!supplied,credential_admin:!supplied},principal:supplied ? 'agent:offline-preview' : "human:preview",local_owner_preview:true},
        '/owner/api/graph':empty?{nodes:[],edges:[]}:graph,
        '/owner/api/context':empty?{governed_context:[],relations:[]}:context,
        '/owner/api/activity':empty?[]:activity,
        '/owner/api/technical-logs':[],
        '/owner/api/runs':{runs:empty?[]:runs},
        '/owner/api/review-policy':policy,
        '/owner/api/capture-policy':{version:0,settings:{purpose:'Preserve bounded findings that future work can reuse.',capture:['Evidence-backed conclusions','Durable decisions','Reproducible results'],exclude:['Unvalidated hypotheses','Duplicate findings','Routine progress updates']}},
        '/v1/owner/credentials':{credentials:[{credential_id:'preview-agent',principal_id:'agent:research',label:'Research agent · example',role:'agent',created_at:'2026-10-13T15:30:00Z'}]},
      };
      const claim = receipts[decodeURIComponent(url.pathname.replace('/owner/api/claims/',''))];
      const run = runs.find(run=>`/owner/api/runs/${run.id}`===url.pathname);
      const result = routes[url.pathname] ?? claim ?? run;
      return result ? send({ok:true,result}) : send({ok:false,error:{message:'Preview record not found.'}},404);
    });
  }}],
});
await server.listen();
console.log(`Proofpress UI preview: http://127.0.0.1:${port}/home`);
console.log(supplied ? 'Offline receipt bundle · read-only · no hosted connection' : 'Synthetic data · read-only · no hosted connection');
for (const signal of ['SIGINT','SIGTERM']) process.on(signal,async()=>{await server.close();process.exit(0);});
