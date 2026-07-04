% order5v2_1751  eq1=17805 eq2=9901  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(W,f(W,W)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(W,f(Y,Z)))) )).
