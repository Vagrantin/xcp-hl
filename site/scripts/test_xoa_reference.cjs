// Client/configuration contracts only: no running appliance or XAPI operations.
// Run with XOA_REFERENCE_MODULES pointing to the pinned fixture dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const https = require('node:https');
const { spawn, execFileSync } = require('node:child_process');
const { createHash } = require('node:crypto');
const modules = process.env.XOA_REFERENCE_MODULES;
assert(modules, 'Set XOA_REFERENCE_MODULES to the fixture node_modules directory');
const cli = path.join(modules, 'xo-cli/index.mjs');
for (const [name, version] of [['xo-cli','0.32.2'], ['xo-lib','0.11.1'], ['app-conf','3.0.0'], ['@iarna/toml','2.2.5'], ['ws','8.18.3']]) {
  assert.equal(JSON.parse(fs.readFileSync(path.join(modules,name,'package.json'))).version, version);
}
// The npm CLI's help text differs from the pin. The runner fetches these exact
// source files; hashes prevent an unnoticed move to current upstream.
for (const [name, hash] of [
  ['index.mjs','88ab9dd096b21a60d72cc0adf26eaa29f2a797a0661844cfc4f89616515872b8'],
  ['config.mjs','70b55517018213fd861a52f645eaedaa41f3db80b44e37366266328120af4698'],
]) assert.equal(createHash('sha256').update(fs.readFileSync(path.join(modules,'xo-cli',name))).digest('hex'),hash);
const { WebSocketServer } = require(path.join(modules,'ws'));
const TOML = require(path.join(modules,'@iarna/toml'));
const appConf = require(path.join(modules,'app-conf'));
const scratch = fs.mkdtempSync(path.join(os.tmpdir(),'xoa-reference-'));
process.umask(0o077);
const configRoot = path.join(scratch,'client');
const key = path.join(scratch,'key.pem'), cert = path.join(scratch,'cert.pem');
execFileSync('openssl',['req','-x509','-newkey','rsa:2048','-nodes','-days','1',
  '-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost','-keyout',key,'-out',cert],{stdio:'ignore'});
