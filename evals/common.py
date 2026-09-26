"""Read-only Claude evaluation helpers; no model calls on import."""
from pathlib import Path
import hashlib
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def files_digest(path):
    items={}
    for p in sorted(Path(path).rglob('*')):
        if '__pycache__' in p.parts or p.suffix=='.pyc': continue
        if p.is_symlink(): raise ValueError(f'Symlink in frozen input: {p}')
        if p.is_file(): items[p.relative_to(path).as_posix()]=sha(p.read_bytes())
    return items

def write(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    # Never silently reuse or overwrite an experiment artifact.
    with path.open('x') as f: json.dump(value,f,indent=2)

def parse_stream(stdout, returncode):
    invalid=[]; calls=[]; tool_errors=[]; terminal=None; models=set()
    for line in stdout.splitlines():
        if not line.strip(): continue
        try: event=json.loads(line)
        except ValueError: invalid.append(line); continue
        if not isinstance(event,dict):invalid.append(line);continue
        if event.get('type') in ['assistant','user']:
            message=event.get('message',{})
            if not isinstance(message,dict):invalid.append(line);continue
            model=message.get('model')
            if isinstance(model,str):models.add(model)
            content=message.get('content',[])
            if isinstance(content,str):content=[]
            if not isinstance(content,list):invalid.append(line);continue
            for c in content:
                if not isinstance(c,dict):invalid.append(line);continue
                if c.get('type')=='tool_use':calls.append(c)
                if c.get('type')=='tool_result' and c.get('is_error'):tool_errors.append(c)
        if event.get('type')=='result':terminal=event
    denied=(terminal or {}).get('permission_denials',[])
    answer=(terminal or {}).get('result','')
    if not isinstance(answer,str):invalid.append('Non-text result');answer=''
    valid=returncode==0 and terminal is not None and not terminal.get('is_error') and bool(answer.strip()) and not tool_errors and not denied and not invalid
    return {'valid':valid,'result':answer,
            'calls':calls,'tool_errors':tool_errors,'permission_denials':denied,
            'observed_models':sorted(models),'cost_usd':(terminal or {}).get('total_cost_usd'),
            'terminal':terminal,'unparsed_lines':invalid}

def invoke(prompt, model, cwd, plugin=None, tools='Read,Glob,Grep,Skill,Agent', timeout=900):
    cmd=['claude','--restricted','--setting-sources','','--strict-mcp-config',
         '--mcp-config','{"mcpServers":{}}','--model',model,'--tools',tools,
         '--output-format','stream-json','--verbose','-p',prompt]
    if tools:cmd+=['--allowedTools',tools]
    if plugin:cmd+=['--plugin-dir',str(plugin),'--add-dir',str(plugin)]
    started=time.monotonic()
    try:
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=timeout)
        stdout,stderr,code=p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:
        stdout=e.stdout or '';stderr=e.stderr or ''
        if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
        if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
        code=124
    except OSError as e:
        stdout='';stderr=str(e);code=127
    result=parse_stream(stdout,code)
    result.update(stdout=stdout,stderr=stderr,returncode=code,seconds=time.monotonic()-started,command=cmd)
    return result

def verify_frozen(experiment):
    experiment=Path(experiment)
    m=json.loads((experiment/'manifest.json').read_text())
    for name,expected in m['frozen'].items():
        p=experiment/name
        actual=files_digest(p) if p.is_dir() else sha(p.read_bytes())
        if actual!=expected: raise ValueError(f'Experiment input drift: {name}')
    return m

def combine_orders(judgments):
    if len(judgments)!=2 or {j['order'] for j in judgments}!={'AB','BA'}:
        return 'incomplete'
    choices={j['preference'] for j in judgments}
    return choices.pop() if len(choices)==1 else 'order_sensitive'
