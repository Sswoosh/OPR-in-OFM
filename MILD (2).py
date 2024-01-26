from knitro import *
import numpy as np
import random 
import math
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance as wd
import pandas as pd
time=5000
repeat=30
buyers,goods  = 20, 30
Ek=np.zeros(buyers,dtype=float)
avg_Ek=np.zeros(buyers,dtype=float)
Q=np.zeros(time,dtype=float)
sum_ind=0
initial_val=np.zeros((buyers,goods),dtype=float)
avg_val=np.zeros((buyers,goods),dtype=float)
log_val=np.zeros((buyers,goods),dtype=float)
avg_qua=np.zeros((buyers,goods),dtype=float)
value=np.zeros((time,buyers,goods),dtype=float)  #v
value_exp=np.zeros((time,buyers,goods),dtype=float)
random_error=np.zeros((time,buyers,goods),dtype=float)
quantity=np.zeros((time,buyers,goods),dtype=float)  #x
quantity_exp=np.zeros((time,buyers,goods),dtype=float)
quantity_opt=np.zeros((buyers,goods),dtype=float)  #x*
price=np.zeros((time+1,goods),dtype=float)  #p
price_exp=np.zeros((time+1,goods),dtype=float)
price_opt=np.zeros(goods,dtype=float)  #p*
P=np.zeros((time,buyers,goods),dtype=float)
budget=np.zeros((time+1,buyers),dtype=float)  #B
budget_opt=np.zeros(buyers,dtype=float)
bidprice=np.zeros((time+1,buyers,goods),dtype=float)  #b
bidprice_exp=np.zeros((time+1,buyers,goods),dtype=float)
bidprice_opt=np.zeros((buyers,goods),dtype=float)  #b*
sumvx=np.zeros((time,buyers),dtype=float)
sumvx_exp=np.zeros((time,buyers),dtype=float)
sumvx_opt=np.zeros((time,buyers),dtype=float)
u=np.zeros((time,buyers),dtype=float)
U=np.zeros(buyers,dtype=float)
Dh=np.zeros(time,dtype=float)
v_sum=np.zeros(buyers*goods,dtype=float)
Unsw=0
social_regret=0
OPTnsw=0
g=0
price_norm=np.zeros(time,dtype=float)
price_norm_exp=np.zeros(time,dtype=float)
U_opt=np.zeros(buyers,dtype=float)
u_opt=np.zeros((time,buyers),dtype=float)
individual_regret=np.zeros(buyers,dtype=float)
envy=np.zeros(buyers,dtype=float)
E_opt=np.zeros((buyers,time),dtype=float)
E=np.zeros((buyers,time),dtype=float)
sumE=np.zeros(buyers,dtype=float)
sumE_opt=np.zeros(buyers,dtype=float)
avgind=np.zeros((repeat,11),dtype=float)
avgsoc=np.zeros((repeat,11),dtype=float)
avgenv=np.zeros((repeat,10),dtype=float)
indavgT=np.zeros(time,dtype=float)
socavgT=np.zeros(time,dtype=float)
envyT=np.zeros(10,dtype=float)
noise=np.zeros((time,buyers,goods),dtype=float)
avg_noise=0
sum_noise=np.zeros(time,dtype=float)
data=np.zeros((repeat,time),dtype=float)
for i in range(buyers):
    budget[0][i]=time/buyers
valuesum=np.zeros(buyers)
valuesumT=0
for i in range(buyers):
    for j in range(goods):
        initial_val[i][j]=np.random.uniform(5, 10)
