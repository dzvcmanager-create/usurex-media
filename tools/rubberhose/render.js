// node render.js out_dir  -> one mp4 per scene, then concat
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const out=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/rex.html');await p.evaluate(()=>document.fonts.ready);
const scenes=await p.evaluate(()=>window.SCENES);let list='';
const only=process.argv[3];
for(let i=0;i<scenes.length;i++){if(only!==undefined&&+only!==i){list+=`file 's${i}.mp4'\n`;continue;}const [a,bb]=scenes[i];const n=Math.round((bb-a)*30);
 const tmp=`${out}/s${i}.tmp.mp4`,fin=`${out}/s${i}.mp4`;
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r','30','-f','mp4',tmp]);
 for(let f=0;f<n;f++){await p.evaluate(t=>render(t),a+f/30);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
 ff.stdin.end();const code=await new Promise(r=>ff.on('close',r));if(code!==0)throw new Error('ffmpeg '+i);
 fs.renameSync(tmp,fin);list+=`file 's${i}.mp4'\n`;console.log('scene',i,n,'frames');}
fs.writeFileSync(out+'/list.txt',list);await b.close();})();
