% hard3_0095  eq1=735 eq2=2812  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(f(Z,W),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(Z,Z)),X) )).