for k in range(repeat):
    for i in range(buyers):
       for j in range(goods):
            value[0][i][j]=initial_val[i][j]
            valuesum[i]=value[0][i][j]+valuesum[i]
    for i in range (buyers):
        for j in range(goods):       
            value[0][i][j]=value[0][i][j]/valuesum[i]
    for i in range (buyers):
        for j in range(goods):
            bidprice[0][i][j]=budget[0][i]/(time*goods)
            price[0][j]=price[0][j]+bidprice[0][i][j]
    for i in range (buyers):
        for j in range(goods):       
            quantity[0][i][j]=bidprice[0][i][j]/price[0][j]
            valuesum[i]=0
            
    distribution=np.random.normal(0,(0.01),1000)
    for t in range(1,time):
        M=np.random.uniform(-0.01,0.01)
        N=np.random.uniform(0,0.01)
        noise=np.random.normal(M,N,1000)
        distance=wd(distribution,noise)
        for i in range(buyers):
            for j in range(goods):
                random_error[t][i][j]=np.random.choice(noise,1)

    
    for t in range(1,time):
        for i in range (buyers):
            for j in range(goods):
                    value[t][i][j]=math.exp(math.log((value[0][i][j]))+random_error[t][i][j])
                    value_exp[t][i][j]=math.exp(math.log((value[0][i][j]))+np.random.normal(0,0))
        for i in range (buyers):
            for j in range(goods): 
                    sumvx[t][i]=sumvx[t][i]+(value[t][i][j]*quantity[t-1][i][j])
                    sumvx_exp[t][i]=sumvx_exp[t][i]+(value_exp[t][i][j]*quantity_exp[t-1][i][j])
                    valuesum[i]=value[t][i][j]+valuesum[i]
        for i in range (buyers):
            for j in range(goods): 
                    bidprice[t][i][j]=(value[t][i][j]*quantity[t-1][i][j])/(sumvx[t][i]*buyers)
                    bidprice_exp[t][i][j]=(value_exp[t][i][j]*quantity_exp[t-1][i][j])/(sumvx_exp[t][i]*buyers)
                    value[t][i][j]=value[t][i][j]/valuesum[i]
        for j in range (goods):
                for i in range (buyers):
                    price[t][j]=price[t][j]+bidprice[t][i][j]
                    price_exp[t][j]=price_exp[t][j]+bidprice_exp[t][i][j]
        for i in range (buyers):
            for j in range(goods):
                    budget[t][i]=budget[t][i]+bidprice[t][i][j]
        for i in range (buyers):
            for j in range(goods): 
                    quantity[t][i][j]=bidprice[t][i][j]/price[t][j] 
                    quantity_exp[t][i][j]=bidprice_exp[t][i][j]/price_exp[t][j]
                    valuesum[i]=0


    #    print(a,1/t)
    #for t in range (time): 
    #    print('%f'%value[t][0][0],'%f'%value[t][0][1],'%f'%value[t][0][2],'%f'%value[t][0][3],'%f'%value[t][0][4])        
        #print(quantity[t][0][0],'%f'%quantity[t][0][1],'%f'%quantity[t][0][2],'%f'%quantity[t][0][3])
        #print('%f'%bidprice[t][0][0],'%f'%bidprice[t][0][1],'%f'%bidprice[t][0][2],'%f'%bidprice[t][0][3],'%f'%bidprice[t][0][4],'%f'%bidprice[t][0][5],'%f'%bidprice[t][0][6],'%f'%bidprice[t][0][7],'%f'%bidprice[t][0][8],'%f'%bidprice[t][0][9])
        #print('%f'%price[t][0],'%f'%price[t][1],'%f'%price[t][2],'%f'%price[t][3],'%f'%price[t][4],'%f'%price[t][5],'%f'%price[t][6],'%f'%price[t][7],'%f'%price[t][8],'%f'%price[t][9])
        #print('%f'%price_exp[t][0],'%f'%price_exp[t][1],'%f'%price_exp[t][2],'%f'%price_exp[t][3],'%f'%price_exp[t][4],'%f'%price_exp[t][5],'%f'%price_exp[t][6],'%f'%price_exp[t][7],'%f'%price_exp[t][8],'%f'%price_exp[t][9])
    
    z=0
    for i in range (buyers):
        for j in range(goods): 
            for t in range (time):
                v_sum[z]=v_sum[z]+math.log(value[t][i][j].copy())
            z+=1
    for i in range (z):
        v_sum[i]=(v_sum[i]/time)    
    z=0
    for i in range(buyers):
            for j in range (goods):
                log_val[i][j]=v_sum[z]
                z+=1
    for t in range (time):
        for i in range(buyers):
            for j in range (goods):
                avg_val[i][j]=avg_val[i][j]+value[t][i][j]
    for i in range(buyers):
        for j in range (goods):
            avg_val[i][j]=(avg_val[i][j]/time)

    def callbackEvalF (kc, cb, evalRequest, evalResult, userParams):
        if evalRequest.type != KN_RC_EVALFC:
            #print ("*** callbackEvalF incorrectly called with eval type %d" % evalRequest.type)
            return -1
        x = evalRequest.x

        # Evaluate nonlinear objective
        dTmp1 =x[0]+x[30]+x[60]+x[90]+x[120]+x[150]+x[180]+x[210]+x[ 240 ]+x[ 270 ]+x[ 300 ]+x[ 330 ]+x[ 360 ]+x[ 390 ]+x[ 420 ]+x[ 450 ]+x[ 480 ]+x[ 510 ]+x[ 540 ]+x[ 570 ]
        dTmp2 =x[1]+x[31]+x[61]+x[91]+x[121]+x[151]+x[181]+x[211]+x[ 241 ]+x[ 271 ]+x[ 301 ]+x[ 331 ]+x[ 361 ]+x[ 391 ]+x[ 421 ]+x[ 451 ]+x[ 481 ]+x[ 511 ]+x[ 541 ]+x[ 571 ]
        dTmp3 =x[2]+x[32]+x[62]+x[92]+x[122]+x[152]+x[182]+x[212]+x[ 242 ]+x[ 272 ]+x[ 302 ]+x[ 332 ]+x[ 362 ]+x[ 392 ]+x[ 422 ]+x[ 452 ]+x[ 482 ]+x[ 512 ]+x[ 542 ]+x[ 572 ]
        dTmp4 =x[3]+x[33]+x[63]+x[93]+x[123]+x[153]+x[183]+x[213]+x[ 243 ]+x[ 273 ]+x[ 303 ]+x[ 333 ]+x[ 363 ]+x[ 393 ]+x[ 423 ]+x[ 453 ]+x[ 483 ]+x[ 513 ]+x[ 543 ]+x[ 573 ]
        dTmp5 =x[4]+x[34]+x[64]+x[94]+x[124]+x[154]+x[184]+x[214]+x[ 244 ]+x[ 274 ]+x[ 304 ]+x[ 334 ]+x[ 364 ]+x[ 394 ]+x[ 424 ]+x[ 454 ]+x[ 484 ]+x[ 514 ]+x[ 544 ]+x[ 574 ]
        dTmp6 =x[5]+x[35]+x[65]+x[95]+x[125]+x[155]+x[185]+x[215]+x[ 245 ]+x[ 275 ]+x[ 305 ]+x[ 335 ]+x[ 365 ]+x[ 395 ]+x[ 425 ]+x[ 455 ]+x[ 485 ]+x[ 515 ]+x[ 545 ]+x[ 575 ]
        dTmp7 =x[6]+x[36]+x[66]+x[96]+x[126]+x[156]+x[186]+x[216]+x[ 246 ]+x[ 276 ]+x[ 306 ]+x[ 336 ]+x[ 366 ]+x[ 396 ]+x[ 426 ]+x[ 456 ]+x[ 486 ]+x[ 516 ]+x[ 546 ]+x[ 576 ]
        dTmp8 =x[7]+x[37]+x[67]+x[97]+x[127]+x[157]+x[187]+x[217]+x[ 247 ]+x[ 277 ]+x[ 307 ]+x[ 337 ]+x[ 367 ]+x[ 397 ]+x[ 427 ]+x[ 457 ]+x[ 487 ]+x[ 517 ]+x[ 547 ]+x[ 577 ]
        dTmp9 =x[8]+x[38]+x[68]+x[98]+x[128]+x[158]+x[188]+x[218]+x[ 248 ]+x[ 278 ]+x[ 308 ]+x[ 338 ]+x[ 368 ]+x[ 398 ]+x[ 428 ]+x[ 458 ]+x[ 488 ]+x[ 518 ]+x[ 548 ]+x[ 578 ]
        dTmp10 =x[9]+x[39]+x[69]+x[99]+x[129]+x[159]+x[189]+x[219]+x[ 249 ]+x[ 279 ]+x[ 309 ]+x[ 339 ]+x[ 369 ]+x[ 399 ]+x[ 429 ]+x[ 459 ]+x[ 489 ]+x[ 519 ]+x[ 549 ]+x[ 579 ]
        dTmp11 =x[10]+x[40]+x[70]+x[100]+x[130]+x[160]+x[190]+x[220]+x[ 250 ]+x[ 280 ]+x[ 310 ]+x[ 340 ]+x[ 370 ]+x[ 400 ]+x[ 430 ]+x[ 460 ]+x[ 490 ]+x[ 520 ]+x[ 550 ]+x[ 580 ]
        dTmp12 =x[11]+x[41]+x[71]+x[101]+x[131]+x[161]+x[191]+x[221]+x[ 251 ]+x[ 281 ]+x[ 311 ]+x[ 341 ]+x[ 371 ]+x[ 401 ]+x[ 431 ]+x[ 461 ]+x[ 491 ]+x[ 521 ]+x[ 551 ]+x[ 581 ]
        dTmp13 =x[12]+x[42]+x[72]+x[102]+x[132]+x[162]+x[192]+x[222]+x[ 252 ]+x[ 282 ]+x[ 312 ]+x[ 342 ]+x[ 372 ]+x[ 402 ]+x[ 432 ]+x[ 462 ]+x[ 492 ]+x[ 522 ]+x[ 552 ]+x[ 582 ]
        dTmp14 =x[13]+x[43]+x[73]+x[103]+x[133]+x[163]+x[193]+x[223]+x[ 253 ]+x[ 283 ]+x[ 313 ]+x[ 343 ]+x[ 373 ]+x[ 403 ]+x[ 433 ]+x[ 463 ]+x[ 493 ]+x[ 523 ]+x[ 553 ]+x[ 583 ]
        dTmp15 =x[14]+x[44]+x[74]+x[104]+x[134]+x[164]+x[194]+x[224]+x[ 254 ]+x[ 284 ]+x[ 314 ]+x[ 344 ]+x[ 374 ]+x[ 404 ]+x[ 434 ]+x[ 464 ]+x[ 494 ]+x[ 524 ]+x[ 554 ]+x[ 584 ]
        dTmp16 =x[15]+x[45]+x[75]+x[105]+x[135]+x[165]+x[195]+x[225]+x[ 255 ]+x[ 285 ]+x[ 315 ]+x[ 345 ]+x[ 375 ]+x[ 405 ]+x[ 435 ]+x[ 465 ]+x[ 495 ]+x[ 525 ]+x[ 555 ]+x[ 585 ]
        dTmp17 =x[16]+x[46]+x[76]+x[106]+x[136]+x[166]+x[196]+x[226]+x[ 256 ]+x[ 286 ]+x[ 316 ]+x[ 346 ]+x[ 376 ]+x[ 406 ]+x[ 436 ]+x[ 466 ]+x[ 496 ]+x[ 526 ]+x[ 556 ]+x[ 586 ]
        dTmp18 =x[17]+x[47]+x[77]+x[107]+x[137]+x[167]+x[197]+x[227]+x[ 257 ]+x[ 287 ]+x[ 317 ]+x[ 347 ]+x[ 377 ]+x[ 407 ]+x[ 437 ]+x[ 467 ]+x[ 497 ]+x[ 527 ]+x[ 557 ]+x[ 587 ]
        dTmp19 =x[18]+x[48]+x[78]+x[108]+x[138]+x[168]+x[198]+x[228]+x[ 258 ]+x[ 288 ]+x[ 318 ]+x[ 348 ]+x[ 378 ]+x[ 408 ]+x[ 438 ]+x[ 468 ]+x[ 498 ]+x[ 528 ]+x[ 558 ]+x[ 588 ]
        dTmp20 =x[19]+x[49]+x[79]+x[109]+x[139]+x[169]+x[199]+x[229]+x[ 259 ]+x[ 289 ]+x[ 319 ]+x[ 349 ]+x[ 379 ]+x[ 409 ]+x[ 439 ]+x[ 469 ]+x[ 499 ]+x[ 529 ]+x[ 559 ]+x[ 589 ]
        dTmp21 =x[20]+x[50]+x[80]+x[110]+x[140]+x[170]+x[200]+x[230]+x[ 260 ]+x[ 290 ]+x[ 320 ]+x[ 350 ]+x[ 380 ]+x[ 410 ]+x[ 440 ]+x[ 470 ]+x[ 500 ]+x[ 530 ]+x[ 560 ]+x[ 590 ]
        dTmp22 =x[21]+x[51]+x[81]+x[111]+x[141]+x[171]+x[201]+x[231]+x[ 261 ]+x[ 291 ]+x[ 321 ]+x[ 351 ]+x[ 381 ]+x[ 411 ]+x[ 441 ]+x[ 471 ]+x[ 501 ]+x[ 531 ]+x[ 561 ]+x[ 591 ]
        dTmp23 =x[22]+x[52]+x[82]+x[112]+x[142]+x[172]+x[202]+x[232]+x[ 262 ]+x[ 292 ]+x[ 322 ]+x[ 352 ]+x[ 382 ]+x[ 412 ]+x[ 442 ]+x[ 472 ]+x[ 502 ]+x[ 532 ]+x[ 562 ]+x[ 592 ]
        dTmp24 =x[23]+x[53]+x[83]+x[113]+x[143]+x[173]+x[203]+x[233]+x[ 263 ]+x[ 293 ]+x[ 323 ]+x[ 353 ]+x[ 383 ]+x[ 413 ]+x[ 443 ]+x[ 473 ]+x[ 503 ]+x[ 533 ]+x[ 563 ]+x[ 593 ]
        dTmp25 =x[24]+x[54]+x[84]+x[114]+x[144]+x[174]+x[204]+x[234]+x[ 264 ]+x[ 294 ]+x[ 324 ]+x[ 354 ]+x[ 384 ]+x[ 414 ]+x[ 444 ]+x[ 474 ]+x[ 504 ]+x[ 534 ]+x[ 564 ]+x[ 594 ]
        dTmp26 =x[25]+x[55]+x[85]+x[115]+x[145]+x[175]+x[205]+x[235]+x[ 265 ]+x[ 295 ]+x[ 325 ]+x[ 355 ]+x[ 385 ]+x[ 415 ]+x[ 445 ]+x[ 475 ]+x[ 505 ]+x[ 535 ]+x[ 565 ]+x[ 595 ]
        dTmp27 =x[26]+x[56]+x[86]+x[116]+x[146]+x[176]+x[206]+x[236]+x[ 266 ]+x[ 296 ]+x[ 326 ]+x[ 356 ]+x[ 386 ]+x[ 416 ]+x[ 446 ]+x[ 476 ]+x[ 506 ]+x[ 536 ]+x[ 566 ]+x[ 596 ]
        dTmp28 =x[27]+x[57]+x[87]+x[117]+x[147]+x[177]+x[207]+x[237]+x[ 267 ]+x[ 297 ]+x[ 327 ]+x[ 357 ]+x[ 387 ]+x[ 417 ]+x[ 447 ]+x[ 477 ]+x[ 507 ]+x[ 537 ]+x[ 567 ]+x[ 597 ]
        dTmp29 =x[28]+x[58]+x[88]+x[118]+x[148]+x[178]+x[208]+x[238]+x[ 268 ]+x[ 298 ]+x[ 328 ]+x[ 358 ]+x[ 388 ]+x[ 418 ]+x[ 448 ]+x[ 478 ]+x[ 508 ]+x[ 538 ]+x[ 568 ]+x[ 598 ]
        dTmp30 =x[29]+x[59]+x[89]+x[119]+x[149]+x[179]+x[209]+x[239]+x[ 269 ]+x[ 299 ]+x[ 329 ]+x[ 359 ]+x[ 389 ]+x[ 419 ]+x[ 449 ]+x[ 479 ]+x[ 509 ]+x[ 539 ]+x[ 569 ]+x[ 599 ]
        evalResult.obj = (-dTmp1*math.log(dTmp1)-dTmp2*math.log(dTmp2)-dTmp3*math.log(dTmp3)-dTmp4*math.log(dTmp4)-dTmp5*math.log(dTmp5)-dTmp6*math.log(dTmp6)-dTmp7*math.log(dTmp7)-dTmp8*math.log(dTmp8)-dTmp9*math.log(dTmp9)-dTmp10*math.log(dTmp10)-dTmp11*math.log(dTmp11)-dTmp12*math.log(dTmp12)-dTmp13*math.log(dTmp13)-dTmp14*math.log(dTmp14)-dTmp15*math.log(dTmp15)-dTmp16*math.log(dTmp16)-dTmp17*math.log(dTmp17)-dTmp18*math.log(dTmp18)-dTmp19*math.log(dTmp19)-dTmp20*math.log(dTmp20)-dTmp21*math.log(dTmp21)-dTmp22*math.log(dTmp22)-dTmp23*math.log(dTmp23)-dTmp24*math.log(dTmp24)-dTmp25*math.log(dTmp25)-dTmp26*math.log(dTmp26)-dTmp27*math.log(dTmp27)-dTmp28*math.log(dTmp28)-dTmp29*math.log(dTmp29)-dTmp30*math.log(dTmp30))


        return 0




    try:
        kc = KN_new ()
    except:
        print ("Failed to find a valid license.")
        quit ()


    KN_load_param_file (kc, "C:\Program Files\Artelys\Knitro 13.1.0\examples\Python\examples\knitro.opt")

    n = 600
    KN_add_vars (kc, n)
    KN_set_var_lobnds (kc, xLoBnds = [0]*n) # not necessary since infinite
    KN_set_var_upbnds (kc, xUpBnds = [0.1]*n)
    # Define an initial point.  If not set, Knitro will generate one.


    # Add the constraints and set their lower bounds
    m = 20
    KN_add_cons(kc, m)
    KN_set_con_lobnds (kc, cLoBnds = [0.05, 0.05, 0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05, 0.05, 0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05])
    KN_set_con_upbnds (kc, cUpBnds = [0.05, 0.05, 0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05, 0.05, 0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05])

    # Add the linear structure in the objective function.
    objGradIndexVars = [0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 ,27 ,28 ,29 ,30 ,31 ,32 ,33 ,34 ,35 ,36 ,37 ,38 ,39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,48 ,49 ,50 ,51 ,52 ,53 ,54 ,55 ,56 ,57 ,58 ,59 ,60 ,61 ,62 ,63 ,64 ,65 ,66 ,67 ,68 ,69 ,70 ,71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,79 ,80 ,81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89 ,90 ,91 ,92 ,93 ,94 ,95 ,96 ,97 ,98 ,99 ,100 ,101 ,102 ,103 ,104 ,105 ,106 ,107 ,108 ,109 ,110 ,111 ,112 ,113 ,114 ,115 ,116 ,117 ,118 ,119 ,120 ,121 ,122 ,123 ,124 ,125 ,126 ,127 ,128 ,129 ,130 ,131 ,132 ,133 ,134 ,135 ,136 ,137 ,138 ,139 ,140 ,141 ,142 ,143 ,144 ,145 ,146 ,147 ,148 ,149 ,150 ,151 ,152 ,153 ,154 ,155 ,156 ,157 ,158 ,159 ,160 ,161 ,162 ,163 ,164 ,165 ,166 ,167 ,168 ,169 ,170 ,171 ,172 ,173 ,174 ,175 ,176 ,177 ,178 ,179 ,180 ,181 ,182 ,183 ,184 ,185 ,186 ,187 ,188 ,189 ,190 ,191 ,192 ,193 ,194 ,195 ,196 ,197 ,198 ,199 ,200 ,201 ,202 ,203 ,204 ,205 ,206 ,207 ,208 ,209 ,210 ,211 ,212 ,213 ,214 ,215 ,216 ,217 ,218 ,219 ,220 ,221 ,222 ,223 ,224 ,225 ,226 ,227 ,228 ,229 ,230 ,231 ,232 ,233 ,234 ,235 ,236 ,237 ,238 ,239 ,240 ,241 ,242 ,243 ,244 ,245 ,246 ,247 ,248 ,249 ,250 ,251 ,252 ,253 ,254 ,255 ,256 ,257 ,258 ,259 ,260 ,261 ,262 ,263 ,264 ,265 ,266 ,267 ,268 ,269 ,270 ,271 ,272 ,273 ,274 ,275 ,276 ,277 ,278 ,279 ,280 ,281 ,282 ,283 ,284 ,285 ,286 ,287 ,288 ,289 ,290 ,291 ,292 ,293 ,294 ,295 ,296 ,297 ,298 ,299 ,300 ,301 ,302 ,303 ,304 ,305 ,306 ,307 ,308 ,309 ,310 ,311 ,312 ,313 ,314 ,315 ,316 ,317 ,318 ,319 ,320 ,321 ,322 ,323 ,324 ,325 ,326 ,327 ,328 ,329 ,330 ,331 ,332 ,333 ,334 ,335 ,336 ,337 ,338 ,339 ,340 ,341 ,342 ,343 ,344 ,345 ,346 ,347 ,348 ,349 ,350 ,351 ,352 ,353 ,354 ,355 ,356 ,357 ,358 ,359 ,360 ,361 ,362 ,363 ,364 ,365 ,366 ,367 ,368 ,369 ,370 ,371 ,372 ,373 ,374 ,375 ,376 ,377 ,378 ,379 ,380 ,381 ,382 ,383 ,384 ,385 ,386 ,387 ,388 ,389 ,390 ,391 ,392 ,393 ,394 ,395 ,396 ,397 ,398 ,399 ,400 ,401 ,402 ,403 ,404 ,405 ,406 ,407 ,408 ,409 ,410 ,411 ,412 ,413 ,414 ,415 ,416 ,417 ,418 ,419 ,420 ,421 ,422 ,423 ,424 ,425 ,426 ,427 ,428 ,429 ,430 ,431 ,432 ,433 ,434 ,435 ,436 ,437 ,438 ,439 ,440 ,441 ,442 ,443 ,444 ,445 ,446 ,447 ,448 ,449 ,450 ,451 ,452 ,453 ,454 ,455 ,456 ,457 ,458 ,459 ,460 ,461 ,462 ,463 ,464 ,465 ,466 ,467 ,468 ,469 ,470 ,471 ,472 ,473 ,474 ,475 ,476 ,477 ,478 ,479 ,480 ,481 ,482 ,483 ,484 ,485 ,486 ,487 ,488 ,489 ,490 ,491 ,492 ,493 ,494 ,495 ,496 ,497 ,498 ,499 ,500 ,501 ,502 ,503 ,504 ,505 ,506 ,507 ,508 ,509 ,510 ,511 ,512 ,513 ,514 ,515 ,516 ,517 ,518 ,519 ,520 ,521 ,522 ,523 ,524 ,525 ,526 ,527 ,528 ,529 ,530 ,531 ,532 ,533 ,534 ,535 ,536 ,537 ,538 ,539 ,540 ,541 ,542 ,543 ,544 ,545 ,546 ,547 ,548 ,549 ,550 ,551 ,552 ,553 ,554 ,555 ,556 ,557 ,558 ,559 ,560 ,561 ,562 ,563 ,564 ,565 ,566 ,567 ,568 ,569 ,570 ,571 ,572 ,573 ,574 ,575 ,576 ,577 ,578 ,579 ,580 ,581 ,582 ,583 ,584 ,585 ,586 ,587 ,588 ,589 ,590 ,591 ,592 ,593,594,595,596,597,598,599]
    objGradCoefs = [v_sum[  0  ],v_sum[  1  ],v_sum[  2  ],v_sum[  3  ],v_sum[  4  ],v_sum[  5  ],v_sum[  6  ],v_sum[  7  ],v_sum[  8  ],v_sum[  9  ],v_sum[  10  ],v_sum[  11  ],v_sum[  12  ],v_sum[  13  ],v_sum[  14  ],v_sum[  15  ],v_sum[  16  ],v_sum[  17  ],v_sum[  18  ],v_sum[  19  ],v_sum[  20  ],v_sum[  21  ],v_sum[  22  ],v_sum[  23  ],v_sum[  24  ],v_sum[  25  ],v_sum[  26  ],v_sum[  27  ],v_sum[  28  ],v_sum[  29  ],v_sum[  30  ],v_sum[  31  ],v_sum[  32  ],v_sum[  33  ],v_sum[  34  ],v_sum[  35  ],v_sum[  36  ],v_sum[  37  ],v_sum[  38  ],v_sum[  39  ],v_sum[  40  ],v_sum[  41  ],v_sum[  42  ],v_sum[  43  ],v_sum[  44  ],v_sum[  45  ],v_sum[  46  ],v_sum[  47  ],v_sum[  48  ],v_sum[  49  ],v_sum[  50  ],v_sum[  51  ],v_sum[  52  ],v_sum[  53  ],v_sum[  54  ],v_sum[  55  ],v_sum[  56  ],v_sum[  57  ],v_sum[  58  ],v_sum[  59  ],v_sum[  60  ],v_sum[  61  ],v_sum[  62  ],v_sum[  63  ],v_sum[  64  ],v_sum[  65  ],v_sum[  66  ],v_sum[  67  ],v_sum[  68  ],v_sum[  69  ],v_sum[  70  ],v_sum[  71  ],v_sum[  72  ],v_sum[  73  ],v_sum[  74  ],v_sum[  75  ],v_sum[  76  ],v_sum[  77  ],v_sum[  78  ],v_sum[  79  ],v_sum[  80  ],v_sum[  81  ],v_sum[  82  ],v_sum[  83  ],v_sum[  84  ],v_sum[  85  ],v_sum[  86  ],v_sum[  87  ],v_sum[  88  ],v_sum[  89  ],v_sum[  90  ],v_sum[  91  ],v_sum[  92  ],v_sum[  93  ],v_sum[  94  ],v_sum[  95  ],v_sum[  96  ],v_sum[  97  ],v_sum[  98  ],v_sum[  99  ],v_sum[  100  ],v_sum[  101  ],v_sum[  102  ],v_sum[  103  ],v_sum[  104  ],v_sum[  105  ],v_sum[  106  ],v_sum[  107  ],v_sum[  108  ],v_sum[  109  ],v_sum[  110  ],v_sum[  111  ],v_sum[  112  ],v_sum[  113  ],v_sum[  114  ],v_sum[  115  ],v_sum[  116  ],v_sum[  117  ],v_sum[  118  ],v_sum[  119  ],v_sum[  120  ],v_sum[  121  ],v_sum[  122  ],v_sum[  123  ],v_sum[  124  ],v_sum[  125  ],v_sum[  126  ],v_sum[  127  ],v_sum[  128  ],v_sum[  129  ],v_sum[  130  ],v_sum[  131  ],v_sum[  132  ],v_sum[  133  ],v_sum[  134  ],v_sum[  135  ],v_sum[  136  ],v_sum[  137  ],v_sum[  138  ],v_sum[  139  ],v_sum[  140  ],v_sum[  141  ],v_sum[  142  ],v_sum[  143  ],v_sum[  144  ],v_sum[  145  ],v_sum[  146  ],v_sum[  147  ],v_sum[  148  ],v_sum[  149  ],v_sum[  150  ],v_sum[  151  ],v_sum[  152  ],v_sum[  153  ],v_sum[  154  ],v_sum[  155  ],v_sum[  156  ],v_sum[  157  ],v_sum[  158  ],v_sum[  159  ],v_sum[  160  ],v_sum[  161  ],v_sum[  162  ],v_sum[  163  ],v_sum[  164  ],v_sum[  165  ],v_sum[  166  ],v_sum[  167  ],v_sum[  168  ],v_sum[  169  ],v_sum[  170  ],v_sum[  171  ],v_sum[  172  ],v_sum[  173  ],v_sum[  174  ],v_sum[  175  ],v_sum[  176  ],v_sum[  177  ],v_sum[  178  ],v_sum[  179  ],v_sum[  180  ],v_sum[  181  ],v_sum[  182  ],v_sum[  183  ],v_sum[  184  ],v_sum[  185  ],v_sum[  186  ],v_sum[  187  ],v_sum[  188  ],v_sum[  189  ],v_sum[  190  ],v_sum[  191  ],v_sum[  192  ],v_sum[  193  ],v_sum[  194  ],v_sum[  195  ],v_sum[  196  ],v_sum[  197  ],v_sum[  198  ],v_sum[  199  ],v_sum[  200  ],v_sum[  201  ],v_sum[  202  ],v_sum[  203  ],v_sum[  204  ],v_sum[  205  ],v_sum[  206  ],v_sum[  207  ],v_sum[  208  ],v_sum[  209  ],v_sum[  210  ],v_sum[  211  ],v_sum[  212  ],v_sum[  213  ],v_sum[  214  ],v_sum[  215  ],v_sum[  216  ],v_sum[  217  ],v_sum[  218  ],v_sum[  219  ],v_sum[  220  ],v_sum[  221  ],v_sum[  222  ],v_sum[  223  ],v_sum[  224  ],v_sum[  225  ],v_sum[  226  ],v_sum[  227  ],v_sum[  228  ],v_sum[  229  ],v_sum[  230  ],v_sum[  231  ],v_sum[  232  ],v_sum[  233  ],v_sum[  234  ],v_sum[  235  ],v_sum[  236  ],v_sum[  237  ],v_sum[  238  ],v_sum[  239  ],v_sum[  240  ],v_sum[  241  ],v_sum[  242  ],v_sum[  243  ],v_sum[  244  ],v_sum[  245  ],v_sum[  246  ],v_sum[  247  ],v_sum[  248  ],v_sum[  249  ],v_sum[  250  ],v_sum[  251  ],v_sum[  252  ],v_sum[  253  ],v_sum[  254  ],v_sum[  255  ],v_sum[  256  ],v_sum[  257  ],v_sum[  258  ],v_sum[  259  ],v_sum[  260  ],v_sum[  261  ],v_sum[  262  ],v_sum[  263  ],v_sum[  264  ],v_sum[  265  ],v_sum[  266  ],v_sum[  267  ],v_sum[  268  ],v_sum[  269  ],v_sum[  270  ],v_sum[  271  ],v_sum[  272  ],v_sum[  273  ],v_sum[  274  ],v_sum[  275  ],v_sum[  276  ],v_sum[  277  ],v_sum[  278  ],v_sum[  279  ],v_sum[  280  ],v_sum[  281  ],v_sum[  282  ],v_sum[  283  ],v_sum[  284  ],v_sum[  285  ],v_sum[  286  ],v_sum[  287  ],v_sum[  288  ],v_sum[  289  ],v_sum[  290  ],v_sum[  291  ],v_sum[  292  ],v_sum[  293  ],v_sum[  294  ],v_sum[  295  ],v_sum[  296  ],v_sum[  297  ],v_sum[  298  ],v_sum[  299  ],v_sum[  300  ],v_sum[  301  ],v_sum[  302  ],v_sum[  303  ],v_sum[  304  ],v_sum[  305  ],v_sum[  306  ],v_sum[  307  ],v_sum[  308  ],v_sum[  309  ],v_sum[  310  ],v_sum[  311  ],v_sum[  312  ],v_sum[  313  ],v_sum[  314  ],v_sum[  315  ],v_sum[  316  ],v_sum[  317  ],v_sum[  318  ],v_sum[  319  ],v_sum[  320  ],v_sum[  321  ],v_sum[  322  ],v_sum[  323  ],v_sum[  324  ],v_sum[  325  ],v_sum[  326  ],v_sum[  327  ],v_sum[  328  ],v_sum[  329  ],v_sum[  330  ],v_sum[  331  ],v_sum[  332  ],v_sum[  333  ],v_sum[  334  ],v_sum[  335  ],v_sum[  336  ],v_sum[  337  ],v_sum[  338  ],v_sum[  339  ],v_sum[  340  ],v_sum[  341  ],v_sum[  342  ],v_sum[  343  ],v_sum[  344  ],v_sum[  345  ],v_sum[  346  ],v_sum[  347  ],v_sum[  348  ],v_sum[  349  ],v_sum[  350  ],v_sum[  351  ],v_sum[  352  ],v_sum[  353  ],v_sum[  354  ],v_sum[  355  ],v_sum[  356  ],v_sum[  357  ],v_sum[  358  ],v_sum[  359  ],v_sum[  360  ],v_sum[  361  ],v_sum[  362  ],v_sum[  363  ],v_sum[  364  ],v_sum[  365  ],v_sum[  366  ],v_sum[  367  ],v_sum[  368  ],v_sum[  369  ],v_sum[  370  ],v_sum[  371  ],v_sum[  372  ],v_sum[  373  ],v_sum[  374  ],v_sum[  375  ],v_sum[  376  ],v_sum[  377  ],v_sum[  378  ],v_sum[  379  ],v_sum[  380  ],v_sum[  381  ],v_sum[  382  ],v_sum[  383  ],v_sum[  384  ],v_sum[  385  ],v_sum[  386  ],v_sum[  387  ],v_sum[  388  ],v_sum[  389  ],v_sum[  390  ],v_sum[  391  ],v_sum[  392  ],v_sum[  393  ],v_sum[  394  ],v_sum[  395  ],v_sum[  396  ],v_sum[  397  ],v_sum[  398  ],v_sum[  399  ],v_sum[  400  ],v_sum[  401  ],v_sum[  402  ],v_sum[  403  ],v_sum[  404  ],v_sum[  405  ],v_sum[  406  ],v_sum[  407  ],v_sum[  408  ],v_sum[  409  ],v_sum[  410  ],v_sum[  411  ],v_sum[  412  ],v_sum[  413  ],v_sum[  414  ],v_sum[  415  ],v_sum[  416  ],v_sum[  417  ],v_sum[  418  ],v_sum[  419  ],v_sum[  420  ],v_sum[  421  ],v_sum[  422  ],v_sum[  423  ],v_sum[  424  ],v_sum[  425  ],v_sum[  426  ],v_sum[  427  ],v_sum[  428  ],v_sum[  429  ],v_sum[  430  ],v_sum[  431  ],v_sum[  432  ],v_sum[  433  ],v_sum[  434  ],v_sum[  435  ],v_sum[  436  ],v_sum[  437  ],v_sum[  438  ],v_sum[  439  ],v_sum[  440  ],v_sum[  441  ],v_sum[  442  ],v_sum[  443  ],v_sum[  444  ],v_sum[  445  ],v_sum[  446  ],v_sum[  447  ],v_sum[  448  ],v_sum[  449  ],v_sum[  450  ],v_sum[  451  ],v_sum[  452  ],v_sum[  453  ],v_sum[  454  ],v_sum[  455  ],v_sum[  456  ],v_sum[  457  ],v_sum[  458  ],v_sum[  459  ],v_sum[  460  ],v_sum[  461  ],v_sum[  462  ],v_sum[  463  ],v_sum[  464  ],v_sum[  465  ],v_sum[  466  ],v_sum[  467  ],v_sum[  468  ],v_sum[  469  ],v_sum[  470  ],v_sum[  471  ],v_sum[  472  ],v_sum[  473  ],v_sum[  474  ],v_sum[  475  ],v_sum[  476  ],v_sum[  477  ],v_sum[  478  ],v_sum[  479  ],v_sum[  480  ],v_sum[  481  ],v_sum[  482  ],v_sum[  483  ],v_sum[  484  ],v_sum[  485  ],v_sum[  486  ],v_sum[  487  ],v_sum[  488  ],v_sum[  489  ],v_sum[  490  ],v_sum[  491  ],v_sum[  492  ],v_sum[  493  ],v_sum[  494  ],v_sum[  495  ],v_sum[  496  ],v_sum[  497  ],v_sum[  498  ],v_sum[  499  ],v_sum[  500  ],v_sum[  501  ],v_sum[  502  ],v_sum[  503  ],v_sum[  504  ],v_sum[  505  ],v_sum[  506  ],v_sum[  507  ],v_sum[  508  ],v_sum[  509  ],v_sum[  510  ],v_sum[  511  ],v_sum[  512  ],v_sum[  513  ],v_sum[  514  ],v_sum[  515  ],v_sum[  516  ],v_sum[  517  ],v_sum[  518  ],v_sum[  519  ],v_sum[  520  ],v_sum[  521  ],v_sum[  522  ],v_sum[  523  ],v_sum[  524  ],v_sum[  525  ],v_sum[  526  ],v_sum[  527  ],v_sum[  528  ],v_sum[  529  ],v_sum[  530  ],v_sum[  531  ],v_sum[  532  ],v_sum[  533  ],v_sum[  534  ],v_sum[  535  ],v_sum[  536  ],v_sum[  537  ],v_sum[  538  ],v_sum[  539  ],v_sum[  540  ],v_sum[  541  ],v_sum[  542  ],v_sum[  543  ],v_sum[  544  ],v_sum[  545  ],v_sum[  546  ],v_sum[  547  ],v_sum[  548  ],v_sum[  549  ],v_sum[  550  ],v_sum[  551  ],v_sum[  552  ],v_sum[  553  ],v_sum[  554  ],v_sum[  555  ],v_sum[  556  ],v_sum[  557  ],v_sum[  558  ],v_sum[  559  ],v_sum[  560  ],v_sum[  561  ],v_sum[  562  ],v_sum[  563  ],v_sum[  564  ],v_sum[  565  ],v_sum[  566  ],v_sum[  567  ],v_sum[  568  ],v_sum[  569  ],v_sum[  570  ],v_sum[  571  ],v_sum[  572  ],v_sum[  573  ],v_sum[  574  ],v_sum[  575  ],v_sum[  576  ],v_sum[  577  ],v_sum[  578  ],v_sum[  579  ],v_sum[  580  ],v_sum[  581  ],v_sum[  582  ],v_sum[  583  ],v_sum[  584  ],v_sum[  585  ],v_sum[  586  ],v_sum[  587  ],v_sum[  588  ],v_sum[  589  ],v_sum[  590  ],v_sum[  591  ],v_sum[  592  ],v_sum[  593  ],v_sum[  594  ],v_sum[  595  ],v_sum[  596  ],v_sum[  597  ],v_sum[  598  ],v_sum[  599  ],]
    KN_add_obj_linear_struct (kc, objGradIndexVars, objGradCoefs)
    z=0
    # Add linear term x0 in the second constraint
    for i in range(buyers):
        for j in range(goods):
                KN_add_con_linear_struct (kc, i, z, 1.0)
                z+=1



    cb = KN_add_eval_callback (kc, evalObj = True, funcCallback = callbackEvalF)
    



    KN_set_int_param (kc, KN_PARAM_HESSIAN_NO_F, KN_HESSIAN_NO_F_ALLOW)

    KN_set_obj_goal (kc, KN_OBJGOAL_MAXIMIZE)

    KN_set_int_param (kc, KN_PARAM_DERIVCHECK, KN_DERIVCHECK_ALL)

    nStatus = KN_solve (kc)

    nStatus, objSol, x, lambda_ = KN_get_solution (kc)
    tcpu = KN_get_solve_time_cpu(kc)
    treal = KN_get_solve_time_real(kc)







    #print ("Optimal objective value  = %f" % objSol)
    #print ("Total CPU time           = %f" % tcpu)
    #print ("Total real time          = %f" % treal)
    #print ("Optimal x (with corresponding multiplier)")
    #for i in range (n):
    #    print ("  x[%d] = %f (lambda = %e)" % (i, x[i], lambda_[m+i]))
    #print ("Optimal constraint values (with corresponding multiplier)")
    c = KN_get_con_values (kc)
    #for j in range (m):
    #    print ("  c[%d] = %e (lambda = %e)" % (i, c[i], lambda_[i]))
    #print ("  feasibility violation    = %e" % KN_get_abs_feas_error (kc))
    #print ("  KKT optimality violation = %e" % KN_get_abs_opt_error (kc))
    #print(value[0])

    z=0
    OPTnsw=objSol
    for i in range(buyers):
        for j in range (goods):
            bidprice_opt[i][j]=x[z]
            z+=1
    for i in range(buyers):
        for j in range (goods):
            budget_opt[i]=budget_opt[i]+bidprice_opt[i][j]

    # Delete the Knitro solver instance.
    KN_free (kc)
        
    



    for i in range(buyers):
        for j in range (goods):
            price_opt[j]=price_opt[j]+bidprice_opt[i][j].copy()
    for i in range(buyers):
        for j in range (goods):        
            quantity_opt[i][j]=bidprice_opt[i][j].copy()/price_opt[j].copy()
        


    for i in range(buyers):
        for t in range(time):
            for j in range(goods):
                #u[t][i]=u[t][i]+value[t][i][j].copy()*quantity[t][i][j].copy()
                u[t][i]=u[t][i]+avg_val[i][j].copy()*quantity[t][i][j].copy()
                u_opt[t][i]=u_opt[t][i]+value[0][i][j].copy()*quantity_opt[i][j].copy()


    for t in range(time):
        for i in range(buyers):
            U[i]=U[i]+u[t][i].copy()
            U_opt[i]=U_opt[i]+u_opt[t][i].copy()
            individual_regret[i]=(U_opt[i].copy()-U[i].copy())/U_opt[i].copy()
            #print(individual_regret[0],t,U_opt[0])
        max_ind=0
        for p in range(10):
            if individual_regret[p] > max_ind:
                max_ind = individual_regret[p]  
        sum_ind=max_ind
        #print(individual_regret,t)
        #print(u_opt[t][0])
        indavgT[t]=indavgT[t]+sum_ind
        if   t==1:
            avgind[k][0]=sum_ind
        elif t==500 :
            avgind[k][1]=sum_ind
        elif t==1000:
            avgind[k][2]=sum_ind
        elif t==1500:
            avgind[k][3]=sum_ind
        elif t==2000:
            avgind[k][4]=sum_ind
        elif t==2500:
            avgind[k][5]=sum_ind
        elif t==3000:
            avgind[k][6]=sum_ind
        elif t==3500:
            avgind[k][7]=sum_ind
        elif t==4000:
            avgind[k][8]=sum_ind
        elif t==4500:
            avgind[k][9]=sum_ind
        elif t==4999:
            avgind[k][10]=sum_ind
        sum_ind=0
    #print(U_opt[0])
    for t in range(time):
        for i in range(buyers):
            for j in range(goods):
                Unsw=Unsw+(bidprice[t][i][j]*log_val[i][j]-bidprice[t][i][j]*math.log(price[t][j]))
                #Unsw=Unsw+(bidprice[t][i][j]*math.log(value[t][i][j]/price[t][j]))
                #OPTnsw=OPTnsw+(bidprice_opt[i][j]*log_val[i][j]-bidprice_opt[i][j]*math.log(price_opt[j]))
        Q[t]=(OPTnsw-Unsw)
        #if abs(Q[t])<0.002:
        #    Q[t]=0
        social_regret=social_regret+Q[t]

        #print(OPTnsw,Unsw,t)
        #OPTnsw=0
        Unsw=0
        #print('%f'%social_regret)
        socavgT[t]=socavgT[t]+social_regret
        data[k][t]=social_regret
        if   t==1:
            avgsoc[k][0]=social_regret
        elif t==500 :
            avgsoc[k][1]=social_regret
        elif t==1000:
            avgsoc[k][2]=social_regret
        elif t==1500:
            avgsoc[k][3]=social_regret
        elif t==2000:
            avgsoc[k][4]=social_regret
        elif t==2500:
            avgsoc[k][5]=social_regret
        elif t==3000:
            avgsoc[k][6]=social_regret
        elif t==3500:
            avgsoc[k][7]=social_regret
        elif t==4000:
            avgsoc[k][8]=social_regret
        elif t==4500:
            avgsoc[k][9]=social_regret
        elif t==4999:
            avgsoc[k][10]=social_regret
    #print(sum(U))
    #print(OPTnsw,Unsw)
    #print('%f'%bidprice_opt[0][0][0],'%f'%price_opt[0][0],quantity_opt[0][0][0])
    #for t in range(time):
    #    for i in range(buyers):
    #        for j in range(goods):
    #            Dh[t]=Dh[t]+(bidprice_opt[i][j]*math.log(bidprice_opt[i][j]/bidprice[t][i][j]))
    #for t in range(time-1):
    #    print('%f'%(Dh[t]-Dh[t+1]-Q[t+1]))
    #print(Dh[0])

    #print('%f'%sum(individual_regret))

    #print('%f'%individual_regret[0],'%f'%individual_regret[1],'%f'%individual_regret[2],'%f'%social_regret)

    #for i in range (buyers):
        #print('%f'%U[i],'%f'%U_opt[i])

    for t in range (1,time):
        for j in range(goods):
            Ek[0]=Ek[0]+value[t][0][j]*quantity[t][0][j]
            Ek[1]=Ek[1]+value[t][0][j]*quantity[t][1][j]
            Ek[2]=Ek[2]+value[t][0][j]*quantity[t][2][j]
            Ek[3]=Ek[3]+value[t][0][j]*quantity[t][3][j]
            Ek[4]=Ek[4]+value[t][0][j]*quantity[t][4][j]
            Ek[5]=Ek[5]+value[t][0][j]*quantity[t][5][j]
            Ek[6]=Ek[6]+value[t][0][j]*quantity[t][6][j]
            Ek[7]=Ek[7]+value[t][0][j]*quantity[t][7][j]
            Ek[8]=Ek[8]+value[t][0][j]*quantity[t][8][j]
            Ek[9]=Ek[9]+value[t][0][j]*quantity[t][9][j]
        # E[0][t]=E[0][t]+value[t][0][j]*quantity[t][0][j]
        max_val = 0
        #print(Ek)
        #print(E[0][t])
        for i in range(buyers):
            avg_Ek[i]=(Ek[i]/t)
        for p in range(10):
            if avg_Ek[p] > max_val:
                max_val = avg_Ek[p]  
                #print(Ek[p],"1")      
        sumE_opt[0]=sumE_opt[0]+max_val
        sumE[0]=sumE[0]+avg_Ek[0]
        envy[0]=(max_val-avg_Ek[0])
        #print(Ek,t)
        #Ek[0]=0
        #Ek[1]=0
        #Ek[2]=0
        #Ek[3]=0
        #Ek[4]=0
        #Ek[5]=0
        #Ek[6]=0
        #Ek[7]=0
        #Ek[8]=0
        #Ek[9]=0
        
        if  t==100 :
            avgenv[k][0]=envy[0]
            #print(sum(envy))
        elif t==200:
            avgenv[k][1]=envy[0]
            #print(sum(envy))
        elif t==300:
            avgenv[k][2]=envy[0]
            #print(sum(envy))
        elif t==400:
            avgenv[k][3]=envy[0]
            #print(sum(envy))
        elif t==500:
            avgenv[k][4]=envy[0]
            #print(sum(envy))
        elif t==600:
            avgenv[k][5]=envy[0]
            #print(sum(envy))
        elif t==700:
            avgenv[k][6]=envy[0]
            #print(sum(envy))
        elif t==800:
            avgenv[k][7]=envy[0]
            #print(sum(envy))
        elif t==900:
            avgenv[k][8]=envy[0]
            #print(sum(envy))
        elif t==999:
            avgenv[k][9]=envy[0]
            #print(sum(envy))
    #for j in range(goods):
    #    print(bidprice[999][0][j],'alg')
    #    print(bidprice_opt[0][j],'opt')
    #print('%f'%price[999][0],'%f'%price[999][1],'%f'%price[999][2],'%f'%price[999][3],'%f'%price[999][4],'%f'%price[999][5],'%f'%price[999][6],'%f'%price[999][7],'%f'%price[999][8],'%f'%price[999][9],'price alg')
    #print(price_opt,'price opt')
    for t in range(time):
        for j in range(goods):
            price_norm[t]=price_norm[t]+abs(price[t][j].copy()-price_opt[j].copy())
            #price_norm_exp[t]=price_norm_exp[t]+math.pow((price_exp[t][j].copy()-price_opt[j].copy()),2)
        #print(price_norm_exp[t])
    #print('1')
    #for t in range(100):
    #    print(price_norm[t])
    #print(avg_val,value[0][0][0])
    price*=0
    price_exp*=0
    Q*=0
    social_regret=0
    price_opt*=0
    #bidprice*=0
    #bidprice_opt*=0  
    sumvx*=0
    sumvx_opt*=0
    sumvx_exp*=0
    u*=0
    U*=0
    Unsw*=0
    OPTnsw*=0
    U_opt*=0
    u_opt*=0
    individual_regret*=0
    envy*=0
    E*=0
    sumE[0]=0
    sumE_opt[0]=0
    valuesum*=0
    sum_ind*=0
    avg_qua*=0
    avg_val*=0
    Ek*=0
    v_sum*=0
df = pd.DataFrame(data)

# 將DataFrame寫入Excel文件
with pd.ExcelWriter('mild.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False, header=False)

for t in range (time):
    price_norm[t]=(price_norm[t]/repeat)
    socavgT[t]=(socavgT[t]/repeat)
    indavgT[t]=(indavgT[t]/repeat)

#for t in range (time):
#    print(price_norm_exp[t]/a)
print(indavgT,'individual regret')
print(socavgT,'social regret')
##print(envyT,"envy")
path = 'mild.txt'
f = open(path, 'r+')
np.savetxt(f, price_norm)
#content = str(price_norm)
#f.write(content)
f.close()
path = 'INDmild.txt'
f = open(path, 'r+')
np.savetxt(f, indavgT)
#content = str(price_norm)
#f.write(content)
f.close()
path = 'SOCmild.txt'
f = open(path, 'r+')
np.savetxt(f, socavgT)
#content = str(price_norm)
#f.write(content)
f.close()

