import pygame, random, math

def mealworm_tv_for_reptiles(grid_size=50, cell_size=15, worm_count=6, worm_length=8, fps=30):
    pygame.init()
    w = grid_size * cell_size
    h = grid_size * cell_size
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Mealworm TV")
    clock = pygame.time.Clock()
    base_bg = pygame.Surface((w, h))
    for y in range(h):
        for x in range(w):
            r = 160 + random.randint(-20,20)
            g = 140 + random.randint(-20,20)
            b = 100 + random.randint(-20,20)
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))
            base_bg.set_at((x,y), (r,g,b))
    for _ in range(400):
        rx, ry = random.randint(0,w-1), random.randint(0,h-1)
        rc, gc, bc = base_bg.get_at((rx, ry))[:3]
        base_bg.set_at((rx, ry), (max(0,rc-40), max(0,gc-35), max(0,bc-20)))
    worms = []
    for _ in range(worm_count):
        body = []
        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        while len(body) < worm_length:
            sx = random.randint(0, grid_size-1)
            sy = random.randint(0, grid_size-1)
            sz = 0
            body = [(sx,sy,sz)]
            for _ in range(1, worm_length):
                lx, ly, lz = body[-1]
                nx, ny = lx+dx, ly+dy
                if 0<=nx<grid_size and 0<=ny<grid_size:
                    body.append((nx, ny, lz))
                else:
                    break
        worms.append({
            "body": body,
            "dir": (dx, dy),
            "burrow": False,
            "burrow_timer": random.randint(80,160),
            "pause_timer": 0,
            "move_delay": random.randint(4,7),
            "move_delay_count": random.randint(0,6),
            "wiggle_chance": 0.1
        })
    raining = False
    rain_timer = 0
    drops = []
    def spawn_drop():
        return {
            "x": random.randint(0, w),
            "y": -10,
            "speed": random.uniform(4,7),
            "length": random.randint(5,15),
            "alpha": random.randint(180,255)
        }
    def move_worms():
        for worm in worms:
            worm["move_delay_count"] -= 1
            if worm["move_delay_count"]>0:
                continue
            worm["move_delay_count"] = worm["move_delay"]
            if worm["pause_timer"]>0:
                worm["pause_timer"]-=1
                continue
            worm["burrow_timer"]-=1
            if worm["burrow_timer"]<0:
                worm["burrow"]=not worm["burrow"]
                worm["burrow_timer"]=random.randint(80,160)
            hx,hy,hz = worm["body"][0]
            dx,dy = worm["dir"]
            if random.random()<worm["wiggle_chance"]:
                dx,dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                worm["dir"]=(dx,dy)
            if random.random()<0.02:
                worm["pause_timer"]=random.randint(5,15)
            nx,ny = hx+dx, hy+dy
            if not(0<=nx<grid_size and 0<=ny<grid_size):
                worm["dir"]=(-dx,-dy)
                nx,ny = hx-dx, hy-dy
            new_head=(nx,ny,1 if worm["burrow"] else 0)
            worm["body"].insert(0,new_head)
            while len(worm["body"])>worm_length:
                worm["body"].pop()
    def draw_worms():
        screen.blit(base_bg,(0,0))
        for worm in worms:
            for i in range(len(worm["body"])-1):
                ax,ay,az=worm["body"][i]
                bx,by,bz=worm["body"][i+1]
                ang=math.degrees(math.atan2(by-ay,bx-ax))
                rx=ax*cell_size
                ry=ay*cell_size
                rect=pygame.Rect(rx,ry,cell_size,int(cell_size*0.5))
                seg=pygame.Surface(rect.size, pygame.SRCALPHA)
                c=(110,80,50) if az==0 else (80,60,40)
                pygame.draw.ellipse(seg, c, (0,0,rect.width, rect.height))
                rot=pygame.transform.rotate(seg,ang)
                screen.blit(rot, rect.topleft)
    def update_rain():
        nonlocal raining, rain_timer
        if rain_timer<=0:
            if random.random()<0.002:
                raining=not raining
            rain_timer=60
        else:
            rain_timer-=1
        if raining:
            for _ in range(random.randint(2,5)):
                drops.append(spawn_drop())
        for d in drops:
            d["y"]+=d["speed"]
        i=0
        while i<len(drops):
            if drops[i]["y"]>h+50:
                drops.pop(i)
            else:
                i+=1
    def draw_rain():
        for d in drops:
            sx, sy, sp, ln, al = d["x"], d["y"], d["speed"], d["length"], d["alpha"]
            c=(150,150,255,al)
            dr=pygame.Surface((2,ln),pygame.SRCALPHA)
            pygame.draw.rect(dr,c,(0,0,2,ln))
            screen.blit(dr,(sx,sy))
    run=True
    while run:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
        move_worms()
        update_rain()
        draw_worms()
        draw_rain()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

if __name__=="__main__":
    mealworm_tv_for_reptiles(
        grid_size=50,
        cell_size=15,
        worm_count=6,
        worm_length=10,
        fps=30
    )
