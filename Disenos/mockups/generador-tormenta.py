import numpy as np, random
from PIL import Image, ImageFilter, ImageDraw
T='/tmp/claude-0/tees/video-draguz/assets/img/'; S='/mnt/project-files/sin-fondo/'
S2=2000
def noise(seed):
    rng=np.random.default_rng(seed); acc=np.zeros((S2,S2))
    for i,sz in enumerate([4,8,16,32,64,128,256]):
        n=rng.random((sz,sz)); im=Image.fromarray((n*255).astype(np.uint8)).resize((S2,S2),Image.BICUBIC)
        acc+=np.asarray(im)/255*(0.55**i)
    acc=(acc-acc.min())/(acc.max()-acc.min()); return acc
def mpd(p0,p1,disp,depth,rng):
    if depth==0: return [p0,p1]
    mx=(p0[0]+p1[0])/2; my=(p0[1]+p1[1])/2
    dx=p1[0]-p0[0]; dy=p1[1]-p0[1]; L=(dx*dx+dy*dy)**0.5+1e-6
    o=rng.normal(0,disp); mid=(mx-dy/L*o, my+dx/L*o)
    return mpd(p0,mid,disp/2,depth-1,rng)[:-1]+mpd(mid,p1,disp/2,depth-1,rng)
def draw_bolt(draw,p0,p1,w,rng,branch=True,lvl=0):
    L=((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)**0.5
    pts=mpd(p0,p1,L*0.18,8,rng)
    n=len(pts)
    for i in range(n-1):
        t=i/(n-1); ww=max(1,int(round(w*(1-0.75*t))))
        draw.line([pts[i],pts[i+1]],fill=255,width=ww)
    if branch and lvl<2:
        for _ in range(rng.integers(3,7)):
            i=rng.integers(int(n*0.1),int(n*0.8)); bx,by=pts[i]
            ang=np.arctan2(p1[1]-p0[1],p1[0]-p0[0])+rng.choice([-1,1])*rng.uniform(0.35,0.9)
            bl=L*rng.uniform(0.15,0.35)
            draw_bolt(draw,(bx,by),(bx+np.cos(ang)*bl,by+np.sin(ang)*bl),max(1,int(w*0.45*(1-i/n))),rng,branch=rng.random()<0.5,lvl=lvl+1)
def background(accent,seed):
    a=np.array(accent,float)
    c=noise(seed); c2=noise(seed+7)
    clouds=np.clip((c*0.7+c2*0.3-0.35)*1.9,0,1)**1.4
    yy,xx=np.mgrid[0:S2,0:S2]; vign=np.clip(1-np.sqrt((xx-1000)**2+(yy-900)**2)/1300,0,1)
    base=np.array([6,7,9],float)
    rgb=base+clouds[...,None]*(a*0.55+20)*(0.35+0.65*vign[...,None])
    glow=np.clip(1-np.sqrt((xx-1000)**2+(yy-950)**2)/900,0,1)**2
    rgb+=glow[...,None]*a*0.35
    rng=np.random.default_rng(seed)
    m=Image.new('L',(S2,S2),0); d=ImageDraw.Draw(m)
    for x0,x1 in [(rng.uniform(150,450),rng.uniform(80,420)),(rng.uniform(1550,1850),rng.uniform(1580,1920))]:
        draw_bolt(d,(x0,-10),(x1,rng.uniform(900,1300)),7,rng)
    if rng.random()<0.7:
        x0=rng.uniform(700,1300); draw_bolt(d,(x0,-10),(x0+rng.normal(0,150),rng.uniform(250,420)),4,rng)
    M=np.asarray(m).astype(float)/255
    wide=np.asarray(m.filter(ImageFilter.GaussianBlur(90))).astype(float)/255
    mid=np.asarray(m.filter(ImageFilter.GaussianBlur(14))).astype(float)/255
    tight=np.asarray(m.filter(ImageFilter.GaussianBlur(3))).astype(float)/255
    lit=np.clip(wide*9,0,1)
    rgb=rgb*(1+lit[...,None]*1.6)+lit[...,None]*(a*0.5+30)*clouds[...,None]*1.5   # flash lights up clouds
    col=np.clip(a*1.1+70,0,255)
    rgb=rgb+np.clip(mid*2.2,0,1)[...,None]*col*0.8+np.clip(tight*2.5,0,1)[...,None]*np.clip(col*0.4+170,0,255)
    core=np.clip(M,0,1)[...,None]
    rgb=rgb*(1-core)+core*np.array([250,255,252.])
    return Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).convert('RGBA')
def tee_img(kind,color):
    t=Image.open(T+f'tee-{kind}.png').convert('RGBA')
    sc=S2*0.80/t.width; t=t.resize((int(t.width*sc),int(t.height*sc)),Image.LANCZOS)
    A=np.asarray(t).astype(float); L=A[...,:3].mean(2); al=A[...,3]; Lm=np.median(L[al>200])
    if color is None: return t,np.clip(1+(L-Lm)/60,0.55,1.25)
    f=np.clip(1+(L-Lm)*3.0/232,0.65,1.1); c=np.array(color,float)
    return Image.fromarray(np.dstack([np.clip(c*f[...,None],0,255),al]).astype(np.uint8),'RGBA'),f
def mock(design,accent,out,kind='oversize',color=None,wfrac=0.50,hmax=0.60,py=0.17,seed=1):
    bg=background(accent,seed)
    sh=Image.new('L',(S2,S2),0); ImageDraw.Draw(sh).ellipse([520,1770,1480,1890],fill=170); sh=sh.filter(ImageFilter.GaussianBlur(40))
    bg=Image.composite(Image.new('RGBA',(S2,S2),(0,0,0,255)),bg,sh)
    tee,shade=tee_img(kind,color)
    d0=Image.open(S+design).convert('RGBA')
    dw=int(tee.width*wfrac); dh=int(d0.height*dw/d0.width)
    if dh>tee.height*hmax: dh=int(tee.height*hmax); dw=int(d0.width*dh/d0.height)
    dz=d0.resize((dw,dh),Image.LANCZOS); px=(tee.width-dw)//2; pyy=int(tee.height*py)
    da=np.asarray(dz).astype(float); s=shade[pyy:pyy+dh,px:px+dw]
    da[...,:3]=np.clip(da[...,:3]*np.clip(0.8+0.2*s,0.7,1.08)[...,None],0,255)
    t=tee.copy(); t.alpha_composite(Image.fromarray(da.astype(np.uint8),'RGBA').filter(ImageFilter.GaussianBlur(0.7)),(px,pyy))
    gcol=tuple(int(v) for v in np.clip(np.array(accent)*1.2+30,0,255))
    glow=Image.new('RGBA',t.size,gcol+(0,)); glow.putalpha(t.getchannel('A').filter(ImageFilter.GaussianBlur(30)).point(lambda v:int(v*0.5)))
    t=t.rotate(-4,resample=Image.BICUBIC,expand=True); glow=glow.rotate(-4,resample=Image.BICUBIC,expand=True)
    ox=(S2-t.width)//2; oy=(S2-t.height)//2+20
    bg.alpha_composite(glow,(ox,oy)); bg.alpha_composite(t,(ox,oy))
    logo=Image.open(T+'logo.png').convert('RGBA'); lw=320; l=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
    bg.alpha_composite(l,(S2-lw-70,S2-l.height-60))
    bg.convert('RGB').save(S+'mockups/'+out,quality=93)
    return bg
