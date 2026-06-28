% hard3_0295  eq1=2816 eq2=1953  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(Z,W)),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(W,X)) )).