const calls=[];
let revoked=false;
const objects = {
  'vm-fixture': { id:'vm-fixture',type:'VM',name_label:'Disposable VM',power_state:'Halted',privateFixtureField:'omitted' },
  'host-fixture': { id:'host-fixture',type:'host',name_label:'Disposable host' },
};
const server = https.createServer({key:fs.readFileSync(key),cert:fs.readFileSync(cert)});
const wss = new WebSocketServer({server});
wss.on('connection',(socket,request)=> {
  assert.equal(request.url,'/api/');
  let authenticated=false;
  socket.on('message',raw=> {
    const request=JSON.parse(raw);
    const {id,method,params={}}=request;
    // All credentials are invented fixture data, never an appliance secret.
    calls.push({method,params});
    let result, error;
    if(method==='session.signIn') {
      authenticated=!revoked && (params.token==='fixture-token' ||
        params.email==='fixture@example.invalid' && params.password==='fixture-password');
      if(authenticated) result={id:'fixture-user',email:'fixture@example.invalid',permission:'none'};
      else error={code:1,message:'invalid credentials'};
    } else if(!authenticated) error={code:1,message:'authentication required'};
    else if(method==='token.create') result='fixture-token';
    else if(method==='system.getServerVersion') result='5.193.1';
    else if(method==='system.getMethodsInfo') result={
      'xo.getAllObjects':{params:{filter:{type:['object','string'],optional:true},limit:{type:'number',optional:true}}},
      'vm.start':{params:{id:{type:'string'}}},
    };
    else if(method==='xo.getAllObjects') {
      const selected=Object.entries(objects).filter(([,o])=>!params.filter ||
        Object.entries(params.filter).every(([k,v])=>o[k]===v));
      result=Object.fromEntries(selected.slice(0,params.limit ?? selected.length));
    } else error={code:-32601,message:'unknown fixture method'};
    socket.send(JSON.stringify({jsonrpc:'2.0',id,...(error ? {error} : {result})}));
  });
});
function run(args,{trust=true,prompt=false}={}) {
  // A real PTY exercises the CLI's existing password reader without changing it.
  const ptyRunner = `import os,pty,select,subprocess,sys,time,termios\nm,s=pty.openpty()\np=subprocess.Popen(sys.argv[1:],stdin=s,stdout=s,stderr=s,close_fds=True)\nos.close(s)\nsent=False\nwhile True:\n try:\n  data=os.read(m,4096)\n except OSError:\n  break\n if not data: break\n sys.stdout.buffer.write(data);sys.stdout.buffer.flush()\n if b'Password: ' in data and not sent:\n  deadline=time.monotonic()+2\n  while termios.tcgetattr(m)[3] & termios.ECHO and time.monotonic()<deadline:\n   time.sleep(0.01)\n  os.write(m,b'fixture-password\\n');sent=True\nos.close(m)\nsys.exit(p.wait())\n`;
  const command=prompt?'python3':process.execPath;
  const argv=prompt?['-c',ptyRunner,process.execPath,cli,...args]:[cli,...args];
  return new Promise((resolve,reject)=> {
    const env={...process.env,XDG_CONFIG_HOME:configRoot};
    delete env.NODE_EXTRA_CA_CERTS;
    delete env.NODE_TLS_REJECT_UNAUTHORIZED;
    if(trust) env.NODE_EXTRA_CA_CERTS=cert;
    const child=spawn(command,argv,{env,stdio:['ignore','pipe','pipe']});
    let stdout='',stderr='';
    child.stdout.on('data',d=>stdout+=d); child.stderr.on('data',d=>stderr+=d);
    const timeout=setTimeout(()=>{child.kill('SIGKILL');reject(new Error('CLI fixture timeout'));},15000);
    child.on('error',reject);
    child.on('close',code=>{clearTimeout(timeout);resolve({code,stdout,stderr});});
  });
}
(async()=> {
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const url=`https://localhost:${server.address().port}`;
  // Untrusted TLS must fail with the client's normal verification enabled.
  let result=await run(['register','--token','fixture-token',url],{trust:false});
  // --token register only stores credentials; verification happens on connect.
  assert.equal(result.code,0);
  result=await run(['system.getServerVersion','--json'],{trust:false});
  assert.notEqual(result.code,0);
  assert.match(result.stderr,/self.signed|certificate/i);
  assert.equal(calls.length,0);
  result=await run(['register','--token','fixture-token',url.replace('localhost','127.0.0.1')]);
  assert.equal(result.code,0);
  result=await run(['system.getServerVersion','--json']);
  assert.notEqual(result.code,0);
  assert.match(result.stderr,/altname|altnames|certificate.*IP/i);
  assert.equal(calls.length,0,'trust must not disable hostname validation');
  result=await run(['unregister']); assert.equal(result.code,0);
  result=await run(['register','--expiresIn','1 hour',url,'fixture@example.invalid'],{prompt:true});
  assert.equal(result.code,0,result.stderr+result.stdout);
  assert.match(result.stdout,/Password:/);
  assert(!result.stdout.includes('fixture-password'));
  assert.equal(calls.find(c=>c.method==='token.create').params.expiresIn,'1 hour');
  const configFile=path.join(configRoot,'xo-cli/config.json');
  assert.equal(fs.statSync(configFile).mode & 0o777,0o600);
  assert.equal(JSON.parse(fs.readFileSync(configFile)).allowUnauthorized,false);
  result=await run(['list-commands','xo.getAllObjects']);
  assert.equal(result.code,0,result.stderr);
  assert.match(result.stdout,/xo\.getAllObjects/);assert(!result.stdout.includes('vm.start'));
  result=await run(['system.getServerVersion','--json']);
  assert.equal(result.code,0,result.stderr);assert.equal(JSON.parse(result.stdout),'5.193.1');
  result=await run(['list-objects','--id','--name_label','--power_state','type=VM']);
  assert.equal(result.code,0,result.stderr);
  assert.deepEqual(JSON.parse(result.stdout),[{id:'vm-fixture',name_label:'Disposable VM',power_state:'Halted'}]);
  assert.deepEqual(calls.at(-1),{method:'xo.getAllObjects',params:{filter:{type:'VM'}}});
  result=await run(['xo.getAllObjects','--json','filter=json:{"type":"VM"}','limit=json:1']);
  assert.equal(result.code,0,result.stderr);
  assert.deepEqual(calls.at(-1),{method:'xo.getAllObjects',params:{filter:{type:'VM'},limit:1}});
  assert.deepEqual(Object.keys(JSON.parse(result.stdout)),['vm-fixture']);
  const count=calls.length;
  result=await run(['xo.getAllObjects','--json','filter=json:{broken']);
  assert.notEqual(result.code,0);assert.equal(calls.length,count,'malformed JSON must fail before RPC');
  result=await run(['unregister']);assert.equal(result.code,0);
  assert.equal(calls.length,count,'unregister must not be mistaken for server revocation');
  const cleared=JSON.parse(fs.readFileSync(configFile));
  assert(!('token' in cleared));assert(!('server' in cleared));
  result=await run(['register','--token','fixture-token',url]);assert.equal(result.code,0);
  result=await run(['system.getServerVersion','--json']);assert.equal(result.code,0,'unregister leaves fixture token usable');
  revoked=true;
  result=await run(['system.getServerVersion','--json']);assert.notEqual(result.code,0);
  assert.match(result.stderr,/invalid credentials/);
  // TOML parser and configuration merge, without touching /root or /etc.
  const vendor=path.join(scratch,'vendor');fs.mkdirSync(vendor);
  fs.writeFileSync(path.join(vendor,'config.toml'),'[http.listen.0]\nport = 80\n');
  const operator=path.join(scratch,'operator');fs.mkdirSync(operator);
  fs.writeFileSync(path.join(operator,'config.toml'),
    '[http]\npublicUrl = "https://xoa.lab.example"\n[[http.listen]]\nport = 443\ncert = "/opt/xo/xoahl.crt"\nkey = "/opt/xo/xoahl.key"\n[redis]\nuri = "redis://127.0.0.1:6379/0"\n');
  const source=fs.readFileSync(path.join(operator,'config.toml'),'utf8');
  assert.equal(TOML.parse(source).http.publicUrl,'https://xoa.lab.example');
  assert.throws(()=>TOML.parse(source+'\n[http]\npublicUrl = "duplicate"\n'));
  // Whitelist vendor entries and point its appDir at each fixture in turn.
  const defaults=await appConf.load('xoa-reference-fixture',{appDir:vendor,entries:['vendor']});
  const merged=await appConf.load('xoa-reference-fixture',{appDir:operator,defaults,entries:['vendor']});
  assert.equal(merged.http.listen[0].port,443);
  assert.equal(merged.http.listen[0].key,'/opt/xo/xoahl.key');
  assert.equal(merged.redis.uri,'redis://127.0.0.1:6379/0');
  console.log('PASS: pinned CLI TLS trust and hostname/password prompt/expiry request/discovery/version/inventory/typed JSON/errors/local cleanup/revocation refusal; TOML syntax and app-conf merge');
})().catch(error=>{console.error(error);process.exitCode=1;}).finally(()=> {
  for(const socket of wss.clients) socket.terminate();
  wss.close();server.close();fs.rmSync(scratch,{recursive:true,force:true});
});
